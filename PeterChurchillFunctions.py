'''
This file is a list of functions that I have used in my Master Thesis that would come in handy for my PhD. 
The functions work for NorESM and EC-Earth
'''

import xarray as xr
import numpy as np

def NorESMExtract(NorPath, station, VarList, Xspace):
    '''
    This function takes the Path of the ncdf file of NorESM and outputs a xarray
    with the variables for aerosol distribution and any Variables in the Varible List.
    This fuction only works for a single station. 
    NorPath = string
    VariableList = List of Strings
    station = string
    '''
    ds = xr.Dataset()
    PNSD_ds = xr.Dataset()
    Data = xr.open_dataset(NorPath)
    Data = Data.sel(station = station)
    ## Create a PNSD for each mode
    for i in range(0,16):
        if f'SIGMA{i:02d}' not in Data:
            continue   
        PNSD_ds[f'SIGMA{i:02d}'] =  Data[f'SIGMA{i:02d}']
        PNSD_ds[f'NMR{i:02d}'] = Data[f'NMR{i:02d}']
        PNSD_ds[f'NCONC{i:02d}'] = Data[f'NCONC{i:02d}']
        PNSD_ds[f'dNdlogD{i:02d}'] = dNdlogD(Data[f'NCONC{i:02d}'], Xspace, Data[f'NMR{i:02d}'], Data[f'SIGMA{i:02d}']) 
        
    ds['dNdlogD']=PNSD_ds['dNdlogD01']
    for i in range(2,16):
        if f'dNdlogD{i:02d}' not in Data:
           continue
        ds['dNdlogD'] = ds['dNdlogD']+PNSD_ds[f'dNdlogD{i:02d}']
        
    ## Extract the variables from the list 
    if len(VarList) >= 1:
        for var in VarList:
            ds[var] = Data[var]

    
    return ds, PNSD_ds


def ECearthExtract(ECPath, station, ifsVarList, ifsVarNames, Xspace):
    Data = xr.open_dataset(ECPath)
    Data = Data.sel(station = station)
    ds=xr.Dataset()
    PNSD_ds = xr.Dataset()
    
    ## Variables to make the particle number size distribution
    radius_variables = ['RDRY_NUS', 'RDRY_AIS', 'RDRY_ACS', 'RWET_AII', 'RDRY_COS','RWET_ACI','RWET_COI',]
    Numb_variables = ['N_NUS','N_AIS','N_ACS','N_AII','N_COS','N_ACI','N_COI',]
    Sigma = [1.59,1.59,1.59,2,1.59,1.59,2]
    
    for radius, conc in zip(radius_variables, Numb_variables):
        PNSD_ds[f'{radius}'] = Data[f'{radius}']
        PNSD_ds[f'{conc}'] = Data[f'{conc}']
        
    for r in radius_variables:
        Data[r] = Data[r].where(Data[r]>0)
        if Data[r].units == 'm':
            Data[r] = Data[r] * 1e9
            Data[r].attrs['units'] = 'nm'
            print('changing to nm')
    dis_variable = ['NUS_dis', 'AIS_dis', 'ACS_dis', 'COS_dis', 'AII_dis', 'ACI_dis', 'COI_dis']

    for radius, conc, sigma, dist  in zip(radius_variables, Numb_variables, Sigma,  dis_variable):
        PNSD_ds[dist] = dNdlogD(PNSD_ds[conc], Xspace, PNSD_ds[radius]*2 , sigma)
    ds['dNdlogD'] = sum(PNSD_ds[i] for i in dis_variable)
    
    ## For the IFS variables, Required to rename them and reindex them to same pressure levels. 
    ds['lev_ifs'] = Data['var54'].mean('time')
    
    if len(ifsVarList) >= 0:
        for ifs, name in zip(ifsVarList, ifsVarNames):
            ds[name] = Data[ifs].isel(lev=0).drop_vars('lev')
            ds[name] = ds.sel(lev_ifs = ds['lev'], method='nearest')[name]
    ds = ds.drop_vars('lev_ifs')
    ds['lev']=Data['pressure'].mean('time')
    ds['lev'] = ds['lev']/100 ## To get the unit to be hPa. 
    return ds, PNSD_ds

def NorComposition(NorPath, station):
    Data = xr.open_dataset(NorPath)
    Data = Data.sel(station = station)
    ds = xr.Dataset()
    ## Name of all the variables
    OA_ls = ['SOA_NA', 'SOA_A1', 'OM_AC', 'OM_AI', 
                'OM_NI', 'SOA_NA_OCW', 'SOA_A1_OCW', 'OM_AC_OCW', 
                'OM_AI_OCW', 'OM_NI_OCW']
    SO4_ls = ['SO4_NA', 'SO4_A1', 'SO4_A2', 'SO4_AC',
                 'SO4_PR', 'SO4_NA_OCW', 'SO4_A1_OCW', 'SO4_A2_OCW',
                 'SO4_AC_OCW', 'SO4_PR_OCW',]
    Seasalt_ls = ['SS_A1', 'SS_A2', 'SS_A1_OCW', 'SS_A2_OCW',]
    Dust_ls = ['DST_A2', 'DST_A2_OCW',]
    BC_ls = ['BC_N', 'BC_AX', 'BC_NI', 'BC_A',
                'BC_AI', 'BC_AC', 'BC_N_OCW', 'BC_NI_OCW',
                'BC_A_OCW', 'BC_AI_OCW', 'BC_AC_OCW',]
    
    CompositionList = [OA_ls, SO4_ls, Seasalt_ls, Dust_ls, BC_ls]
    VarMassName = ['OA_Mass','SO4_Mass','Seasalt_Mass','Dust_Mass', 'BC_Mass']
    VarFracName = ['OA_Frac','SO4_Frac','Seasalt_Frac','Dust_Frac', 'BC_Frac']    
    ## Calculate teh mass of the 5 compsition categories
    for var, varname in zip(CompositionList, VarMassName):
        ds[varname] = sum(Data[i] for i in var) 
        
    ## Calculate the total mass         
    ds['Total_Mass'] = sum(ds[i] for i in VarMassName)

    ## Find the mass fraction 
    for varFrac, varMass in zip(VarFracName, VarMassName):
        ds[varFrac] = ds[varMass]/ds['Total_Mass']
        
    return ds


def ECComposition(ECPath, station):
    Data = xr.open_dataset(ECPath)
    Data = Data.sel(station = station)
    ds = xr.Dataset()
    ## Name of all the variables

    OA_ls = ['M_SOANUS','M_POMAIS','M_SOAAIS','M_POMACS','M_SOAACS','M_POMAII', 'M_SOAAII',]
    SO4_ls = ['M_SO4NUS','M_SO4ACS', 'M_SO4AIS_es']
    Seasalt_ls= ['M_SSACS'] 
    Dust_ls = ['M_DUACI','M_DUACS'] 
    BC_ls = ['M_BCACS','M_BCAII','M_BCAIS',] 
    ## Calculate the estimate of SO4 in the Aitken mode using ratio of masses from accumulation and aitken
    Data['M_SO4AIS_es'] =(Data['M_SO4ACS'] / 
                  (Data['M_BCACS'] + Data['M_POMACS'] + Data['M_SOAACS'])
                 ) * (Data['M_BCAIS'] + Data['M_POMAIS'] + Data['M_SOAAIS'])
    
    CompositionList = [OA_ls, SO4_ls, Seasalt_ls, Dust_ls, BC_ls]
    VarMassName = ['OA_Mass','SO4_Mass','Seasalt_Mass','Dust_Mass', 'BC_Mass']
    VarFracName = ['OA_Frac','SO4_Frac','Seasalt_Frac','Dust_Frac', 'BC_Frac']    
    ## Calculate teh mass of the 5 compsition categories
    for var, varname in zip(CompositionList, VarMassName):
        ds[varname] = sum(Data[i] for i in var) 
        
    ## Calculate the total mass         
    ds['Total_Mass'] = sum(ds[i] for i in VarMassName)

    ## Find the mass fraction 
    for varFrac, varMass in zip(VarFracName, VarMassName):
        ds[varFrac] = ds[varMass]/ds['Total_Mass']
        
    return ds


def dNdlogD(N,x,mu,sigma):
    return N*np.exp(-(np.log10(x) - np.log10(mu*2))**2 / (2 * np.log10(sigma)**2))/ (np.log10(sigma) * np.sqrt(2 * np.pi))    











