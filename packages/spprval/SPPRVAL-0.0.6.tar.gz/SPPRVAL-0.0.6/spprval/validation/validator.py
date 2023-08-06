from cProfile import label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bootstrap
from typing import List
import datetime
from copy import copy
import seaborn as sns
import warnings
from os import listdir
from os.path import isfile, join
import json
import os


from .aggregator import get_all_seq_statistic, get_res_ved_stat
from .dataset_wrapper import get_work_pulls, get_validation_dataset, create_model_dataset
from .rendering import create_res_html
warnings.simplefilter(action='ignore', category=FutureWarning)

warnings.simplefilter(action='ignore', category=RuntimeWarning)

import matplotlib as mpl


config = pd.read_csv('Config_of_params.csv')

PERC = config.loc[0, 'Percent delta']
Q_L = config.loc[0, ' Low quantile']
Q_U = config.loc[0, ' Upper quantile']



def quantiles_10(x, axis):
    return np.quantile(x,Q_L, axis=-1)

def quantiles_99(x, axis):
    return np.quantile(x,Q_U, axis=-1)



def validate_resources(model_dataset, df_wind_val, act, res):
    """Function to validate resources volumes

    Args:
        model_dataset (df): dataset for validation
        df_wind_val (df): validation dataset
        act (list): list of works
        res (list): list of resources
        name (str): name of ksg file

    Returns:
        df: result of validation
    """    
    df_perc_agg = pd.DataFrame()
    df_style = pd.DataFrame() 
    df_volume = pd.DataFrame() 
    fig_dict = dict() 
    for i in model_dataset.index:
 
        c_pair = [ci for ci in act if model_dataset.loc[i,ci] != 0]
        c_act = c_pair
        volume = [model_dataset.loc[i,ci] for ci in c_act]
        delta = [PERC * volumei for volumei in volume]
        not_c = [ci for ci in act if ci not in c_act]
        zero_ind = df_wind_val[not_c][(df_wind_val[not_c] == 0).all(axis=1)].index
        sample_non = df_wind_val.loc[zero_ind,:]

        non_zero = sample_non[c_act][(sample_non[c_act] != 0).all(axis=1)].index
        sample_non = pd.DataFrame(sample_non.loc[non_zero,:])
        sample = pd.DataFrame()
        for j, ci in enumerate(c_act):
            sample = sample_non.loc[(sample_non[ci] >= volume[j] - delta[j]) & (sample_non[ci] <= volume[j] + delta[j])]
        sample = pd.DataFrame(sample)
      
        if sample.shape[0] > 20:
            for r in res:
                value = model_dataset.loc[i,r]
                q1, q99 = np.quantile(sample[r].values, [Q_L,  Q_U])
                if value < q1 or value > q99:
                    df_style.loc[i,r] = "red"
                    df_volume.loc[i,r] = value
                    for ci in c_act:
                        key = str(c_act)+" "+r+" "+ci
                        blue_points = {'x':list(sample_non[ci].values), 'y':list(sample_non[r].values)}
                        black_points = {'x':list(sample[ci].values), 'y':list(sample[r].values)}
                        star = {'x':model_dataset.loc[i, ci], 'y':model_dataset.loc[i,r]}
                        color = 'red'
                        fig_dict[key] = {'Blue points':blue_points, 'Black points':black_points, 'Star':star, 'Color':color}
                else:
                    df_style.loc[i,r] = "green"
                    df_volume.loc[i,r] = value
                    for ci in c_act:
                        key = str(c_act)+" "+r+" "+ci
                        blue_points = {'x':list(sample_non[ci].values), 'y':list(sample_non[r].values)}
                        black_points = {'x':list(sample[ci].values), 'y':list(sample[r].values)}
                        star = {'x':model_dataset.loc[i, ci], 'y':model_dataset.loc[i,r]}
                        color = 'green'
                        fig_dict[key] = {'Blue points':blue_points, 'Black points':black_points, 'Star':star, 'Color':color}
            df_style.loc[i,'Наименование'] = str(c_act)
            df_volume.loc[i,'Наименование'] = str(c_act)
        elif sample.shape[0] <= 20 and sample.shape[0] > 4:
            for r in res:
                value = model_dataset.loc[i,r]
                #q1_ci = bootstrap((sample[r].values,), quantiles_10, confidence_level=0.95, method='bca').confidence_interval
                #q99_ci = bootstrap((sample[r].values,), quantiles_99, confidence_level=0.95, method='bca').confidence_interval
                #q1 = (q1_ci[1] - q1_ci[0]) / 2
                #q99 = (q99_ci[1] - q99_ci[0]) / 2
                q1, q99 = np.quantile(sample[r].values, [Q_L,  Q_U])
                if value < q1 or value > q99:
                    df_style.loc[i,r] = "red"
                    df_volume.loc[i,r] = value
                    for ci in c_act:
                        key = str(c_act)+" "+r+" "+ci
                        blue_points = {'x':list(sample_non[ci].values), 'y':list(sample_non[r].values)}
                        black_points = {'x':list(sample[ci].values), 'y':list(sample[r].values)}
                        star = {'x':model_dataset.loc[i, ci], 'y':model_dataset.loc[i,r]}
                        color = 'red'
                        fig_dict[key] = {'Blue points':blue_points, 'Black points':black_points, 'Star':star, 'Color':color}
                else:
                    df_style.loc[i,r] = "green"
                    df_volume.loc[i,r] = value
                    for ci in c_act:
                        key = str(c_act)+" "+r+" "+ci
                        blue_points = {'x':list(sample_non[ci].values), 'y':list(sample_non[r].values)}
                        black_points = {'x':list(sample[ci].values), 'y':list(sample[r].values)}
                        star = {'x':model_dataset.loc[i, ci], 'y':model_dataset.loc[i,r]}
                        color = 'green'
                        fig_dict[key] = {'Blue points':blue_points, 'Black points':black_points, 'Star':star, 'Color':color}
            df_style.loc[i,'Наименование'] = str(c_act)
            df_volume.loc[i,'Наименование'] = str(c_act)
        elif sample.shape[0] <= 4:
            df_style.loc[i,'Наименование'] = str(c_act)
            df_volume.loc[i,'Наименование'] = str(c_act)
            for r in res:
                value = model_dataset.loc[i,r]
                df_style.loc[i,r] = "grey"
                df_volume.loc[i,r] = value
    new_df_color = df_style[(df_style != 'grey').all(1)]
    not_perc = (((df_style.shape[0]*df_style.shape[1]) - (new_df_color.shape[0]*new_df_color.shape[1])) / (df_style.shape[0]*df_style.shape[1]))*100
    j = 0
 
    for c in act:
        new_sample = new_df_color.loc[new_df_color['Наименование'].str.count(c) != 0]
        if new_sample.shape[0] != 0:
            for r in res:
                df_perc_agg.loc[j,'Наименование ресурса'] = r
                df_perc_agg.loc[j,'Наименование работы'] = c
                value_dict = new_sample[r].value_counts().to_dict()
                if 'green' in list(value_dict.keys()):
                    df_perc_agg.loc[j, 'Соотношение'] = round(((value_dict['green']) / new_sample.shape[0])*100)
                else:
                    df_perc_agg.loc[j, 'Соотношение'] = 0
                j += 1
        else:
            for r in res:
                df_perc_agg.loc[j,'Наименование ресурса'] = r
                df_perc_agg.loc[j,'Наименование работы'] = c
                df_perc_agg.loc[j, 'Соотношение'] = 0
                j += 1

    norm_perc = df_perc_agg['Соотношение'].mean()
    df_final_volume = pd.DataFrame()
    df_final_style = pd.DataFrame()
    for i, p in enumerate(list(df_volume['Наименование'].unique())):
        sample1 = df_volume.loc[df_volume['Наименование'] == p]
        sample2 = df_style.loc[df_style['Наименование'] == p]
        date = str(sample1.index[0]) +' '+str(sample1.index[-1])
        df_final_volume.loc[i, 'Наименование'] = p
        df_final_volume.loc[i, 'Даты'] = date
        df_final_volume.loc[i,res] = sample1.loc[sample1.index[0],res] 
        df_final_style.loc[i, 'Наименование'] = p
        df_final_style.loc[i, 'Даты'] = date
        df_final_style.loc[i,res] = sample2.loc[sample2.index[0],res] 
 




    return df_perc_agg, df_final_volume, df_final_style, fig_dict, not_perc, norm_perc



def validate_works_vol(model_dataset, df_wind_val, act):
    """Function to validate average works volume

    Args:
        model_dataset (df): dataset for validation
        df_wind_val (df): validation dataset
        act (list): list of works
        name (str): name of ksg file

    Returns:
        df: result of validation
    """    
    df_stat = pd.DataFrame()
    dist_dict = dict()
    j = 0
    for c in act:
        for i in model_dataset.index:
            value = model_dataset.loc[i,c]
            if value != 0:
                sample = df_wind_val.loc[df_wind_val[c] != 0]
                if sample.shape[0] != 0:
                    q1, q99 = np.quantile(sample[c].values, [Q_L, Q_U])
                    q1 = int(q1)
                    q99 = int(q99)
                    if value < q1 or value > q99:
                        df_stat.loc[j,'Работа'] = c
                        df_stat.loc[j,'Метка работы'] = "red"
                        key = c
                        line = value
                        color = 'red'
                        counts, bins, _ = plt.hist(sample[c].values)
                        dist_dict[key] = {'Line':line, 'color':color, 'Hight':counts, 'Bins':bins, 'Q1': q1, 'Q99':q99}
                    else:
                        df_stat.loc[j,'Работа'] = c
                        df_stat.loc[j,'Метка работы'] = "green"
                        key = c
                        line = value
                        color = 'green'
                        counts, bins, _ = plt.hist(sample[c].values)
                        dist_dict[key] = {'Line':line, 'color':color, 'Hight':counts, 'Bins':bins, 'Q1': q1, 'Q99':q99}
                    j+=1
                else:
                    df_stat.loc[j,'Работа'] = c
                    df_stat.loc[j,'Метка работы'] = "grey"
    not_grey = df_stat.loc[df_stat['Метка работы'] != 'grey']
    not_perc = ((df_stat.shape[0] - not_grey.shape[0]) / df_stat.shape[0]) * 100
    norm_df = df_stat.loc[df_stat['Метка работы'] == 'green']
    norm_perc = ((not_grey.shape[0] - norm_df.shape[0]) / not_grey.shape[0]) * 100
    df_final_stat = pd.DataFrame()
    for i, c in enumerate(act):
        df_final_stat.loc[i,'Наименование'] = c
        sample = not_grey.loc[not_grey['Работа'] == c]
        count_dict = sample['Метка работы'].value_counts().to_dict()
        if 'green' not in list(count_dict.keys()):
            df_final_stat.loc[i,'Среднедневная выработка'] = 0
        else:
            df_final_stat.loc[i,'Среднедневная выработка'] = (count_dict['green'] / sample.shape[0]) * 100
    return df_final_stat, dist_dict, norm_perc, not_perc
            





def validate_time(df_wind_model, df_wind_val, act):
    """Function to validate time of work

    Args:
        df_wind_model (df): dataset for validation
        df_wind_val (df): validation dataset
        act (list): list of works

    Returns:
        df: result of validation
    """    
    df_stat = pd.DataFrame()
    dict_fig = dict()
    final_df = pd.DataFrame()
    j = 0
    for c in act:
        for i in df_wind_model.index:
            if df_wind_model.loc[i,c] != 0:
                c_act = [c] 
                volume = [df_wind_model.loc[i,ci] for ci in c_act]
                delta = [PERC * volumei for volumei in volume]
                sample = copy(df_wind_val)
                for k, ci in enumerate(c_act):
                    sample = sample.loc[(sample[ci] >= volume[k] - delta[k]) & (sample[ci] <= volume[k] + delta[k])]
                if sample.shape[0] > 20:
                    value = df_wind_model.loc[i,c.split('_')[0]+'_real_time_act']
                    q1, q99 = np.quantile(sample[c.split('_')[0]+'_real_time_act'].values, [Q_L, Q_U])
                    q1 = int(q1)
                    q99 = int(q99)
                    if value < q1 or value > q99:
                        df_stat.loc[j,'Работа'] = c
                        df_stat.loc[j,'Метка времени'] = "red"
                        key = c
                        blue_points = {'x':list(df_wind_val[c].values), 'y':list(df_wind_val[c.split('_')[0]+'_real_time_act'].values)}
                        black_points = {'x':list(sample[c].values), 'y':list(sample[c.split('_')[0]+'_real_time_act'].values)}
                        star = {'x':df_wind_model.loc[i, c], 'y': df_wind_model.loc[i,c.split('_')[0]+'_real_time_act']}
                        color = 'red'
                        dict_fig[key] = {'Blue points':blue_points, 'Black points':black_points, 'Star':star, 'Color':color, 'Q1': q1, 'Q99':q99}
                    else:
                        df_stat.loc[j,'Работа'] = c
                        df_stat.loc[j,'Метка времени'] = "green"
                        key = c
                        blue_points = {'x':list(df_wind_val[c].values), 'y':list(df_wind_val[c.split('_')[0]+'_real_time_act'].values)}
                        black_points = {'x':list(sample[c].values), 'y':list(sample[c.split('_')[0]+'_real_time_act'].values)}
                        star = {'x':df_wind_model.loc[i, c], 'y': df_wind_model.loc[i,c.split('_')[0]+'_real_time_act']}
                        color = 'green'
                        dict_fig[key] = {'Blue points':blue_points, 'Black points':black_points, 'Star':star, 'Color':color, 'Q1': q1, 'Q99':q99}
                elif sample.shape[0] > 3 and sample.shape[0] <= 20:
                    value = df_wind_model.loc[i,c.split('_')[0]+'_real_time_act']
                    q1, q99 = np.quantile(sample[c.split('_')[0]+'_real_time_act'].values, [Q_L, Q_U])
                    q1 = int(q1)
                    q99 = int(q99)
                    #q1_ci = bootstrap((sample[c.split('_')[0]+'_real_time_act'].values,), quantiles_10, confidence_level=0.95, n_resamples=1000, method='basic').confidence_interval
                    #q99_ci = bootstrap((sample[c.split('_')[0]+'_real_time_act'].values,), quantiles_99, confidence_level=0.95, n_resamples=1000, method='basic').confidence_interval
                    # q1 = (q1_ci[1] - q1_ci[0]) / 2
                    # q99 = (q99_ci[1] - q99_ci[0]) / 2
                    if value < q1 or value > q99:
                        df_stat.loc[j,'Работа'] = c
                        df_stat.loc[j,'Метка времени'] = "red"
                        key = c
                        blue_points = {'x':list(df_wind_val[c].values), 'y':list(df_wind_val[c.split('_')[0]+'_real_time_act'].values)}
                        black_points = {'x':list(sample[c].values), 'y':list(sample[c.split('_')[0]+'_real_time_act'].values)}
                        star = {'x':df_wind_model.loc[i, c], 'y': df_wind_model.loc[i,c.split('_')[0]+'_real_time_act']}
                        color = 'red'
                        dict_fig[key] = {'Blue points':blue_points, 'Black points':black_points, 'Star':star, 'Color':color,'Q1': q1, 'Q99':q99}
                    else:
                        df_stat.loc[j,'Работа'] = c
                        df_stat.loc[j,'Метка времени'] = "green"
                        key = c
                        blue_points = {'x':list(df_wind_val[c].values), 'y':list(df_wind_val[c.split('_')[0]+'_real_time_act'].values)}
                        black_points = {'x':list(sample[c].values), 'y':list(sample[c.split('_')[0]+'_real_time_act'].values)}
                        star = {'x':df_wind_model.loc[i, c], 'y': df_wind_model.loc[i,c.split('_')[0]+'_real_time_act']}
                        color = 'green'
                        dict_fig[key] = {'Blue points':blue_points, 'Black points':black_points, 'Star':star, 'Color':color,'Q1': q1, 'Q99':q99}
                else:
                    df_stat.loc[j,'Работа'] = c
                    df_stat.loc[j,'Метка времени'] = "grey"
                j+=1
    not_grey = df_stat.loc[df_stat['Метка времени'] != 'grey']
    not_perc = ((df_stat.shape[0] - not_grey.shape[0]) / df_stat.shape[0]) * 100
    norm_df = df_stat.loc[df_stat['Метка времени'] == 'green']
    norm_perc = ((not_grey.shape[0] - norm_df.shape[0]) / not_grey.shape[0]) * 100
    for i, c in enumerate(act):
        final_df.loc[i,'Наименование'] = c
        sample = not_grey.loc[not_grey['Работа'] == c]
        count_dict = sample['Метка времени'].value_counts().to_dict()
        if 'green' not in list(count_dict.keys()):
           final_df.loc[i,'Время на ед. объёма'] = 0
        else:
            final_df.loc[i,'Время на ед. объёма'] = (count_dict['green'] / sample.shape[0]) * 100
    return final_df, dict_fig, norm_perc, not_perc



def get_statistic_for_properties_and_all_stat(norm_res, norm_ved, norm_volume, norm_time, norm_seq, not_res, not_ved, not_volume, not_time, not_seq):
    result_dict = dict()
    result_dict['Процент нормальных значений объёмов ресурсов'] = round(norm_res)
    if not_res != 100:
        result_dict['Процент нетипичных значений объёмов ресурсов'] = 100 - round(norm_res)
    else:
        result_dict['Процент нетипичных значений объёмов ресурсов'] = 0

    result_dict['Процент нормальных ресурсов по ведомостям'] = round(norm_ved)
    if not_ved != 100:
        result_dict['Процент нетипичных ресурсов по ведомостям'] = 100 - round(norm_ved)
    else:
        result_dict['Процент нетипичных ресурсов по ведомостям'] = 100
    result_dict['Процент нормальных значений времени работ'] = round(norm_time)
    if not_time != 100:
        result_dict['Процент нетипичных значений времени работ'] = 100 - round(norm_time)
    else:
        result_dict['Процент нетипичных значений времени работ']  = 0
    

    result_dict['Процент нормальных значений объёмов работ'] = round(norm_volume)

    if not_volume != 100:
        result_dict['Процент нетипичных значений объёмов работ'] = 100 - round(norm_volume)
    else:
        result_dict['Процент нетипичных значений объёмов работ'] = 0
    result_dict['Процент нормальных значений связей работ'] = round(norm_seq)
    if not_seq != 100:
        result_dict['Процент нетипичных значений связей работ'] = 100 - round(norm_seq)
    else:
        result_dict['Процент нетипичных значений связей работ'] = 0

    result_dict['Процент нормальных занчений по всем работам'] = round((round(norm_time) +  round(norm_volume) + round(norm_seq)) / 3)
    result_dict['Процент критических занчений по всем работам'] = 100 - round((round(norm_time) +  round(norm_volume) + round(norm_seq)) / 3)


    result_dict['Процент нормальных значений по всем ресурсам'] = round((round(norm_res) +  round(norm_ved) ) / 2)
    result_dict['Процент критических значений по всем ресурсам'] = 100 - round((round(norm_res) +  round(norm_ved) ) / 2)

    return result_dict

def get_plan_statistic(norm_res, norm_ved, norm_volume, norm_time, norm_seq, not_res, not_ved, not_volume, not_time, not_seq):
    norm_value = round((norm_res + norm_ved + norm_volume + norm_time + norm_seq) / 5)
    crit_value = 100 - norm_value
    not_val = round((not_res + not_ved + not_volume + not_time + not_seq) / 5)
    tested_val = 100 - not_val
    dict_result = {'Процент нормальных значений плана': norm_value, 'Процент нетипичных значений плана': crit_value, 'Процент непокрытых валидацией значений плана': not_val, 'Процент покрытых валидацией значений плана': tested_val}
    
    return dict_result







            


    


        

        
        

            
                









        



    





