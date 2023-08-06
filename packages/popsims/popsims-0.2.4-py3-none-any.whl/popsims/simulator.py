##purpose: simulate a brown dwarf population
###
#imports
from .galaxy import * 
from .core import *
from .core_tools import *
from .relations import teff_to_spt_subdwarf
import seaborn as sns
#from tqdm import tqdm
#tqdm.pandas()


class Population(object):
    """
    Class for a poulation

    Attributes:
    ----
        x_grid: grid of values ( array)
        cdf:  corresponding values from the CDF
        nsample: optional, number of samples

    Properties:
    -------
        random draws

    Methods:
    --------

    Example:
    -------
        > x = np.arange(0, 10)
        > cdf = x**3/(x[-1]**3)
        > res= random_draw(x, cdf)

    """
    def __init__(self, **kwargs):

        self.imfpower= kwargs.get('imf_power', -0.6)
        self.binaryfraction= kwargs.get('binary_fraction', 0.2)
        self.binaryq= kwargs.get('binary_q', 4)
        self.evolmodel_name= kwargs.get('evolmodel', 'burrows1997')
        self.metallicity=kwargs.get('metallicity', 'dwarfs')
        self.agerange= kwargs.get('age_range', [0.01, 14.])
        self.massrange= kwargs.get('mass_range', [0.01, 1.])
        self.nsample= kwargs.get('nsample',1e4)
        self.evol_model=kwargs.get('evol_model', None) #evolutionary model object

    def _sample_ages(self):
        return np.random.uniform(*self.agerange, int(self.nsample))
    
    def _sample_masses(self):
        if self.imfpower=='kroupa':
            m0, m1, m2 = (
                sample_from_powerlaw(-0.3, xmin=0.03, xmax=0.08, nsample=int(self.nsample)),
                sample_from_powerlaw(-1.3, xmin=0.08, xmax=0.5, nsample=int(self.nsample)),
                sample_from_powerlaw(-2.3, xmin=0.5, xmax=100, nsample=int(self.nsample))
            )
            m = np.concatenate([m0, m1, m2]).flatten()
            mask = np.logical_and(m > self.massrange[0], m < self.massrange[1])
            masses = np.random.choice(m[mask], int(self.nsample))
            return masses
        else:
            return sample_from_powerlaw(
                self.imfpower,
                xmin=self.massrange[0],
                xmax=self.massrange[1],
                nsample=int(self.nsample),
            )

    def _interpolate_evolutionary_model(self, mass, age, additional_columns=[]):
        #columns that I need are mass, age, teff, luminosity,
       
        #reinitialize evolmodel object if necessary
        required_columns=np.concatenate([['mass', 'age', 'temperature', 'luminosity'], additional_columns])
        if self.evol_model is None and self.evolmodel_name is None:
            raise ValueError('Please specify evolutionay model grid')
        
        if  self.evol_model is None:
            df=pd.DataFrame(EVOL_MODELS[self.evolmodel_name])
            self.evol_model=EvolutionaryModel(df)
        
        #first remove nans
        lmass=np.log10(mass)
        lage= np.log10(age)

        res=self.evol_model.interpolate('mass','age', lmass, lage, \
                                        logscale=['mass', 'age', 'temperature'], \
                                            interp_columns=required_columns)
        #return evolutionary_model_interpolator(mass, age, self.evolmodel)
        res['mass']=10**lmass
        res['age']=10**lage
        res['temperature']=10**res.temperature.values
        #res['luminosity']= 10**res.luminosity.values
        return res
    
    def scale_to_local_lf(self):
        scale, scale_unc, scale_times_model = scale_to_local_lf(self.temperature)
        self.scale= scale
        self.scale_unc= scale_unc
        self.scale_times_model= scale_times_model

    def simulate(self, additional_columns=[]):
        """
        Class for a poulation

        Attributes:
        ----
            x_grid: grid of values ( array)
            cdf:  corresponding values from the CDF
            nsample: optional, number of samples

        Properties:
        -------
            random draws

        Methods:
        --------

        Example:
        -------
            > x = np.arange(0, 10)
            > cdf = x**3/(x[-1]**3)
            > res= random_draw(x, cdf)

        """
        #single stars
        m_singles=self._sample_masses()
        ages_singles= self._sample_ages()
        #binaries
        qs=sample_from_powerlaw(self.binaryq, xmin= 1e-10, xmax=1., nsample=self.nsample)
        m_prims = self._sample_masses()
        m_sec=m_prims*qs
        ages_bin=self._sample_ages()

        #interpolate evolurionary models
        single_evol=self._interpolate_evolutionary_model(m_singles, ages_singles, additional_columns=additional_columns)
        primary_evol=self._interpolate_evolutionary_model(m_prims,ages_bin, additional_columns=additional_columns)
        secondary_evol=self._interpolate_evolutionary_model(m_sec,ages_bin, additional_columns=additional_columns)


        # Vectorize the following operations for better performance
        teffs_singl, teffs_primar, teffs_second = (
            single_evol["temperature"], #.value,
            primary_evol["temperature"], #.value,
            secondary_evol["temperature"], #.value,
        )
        
        spts_singl, spt_primar, spt_second = (
            teff_to_spt_kirkpatrick(teffs_singl),
            teff_to_spt_kirkpatrick(teffs_primar),
            teff_to_spt_kirkpatrick(teffs_second),
        )
        #use pecaut 
        high_teff_mask = teffs_singl > 2000
        spts_singl[high_teff_mask] = teff_to_spt_pecaut(teffs_singl[high_teff_mask])
        spt_primar[high_teff_mask] = teff_to_spt_pecaut(teffs_primar[high_teff_mask])
        spt_second[high_teff_mask] = teff_to_spt_pecaut(teffs_second[high_teff_mask])

        #compute combined binary spectral types
        xy=np.vstack([np.round(np.array(spt_primar), decimals=0), np.round(np.array(spt_second), decimals=0)]).T
        spt_binr=np.array(get_system_type(xy[:,0], xy[:,1])).astype(float)
        #Remember to assign <15 or >39 primary to primary and 
        out_range=np.logical_or(xy[:,0] < 15, xy[:,0] > 39)
        #print (spt_binr[out_range])
        spt_binr[out_range]=xy[:,0][out_range]


        values={ 'sing_evol': single_evol, 'sing_spt':spts_singl,
                     'prim_evol': primary_evol, 'prim_spt':spt_primar,
                     'sec_evol': secondary_evol, 'sec_spt': spt_second,
                    'binary_spt': spt_binr }

        #make systems
        # these dict values should be properties of the population object --> can be bad for mem, avoid duplicating data
        vals= make_systems(values, self.binaryfraction).sample(n=int(self.nsample)).to_dict(orient='list')
        #add these values as attributes of the object
        for k, v in vals.items():
            setattr(self, k, v)

        assert(len(self.temperature) == len(vals['temperature']))
        #return values
    
    def add_distances(self, gmodel, l, b, dmin, dmax, dsteps=1000):
        """
        Class for a poulation

        Attributes:
        ----
            x_grid: grid of values ( array)
            cdf:  corresponding values from the CDF
            nsample: optional, number of samples

        Properties:
        -------
            random draws

        Methods:
        --------

        Example:
        -------
            > x = np.arange(0, 10)
            > cdf = x**3/(x[-1]**3)
            > res= random_draw(x, cdf)

        """
        #gmodel = galactic component o
        #pick distances from 0.1pc to 10kpc at l=45 deg and b=0
        #case where l and b are floats
        l=np.array([l]).flatten()
        b=np.array([b]).flatten()
        assert len(l)== len(b)
        # Use NumPy broadcasting to avoid loops
        dists = np.concatenate(
            [
                gmodel.sample_distances(
                    dmin,
                    dmax,
                    int(1.5 * self.nsample / len(l)),
                    l=l[idx],
                    b=b[idx],
                    dsteps=dsteps,
                )
                for idx in range(len(l))
            ]
        )
        self.distance=np.random.choice(dists, len(self.temperature))

    def add_magnitudes(self, filters, get_from='spt', **kwargs):
        """
        Class for a poulation

        Attributes:
        ----
            x_grid: grid of values ( array)
            cdf:  corresponding values from the CDF
            nsample: optional, number of samples

        Properties:
        -------
            random draws

        Methods:
        --------

        Example:
        -------
            > x = np.arange(0, 10)
            > cdf = x**3/(x[-1]**3)
            > res= random_draw(x, cdf)

        """
        if get_from=='spt':
            mags=pop_mags(np.array(self.spt), keys=filters, get_from='spt', **kwargs)
        
        if get_from=='teff':
            mags=pop_mags(np.array(self.temperature), keys=filters,  get_from='teff', **kwargs)

        if  self.distance is not None:
            for f in filters: mags[f] = mags['abs_{}'.format(f)].values+5*np.log10(self.distance/10.0)

        vals=mags.to_dict(orient='list')
        #add these values as attributes of the object
        for k, v in vals.items():
            setattr(self, k, v)
            
    def to_dataframe(self, columns):
        data = {col: self.__dict__[col] for col in columns}
        df = pd.DataFrame(data)
        return df

    def visualize(self, keys=['mass', 'age', 'spt'], ms=0.1):
        """
        Class for a poulation

        Attributes:
        ----
            x_grid: grid of values ( array)
            cdf:  corresponding values from the CDF
            nsample: optional, number of samples

        Properties:
        -------
            random draws

        Methods:
        --------

        Example:
        -------
            > x = np.arange(0, 10)
            > cdf = x**3/(x[-1]**3)
            > res= random_draw(x, cdf)

        """
        df=pd.DataFrame.from_records([self.__dict__[x] for x in  keys]).T
        df.columns=keys

        import matplotlib.pyplot as plt
        g = sns.PairGrid(df[keys] , diag_sharey=False, corner=True)
        g.map_diag(plt.hist, log=True, bins=32)
        g.map_offdiag(sns.scatterplot, size=ms, color='k', alpha=0.1)

    def add_kinematics(self, ra, dec, kind='thin_disk', red_prop_motions_keys=[]):
        #transform whatever footprint to have the same shape as the distance array
        idxs=np.random.choice(range(len(ra)), len(self.distance), replace=True) #temporary solution
        vs=get_velocities(np.array(ra)[idxs], np.array(dec)[idxs], np.array(self.distance), population=kind, age=np.array(self.age))

        for k in red_prop_motions_keys:
            #compute red 
            mu= (vs.mu_alpha_cosdec**2+vs.mu_delta**2)**0.5
            mag=np.array( getattr(self, k))
            vs['redH_'+k]= mag+5*np.log10(mu)-10 #

        #add these values as attributes of the object
        vals=vs.to_dict(orient='list')
        for k, v in vals.items():
            setattr(self, k, v)


    def apply_selection():
        #should delete previous entries to save space
        #selection should be a complex string --> sql to pass into series
        # must think about color-cuts
        #there must be a way to resample to nsample after making selection to not risk losing too many stars
        raise NotImplementedError


#need to rewrite to account for when magnitudes are passed as well
def make_systems(mods, bfraction):
    
    def create_singles(mods):
        singles = mods['sing_evol'].copy()
        singles['is_binary'] = np.zeros_like(mods['sing_spt'], dtype=bool)
        singles['spt'] = mods['sing_spt']
        singles['prim_spt'] = mods['sing_spt']
        singles['sec_spt'] = np.full(mods['sing_spt'].shape, np.nan)
        
        return singles
    
    def create_binaries(mods):
        binaries = {
            'age': mods['prim_evol']['age'],
            'mass': mods['prim_evol']['mass'] + mods['sec_evol']['mass'],
            'pri_mass': mods['prim_evol']['mass'],
            'sec_mass': mods['sec_evol']['mass'],
            'luminosity': np.log10(10 ** mods['prim_evol']['luminosity'] + 10 ** mods['sec_evol']['luminosity']),
            'spt': np.random.normal(mods['binary_spt'], 0.3),
            'prim_spt': mods['prim_spt'],
            'sec_spt': mods['sec_spt'],
            'prim_luminosity': 10 ** mods['prim_evol']['luminosity'],
            'sec_luminosity': 10 ** mods['sec_evol']['luminosity'],
            'is_binary': np.ones_like(mods['sec_spt'], dtype=bool)
        }

        mask = binaries['spt'] > 20
        teff_func = np.vectorize(lambda spt: spt_to_teff_kirkpatrick(spt)[0] if spt > 20 else spt_to_teff_pecaut(spt))
        binaries['temperature'] = teff_func(binaries['spt'])
        return binaries

    def choose_binaries(binaries, n_draw):
        random_int = np.random.choice(np.arange(len(binaries['spt'])), n_draw)
        return {k: binaries[k][random_int] for k in binaries.keys()}

    singles = create_singles(mods)
    binaries = create_binaries(mods)

    n_draw = int(len(mods['sing_spt']) / (1 - bfraction)) - len(mods['sing_spt'])
    chosen_binaries = choose_binaries(binaries, n_draw)

    res = pd.concat([pd.DataFrame(singles), pd.DataFrame(chosen_binaries)])
    return res

def pop_mags(x, d=None, keys=[], object_type='dwarfs', get_from='spt', reference=None, pol=None):
    """
    Compute magnitudes from pre-computed absolute mag relations

        Class for a poulation

        Attributes:
        ----
            x_grid: grid of values ( array)
            cdf:  corresponding values from the CDF
            nsample: optional, number of samples

        Properties:
        -------
            random draws

        Methods:
        --------

        Example:
        -------
            > x = np.arange(0, 10)
            > cdf = x**3/(x[-1]**3)
            > res= random_draw(x, cdf)

    """
    from .abs_mag_relations import POLYNOMIALS
    res={}
    if pol is None: pol=POLYNOMIALS['absmags_{}'.format(get_from)][object_type]
    if reference is not None: pol=POLYNOMIALS['references'][reference]
    for k in keys:
        #print (keys)
        #sometimes sds don't have absolute magnitudes defined 
        if k not in pol.keys():
            warnings.warn("{} relation not available for {} ".format(k,object_type))

        fit=np.poly1d(pol[k]['fit'])
        #scat=pol[k]['scatter'] #ignore scatter for now
        scat=0.01

        #print (k, 'scatter', scat)
        rng=pol[k]['range']
        mag_key=pol[k]['y']
        offset=pol[k]['x0']
        #put constraints on spt range
        mask= np.logical_and(x >rng[0], x <=rng[-1])
        absmag= np.random.normal(fit(x-offset),scat)
        #forget about scatter for now
        #absmag= fit(x-offset)

        masked_abs_mag= np.ma.masked_array(data=absmag, mask=~mask)
        #make it nans outside the range
        if d is not None: 
            res.update({ k: masked_abs_mag.filled(np.nan)+5*np.log10(d/10.0) })
        res.update({'abs_'+ k: masked_abs_mag.filled(np.nan)})


    return pd.DataFrame(res)


def compute_vols_and_numbers(df, gmodel, sptgrid, footprint, maglimits):
    from .abs_mag_relations import POLYNOMIALS
    counts={}
    vols={}
    dists={}

    for spt in sptgrid:
        
        dmins=[]
        dmaxs=[]
        
        dmins_sd=[]
        dmaxs_sd=[]
        
        for k in maglimits.keys():
            mag_cut= maglimits[k]
            absmag= np.poly1d(POLYNOMIALS['absmags_spt']['dwarfs'][k]['fit'])(spt)
            
            #absmag_sd= np.poly1d(POLYNOMIALS['absmags_spt']['subdwarfs'][k]['fit'])(spt)
        
            mag_cut= maglimits[k]
            
            dmin=10.**(-(absmag-mag_cut[0])/5. + 1.)
            dmax=10.**(-(absmag-mag_cut[1])/5. + 1.)
            
            #dmin_sd=10.**(-(absmag_sd-14)/5. + 1.)
            #dmax_sd=10.**(-(absmag_sd-mag_cut)/5. + 1.)
        
            
            dmins.append(dmin)
            dmaxs.append(dmax)
            
            #dmins_sd.append(dmin)
            #dmaxs_sd.append(dmax)
            
        dmin=np.nanmedian(dmins)
        dmax=np.nanmedian(dmaxs)
        
        #dmin_sd=np.nanmedian(dmins_sd)
        #dmax_sd=np.nanmedian(dmaxs_sd)
        
        #print (spt, dmin, dmax)
        #print (df)
        #print (df.scale)
        scale=[df.scale.mean(), df.scale_unc.mean(), df.scale_times_model.mean()]
        
        sn= len(df)
        #sn= len(df.query('population == "thin disk"'))
        #snt= len(df.query('population == "thick disk"'))
        #snh= len(df.query('population == "halo"'))
      
        sn_c= len(df.query('spt < {}'.format(spt, spt+0.9)))
        #snt_c= len(df.query('population == "thick disk" and spt >= {} and spt < {}'.format(spt, spt+0.9)))
        #snh_c= len(df.query('population == "halo" and spt >= {} and spt < {}'.format(spt, spt+0.9)))
        
        
        volumes={'volume': 0.0}
        
        cnts={'number':  sn_c*np.divide(scale[-1], sn)}
        for s in  footprint:
            l=s.galactic.l.radian
            b=s.galactic.b.radian
            volumes['volume'] += gmodel.volume(l, b, dmin, dmax)/len(footprint)
            #volumes['thick'] += tdisk.volume(l, b, dmin, dmax)/len(footprint)
            #volumes['halo'] += halo.volume(l, b, dmin, dmax)/len(footprint)
            
        vols.update({spt: volumes})
        counts.update({spt: cnts})
        dists.update({spt: dmax})
        
        
    return pd.DataFrame.from_records(vols).T.replace(np.inf, np.nan),\
    pd.DataFrame.from_records(counts).T.replace(np.inf, np.nan),\
    dists
