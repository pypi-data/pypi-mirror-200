import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
config = pd.read_csv('Config_of_params.csv')

CRIT_VALUE = config.loc[0, 'Crit value of Brave']


def get_all_seq_statistic(start_end_data, model_data):
    df_grouped  = start_end_data.groupby('upper works')['work_name'].apply(list).reset_index(name="Works")

    works1 = []
    works2 = []
    labels = dict()
    works_dict = dict()

    for act in model_data['activities']:
        works_dict[act['activity_id']] = act['activity_name']
    for act in model_data['activities']:
        if len(act['descendant_activities']) != 0:
            for el in act['descendant_activities']:
                works1.append(act['activity_name'])
                works2.append(works_dict[el[0]])
                labels[act['activity_name'] +' -- '+works_dict[el[0]]] = el[1]
    
    
    if len(works1) != 0:
        pairs = []
        for w1, w2 in zip(works1, works2):
            pairs.append(w1 +' -- '+w2)
        freq_dict = dict()
        for w1, w2 in zip(works1, works2):
            if w1 != w2:
                fs = 0
                ss = 0
                ff = 0
                mix = 0
                for i in df_grouped.index:
                    work_list = df_grouped.loc[i,'Works']
                    if w1 in work_list and w2 in work_list:
                        ind1 = start_end_data.loc[(start_end_data['upper works'] == df_grouped.loc[i,'upper works']) & (start_end_data['work_name'] == w1)]
                        ind2 = start_end_data.loc[(start_end_data['upper works'] == df_grouped.loc[i,'upper works']) & (start_end_data['work_name'] == w2)]
        
                        s1 = ind1['first_day'].min()
                        f1 = ind1['last_day'].max()
                        s2 = ind2['first_day'].min()
                        f2 = ind2['last_day'].max()
                        if s1 > f2:
                            continue
                        else:
                            if f1 < s2:
                                fs += 1
                            if s1 == s2:
                                ss += 1
                            if f1 == f2:
                                ff += 1
                            if s2 < f1:
                                mix += 1
                if w1 +' -- '+w2 in pairs:
                    freq_dict[w1 +' -- '+w2] = {'count': fs+ss+ff+mix, 'fs': fs, 'ss': ss, 'ff': ff, 'ffs': mix}
        df_bar = pd.DataFrame()
        df_color = pd.DataFrame()
        links = ['FFS', 'FS', 'SS', 'FF']
        i = 0
        for k in freq_dict.keys():
            if freq_dict[k]['count'] != 0:
                w1 = k.split(' -- ')[0]
                w2 = k.split(' -- ')[1]
                df_bar.loc[i,'Наименование работы 1'] = w1
                df_bar.loc[i,'Наименование работы 2'] = w2
                df_bar.loc[i, 'Связь в плане'] = labels[k]
                
                mix_val = freq_dict[k]['ffs'] / freq_dict[k]['count']
                fs_val = freq_dict[k]['fs'] / freq_dict[k]['count'] 
                ss_val = freq_dict[k]['ss'] / freq_dict[k]['count']
                ff_val = freq_dict[k]['ff'] / freq_dict[k]['count']
                df_bar.loc[i, 'FFS'] = mix_val * 100
                df_bar.loc[i, 'FS'] = fs_val * 100
                df_bar.loc[i, 'SS'] = ss_val * 100
                df_bar.loc[i, 'FF'] = ff_val * 100
                links_perc = [mix_val, fs_val, ss_val, ff_val]
                max_label = links[np.argmax(links_perc)]
                df_color.loc[i,'Наименование работы 1'] = w1
                df_color.loc[i,'Наименование работы 2'] = w2
                if max_label == labels[k]:
                    df_color.loc[i,'color'] = 'green'
                else:
                    df_color.loc[i, 'color'] = 'red'
                i += 1
        perc_dict = df_color['color'].value_counts().to_dict()
        norm_perc = 0
        if 'green' in perc_dict.keys():
            norm_perc = (perc_dict['green'] / df_color.shape[0]) * 100
        not_perc = 0
    return df_bar, df_color, norm_perc, not_perc






def get_res_ved_stat(brave, ksg_for_val_data, act):
    
    df_stat = pd.DataFrame()
    j = 0
    
    for w in ksg_for_val_data['activities']:
        for r in w["labor_resources"]:
            df_stat.loc[j,'Работа'] = w['activity_name']
            df_stat.loc[j, 'Ресурс'] = r['labor_name']
            if w['activity_name']+'_act_fact' in brave.columns and str(r['labor_name'])+'_res_fact' in brave.index:
                if brave.loc[r['labor_name']+'_res_fact', w['activity_name']+'_act_fact'] >= CRIT_VALUE:
                    df_stat.loc[j,'Метка ресурса'] = 'green'
                else:
                    df_stat.loc[j,'Метка ресурса'] = 'red'
            else:
                df_stat.loc[j,'Метка ресурса'] = 'grey'
            j+=1
    not_grey = df_stat.loc[df_stat['Метка ресурса'] != 'grey']
    not_perc = ((df_stat.shape[0] - not_grey.shape[0]) / df_stat.shape[0])* 100
    norm_perc = (not_grey['Метка ресурса'].value_counts().to_dict()['green'] / not_grey.shape[0]) * 100
    return df_stat, not_perc, norm_perc







   
    


    
    
        




    







    

    




