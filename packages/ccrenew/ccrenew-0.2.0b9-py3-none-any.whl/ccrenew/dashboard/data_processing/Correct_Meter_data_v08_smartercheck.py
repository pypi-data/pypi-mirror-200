# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:45:14 2016

@author: SEBASTIAN


Code to correct meter data.  Meter data is calculated as a sum of different meters.
There is a case that some meters are off, but inverters are on.  When the meter is back
online there is an increment in energy. 
Code corrects this issue.

See Boseman Solar Center  month: MARCH
"""

import pandas as pd
import numpy as np


def list_pairs(lis):
    #find pairs that are at least 2 hours in duration
    beg = []
    end = []
    
    start_time = 0
    
    while start_time < len(lis):
        end_time = start_time+1
        while end_time < len(lis) and lis[end_time] - lis[end_time-1] == pd.Timedelta('1h'):
            end_time = end_time+1
        # end_time overshoots by one hour, so compare to > 2 to make sure it's longer than 1 hr
        if end_time - start_time > 2:
            beg.append(lis[start_time])
            end.append(lis[end_time-1])
        start_time = end_time
    return beg, end
    
def Correct_Meter_with_Inv_data_v01(df, pos_Meter, pos_Meter_Cum, clipping_KW, df_sensor_ON):
    #error handling 
    error_log = pd.DataFrame(columns = ['Site_name', 'year', 'ii', 'p', 'p_max', 'hours'])

    #if no cum meter data, don't go through function
    if df[pos_Meter_Cum].sum().sum() == 0:
        aux_Meter_Corrected = df[pos_Meter].rename(columns = {x:x + '_OK' for x in pos_Meter})
        return aux_Meter_Corrected, [], error_log
    
    #
    pos_Inv = [s for s in df.columns if 'Inv_kw_' in s]
    pos_Inv_cum = [s for s in df.columns if 'Inv_kwnet' in s]
    df_mtr_inv = pd.DataFrame()
    df_mtr_inv = df[pos_Inv + pos_Inv_cum + pos_Meter + pos_Meter_Cum]
    
    # find if all Inv are on
    df_mtr_inv['ALL INV ON'] = df_mtr_inv[pos_Inv].prod(axis=1).values
    df_mtr_inv.loc[df_mtr_inv['ALL INV ON']>0,'ALL INV ON'] = 1
    df_mtr_inv.loc[df_mtr_inv['ALL INV ON']<1,'ALL INV ON'] = 0
    
    #find if all INV CUM ON
    df_mtr_inv['ALL_INV_CUM_ON'] = df_mtr_inv[pos_Inv_cum].prod(axis=1).values
    df_mtr_inv.loc[df_mtr_inv['ALL_INV_CUM_ON']>0,'ALL_INV_CUM_ON'] = 1
    df_mtr_inv.loc[df_mtr_inv['ALL_INV_CUM_ON']<1,'ALL_INV_CUM_ON'] = 0
    
    #find if all Meters are on
    df_mtr_inv.loc[df_mtr_inv.index, 'ALL_METER_ON'] = df_mtr_inv[pos_Meter].prod(axis=1).values
    df_mtr_inv.loc[df_mtr_inv['ALL_METER_ON']>0,'ALL_METER_ON'] = 1
    df_mtr_inv.loc[df_mtr_inv['ALL_METER_ON']<1,'ALL_METER_ON'] = 0

    aux_Meter_Corrected = pd.DataFrame()
    
    draker_flags = []
    
    # Loop the meters
    for ii in range(0,len(pos_Meter)):
        
        meter = pos_Meter[ii]
        meter_c = 'Meter_kwhnet_' + pos_Meter[ii].split("_")[-1]
        #
        aux_m = pd.DataFrame()
        aux_m = df_mtr_inv[[meter] +[meter_c]]
        
        #cum meter can't drop go downwards
        #QUESTION: why is this using clipping_KW * -0.02 as the cutoff?
        aux_m.loc[aux_m[meter_c].diff() < clipping_KW * -0.02, [meter] +[ meter_c]] = 0
        
        # remove data as set in the config file
        aux_m.loc[df_sensor_ON[meter] != True, meter] = 0
        
        #find spikes above max power
        high_prod_flags = aux_m.loc[(aux_m[meter_c].diff() > (1.3 * clipping_KW) / len(pos_Meter)), :].index
        # Find timestamps when meter is zero - checks that meter cum isn't zero to ensure it's not a comms outage
        no_prod_flags = aux_m.loc[(df_sensor_ON[meter] == True) & (aux_m[meter] == 0) & (aux_m[meter_c] != 0)].index
        
        targets = []
        for idx in [aux_m.index.get_loc(x) for x in high_prod_flags]:
            i = 1
            while (aux_m.iloc[idx-i].name in high_prod_flags) or (aux_m.iloc[idx-i].name in no_prod_flags):
                targets = targets + [aux_m.iloc[idx-i].name]
                i = i + 1
        
        aux_m.loc[targets, [meter] +[meter_c]] = 0 
        draker_flags = draker_flags + targets

        # Flag for timestamps when the cum meter shows zero
        aux_m.loc[(aux_m[meter_c] == 0), 'M_CUM_OFF'] = 1   #exclude times when all inverters are on
        aux_m = aux_m.fillna(0)
        
        aux_m_i = aux_m.loc[aux_m['M_CUM_OFF'] == 1,'M_CUM_OFF']
        aux_m['M_CUM_OFF_1'] = 0                                                        #create blank column first. It wonn't be created below if no outages
        
        for idx in range (0, len(aux_m_i)):
            aux_m.loc[aux_m.index == aux_m_i.index[idx] ,'M_CUM_OFF_1'] = 1
            aux_m.loc[aux_m.index == aux_m_i.index[idx] +  pd.DateOffset(hours = 1),'M_CUM_OFF_1'] = 1
            aux_m.loc[aux_m.index == aux_m_i.index[idx] + pd.DateOffset(hours = -1) ,'M_CUM_OFF_1'] = 1
        
        # find increments in cum meter
        aux_m = aux_m.fillna(0)
        aux_m['M_CUM_OFF_2'] = aux_m['M_CUM_OFF_1'] - aux_m['M_CUM_OFF']
        
        # filter out 1-hour data rows in an outage
        # this prevents the start of one outage being the same as the end of the previous, which confuses the script.
        # if 'M_CUM_OFF' in this row is 0, and the previous row is 1, and the next row is 1, reject it
        aux_curr = aux_m['M_CUM_OFF']
        aux_prev = aux_m['M_CUM_OFF'].shift(1)
        aux_next = aux_m['M_CUM_OFF'].shift(-1)
        bad_indices = list((aux_curr == 0) & (aux_prev == 1) & (aux_next == 1))
        aux_m.loc[bad_indices, 'M_CUM_OFF_2'] = 0

        aux_m_Missing = pd.Series(0,index = aux_m.index, name = meter_c, dtype = 'float')

        #  #  Meter Expected Production.  Based on historical data.
        aux_meter_exp = df_mtr_inv.loc[df_mtr_inv['ALL_METER_ON'] == 1, [meter, meter_c]]
        aux_meter_exp['hour'] = aux_meter_exp.index.hour

        aux_meter_exp = aux_meter_exp.groupby( aux_meter_exp['hour'].values).mean()

        aux_meter_exp_2 = pd.DataFrame(index = range(0,24))
        aux_meter_exp = pd.concat([aux_meter_exp_2, aux_meter_exp], axis = 1).fillna(0) 
        aux_meter_exp.columns = ['KW_M_Expect', 'KWh_M_Expect','hour']

        aux_meter_exp = aux_meter_exp['KW_M_Expect']
        
        fill_m = pd.DataFrame()
        fill_m[aux_m.columns] = aux_m[aux_m['M_CUM_OFF'] == 1]

        try:
            fill_m['hour'] = fill_m.index.hour
        except AttributeError:
            fill_m = fill_m.reindex(columns=fill_m.columns.to_list() + ['hour'])
        
        aux_fill = []
        date_fill = []
        for i in range(0, len(fill_m.index)):
            hour_fill = fill_m.index.hour[i]
            aux_fill.append(aux_meter_exp[aux_meter_exp.index == hour_fill].values[0])
            date_fill.append( fill_m.index[i])
           
        aux_fill = pd.DataFrame(aux_fill, index = date_fill, columns = ['E_sum_Fill'] )
        aux_fill = aux_fill.set_index(aux_m[aux_m['M_CUM_OFF'] == 1].index)
        
        aux_f = pd.concat([df_mtr_inv,aux_m, aux_fill], axis=1)
        aux_f = aux_f.fillna(0)
        aux_f.rename(columns={0:'Missing_M'}, inplace=True)
        
        #  Distribute energy
        outage_dates = aux_f.loc[aux_f['M_CUM_OFF_2'] > 0, 'M_CUM_OFF_2'].index 
        
        # if the file starts out with missing data, then the end of this block will mistakenly be
        # identified as the beginning of a block.  Check to see if this is the case, and correct if necessary
        if aux_f['M_CUM_OFF'][0] == 1:
            outage_dates = outage_dates[1:]
        # similarly, if the file ends with missing data, remove the last element of pos
        if aux_f['M_CUM_OFF'][-1] == 1:
            outage_dates = outage_dates[:-1]

        #  Only loop if Energy is bigger than 300 W
        aux_m_Missing = aux_m.loc[outage_dates, meter_c].diff()[1::2]
        aux_m_Missing = aux_m_Missing[aux_m_Missing > 300]
        aux_m_Missing = aux_m_Missing.rename('Missing_KW')
        aux_f = pd.concat([aux_f, aux_m_Missing], axis=1)

        aux_f['Missing_M_ADDED'] = 0               #initial column to fill data
        
        for p in range(0,len(outage_dates),2): 
            aux_e_filled_value = []                 #for each loop, blank data and start over
            aux_e_filled_date = []
            
            e_to_distribute = aux_f['E_sum_Fill'][outage_dates[p]:outage_dates[p+1]]
            # Manual sorting to match old sorting algorithm in Python 2.7 process
            sort = e_to_distribute.argsort()[::-1]
            e_to_distribute = e_to_distribute[sort]
            e_to_fill = aux_f['Missing_KW'][outage_dates[p+1]] 
            
            k = 0
            while k < len(e_to_distribute):
                if e_to_distribute[k] < e_to_fill:
                    aux_e_filled_value.append(e_to_distribute[k])
                    aux_e_filled_date.append(e_to_distribute.index[k])
                    e_to_fill = e_to_fill - e_to_distribute[k] 
                k = k+1
                
            ##input scale factor due to left over energy            
            if aux_e_filled_value != []:
                aux_factor = (np.sum(aux_e_filled_value) +e_to_fill) / np.sum(aux_e_filled_value)
                if aux_factor < 1.5:
                    aux_e_filled_value = [x * aux_factor for x in aux_e_filled_value]       #multiply factor through
                else:
                    aux_factor = 1.5                
                    aux_e_filled_value = [x * aux_factor for x in aux_e_filled_value]       #multiply factor through
                aux_e_filled_value = [min(x, clipping_KW) for x in aux_e_filled_value]
            
        
            #create export dataframe
            aux_e_filled = pd.DataFrame(aux_e_filled_value, index = aux_e_filled_date)
            aux_e_filled.rename(columns={0:'Missing_M_ADDED'}, inplace=True) 
            #export out of loop
            if not aux_e_filled.empty:              #if it has data, append it in. If empty just skip
                aux_f.loc[ (aux_e_filled.index), 'Missing_M_ADDED'] = aux_e_filled['Missing_M_ADDED'].values
                
        #
        aux_f = aux_f.fillna(0)
        aux_f['Missing_M_ADDED'] = aux_f['Missing_M_ADDED'].multiply(aux_f['M_CUM_OFF'])
        name_c = meter +'_OK'
        #
        aux_Meter_Corrected[name_c] = aux_m[meter] + aux_f['Missing_M_ADDED']  #combined corrected sensor
        #aux_Meter_Corrected.loc[ aux_Meter_Corrected[name_c] < 0, name_c] = 0      #remove off hours
        
        
        ## Check work using cumulative sum
        # remove day time points
        aux_ind = aux_f.loc[(aux_f.index.hour <= 4) | (aux_f.index.hour >= 22), :]
        aux_f['Check'] = 0                          #create identifier column if WRAPPED around loop range
        aux_f['Pos'] = 0                            #create identifier column if within loop range

        
        #for each loop in pos
        for p in range(0,len(outage_dates),2):
            #ignore times when meter starts or ends in outage (causes error and no corrections anyway)
            if outage_dates[p] != aux_f.index[0] and outage_dates[p+1] != aux_f.index[-1]:
                aux_f.loc[(aux_f.index <= outage_dates[p+1]) & (outage_dates[p] <= aux_f.index), 'Pos'] = 1
                try:
                    check_beg = aux_ind.loc[(aux_ind.index < outage_dates[p]) & (aux_ind['M_CUM_OFF'] == 0), :].index[-1]
                    check_end = aux_ind.loc[(outage_dates[p+1] < aux_ind.index) & (aux_ind['M_CUM_OFF'] == 0), :].index[0]
                    aux_f.loc[(check_beg <= aux_f.index) & (aux_f.index <= check_end), 'Check' ] = 1
                except:
                    error_append = pd.DataFrame(index = [0], columns = error_log.columns.tolist())
                    error_append[[u'ii', u'p', 'p_max', u'hours']] = [ii, p, range(0,len(outage_dates),2)[-1], (outage_dates[p+1] - outage_dates[p]).seconds/60/60]
                    error_log = error_log.append(error_append)
                    pass

        
        #find outer 
        beg_list, end_list = list_pairs( aux_f.loc[aux_f['Check'] == 1, :].index.tolist() )
        
        # function to scale up backfilled meter data to match the total target energy
        # intelligently scales to prevent meter from going above POI limit
        def capped_scale(data, goal_energy, multiplier, limit):
            data = (data * multiplier).clip(upper=limit)

            missing_energy = goal_energy - data.sum()

            if missing_energy > 1e-13:
                if (data[data > 0] == limit).all():
                    # got stuck, can't scale it any more
                    # can we smear the energy around a bit, so that the zeros come into play?
                    if (data > 0).all():
                        # meter correction failed to add all missing energy
                        return data
                    
                    def smooth_out(series):
                        return series.sum() / series.size
                    
                    data = data.rolling(3, center=True, min_periods=1).apply(smooth_out)
                    
                # filter out clipping points
                data_not_yet_clipping = data[data < limit]
                new_goal_energy = goal_energy - data[data == limit].sum()
                new_multiplier = new_goal_energy / data_not_yet_clipping.sum()
                if new_multiplier > 0:
                    data[data < limit] = capped_scale(data_not_yet_clipping, new_goal_energy, new_multiplier, limit)
            return data

        # assume that the meter should not go above this limit
        # pretty bad assumption (see IS-6), but hey what can ya do
        meter_limit = clipping_KW / len(pos_Meter)
        
        #loop through outer check and adjust energy
        for x in range(len(beg_list)):
            start = beg_list[x]
            finish = end_list[x]

            cum_energy = aux_m.loc[finish, meter_c].item() - aux_m.loc[start, meter_c].item()
            meter_added = aux_Meter_Corrected.loc[(start <= aux_f.index) & (aux_f.index <= finish) & (aux_f['Pos'] == 1), name_c]
            meter_sum = meter_added.sum()
            
            # cum_energy represents the total energy produced between nighttime anchor points
            # but since comms outage can end during the day, we need to subtract out
            # the energy corresponding to real meter data, so it doesn't cause creep
            real_energy = aux_m.loc[aux_f['Pos'] != 1, :].loc[start:finish, meter].sum()
            
            delta = (cum_energy - real_energy) - meter_sum
            
            if meter_sum > 0:
                second_factor = (meter_sum + delta) / meter_sum
            else:
                #can't make any adjustments if no energy was added
                second_factor = 1
            
            if (second_factor < 2.0) and (second_factor > 0.1) and (cum_energy > 0):   #4/4 changed from 1.05 to 1.20
                meter_adjusted = capped_scale(meter_added, meter_sum + delta, second_factor, meter_limit)
                aux_Meter_Corrected.loc[meter_adjusted.index, name_c] = meter_adjusted
        
    return aux_Meter_Corrected, draker_flags, error_log