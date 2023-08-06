# -*- coding: utf-8 -*-
import pandas as pd
from ccrenew.dashboard.data_processing.battery_deg import Battery


def Run_AC_Batt(df_kwh, rates, deg_hours):

    # initiate 
    soc = 1065.864
    b = Battery()
    b.power = 499
    b.nameplate_duration = soc/499
    b.limit = 499
    b.charge_eff = 0.88
    b.discharge_eff = 1.0
    b.degradation_hours = deg_hours
    
    # run
    test = b.binary(rates.values, df_kwh.values, soc0 = soc)
    test['SOC'] = test['SOC'][:-1]
    test['inpS'] = df_kwh
    
    df_battery = pd.DataFrame(test, index = df_kwh.index)

    return df_battery



def AC_Batt_PP(df, df_battery):
    POI_limit = 499
    site_limit = 500
    no_load = 0.5 
    copper_loss = site_limit * 0.009
    
    aux = pd.DataFrame([], index = df.index)
    aux['solar+storage'] = df_battery['solar+storage']
    
    #
    aux['MF_XFMR'] =  aux['solar+storage'] - (no_load + (aux['solar+storage']/site_limit)**2 * copper_loss)
    
    #
    AC_wiring_loss = 0.006
    XFMR_year_max = site_limit * 489.646/500.
    aux['AC_wiring'] = aux['MF_XFMR'] * (1-AC_wiring_loss*(aux['MF_XFMR']/XFMR_year_max)**2)
    
    #skipping HV XFMR
    #skipping gen tie
    #skipping PF loss
    #skipping tracker losses
    
    #
    inv_night_loss = 0.570214669
    aux['Inv_night'] = aux['AC_wiring'].copy()
    aux['Inv_night'].loc[aux['Inv_night']<0] = aux['Inv_night'] - inv_night_loss
    
    #
    scada_loss = 1000
    aux['Scada'] = aux['Inv_night'] - (scada_loss*site_limit/8760./1000.)

    ava = 0.99
    aux['POI_cap'] = aux['Scada'].clip(upper=POI_limit)
    aux['ava'] = aux['POI_cap']*ava
    aux['POI'] = aux['ava'].copy()
    aux['POI_no_night'] = aux['POI'].clip(lower=0)

    
    return aux
