
import json as js
import datetime
import os


def timedata(dt:float =1, dtsub:float = 0.1, time_limit:float=2000):
    """create a dictionary containing all entries of timedata namelist

    Parameters
    ----------
    "dt": float          
        outer loop time-step [s] 
    "dtsub": float       
        inner loop time-step [s]
    "time_limit": float  
        maximum simulated time [s]
    """
    return({"dt": dt, "dtsub": dtsub, "time_limit": time_limit})

def commonsdata(na:int=400, na_coa:int=100, mass_accom:float=1, surf_tens_w:float=72, gasconcppm:list=[0,0,0,0,0,0]):
    """create a dictionary containing all entries of commonsdata namelist with exception of nat

    Parameters
    ----------
    "na": int              
        number of bins per aerosol type
    "na_coa": int          
        Number of bins in precipitation distribution
    "mass_accom": float      
        Mass accommodation coefficient [dimensionless]
    "surf_tens_w": float     
        Surface tension [mN/m]
    "gasconcppm": list      
        tracegas concentrations [ppm-v]: so2, o3, h2o2, nho3, nh3, co2
    """
    return({"na": na, "na_coa": na_coa, "mass_accom": mass_accom, "surf_tens_w": surf_tens_w, "gasconcppm": gasconcppm})

def aerosoltype(Nmodes:int=1, modes:list=[[566000000,0.04,2]], massfracs:list=[0,1,0,0,0,0,0,0]):
    """create a dictionary representing one aerosol type

    Parameters
    ----------
    Nmodes : int
        Number of lognormal modes

    modes : list (elements are lists of length = 3)
        list of parameters for each mode. Each entry is list with the following entries,
        representing the respective parameter of a lognormal distribution:
        [number conc [m-3], mean radius [um], geometric standard deviation]
    
    massfracs : list (length = 8, sum = 1)
        list of massfractions for the aerosol composition. The sequence of species is:
        h2so4, (nh4)hso4, (nh4)2so4, OC, BC, dust, seasalt, SVOC
    """
    typedict = {"Nmodes": Nmodes, "massfracs": massfracs}
    mode = 1
    while (mode <= Nmodes):
        typedict["mode"+str(mode)]=modes[mode-1]
        mode = mode+1
    return(typedict)

def custaerosoltype(massfracs=[0,1,0,0,0,0,0,0]):
    return({"massfracs": massfracs})

def dynamicsdata(initial_temperature:float=285.2, initial_pressure:float=95000, updraft:float=0.5, downdraft:float=0, initial_relhum:float=95, \
                 entrainment_param:float=0, cloud_depth:float=1200, initial_height:float=600, initial_radius:float=350, zstopheight:float=0):
    """create a dictionary containing all entries of dynamicsdata namelist

    Parameters
    ----------
    "initial_temperature": float
        Temperature [K] (only needed if iupadiabat=FALSE)
    "initial_pressure": float    
        Pressure [Pa]
    "updraft": float             
        Updraft velocity [m/s]
    "downdraft": float           
       Downdraft velocity [m/s] (this number should be positive, only works with vcycles>0)
    "initial_relhum": flaot      
        Relative humidity [percentage]
    "entrainment_param": float   
        Entrainment parameter, between 0 and 1 [dimensionless]
    "cloud_depth": float         
        Cloud depth [m]
    "initial_height": float      
        Initial parcel height [m]
    "initial_radius": float       
        Initial parcel radius [m]
    "zstopheight": float          
        Only activates if istopheight=TRUE. The parcel vertical velocity is set to 0 at this height.
    """
    return({"initial_temperature": initial_temperature, "initial_pressure": initial_pressure, "updraft": updraft, "downdraft": downdraft, "initial_relhum": initial_relhum, "entrainment_param": entrainment_param, \
            "cloud_depth": cloud_depth, "initial_height": initial_height, "initial_radius": initial_radius, "zstopheight": zstopheight})

def outputdata(pheightstep:float=2, fixed_level_altitude_outputs:list = [0, 50, 100, 150, 200]):
    """create a dictionary containing all entries of outputdata namelist

    Parameters
    ----------
    "pheightstep": float                     
        Profile step length [m]
    "fixed_level_altitude_outputs": list (float)    
        Fixed levels to output at, must be used with ihoutputs=T. outputs to specH files

    Parameters are all entries
    """
    return({"pheightstep": pheightstep, "fixed_level_altitude_outputs": fixed_level_altitude_outputs})

def svocdata(initial_ctot:list[float] = [0.225403, 0.109134, 0.113911, 0.099487, 0.101220, 0.035158, 0.032858, 0.073868], \
             log_cstar_org:list[float] = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], min_org_film_thick:float = 2e-10, sigma_org:float = 30, org_sol_frac:float=1, \
             org_sol_frac_cf:float=0, org_e_sol_frac_vbs:float=1, org_densities:float=1500, \
             org_mol_mass:float=0.2, org_vap_enthalpy:float=1500000, org_alpha:float=1):
    """create a dictionary containing all entries of svocdata namelist

    Parameters
    ----------
    "initial_ctot": list[float]            
        relative total concentrations [dimensionless]
    "log_cstar_org": list[float]           
        Volatility bins (can use up to 16 bins)
    "min_org_film_thick": float      
       Minimum organic film thickness [nm] query: might be meters
    "sigma_org": float                
        Organics surface tension [mNm-1]
    "org_sol_frac": float             
        Soluble fraction used for non-VBS organic component when not modelling surface phase [dimensionless] (0->1)
    "org_sol_frac_cf": float          
        Soluble fraction used for approximate compressed film model [dimensionless] (0->1)
    "org_e_sol_frac_vbs": float       
        Effective solubility fraction [dimensionless] (0->1)
    "org_densities": float            
        Organic densitites (same for all organics) [kg m-3]
    "org_mol_mass": float             
        Organic molar mass (same for all organics) [kg mol-1]
    "org_vap_enthalpy": float         
        Organic enthalpy of vapourisation (same for all organics) [J mol-1]
    "org_alpha": float                
        Organic mass accommodation coefficient (same for all organics) [dimensionless] (0->1)
    """
    return({"initial_ctot": initial_ctot, "log_cstar_org": log_cstar_org, "min_org_film_thick": min_org_film_thick, "sigma_org": sigma_org, \
            "org_sol_frac": org_sol_frac, "org_sol_frac_cf": org_sol_frac_cf, "org_e_sol_frac_vbs": org_e_sol_frac_vbs, "org_densities": org_densities, \
            "org_mol_mass": org_mol_mass, "org_vap_enthalpy": org_vap_enthalpy, "org_alpha": org_alpha})

def _printarray(array):
    print = ""
    for entry in range(len(array)-1):
        print = print+str(array[entry])+", "
    print = print + str(array[-1])
    return print


def _floatstr(val):
    if "." in str(val):
        return(str(val))
    else:
        return(str(val)+".")
    
def _boolstr(val):
    if val == True:
        return "T"
    elif val == False:
        return "F"
    else:
        return "not bool"

def _printfloatarray(array):
    print = ""
    for entry in range(len(array)-1):
        print = print+_floatstr(array[entry])+", "
    print = print + _floatstr(array[-1])
    return print


class PARSEC_UserVars:
    """Data structure representing all User-Variables for input in PARSEC-UFO organized in namelists

    Parameters
    ----------
    timedata : dict-like
        dictionary containing all entries of timedata namelist:
        "dt":           outer loop time-step [s] 
        "dtsub":        inner loop time-step [s]
        "time_limit":   maximum simulated time [s]

    commonsdata : dict-like
        dictionary containing all entries of commonsdata namelist:
        "na":               number of bins per aerosol type
        "na_coa":           Number of bins in precipitation distribution
        "mass_accom":       Mass accommodation coefficient [dimensionless]
        "surf_tens_w":      Surface tension [mN/m]
        "gasconcppm":       tracegas concentrations [ppm-v]: so2, o3, h2o2, nho3, nh3, co2

    aerosoldata : list (length <= 4)
        list of dict-like. Each entry represents one aerosol type, with the following variables:
        Nmodes : integer
            Number of lognormal modes
        modes : list (elements are lists of length = 3)
            list of parameters for each mode. Each entry is list with the following entries,
            representing the respective parameter of a lognormal distribution:
            [number conc [m-3], mean radius [um], geometric standard deviation]        
        massfracs : list (length = 7, sum = 1)
            list of massfractions for the aerosol composition. The sequence of species is:
            h2so4, (nh4)hso4, (nh4)2so4, OC, BC, dust, seasalt

    dynamicsdata : dict-like
        dictionary containing all entries of dynamicsdata namelist:
        "initial_temperature":  Temperature [K] (only needed if iupadiabat=FALSE)
        "initial_pressure":     Pressure [Pa]
        "updraft":              Updraft velocity [m/s]
        "downdraft":            Downdraft velocity [m/s] (this number should be positive, only works with vcycles>0)
        "initial_relhum":       Relative humidity [percentage]
        "entrainment_param":    Entrainment parameter, between 0 and 1 [dimensionless]
        "cloud_depth":          Cloud depth [m]
        "initial_height":       Initial parcel height [m]
        "initial_radius":       Initial parcel radius [m]
        "zstopheight":          Only activates if istopheight=TRUE. The parcel vertical velocity is set to 0 at this height.

    outputdata : dict-like
        dictionary containing entries of outputdata namelist:
        "pheightstep":                      Profile step length [m]
        "fixed_level_altitude_outputs":     Fixed levels to output at, must be used with ihoutputs=T. outputs to specH files

    svocdata : dict-like
        "initial_ctot":         relative total concentrations [dimensionless]
        "log_cstar_org":        Volatility bins (can use up to 16 bins)
        "min_org_film_thick":   Minimum organic film thickness [nm] query: might be meters
        "sigma_org":            Organics surface tension [mNm-1]
        "org_sol_frac":         Soluble fraction used for non-VBS organic component when not modelling surface phase [dimensionless] (0->1)
        "org_sol_frac_cf":      Soluble fraction used for approximate compressed film model [dimensionless] (0->1)
        "org_e_sol_frac_vbs":   Effective solubility fraction [dimensionless] (0->1)
        "org_densities":        Organic densitites (same for all organics) [kg m-3]
        "org_mol_mass":         Organic molar mass (same for all organics) [kg mol-1]
        "org_vap_enthalpy":     Organic enthalpy of vapourisation (same for all organics) [J mol-1]
        "org_alpha":            Organic mass accommodation coefficient (same for all organics) [dimensionless] (0->1)


    
    namelist_UserVars.in
    """
    def __init__(self, timedata=timedata(), commonsdata = commonsdata(), aerosoldata = [aerosoltype()], dynamicsdata = dynamicsdata(), outputdata = outputdata(), svocdata = svocdata()):
        """"Initialize self.  See help(type(self)) for accurate signature.

        Parameters
        ----------
        timedata : dict-like
            see help(timedata())
            dictionary containing all entries of timedata namelist:
            "dt":           outer loop time-step [s] 
            "dtsub":        inner loop time-step [s]
            "time_limit":   maximum simulated time [s]

        commonsdata : dict-like
            dictionary containing all entries of commonsdata namelist:
            "na":               number of bins per aerosol type
            "na_coa":           Number of bins in precipitation distribution
            "mass_accom":       Mass accommodation coefficient [dimensionless]
            "surf_tens_w":      Surface tension [mN/m]
            "gasconcppm":       tracegas concentrations [ppm-v]: so2, o3, h2o2, nho3, nh3, co2

        aerosoldata : list (length <= 4)
            list of dict-like. Each entry represents one aerosol type, with the following variables:
            Nmodes : integer
                Number of lognormal modes
            modes : list (elements are lists of length = 3)
                list of parameters for each mode. Each entry is list with the following entries,
                representing the respective parameter of a lognormal distribution:
                [number conc [m-3], mean radius [um], geometric standard deviation]        
            massfracs : list (length = 7, sum = 1)
                list of massfractions for the aerosol composition. The sequence of species is:
                h2so4, (nh4)hso4, (nh4)2so4, OC, BC, dust, seasalt

        dynamicsdata : dict-like
            dictionary containing all entries of dynamicsdata namelist:
            "initial_temperature":  Temperature [K] (only needed if iupadiabat=FALSE)
            "initial_pressure":     Pressure [Pa]
            "updraft":              Updraft velocity [m/s]
            "downdraft":            Downdraft velocity [m/s] (this number should be positive, only works with vcycles>0)
            "initial_relhum":       Relative humidity [percentage]
            "entrainment_param":    Entrainment parameter, between 0 and 1 [dimensionless]
            "cloud_depth":          Cloud depth [m]
            "initial_height":       Initial parcel height [m]
            "initial_radius":       Initial parcel radius [m]
            "zstopheight":          Only activates if istopheight=TRUE. The parcel vertical velocity is set to 0 at this height.

        outputdata : dict-like
            dictionary containing entries of outputdata namelist:
            "pheightstep":                      Profile step length [m]
            "fixed_level_altitude_outputs":     Fixed levels to output at, must be used with ihoutputs=T. outputs to specH files

        svocdata : dict-like
            "initial_ctot":         relative total concentrations [dimensionless]
            "log_cstar_org":        Volatility bins (can use up to 16 bins)
            "min_org_film_thick":   Minimum organic film thickness [nm] query: might be meters
            "sigma_org":            Organics surface tension [mNm-1]
            "org_sol_frac":         Soluble fraction used for non-VBS organic component when not modelling surface phase [dimensionless] (0->1)
            "org_sol_frac_cf":      Soluble fraction used for approximate compressed film model [dimensionless] (0->1)
            "org_e_sol_frac_vbs":   Effective solubility fraction [dimensionless] (0->1)
            "org_densities":        Organic densitites (same for all organics) [kg m-3]
            "org_mol_mass":         Organic molar mass (same for all organics) [kg mol-1]
            "org_vap_enthalpy":     Organic enthalpy of vapourisation (same for all organics) [J mol-1]
            "org_alpha":            Organic mass accommodation coefficient (same for all organics) [dimensionless] (0->1)
        """
        self.timedata = timedata                #[dt, dtsub, time_limit]
        self.commonsdata = commonsdata          #[na, na_coa, mass_accom, surf_tens_w, gasconcppm]
        self.aerosoldata = aerosoldata          #[aerosoltypes](up to 4) aerosoltype =[Nmodes, modes, massfracs]
        self.nat = len(aerosoldata)             #number of aerosol types(for custom aerosols this needs to be set later for now)
        self.dynamicsdata = dynamicsdata        #[init_t, init_p, updraft, downdraft, init_relh, entrainment_p, could_depth, init_h, init_r, zstopheight]
        self.outputdata = outputdata            #[pheightstep, fixed_level_altitude_outputs]
        self.svocdata = svocdata
        self. customaerosol = 0

    def get_timedata(self, variable:str = None):
        """return timedata namelist as dict, or the values of a specified variable in timedata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function returns the timedata namelist as dict
            if str, this function returns the value of the corresponding variable 
        """
        if variable == None:
            return self.timedata
        else:
            return(self.timedata[variable])
        
    def set_timedata(self, data, variable:str = None):
        """set timedata namelist, or the values of a specified variable in timedata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function sets the complete timedata namelist
            if str, this function sets the value of the corresponding variable 
        data : float, int (depending on variable) or dict (if variable is None)
            the value to set variable to, or the dict to set whole timedata namelist,
            if variable equals None
        """
        if variable == None:
            self.timedata = data
        else:
            self.timedata[variable] = data

    def get_commonsdata(self, variable:str = None):
        """return commonsdata namelist as dict, or the values of a specified variable in commonsdata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function returns the commonsdata namelist as dict
            if str, this function returns the value of the corresponding variable 
        """
        if variable == None:
            return self.commonsdata
        else:
            return(self.commonsdata[variable])

    def set_commonsdata(self, data, variable:str = None):
        """set commonsdata namelist, or the values of a specified variable in commonsdata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function sets the complete commonsdata namelist
            if str, this function sets the value of the corresponding variable 
        data : float, int (depending on variable) or dict (if variable is None)
            the value to set variable to, or the dict to set whole commonsdata namelist,
            if variable equals None
        """
        if variable == None:
            self.commonsdata = data
        else:
            self.commonsdata[variable] = data

    def get_aerosoldata(self, type = None, variable:str = None):
        """return data namelist as dict, or the values of a specified variable in data
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function returns the data namelist as dict
            if str, this function returns the value of the corresponding variable 
        """
        if variable == type == None:
            return self.aerosoldata
        elif (variable == None):
                return(self.aerosoldata[type-1])
        else:
            return(self.aerosoldata[type-1][variable])
        
    def set_aerosoldata(self, data, type=None, variable:str = None):
        """set data namelist, or the values of a specified variable in data
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function sets the complete data namelist
            if str, this function sets the value of the corresponding variable 
        data : float, int (depending on variable) or dict (if variable is None)
            the value to set variable to, or the dict to set whole data namelist,
            if variable equals None
        """
        if variable==type==None:
            self.aerosoldata = data
            self.nat = len(data)
        elif variable ==None:
            self.aerosoldata[type-1] = data
        else:
            self.aerosoldata[type-1][variable] = data

    def get_dynamicsdata(self, variable:str = None):
        """return dynamicsdata namelist as dict, or the values of a specified variable in dynamicsdata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function returns the dynamicsdata namelist as dict
            if str, this function returns the value of the corresponding variable 
        """
        if variable == None:
            return self.dynamicsdata
        else:
            return(self.dynamicsdata[variable])
    
    def set_dynamicsdata(self, data, variable:str = None):
        """set dynamicsdata namelist, or the values of a specified variable in dynamicsdata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function sets the complete dynamicsdata namelist
            if str, this function sets the value of the corresponding variable 
        data : float, int (depending on variable) or dict (if variable is None)
            the value to set variable to, or the dict to set whole dynamicsdata namelist,
            if variable equals None
        """
        if variable == None:
            self.dynamicsdata = data
        else:
            self.dynamicsdata[variable] = data

    def get_outputdata(self, variable = None):
        """return outputdata namelist as dict, or the values of a specified variable in outputdata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function returns the outputdata namelist as dict
            if str, this function returns the value of the corresponding variable 
        """
        if variable == None:
            return self.outputdata
        else:
            return(self.outputdata[variable])
        
    def set_outputdata(self, data, variable:str = None):
        """set outputdata namelist, or the values of a specified variable in outputdata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function sets the complete outputdata namelist
            if str, this function sets the value of the corresponding variable 
        data : float, int (depending on variable) or dict (if variable is None)
            the value to set variable to, or the dict to set whole outputdata namelist,
            if variable equals None
        """
        if variable == None:
            self.outputdata = data
        else:
            self.outputdata[variable] = data

    def get_svocdata(self, variable:str = None):
        """return svocdata namelist as dict, or the values of a specified variable in svocdata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function returns the svocdata namelist as dict
            if str, this function returns the value of the corresponding variable 
        """
        if variable == None:
            return self.svocdata
        else:
            return(self.svocdata[variable])   
        
    def set_svocdata(self, data, variable:str = None):
        """set svocdata namelist, or the values of a specified variable in svocdata
        
        Parameters
        ----------
        variable : str or None (default is None)
            if None, this function sets the complete svocdata namelist
            if str, this function sets the value of the corresponding variable 
        data : float, int (depending on variable) or dict (if variable is None)
            the value to set variable to, or the dict to set whole svocdata namelist,
            if variable equals None
        """
        if variable == None:
            self.svocdata = data
        else:
            self.svocdata[variable] = data
        
    def get_nat(self):
        """return the value of nat, the number of aerosol-types"""
        return self.nat
    
    def normalize_massfracs(self):
        """scales massfracs, so that the sum equals 1"""
        for aer in self.aerosoldata:
            aer["massfracs"]=aer["massfracs"]/sum(aer["massfracs"])
    
    def save_to_file(self, fname:str ="PARSEC_UserVars.json"):
        """save this object to a .json file, which can be loaded later.
        see help(load_UserVars) for more information
        
        Parameters
        ----------
        fname : str
            name of the file to create
        """
        savedict={"timedata": js.dumps(self.get_timedata()), "commonsdata": js.dumps(self.get_commonsdata()), "aerosoldata": js.dumps(self.get_aerosoldata()), 
                  "dynamicsdata": js.dumps(self.get_dynamicsdata()), "outputdata": js.dumps(self.get_outputdata()), "svocdata": js.dumps(self.get_svocdata())}
        outfile= open(fname, "x")
        js.dump(savedict, outfile)
        outfile.close()

    def save_to_str(self):
        """return a json-string representing this object, that can be loaded later. See help(load_UserVars) for more information
        """
        savedict={"timedata": js.dumps(self.get_timedata()), "commonsdata": js.dumps(self.get_commonsdata()), "aerosoldata": js.dumps(self.get_aerosoldata()), 
                  "dynamicsdata": js.dumps(self.get_dynamicsdata()), "outputdata": js.dumps(self.get_outputdata()), "svocdata": js.dumps(self.get_svocdata())}
        return(js.dumps(savedict))
    
    def _custaer(self, customaer, nat):
        self.customaerosol = customaer
        self.nat = nat

    def create_namelist_file(self, dir:str = ""):
        """creates the file namelist_UserVars.in, to be read as input by PARSEC-UFO.
        All variables are set to the values stored in this data-structure.
        
        Parameters
        ----------
        dir : directory as str
            directory to create the .in file, if used for PARSEC-UFO input, this should be the input directory
        """
        namelist = open(dir+"namelist_UserVars.in", "w")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!                           --- VARIABLES FOR ICPM ---                         !\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("! --- Time data ---\n")
        namelist.write("&timedata\n")
        namelist.write("dt         = " + str(self.get_timedata("dt")) + ",   !< Timestep for chemistry and coalescence [s]\n")
        namelist.write("dtsub      = " + str(self.get_timedata("dtsub")) + ",   !< Timestep for dynamics/microphysics (< step for chemistry) [s]\n")
        namelist.write("time_limit = " + str(self.get_timedata("time_limit")) + ",   !< Upper simulation time limit [s] (a safety clause to end simulation)\n")
        namelist.write("!\n")
        namelist.write("&END\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("! --- Commons data ---\n")
        namelist.write("&commonsdata\n")
        namelist.write("na         = " + str(self.get_commonsdata("na")) + ",  !< Number of bins per aerosol type\n")
        namelist.write("na_coa     = " + str(self.get_commonsdata("na_coa")) + ",  !< Number of bins in precipitation distribution\n")
        namelist.write("nat        = "+str(self.get_nat()) + ",  !< Number of different aerosol compositions (types)\n")
        namelist.write("mass_accom = " + str(self.get_commonsdata("mass_accom")) + ",  !< Mass accommodation coefficient [dimensionless]\n")
        namelist.write("surf_tens_w  = " + str(self.get_commonsdata("surf_tens_w")) + ",  !< Surface tension [mN/m] (milli Newtons per m)\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!  tracegas concentrations [ppm-v]: so2, o3, h2o2, nho3, nh3, co2\n")
        namelist.write("gasconcppm = " + _printfloatarray(self.get_commonsdata("gasconcppm")) + " \n")
        namelist.write("!\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        if self.customaerosol <= 1:
            aertype = 1
            while (aertype <= self.get_nat()):
                typedict=self.get_aerosoldata(type=aertype)
                namelist.write("! --- define aerosol data for if nat="+str(aertype)+" ---\n")
                if self.customaerosol == 0:
                    namelist.write("!Aer"+str(aertype)+"_modeX(1) :: Nx: number conc [m-3] || Aer"+str(aertype)+"_propertyX(2) :: Rx: mean radius (um) || Aer"+str(aertype)+"_propertyX(3) :: GSD [nm]\n")
                    namelist.write("Aer"+str(aertype)+"_Nlognorm_modes = "+str(typedict["Nmodes"]) +"\n")
                    mode = 1
                    while (mode <= typedict["Nmodes"]):
                        namelist.write("Aer"+str(aertype)+"_mode"+str(mode) +" = "+_printfloatarray(typedict["mode"+str(mode)])+",\n")
                        mode = mode+1
                namelist.write("!Aer"+str(aertype)+"_massfracs: The sequence of species is: h2so4, (nh4)hso4, (nh4)2so4, OC, BC, dust, seasalt\n")
                namelist.write("Aer"+str(aertype)+"_massfracs = "+_printfloatarray(typedict["massfracs"])+", \n")
                namelist.write("!\n")
                namelist.write("!---------------------------------------\n")
                aertype = aertype+1

        namelist.write("! Variables for usage with init_aer_m7 aerosol initialisation\n")
        namelist.write("! Sulfate [molec/g]\n")
        namelist.write("! conc_nucleation_mode: Sulfate (iso4ns) [molec/g]\n")
        namelist.write("conc_nucleation_mode = 0.,\n")
        namelist.write("! conc_aitken_mode: Sulfate (iso4ks) [molec/g]; Black carbon (ibcks) [ug/g]; Organic carbon (iocks) [ug/g]\n")
        namelist.write("conc_aitken_mode = 0., 0., 0.,\n")
        namelist.write("! conc_accumulation_mode: Sulfate (iso4as) [molec/g]; Black carbon (ibcas) [ug/g]; Organic carbon (iocas) [ug/g]; Sea salt (issas) [ug/g]; Dust (iduas) [ug/g]\n")
        namelist.write("conc_accumulation_mode = 0., 0., 0., 0., 0.,\n")
        namelist.write("! conc_coarse_mode: Sulfate (iso4cs) [molec/g]; Black carbon (ibccs) [ug/g]; Organic carbon (ioccs) [ug/g]; Sea salt (isscs) [ug/g]; Dust (iducs) [ug/g]\n")
        namelist.write("conc_coarse_mode = 0., 0., 0., 0., 0.,\n")
        namelist.write("!\n")
        namelist.write("&END\n")
        namelist.write("!\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("! --- Dynamics data ---\n")
        namelist.write("&dynamicsdata\n")
        namelist.write("initial_temperature = " + str(self.get_dynamicsdata("initial_temperature")) + "          !< Temperature [K] (only needed if iupadiabat=FALSE)\n")
        namelist.write("initial_pressure    = " + str(self.get_dynamicsdata("initial_pressure")) + ",          !< Pressure [Pa]\n")
        namelist.write("updraft             = " + str(self.get_dynamicsdata("updraft")) + ",          !< Updraft velocity [m/s]\n")
        namelist.write("downdraft           = " + str(self.get_dynamicsdata("downdraft")) + ",          !< Downdraft velocity [m/s] (this number should be positive, only works with vcycles>0)\n")
        namelist.write("initial_relhum      = " + str(self.get_dynamicsdata("initial_relhum")) + ",          !< Relative humidity [percentage]\n")
        namelist.write("entrainment_param   = " + str(self.get_dynamicsdata("entrainment_param")) + ",          !< Entrainment parameter, between 0 and 1 [dimensionless]\n")
        namelist.write("cloud_depth         = " + str(self.get_dynamicsdata("cloud_depth")) + ",          !< Cloud depth [m]\n")
        namelist.write("initial_height      = " + str(self.get_dynamicsdata("initial_height")) + ",          !< Initial parcel height [m]\n")
        namelist.write("initial_radius      = " + str(self.get_dynamicsdata("initial_radius")) + ",          !< Initial parcel radius [m]\n")
        namelist.write("zstopheight         = " + str(self.get_dynamicsdata("zstopheight")) + ",          !< Only activates if istopheight=TRUE. The parcel vertical velocity is set to 0 at this height.\n")
        namelist.write("!\n")
        namelist.write("&END\n")
        namelist.write("!\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("! --- Output data ---\n")
        namelist.write("&outputdata\n")
        namelist.write("pheightstep = " + str(self.get_outputdata("pheightstep")) + ",                              !< Profile step length [m]\n")
        namelist.write("fixed_level_altitude_outputs = " + _printarray(self.get_outputdata("fixed_level_altitude_outputs")) + \
                       ",                           !< Fixed levels to output at, must be used with ihoutputs=T. outputs to specH files\n")
        namelist.write("&END\n")
        namelist.write("!\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("! --- SVOC ---\n")
        namelist.write("&svocdata\n")
        namelist.write("initial_ctot = "+_printfloatarray(self.get_svocdata("initial_ctot"))+", !< relative total concentrations [dimensionless]\n")
        namelist.write("log_cstar_org = "+_printfloatarray(self.get_svocdata("log_cstar_org"))+", !< Volatility bins (can use up to 16 bins)\n")
        namelist.write("min_org_film_thick   = "+str(self.get_svocdata("min_org_film_thick"))+",            !< Minimum organic film thickness [nm] query: might be meters\n")
        namelist.write("sigma_org            = "+str(self.get_svocdata("sigma_org"))+",            !< Organics surface tension [mNm-1]\n")
        namelist.write("org_sol_frac         = "+str(self.get_svocdata("org_sol_frac"))+",            !< Soluble fraction used for non-VBS organic component when not modelling surface phase [dimensionless] (0->1)\n")
        namelist.write("org_sol_frac_cf      = "+str(self.get_svocdata("org_sol_frac_cf"))+",            !< Soluble fraction used for approximate compressed film model [dimensionless] (0->1)\n")
        namelist.write("org_e_sol_frac_vbs   = "+str(self.get_svocdata("org_e_sol_frac_vbs"))+",            !< Effective solubility fraction [dimensionless] (0->1)\n")
        namelist.write("org_densities        = "+str(self.get_svocdata("org_densities"))+",            !< Organic densitites (same for all organics) [kg m-3]\n")
        namelist.write("org_mol_mass         = "+str(self.get_svocdata("org_mol_mass"))+",            !< Organic molar mass (same for all organics) [kg mol-1]\n")
        namelist.write("org_vap_enthalpy     = "+str(self.get_svocdata("org_vap_enthalpy"))+",            !< Organic enthalpy of vapourisation (same for all organics) [J mol-1]\n")
        namelist.write("org_alpha            = "+str(self.get_svocdata("org_alpha"))+",            !< Organic mass accommodation coefficient (same for all organics) [dimensionless] (0->1)\n")
        namelist.write("!\n")
        namelist.write("&END\n")
        namelist.write("!\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!END OF FILE\n")
        namelist.close()


def load_UserVars(fname:str="PARSEC_UserVars.json", jsstring:str=None):
    """loads a PARSEC_UserVars instance from given json string or file. If both are input the string is prioritized

    Parameters
    ----------
    fname : str
        path/name of the file to load, see help(PARSEC_UserVars.save_to_file). Is ignored it jsstring != None
    jsstring : str
        json string to load the instance from, see help(PARSEC_UserVars.save_to_str)
    """
    if jsstring != None:
        loaddata = js.loads(jsstring)
    else:
        try:
            loadfile = open(fname)
            loaddata = js.load(loadfile)
            loadfile.close()
        except:
            return None
    return( PARSEC_UserVars(timedata=js.loads(loaddata["timedata"]), commonsdata=js.loads(loaddata["commonsdata"]), aerosoldata=js.loads(loaddata["aerosoldata"]), \
                            dynamicsdata=js.loads(loaddata["dynamicsdata"]), outputdata=js.loads(loaddata["outputdata"]), svocdata=js.loads(loaddata["svocdata"])))

class PARSEC_Switches:
    """class holding all switches for PARSEC-UFO. Includes methods for saving and creating the namelist_switches.in file

    Parameters
    ----------
    initflag : int
        1/2/3/4/5 Sets which aerosol input is desired (2-5 are pre-defined aerosol cases, 1 is user input)
        1 = Will use parameters set in namelist_UserVars.in
        2 = Pre-defined marine average parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)
        3 = Pre-defined marine arctic parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)
        4 = Pre-defined clean continental parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)
        5 = Pre-defined polluted parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)
        See documentation for full defails of the pre-defined cases and full references.
    kprecip : int
        0/1/2/... Number of sub time-steps for precipitation formation through coalescence.
    vcycles : int
        Specify number of vertical up/down cycles through cloud.
    envprofile : int
        1/2/3 Used to switch between environmental temperature profiles.
        1 = User-defined profile
        2 = Pre-defined summer profile
        3 = Pre-defined winter profile
        For full defails on these temperature profiles, see documentation.
        NOTE: only has an effect when iupadiabat=FALSE.
    initwav : int
        1/2/3 Which wavelength file to use for calculation of optical properties.
        1 = user specified
        2 = Pre-defined, using king air campaign instrumentation
        3 = Pre-defined, using ukesm1 campaign instrumentation
        4 = Pre-defined, using activate campaign instrumentation
        For full defails on these wavelengths, see documentation.
    initrebin : int
        1/2/3 Specify which limits to use in the rebinning of the droplet spectra.
        1 = User specified
        2 = Pre-defined, using maseii campaign instrumentation
        3 = Pre-defined, using activate campaign instrumentation
        For full defails on these rebin limits, see documentation.
    initaer : int
        1/2 Sets which aerosol initialisation to use.
        1 = default
        2 = m7par.
    customaer : int
        0/1/2 Sets which aerosol inputs are input from .dat files
        0 = None
        1 = size-distribution (including bins)
        2 = size distribution and composition           
    ccn_output_type : int
        1/2 `ccn_conc_spectrum` will be converted from [number/g of air]->[Number/cm3] using either:
        1 = rho (as calculated within the model);
        2 = p/(RT) (following the ideal gas law).
    iupconst : int
        1/2/3 Defines the updraft/downdraft behaviour.
        1 = Constant updraft/downdraft velocity defined by user-input
        2 = Buoyancy explicitly calculated by the model, and used to set the vertical velocity
        3 = updraft/downdraft behaviour based on height trajectory given by user
    istoptop : bool 
        T/F T = When parcel reaches neutral buoyancy and begins to fall, stop the vertical ascent/descent.
        NOTE: may only be used with iupconst=2.
    irainfall : bool
        T/F T = Perform gravitational settling of precipitation sized drops
    iupadiabat : bool
        T/F Specify ascent/descent dynamics type.
        T = Adiabatic
        F = Pseudo-adiabatic
    iaerenv : bool
        T/F Entraining switch.
        T = Entraining with aerosols (not currenly operational, do not use).
        F = Entraining without aerosols
    istopheight : bool
        T/F T = Parcel will stop vertical ascent at specified height through cloud, see `zstopheight` to set depth from cloud base.
        With this TRUE, be careful to set `time_limit` to a sensible value.
    vclowheight : bool
        T/F Defines lower limit for vcycles.
        T = cloud base
        F = initial heigth
    iendssmax : bool
        T/F T = End simulation at maximum supersaturation
    ihoutputs : bool
        T/F T = Use inputs/fixed_level_alt_out.dat to output at specific height levels
    interp : bool
        T/F T = Perform interpolation after main loop directly onto pheightstep levels
    output_logs : bool
        T/F T = Re-direct the standard I/O output is to `logs/logs.txt` and logs/logs_errors.txt`
    icompfilm : bool
        T/F T=ON F=OFF Approximate compressed film model (Lowe et al. NatComms)
    icondsvocs : bool
        T/F T=ON F=OFF Implementation of SVOC condensation equations
    out_aerdat : bool
        T/F T=ON F=OFF output .dat files of custom aerosol, analogous to custom aerosol input
    icwc : bool
        T/F T=ON F=OFF aqueous phase chemistry calculations(Sulfate production)"""
    def __init__(self, initflag:int=1, kprecip:int=0, vcycles:int=0, envprofile:int=1, initwav:int=1, initrebin:int=1, initaer:int=1, customaer:int=0, ccn_output_type:int=1, iupconst:int=1, istoptop:bool=False, \
                irainfall:bool=False, iupadiabat:bool=True, iaerenv:bool=False, istopheight:bool=False, vclowheight:bool=True, iendssmax:bool=False, ihoutputs:bool=False, interp:bool=True, \
                output_logs:bool=True, icompfilm:bool=False, icondsvocs:bool=False, out_aerdat:bool=False, icwc:bool=False):
        """
        Parameters
        ----------
        initflag : int
            1/2/3/4/5 Sets which aerosol input is desired (2-5 are pre-defined aerosol cases, 1 is user input)
            1 = Will use parameters set in namelist_UserVars.in
            2 = Pre-defined marine average parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)
            3 = Pre-defined marine arctic parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)
            4 = Pre-defined clean continental parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)
            5 = Pre-defined polluted parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)
            See documentation for full defails of the pre-defined cases and full references.
        kprecip : int
            0/1/2/... Number of sub time-steps for precipitation formation through coalescence.
        vcycles : int
            Specify number of vertical up/down cycles through cloud.
        envprofile : int
            1/2/3 Used to switch between environmental temperature profiles.
            1 = User-defined profile
            2 = Pre-defined summer profile
            3 = Pre-defined winter profile
            For full defails on these temperature profiles, see documentation.
            NOTE: only has an effect when iupadiabat=FALSE.
        initwav : int
            1/2/3 Which wavelength file to use for calculation of optical properties.
            1 = user specified
            2 = Pre-defined, using king air campaign instrumentation
            3 = Pre-defined, using ukesm1 campaign instrumentation
            4 = Pre-defined, using activate campaign instrumentation
            For full defails on these wavelengths, see documentation.
        initrebin : int
            1/2/3 Specify which limits to use in the rebinning of the droplet spectra.
            1 = User specified
            2 = Pre-defined, using maseii campaign instrumentation
            3 = Pre-defined, using activate campaign instrumentation
            For full defails on these rebin limits, see documentation.
        initaer : int
            1/2 Sets which aerosol initialisation to use.
            1 = default
            2 = m7par.
        customaer : int
            0/1/2 Sets which aerosol inputs are input from .dat files
            0 = None
            1 = size-distribution (including bins)
            2 = size distribution and composition           
        ccn_output_type : int
            1/2 `ccn_conc_spectrum` will be converted from [number/g of air]->[Number/cm3] using either:
            1 = rho (as calculated within the model);
            2 = p/(RT) (following the ideal gas law).
        iupconst : int
            1/2/3 Defines the updraft/downdraft behaviour.
            1 = Constant updraft/downdraft velocity defined by user-input
            2 = Buoyancy explicitly calculated by the model, and used to set the vertical velocity
            3 = updraft/downdraft behaviour based on height trajectory given by user
        istoptop : bool 
            T/F T = When parcel reaches neutral buoyancy and begins to fall, stop the vertical ascent/descent.
            NOTE: may only be used with iupconst=2.
        irainfall : bool
            T/F T = Perform gravitational settling of precipitation sized drops
        iupadiabat : bool
            T/F Specify ascent/descent dynamics type.
            T = Adiabatic
            F = Pseudo-adiabatic
        iaerenv : bool
            T/F Entraining switch.
            T = Entraining with aerosols (not currenly operational, do not use).
            F = Entraining without aerosols
        istopheight : bool
            T/F T = Parcel will stop vertical ascent at specified height through cloud, see `zstopheight` to set depth from cloud base.
            With this TRUE, be careful to set `time_limit` to a sensible value.
        vclowheight : bool
            T/F Defines lower limit for vcycles.
            T = cloud base
            F = initial heigth
        iendssmax : bool
            T/F T = End simulation at maximum supersaturation
        ihoutputs : bool
            T/F T = Use inputs/fixed_level_alt_out.dat to output at specific height levels
        interp : bool
            T/F T = Perform interpolation after main loop directly onto pheightstep levels
        output_logs : bool
            T/F T = Re-direct the standard I/O output is to `logs/logs.txt` and logs/logs_errors.txt`
        icompfilm : bool
            T/F T=ON F=OFF Approximate compressed film model (Lowe et al. NatComms)
        icondsvocs : bool
            T/F T=ON F=OFF Implementation of SVOC condensation equations
        out_aerdat : bool
            T/F T=ON F=OFF output .dat files of custom aerosol, analogous to custom aerosol input
        icwc : bool
            T/F T=ON F=OFF aqueous phase chemistry calculations(Sulfate production)"""
        self.values={"initflag": initflag, "kprecip": kprecip, "vcycles": vcycles, "envprofile": envprofile, "initwav": initwav, "initrebin": initrebin, \
                     "initaer": initaer, "customaer": customaer, "ccn_output_type": ccn_output_type, "iupconst": iupconst, "istoptop": istoptop, "irainfall": irainfall, \
                     "iupadiabat": iupadiabat, "iaerenv": iaerenv, "istopheight": istopheight, "vclowheight": vclowheight, "iendssmax": iendssmax, \
                     "ihoutputs": ihoutputs, "interp": interp, "output_logs": output_logs, "icompfilm": icompfilm, "icondsvocs": icondsvocs, "out_aerdat": out_aerdat, 
                     "icwc": icwc}
    def getvalue(self, variable:str):
        """return the value of any switch
        Parameters
        ----------
        variable : str
            variable to return value of. See parameters in help(type(self)) 
        """
        return self.values[variable]
    
    def getallvalues(self):
        """return a dictonary with all variables and values of the instance
        """
        return self.values
    
    def setvalue(self, variable:str, value:any):
        """set the value of any switch. See parameters in help(type(self)) 
        Parameters
        ----------
        variable : str
            variable to set value of
        value : int or bool
            value to set the switch to. Make sure the type/range match those specified in help(type(self))
        """
        self.values[variable] = value
    
    def setallvalues(self, dict:dict):
        """set the values of all variables"""
        self.values=dict

    def create_namelist_file(self, dir:str = ""):
        """creates the file namelist_switches.in, to be read as input by PARSEC-UFO.
        All variables are set to the values stored in this data-structure.
        
        Parameters
        ----------
        dir : directory as str
            directory to create the .in file, if used for PARSEC-UFO input, this should be the input directory
        """
        namelist = open(dir+"namelist_switches.in", "w")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!                        --- USER SWITCHES FOR ICPM ---                        !\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("! Switches\n")
        namelist.write("&switchdata\n")
        namelist.write("initflag        = "+str(self.getvalue("initflag"))+",      !< 1/2/3/4/5 : Sets which aerosol input is desired (2-5 are pre-defined aerosol cases)\n")
        namelist.write("                        !!               1 = Will use parameters set in namelist_UserVars.in\n")
        namelist.write("                        !!               2 = Pre-defined marine average parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)\n")
        namelist.write("                        !!               3 = Pre-defined marine arctic parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)\n")
        namelist.write("                        !!               4 = Pre-defined clean continental parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)\n")
        namelist.write("                        !!               5 = Pre-defined polluted parameters from DP2012, DP2011 (all other switches in this namelist will be overrided)\n")
        namelist.write("                        !!               See documentation for full defails of the pre-defined cases and full references.\n")
        namelist.write("kprecip         = "+str(self.getvalue("kprecip"))+",       !< 0/1/2/... : Number of sub time-steps for precipitation formation through coalescence.\n")
        namelist.write("vcycles         = "+str(self.getvalue("vcycles"))+",       !< 0/1/2/... : Specify number of vertical up/down cycles through cloud.\n")
        namelist.write("envprofile      = "+str(self.getvalue("envprofile"))+",    !< 1/2/3 : Used to switch between environmental temperature profiles.\n")
        namelist.write("                        !!               1 = User-defined profile\n")
        namelist.write("                        !!               2 = Pre-defined summer profile\n")
        namelist.write("                        !!               3 = Pre-defined winter profile\n")
        namelist.write("                        !!               For full defails on these temperature profiles, see documentation.\n")
        namelist.write("                        !!               NOTE: only has an effect when iupadiabat=FALSE.\n")
        namelist.write("initwav         = "+str(self.getvalue("initwav"))+",       !< 1/2/3 : Which wavelength file to use for calculation of optical properties.\n")
        namelist.write("                        !!               1 = user specified\n")
        namelist.write("                        !!               2 = Pre-defined, using king air campaign instrumentation\n")
        namelist.write("                        !!               3 = Pre-defined, using ukesm1 campaign instrumentation\n")
        namelist.write("                        !!               4 = Pre-defined, using activate campaign instrumentation\n")
        namelist.write("                        !!               For full defails on these wavelengths, see documentation.\n")
        namelist.write("initrebin       = "+str(self.getvalue("initrebin"))+",     !< 1/2/3 : Specify which limits to use in the rebinning of the droplet spectra.\n")
        namelist.write("                        !!               1 = User specified\n")
        namelist.write("                        !!               2 = Pre-defined, using maseii campaign instrumentation\n")
        namelist.write("                        !!               3 = Pre-defined, using activate campaign instrumentation\n")
        namelist.write("                        !!               For full defails on these rebin limits, see documentation.\n")
        namelist.write("initaer         = "+str(self.getvalue("initaer"))+",        !< 1/2 : Sets which aerosol initialisation to use.\n")
        namelist.write("                        !!               1 = default\n")
        namelist.write("                        !!               2 = m7par.\n")
        namelist.write("customaer = "+str(self.getvalue("customaer"))+",              !< 0/1/2 : Sets which aerosol inputs are input from .dat files\n")
        namelist.write("                        !!               0 = None\n")
        namelist.write("                        !!               1 = size-distribution (including bins)\n")
        namelist.write("                        !!               2 = size distribution and composition \n")
        namelist.write("ccn_output_type = "+str(self.getvalue("ccn_output_type"))+",!< 1/2 : `ccn_conc_spectrum` will be converted from [number/g of air]->[Number/cm3] using either:\n")
        namelist.write("                        !!               1 = rho (as calculated within the model);\n")
        namelist.write("                        !!               2 = p/(RT) (following the ideal gas law).\n")
        namelist.write("iupconst        = "+str(self.getvalue("iupconst"))+",       !< 1/2/3 : Defines the updraft/downdraft behaviour.\n")
        namelist.write("                        !!               1 = Constant updraft/downdraft velocity defined by user-input\n")
        namelist.write("                        !!               2 = Buoyancy explicitly calculated by the model, and used to set the vertical velocity\n")
        namelist.write("                        !!               3 = updraft/downdraft behaviour based on height trajectory given by user\n")
        namelist.write("istoptop        = "+_boolstr(self.getvalue("istoptop"))+",       !< T/F : T = When parcel reaches neutral buoyancy and begins to fall, stop the vertical ascent/descent.\n")
        namelist.write("                        !!               NOTE: may only be used with iupconst=FALSE.\n")
        namelist.write("irainfall       = "+_boolstr(self.getvalue("irainfall"))+",      !< T/F : T = Perform gravitational settling of precipitation sized drops\n")
        namelist.write("iupadiabat      = "+_boolstr(self.getvalue("iupadiabat"))+",     !< T/F : Specify ascent/descent dynamics type.\n")
        namelist.write("                        !!               T = Adiabatic\n")
        namelist.write("                        !!               F = Pseudo-adiabatic\n")
        namelist.write("iaerenv         = "+_boolstr(self.getvalue("iaerenv"))+",        !< T/F : Entraining switch.\n")
        namelist.write("                        !!               T = Entraining with aerosols (not currenly operational, do not use).\n")
        namelist.write("                        !!               F = Entraining without aerosols\n")
        namelist.write("istopheight     = "+_boolstr(self.getvalue("istopheight"))+",    !< T/F : T = Parcel will stop vertical ascent at specified height through cloud, see `zstopheight` to set depth from cloud base.\n")
        namelist.write("                        !!               With this TRUE, be careful to set `time_limit` to a sensible value.\n")
        namelist.write("vclowheight     = "+_boolstr(self.getvalue("vclowheight"))+",       !< T/F : Defines lower limit for vcycles.\n")
        namelist.write("                        !!              T = cloud base\n")
        namelist.write("                        !!              F = initial heigth\n")
        namelist.write("iendssmax       = "+_boolstr(self.getvalue("iendssmax"))+",      !< T/F : T = End simulation at maximum supersaturation\n")
        namelist.write("ihoutputs       = "+_boolstr(self.getvalue("ihoutputs"))+",      !< T/F : T = Use inputs/fixed_level_alt_out.dat to output at specific height levels\n")
        namelist.write("interp          = "+_boolstr(self.getvalue("interp"))+",         !< T/F : T = Perform interpolation after main loop directly onto pheightstep levels\n")
        namelist.write("output_logs     = "+_boolstr(self.getvalue("output_logs"))+",    !< T/F : T = Re-direct the standard I/O output is to `logs/logs.txt` and logs/logs_errors.txt`\n")
        namelist.write("icompfilm       = "+_boolstr(self.getvalue("icompfilm"))+",      !< T/F : T=ON F=OFF : Approximate compressed film model (Lowe et al. NatComms)\n")
        namelist.write("icondsvocs      = "+_boolstr(self.getvalue("icondsvocs"))+",     !< T/F : T=ON F=OFF : Implementation of SVOC condensation equations\n")
        namelist.write("out_aerdat      = "+_boolstr(self.getvalue("out_aerdat"))+",     !< T/F : T=ON F=OFF : output .dat files of custom aerosol, analogous to custom aerosol input\n")
        namelist.write("icwc            = "+_boolstr(self.getvalue("icwc"))+",     !< T/F : T=ON F=OFF : aqueous phase chemistry calculations(Sulfate production)\n")
        namelist.write("&END\n")
        namelist.write("!\n")
        namelist.write("!-------------------------------------------------------------------------------\n")
        namelist.write("!END OF FILE\n")
        namelist.close()

    def save_to_file(self, fname:str="PARSEC_switches.json"):
        """save this object to a .json file, which can be loaded later.
        see help(load_switches) for more information
        
        Parameters
        ----------
        fname : str
            name of the file to create
        """
        outfile= open(fname, "x")
        js.dump(self.values, outfile)
        outfile.close()

    def save_to_str(self):
        """return a json-string representing this object, that can be loaded later. See help(load_switches) for more information
        """
        return(js.dumps(self.values))


def load_switches(fname:str="PARSEC_switches.json", jsstring:str=None):
    """loads a PARSEC_switches instance from given json string or file. If both are input the string is prioritized

    Parameters
    ----------
    fname : str
        path/name of the file to load, see help(PARSEC_switches.save_to_file). Is ignored it jsstring != None
    jsstring : str
        json string to load the instance from, see help(PARSEC_switches.save_to_str)
    """
    if jsstring != None:
        loaddata = js.loads(jsstring)
    else:
        try:
            loadfile = open(fname)
            loaddata = js.load(loadfile)
            loadfile.close()
        except:
            return None
    switches = PARSEC_Switches()
    switches.setallvalues(loaddata)
    return (switches)

class PARSEC_rebin:
    """class holding lists describing bins for rebining in PARSEC-UFO. Also provides methods to store or create input for PARSEC-UFO
    
    Parameters
    ----------
    midpoint_radii : list[float]
        midpoints for rebin [m]
    size_limits : list[list[float]]
        size limits for rebin [m]. Each entry holds a list of length 2 representing [lower_limit, upper_limit]. Length should be the same as midpoint_radii
    """
    def __init__(self, midpoint_radii:list[float] =[1.1225E-06,1.27279E-06,1.42302E-06,1.64317E-06,1.94422E-06,2.31409E-06,2.92276E-06,3.6606E-06,4.31277E-06,4.91732E-06, \
                                        5.49181E-06,6.1636E-06,7.03225E-06,8.03446E-06,9.17701E-06,1.05268E-05,1.19765E-05,1.35734E-05,1.53471E-05,1.76214E-05], \
                 size_limits:list[list[float]]=[[1.05E-06,1.20E-06],[1.20E-06,1.35E-06],[1.35E-06,1.50E-06],[1.50E-06,1.80E-06],[1.80E-06,2.10E-06],[2.10E-06,2.55E-06], \
                                                    [2.55E-06,3.35E-06],[3.35E-06,4.00E-06],[4.00E-06,4.65E-06],[4.65E-06,5.20E-06],[5.20E-06,5.80E-06],[5.80E-06,6.55E-06], \
                                                    [6.55E-06,7.55E-06],[7.55E-06,8.55E-06],[8.55E-06,9.85E-06],[9.85E-06,1.13E-05],[1.13E-05,1.28E-05],[1.28E-05,1.45E-05], \
                                                    [1.45E-05,1.63E-05],[1.63E-05,1.91E-05]]):
        """Parameters
        ----------
        midpoint_radii : list[float]
            midpoints for rebin [m]
        size_limits : list[list[float]]
            size limits for rebin [m]. Each entry holds a list of length 2 representing [lower_limit, upper_limit]. Length should be the same as midpoint_radii
        """
        self.nbins = len(midpoint_radii)
        self.midpoint_radii = midpoint_radii
        self.size_limits = size_limits
    
    def set_midpoint_radii(self, midpoint_radii):
        """set midpoint radii and number of bins

        Parameters
        ----------
        midpoint_radii : list
            midpoint radii to set to. If length is different then nbins before set, make sure the size limits are altered accordingly. See help(self.set_size_limits)
        """
        self.midpoint_radii =midpoint_radii
        self.nbins = len(midpoint_radii)
    
    def get_midpoint_radii(self):
        """return list of midpoint radii
        """
        return self.midpoint_radii
    
    def set_size_limits(self, size_limits):
        """set size limits

        Parameters
        ----------
        midpoint_radii : list
            new size limits. Make sure the length matches number of bins (self.get_nbins)
        """
        self.size_limits =size_limits
    
    def get_size_limits(self):
        """return list of size limits
        """
        return self.size_limits
    
    def get_nbins(self):
        """return number of rebin bin
        """
        return self.nbins
    
    def create_dat_files(self, dir:str=""):
        """Creates the files 'rebin-midpoint_radii.dat' and 'rebin-size_limits.dat', to be read as input by PARSEC-UFO.
        All values are set according to the lists stored in this data-structure.
        
        Parameters
        ----------
        dir : directory as str
            directory to create the .dat files, if used for PARSEC-UFO input, this should be the input directory
        """
        midpfile=open(dir+"rebin-midpoint_radii.dat", "x")
        for midp in self.get_midpoint_radii():
            midpfile.write(str(midp)+"\n")
        midpfile.close()
        slimfile=open(dir+"rebin-size_limits.dat", "x")
        slims = self.get_size_limits()
        for i in range(self.get_nbins()):
            slimfile.write(str(slims[i][0])+"\t")
            slimfile.write(str(slims[i][1])+"\n")
        slimfile.close()

    def save_to_file(self,fname:str="PARSEC_rebin.json"):
        """save this object to a .json file, which can be loaded later.
        see help(load_rebin) for more information
        
        Parameters
        ----------
        fname : str
            name of the file to create
        """
        outfile=open(fname, "x")
        js.dump({"midpoint_radii": self.midpoint_radii, "size_limits": self.size_limits}, outfile)
        outfile.close()

    def save_to_str(self,):
        """return a json-string representing this object, that can be loaded later. See help(load_rebin) for more information
        """
        return(js.dumps({"midpoint_radii": self.midpoint_radii, "size_limits": self.size_limits}))


def load_rebin(fname:str ="PARSEC_rebin.json", jsstring:str = None):
    """loads a PARSEC_rebin instance from given json string or file. If both are input the string is prioritized

    Parameters
    ----------
    fname : str
        path/name of the file to load, see help(PARSEC_rebin.save_to_file). Is ignored it jsstring != None
    jsstring : str
        json string to load the instance from, see help(PARSEC_rebin.save_to_str)
    """
    if jsstring != None:
        loaddata = js.loads(jsstring)
    else:
        try:
            loadfile = open(fname)
            loaddata = js.load(loadfile)
            loadfile.close()
        except:
            return None
    return PARSEC_rebin(midpoint_radii=loaddata["midpoint_radii"], size_limits=loaddata["size_limits"])

class PARSEC_wavelengths:
    """class holding lists describing bins for rebining in PARSEC-UFO. Also provides methods to store or create input for PARSEC-UFO

    Parameters
    ----------
    wavelengths : list[float]
        list of wavelengths
    """
    def __init__(self, wavelengths:list[float] =[0.355e-6,0.532e-6,1.064e-6]):
        """"Initialize self.  See help(type(self)) for accurate signature.
        """
        self.wavelengths = wavelengths

    def set_wavelengths(self, wavelengths:list[float]):
        """set wavelengths
        Parameters
        ----------
        wavelengths : list[float]
            list of new wavelengths
        """
        self.wavelengths = wavelengths
    
    def get_wavelengths(self):
        """return list of wavelengths
        """
        return(self.wavelengths)
    
    def create_dat_file(self, dir:str=""):
        """Creates the file 'wavelenghts.dat', to be read as input by PARSEC-UFO.
        All values are set according to the list stored in this data-structure.
        
        Parameters
        ----------
        dir : directory as str
            directory to create the .dat file, if used for PARSEC-UFO input, this should be the input directory
        """
        datfile = open(dir+"wavelengths.dat", "x")
        for entr in self.get_wavelengths():
            datfile.write(str(entr) + "\n")
        datfile.close()

    def save_to_file(self, fname ="PARSEC_wavelenghts.json"):
        """save this object to a .json file, which can be loaded later.
        see help(load_wavelengths) for more information
        
        Parameters
        ----------
        fname : str
            name of the file to create
        """
        outfile = open(dir+fname, "x")
        js.dump({"wavelengths":self.get_wavelengths()}, outfile)
        outfile.close()
    
    def save_to_str(self):
        """return a json-string representing this object, that can be loaded later. See help(load_wavelengths) for more information
        """
        return(js.dumps({"wavelengths":self.get_wavelengths()}))


def load_wavelengths(fname:str="PARSEC_wavelenghts.json", jsstring:str = None):
    """loads a PARSEC_wavelengths instance from given json string or file. If both are input the string is prioritized

    Parameters
    ----------
    fname : str
        path/name of the file to load, see help(PARSEC_wavelengths.save_to_file). Is ignored it jsstring != None
    jsstring : str
        json string to load the instance from, see help(PARSEC_wavelengths.save_to_str)
    """
    if jsstring != None:
        loaddata = js.loads(jsstring)
    else:
        try:
            loadfile = open(fname)
            loaddata = js.load(loadfile)
            loadfile.close()
        except:
            return None
    return PARSEC_wavelengths(wavelengths=loaddata["wavelengths"])

class PARSEC_custom_aerosol:
    """class holding lists describing the custom aerosol input for PARSEC-UFO and methods for storage and creation of input files. 
    If using custom aerosol input make sure, that customaer switch is 1 or 2 (depending if custom concentration is desired)

    Parameters
    ----------
    midpoint_radii : list[float]
        list of midpoints for bins [m]
    size_limits : list[list[float]]
        list of size limits for bins [m]. Each entry is list with length 2 [lower_limit, upper_limit]. Should have same length as midpoint_radii
    concentration : list[list[float]]
        list of number concentrations for each bin [cm^-3]. The highest level contains one list for each aerosol type. The list for each aerosol type contains
        entrys for each bin (na) with the respective number concentration
    composition : list[list[list[float]]] or None
        composition for each aerosol type and bin in fractions of mass. The highest level contains one list for each aerosol type.
        The list for each aerosoltype has entries for each bin, each a list containing nmass entries (7 for PARSEC-UFOs current version), each representing one massfraction
        The order is [H2SO44, (NH4)HSO4, (NH4)2SO4, OC, BC, dust, seasalt]. massfracs should add up to 1, or be normalized in this data-structure(see help(self.normalize_composition))
        None if composition from UserVars is used
    """
    def __init__(self, midpoint_radii, size_limits, concentration, composition =None):
        """"Initialize self.  

        Parameters
        ----------
        midpoint_radii : list[float]
            list of midpoints for bins [m]
        size_limits : list[list[float]]
            list of size limits for bins [m]. Each entry is list with length 2 [lower_limit, upper_limit]. Should have same length as midpoint_radii
        concentration : list[list[float]]
            list of number concentrations for each bin [cm^-3]. The highest level contains one list for each aerosol type. The list for each aerosol type contains
            entrys for each bin (na) with the respective number concentration
        composition : list[list[list[float]]] or None
            composition for each aerosol type and bin in fractions of mass. The highest level contains one list for each aerosol type.
            The list for each aerosoltype has entries for each bin, each a list containing nmass entries (7 for PARSEC-UFOs current version), each representing one massfraction
            The order is [H2SO44, (NH4)HSO4, (NH4)2SO4, OC, BC, dust, seasalt]. massfracs should add up to 1, or be normalized in this data-structure(see help(self.normalize_composition))
            None if composition from UserVars is used
        """
        self.midpoint_radii = midpoint_radii
        self.size_limits = size_limits
        self.concentration = concentration
        self.composition = composition
        self.numbins = len(self.midpoint_radii)
        self.nat = len(self.concentration)
        if self.composition != None:
            self.nmass = len(self.composition[0][0])
        else:
            self.nmass = 0

    def get_concentration(self):
        """return list of number concentrations per bin
        """
        return(self.concentration)
    
    def set_concentration(self, concentration:list[list[float]]):
        """set number concentration for each aerosol type and bin
        
        Parameters
        ----------
        concentration : list[list[float]]
            list of number concentrations for each bin [cm^-3]. The highest level contains one list for each aerosol type. The list for each aerosol type contains
            entrys for each bin (na) with the respective number concentration
        """
        self.concentration = concentration

    def get_midpoint_radii(self):
        """return list of midpoint_radii per bin"""
        return(self.midpoint_radii)
    
    def get_size_limits(self):
        """return list of size limits per bin
        """
        return(self.size_limits)
    
    def get_numbins(self):
        """return nuber of bins
        """
        return(self.numbins)
    
    def get_nat(self):
        """return number of aerosol types
        """
        return self.nat
    
    def set_bins(self, midpoint_radii:list[float], size_limits:list[list[float]]):
        """set bins with new midpoints and size limits

        Parameters
        ----------
        midpoint_radii : list[float]
            list of midpoints for bins [m]
        size_limits : list[list[float]]
            list of size limits for bins [m]. Each entry is list with length 2 [lower_limit, upper_limit]. Should have same length as midpoint_radii
        """
        self.midpoint_radii=midpoint_radii
        self.size_limits=size_limits
        self.numbins=len(midpoint_radii)
    
    def get_composition(self):
        """return list of composition for each bin
        """
        return(self.composition)
    
    def set_composition(self, composition):
        """set composition for each aerosol type and bin

        Parameters
        ----------
        composition : list[list[list[float]]] or None
            composition for each aerosol type and bin in fractions of mass. The highest level contains one list for each aerosol type.
            The list for each aerosoltype has entries for each bin, each a list containing nmass entries (7 for PARSEC-UFOs current version), each representing one massfraction
            The order is [H2SO44, (NH4)HSO4, (NH4)2SO4, OC, BC, dust, seasalt]. massfracs should add up to 1, or be normalized in this data-structure(see help(self.normalize_composition))
            None if composition from UserVars is used
        """
        self.composition = composition
    
    def normalize_composition(self):
        """scale the composition of each bin, so that the sum equals 1 for each bin respectively"""
        for aerosol in self.composition:
            for bin in aerosol:
                bin = bin/sum(bin)

    def create_dat_files(self, dir:str=""):
        """Creates the files 'custom-midpoint_radii.dat', 'custom-size_limits.dat', 'custom-concentration.dat'
        and 'custom-composition.dat', if composition data is existing in this data-structure.
        All values are set according to the lists stored in this data-structure.
        
        Parameters
        ----------
        dir : directory as str
            directory to create the .dat files, if used for PARSEC-UFO input, this should be the input directory
        """
        midpfile = open(dir+"custom-midpoint_radii.dat", "x")
        slimfile = open(dir+"custom-size_limits.dat", "x")
        concfile = open(dir+"custom-concentration.dat", "x")
        if (self.composition != None): compfile = open(dir+"custom-composition.dat", "x")
        for it in range(self.get_numbins()):
            midpfile.write(str(self.midpoint_radii[it])+"\n")
            slimfile.write(str(self.size_limits[it][0])+"\t")
            slimfile.write(str(self.size_limits[it][1])+"\n")
            for it2 in range(self.nat-1):
                concfile.write(str(self.concentration[it2][it])+"\t")
            concfile.write(str(self.concentration[-1][it])+"\n")
            if self.composition != None:
                for it2 in range(self.nat):
                    for it3 in range(self.nmass-1):
                        compfile.write(str(self.composition[it2][it][it3])+"\t")
                    compfile.write(str(self.composition[it2][it][-1])+"\n")
        midpfile.close()
        slimfile.close()
        concfile.close()
        if (self.composition != None): compfile.close()

    def save_to_file(self, fname="PARSEC_custom_aerosol.json"):
        """save this object to a .json file, which can be loaded later.
        see help(load_custom_aerosol) for more information
        
        Parameters
        ----------
        fname : str
            name of the file to create
        """
        outfile=open(fname, "x")
        js.dump({"midpoint_radii": self.get_midpoint_radii(), "size_limits": self.get_size_limits(), "concentration": self.get_concentration(), "composition": self.get_composition()}, outfile)
        outfile.close()

    def save_to_str(self):
        """return a json-string representing this object, that can be loaded later. See help(load_custom_aerosol) for more information
        """
        return(js.dump({"midpoint_radii": self.get_midpoint_radii(), "size_limits": self.get_size_limits(), "concentration": self.get_concentration(), "composition": self.get_composition()}))

def load_custom_aerosol(fname:str="PARSEC_custom_aerosol", jsstring:str=None):
    """loads a PARSEC_custom_aerosol instance from given json string or file. If both are input the string is prioritized

    Parameters
    ----------
    fname : str
        path/name of the file to load, see help(PARSEC_custom_aerosol.save_to_file). Is ignored it jsstring != None
    jsstring : str
        json string to load the instance from, see help(PARSEC_custom_aerosol.save_to_str)
    """
    if jsstring != None:
        loaddata=js.loads(jsstring)
    else:
        try:
            loadfile = open(fname)
            loaddata=js.load(loadfile)
            loadfile.close()
        except:
            return None
    return PARSEC_custom_aerosol(midpoint_radii=loaddata["midpoint_radii"], size_limits=loaddata["size_limits"], concentration=loaddata["concentration"], composition=loaddata["composition"])
                           



    

class PARSEC_instance:
    """"class holding all input information for a PARSEC-UFO run. Utilizes the respective datastructures in this module for the data. Contains methods for storage, can be loaded from stored .json files 
    and contains a method to create the full inputs/ directory for a PARSEC-UFO run

    Parameters
    ----------
    UserVars : PARSEC_UserVars
        instance of PARSEC_UserVars describing the input for UserVars namelist see help(PARSEC_UserVars)
    switches : PARSEC_Switches
        instance of PARSEC_switches describing the switches for the PARSEC-UFO instance. See help(PARSEC_switches)
    rebin : PARSEC_rebin or None
        instance of PARSEC_rebin describing the bins for rebining or None if a pre defined option is used. See help(PARSEC_rebin)
    custom_aerosol : PARSEC_custom_aerosol or None
        instance describing custom aerosol input for PARSEC or None if lognormal modes form UserVars are used
    wavelengths : PARSEC_wavelengths or None
        instance describing wavelengths for radiation analysis or None, if predefined wavelengths are used
    """
    def __init__(self, UserVars = PARSEC_UserVars(), switches = PARSEC_Switches(), rebin = PARSEC_rebin(), custom_aerosol:PARSEC_custom_aerosol = None, wavelengths = PARSEC_wavelengths()):
        """initilaize self
        
        Parameters
        ----------
        UserVars : PARSEC_UserVars
            instance of PARSEC_UserVars describing the input for UserVars namelist see help(PARSEC_UserVars)
        switches : PARSEC_Switches
            instance of PARSEC_switches describing the switches for the PARSEC-UFO instance. See help(PARSEC_switches)
        rebin : PARSEC_rebin or None
            instance of PARSEC_rebin describing the bins for rebining or None if a pre defined option is used. See help(PARSEC_rebin)
        custom_aerosol : PARSEC_custom_aerosol or None
            instance describing custom aerosol input for PARSEC or None if lognormal modes form UserVars are used
        wavelengths : PARSEC_wavelengths or None
            instance describing wavelengths for radiation analysis or None, if predefined wavelengths are used
        """
        self.UserVars = UserVars
        self.switches = switches
        self.rebin = rebin
        self.custom_aerosol = custom_aerosol
        self.wavelengths = wavelengths
        customaer = self.switches.getvalue("customaer")
        if customaer >= 1:
            self.UserVars._custaer(customaer=customaer, nat=self.custom_aerosol.get_nat())

    
    def _save_to_dir(self, dir:str="", dname:str ="PARSEC_UFO_INPUT" + str(datetime.datetime.now())):
        os.mkdir(dir+dname)
        self.UserVars.save_to_file(dir+dname+"/PARSEC_UserVars.json")
        self.switches.save_to_file(dir+dname+"/PARSEC_switches.json")
        if self.rebin != None:
            self.rebin.save_to_file(dir+dname+"/PARSEC_rebin.json")
        if self.custom_aerosol != None:
            self.custom_aerosol.save_to_file(dir+dname+"/PARSEC_custom_aerosol.json")
        if self.wavelengths != None:
            self.wavelengths.save_to_file(dir+dname+"/PARSEC_wavelenghts.json")
    
    def save_to_file(self, dir:str="", fname:str = "PARSEC_UFO_INPUT" + str(datetime.datetime.now()) + ".json"):
        """save this object to a .json file, which can be loaded later.
        see help(load_PARSEC_instance) for more information
        
        Parameters
        ----------
        dir : str
            directory in which the file gets created, if not current cd this should end on "/"
        fname : str
            name of the file to create
        """
        savedict={"UserVars": self.UserVars.save_to_str(), "switches": self.switches.save_to_str()}
        if self.rebin != None:
            savedict["rebin"] = self.rebin.save_to_str()

        if self.custom_aerosol != None:
            savedict["custom_aerosol"] = self.custom_aerosol.save_to_str()
        else:
            savedict["custom_aerosol"] = None
        if self.wavelengths != None:
            savedict["wavelengths"] = self.wavelengths.save_to_str()
        savefile=open(dir+fname, "x")
        js.dump(savedict, savefile)
        savefile.close()

    def _create_developer_namelist(self, dir:str=""):
        devfile = open(dir+"namelist_developer.in", "x")
        devfile.write("!-------------------------------------------------------------------------------\n")
        devfile.write("!                    --- DEVELOPER VARIABLES FOR ICPM ---                      !\n")
        devfile.write("!-------------------------------------------------------------------------------\n")
        devfile.write("!\n")
        devfile.write("! WARNING: DO NOT CHANGE THESE INPUTS WITHOUT CONSULTING MODEL DEVELOPERS.\n")
        devfile.write("!\n")
        devfile.write("! --- developer data ---\n")
        devfile.write("&developer\n")
        devfile.write("!\n")
        devfile.write("rmin = 0.002,    !< Lower boundary of dry aerosol sizes [um] \n")
        devfile.write("rmax = 10,    !< Upper boundary of dry aerosol sizes [um] \n")
        devfile.write("!\n")
        devfile.write("variable_timestep = F,  !< T/F : Activates variable timestepping, will override user-chosen dt and dtsub\n")
        devfile.write("!\n")
        devfile.write("&END\n")
        devfile.write("!-------------------------------------------------------------------------------\n")
        devfile.write("!END OF FILE\n")
        devfile.close()
        
    
    def create_inputs_folder(self, dir:str="inputs/", overwrite = False):
        """Creates the complete input folder for PARSEC-UFO, or overwrites files in an existing one.
        All variables and .dat values are set according to the information stored in this instance.
        
        Parameters
        ----------
        dir : directory as str
            directory to create or overwrite the input in

        overwrite : bool
            if False, the directory is created. This function will terminate with an error, if the directory allready exists
            if True, all PARSEC.UFO input files in the direcory will be deteleted and created again
        """
        try: 
            os.mkdir(dir)
        except:
            if overwrite == True:
                try:
                    os.system("rm -f " + dir + "namelist_developer.in")
                    os.system("rm -f " + dir + "namelist_UserVars.in")
                    os.system("rm -f " + dir + "namelist_switches.in")
                    os.system("rm -f " + dir + "rebin-midpoint_radii.dat")
                    os.system("rm -f " + dir + "rebin-size_limits.dat")
                    os.system("rm -f " + dir + "wavelengths.dat")
                    os.system("rm -f " + dir + "custom-midpoint_radii.dat")
                    os.system("rm -f " + dir + "custom-size_limits.dat")
                    os.system("rm -f " + dir + "custom-concentration.dat")
                    os.system("rm -f " + dir + "custom-composition.dat")
                except:
                    print("ERROR: the directory contains sub-directories or hidden files")
                    print("To use overwrite = TRUE, make sure the directory only contains visible files or is empty")
                    return
            else:
                print("ERROR: the directory already exists")
                print("use overwrite=TRUE to overwrite inputs in the directory")
                print("this will delete all PARSEC-input files currently in the directory")
                return
        self._create_developer_namelist(dir=dir)
        self.UserVars.create_namelist_file(dir = dir)
        self.switches.create_namelist_file(dir=dir)
        if self.rebin != None:
            self.rebin.create_dat_files(dir=dir)
        if self.custom_aerosol != None:
            self.custom_aerosol.create_dat_files(dir=dir)
        if self.wavelengths != None:
            self.wavelengths.create_dat_file(dir=dir)
        


def load_PARSEC_instance(dir:str="", fname:str = None, jsstring:str = None):
    """loads a PARSEC_instance instance from given json string, file or directory. If multiple are input the order of priority is
    1. jsstring, 2. fname, 3. dir

    Parameters
    ----------
    dir : str
        directory holding .json files for instance variables to load. Is ignored if jsstring or fname != None
    fname : str
        path/name of the file to load, see help(PARSEC_instance.save_to_file). Is ignored it jsstring != None
    jsstring : str
        json string to load the instance from, see help(PARSEC_instance.save_to_str)
    """
    if jsstring != None:
        data = js.loads(jsstring)
    else:
        if fname != None:
            loadfile = open(fname)
            data = js.load(loadfile)
            loadfile.close()
        else:
            return PARSEC_instance(UserVars=load_UserVars(dir), switches=load_switches(dir), rebin=load_rebin(dir), custom_aerosol=load_custom_aerosol(dir), wavelengths=load_wavelengths(dir))
    return PARSEC_instance(UserVars=load_UserVars(jsstring=data["UserVars"]), switches=load_switches(jsstring=data["switches"]), rebin=load_rebin(jsstring=data["rebin"]), \
                           custom_aerosol=load_custom_aerosol(jsstring=data["custom_aerosol"]), wavelengths=load_wavelengths(jsstring=data["wavelengths"]))






    