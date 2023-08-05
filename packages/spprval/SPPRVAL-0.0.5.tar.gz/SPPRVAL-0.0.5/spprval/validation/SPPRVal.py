
from .aggregator import get_all_seq_statistic, get_res_ved_stat
from .dataset_wrapper import get_work_pulls, get_validation_dataset, create_model_dataset
from .validator import validate_resources, validate_works_vol, validate_time, get_statistic_for_properties_and_all_stat, get_plan_statistic
import json
import pandas as pd
from os import listdir
from os.path import isfile, join
from copy import copy
import datetime

def window_zero(df: pd.DataFrame, min_window: int = 2, max_window: int = 21):
    """Function for making time windows of msg files

    Args:
        df (pd.DataFrame): input msg file
        min_window (int, optional): Min length of window. Defaults to 5.
        max_window (int, optional): Max length of window. Defaults to 31.

    Returns:
        DataFrame: msg files with windows
    """    
    act_col = [var for var in df.columns if '_act_fact' in var]
    res_col = [var for var in df.columns if '_res_fact' in var]
    new_zero_lil = [act+'_zero_lil' for act in act_col]
    new_zero_big = [act+'_zero_big' for act in act_col]
    df_new = pd.DataFrame(columns=list(df.columns) + ['Start day', 'Window length'] + new_zero_lil + new_zero_big)
    df_zero = pd.DataFrame(columns=act_col)
    for window_len in [7]:
        for start in range(0, len(df) - window_len + 1):
            new_row = df[act_col].iloc[start:start + window_len].sum(axis=0, skipna=True)
            new_row = {act: 1 if value==0.0 else 0 for act, value in new_row.items()}
            start_day = datetime.datetime.strptime(df.index[start], "%d.%m.%Y")
            end_day = datetime.datetime.strptime(df.index[start + window_len - 1], "%d.%m.%Y")
            df_zero.loc[df.index[start]] = new_row

    window_list = list(range(min_window, max_window + 1))
    for window_len in window_list:

        for start in range(0, len(df) - window_len + 1):
            start_day = datetime.datetime.strptime(df.index[start], "%d.%m.%Y")
            end_day = datetime.datetime.strptime(df.index[start + window_len - 1], "%d.%m.%Y")
            if (end_day-start_day).days == window_len - 1:
                new_row_act = df[act_col].iloc[start:start + window_len].sum(axis=0, skipna=True)
                new_row_res = df[res_col].iloc[start:start + window_len].mean(axis=0, skipna=True)#df[res_col].iloc[start:start + window_len].mode(axis=0, dropna=True).iloc[0]
                new_row = copy(new_row_act)
                new_row = new_row.append(new_row_res)

                lil = {act+'_zero_lil': 0 for act in act_col}
                big = {act+'_zero_big': 0 for act in act_col}
                danger_date = [df.index[ind] for ind in range(start, start + window_len)]
         
                for act in act_col:
                    for i in range(start, start + window_len):
                       
                        if df.iloc[i][act] == 0.0:
                            lil[act+'_zero_lil'] = lil[act+'_zero_lil'] + 1
                            if (i < window_len - 6) and danger_date[i-start] in df_zero.index and df_zero.loc[danger_date[i-start]][act] == 1:
                                if (i > start) and (df_zero.loc[danger_date[i-start - 1]][act] == 1):
                                    big[act+'_zero_big'] = big[act+'_zero_big'] + 1
                                else:
                                    big[act+'_zero_big'] = big[act+'_zero_big'] + 7
                lil = {act+'_zero_lil': lil[act+'_zero_lil'] - big[act+'_zero_big'] for act in act_col}
                
                new_row = {**new_row, **lil, **big}
                new_row['Start day'] = start_day
                new_row['Window length'] = window_len
                df_new = df_new.append(new_row, ignore_index=True)
              

    
    return df_zero, df_new





class Validator:
    

    def __init__(self, plan, database=None, folders=None, valdataset=None):
        """Initialization of parameters

        Args:
            plan (str): path to json with plan
            database (str, optional): path to file with historical data. Defaults to None.
            folders (str, optional): path to folders with historical data. Defaults to None.
            valdataset (str, optional): path to validation dataset. Defaults to None.
        """        
        self.plan = plan
        self.database = database
        self.folders = folders
        self.valdataset = valdataset
    
    def validate(self, plan_path):
        ksg_for_val = open(plan_path, encoding='utf8')
        ksg_for_val_data = json.load(ksg_for_val)
        pulls = get_work_pulls(ksg_for_val_data)
        act = []
        res = []
        for w in ksg_for_val_data['activities']:
            act.append(w['activity_name'])
            for r in w['labor_resources']:
                if r['labor_name'] not in res:
                    if '_res_fact' in r['labor_name']:
                        res.append(r['labor_name'].split('_')[0])
                    else:
                        res.append(r['labor_name'])
        brave = pd.read_csv('data/brave_work_res.csv')
        brave.index = brave['Unnamed: 0'].values
        brave = brave.drop(columns=['Unnamed: 0'])
        validation_dataset = pd.DataFrame()
        if not self.valdataset:
            validation_files = []
            if self.folders:
                for folder in self.folders:
                    mypath = self.database+folder+'/'
                    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                    for file in onlyfiles:
                        msg_file = open(mypath+file, encoding='utf8')
                        msg_data = json.load(msg_file)
                        if len(msg_data['resource']) != 0:
                            for work in msg_data['work']:
                                if work["work title"] in act:
                                    validation_files.append(mypath+file)
                                    break
                        
            else:
                mypath = self.database
                onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                for file in onlyfiles:
                    msg_file = open(mypath+file, encoding='utf8')
                    msg_data = json.load(msg_file)
                    if len(msg_data['resource']) != 0:
                        for work in msg_data['work']:
                            if work["work title"] in act:
                                validation_files.append(mypath+file)
                                break
            
            validation_dataset = get_validation_dataset(validation_files, pulls, act, res)
            validation_dataset.to_csv('convert_test.csv')
 

  
        else:
            validation_dataset = pd.read_csv(self.valdataset)
            validation_dataset.index = validation_dataset['Unnamed: 0'].values
            validation_dataset = validation_dataset.drop(columns=['Unnamed: 0'])
            validation_dataset = validation_dataset[act+res]
            
            right_index = []
    
            for pull in pulls:
                if len(pull) == 1:
                    not_c = [ci for ci in act if ci != pull[0]]
                    zero_ind = validation_dataset[not_c][(validation_dataset[not_c] == 0).all(axis=1)].index
                    for i in validation_dataset.index:
                        if (validation_dataset.loc[i,pull[0]] != 0) and  (i in zero_ind):
                            right_index.append(i)
                else:
                    not_c = [ci for ci in act if ci not in pull]
                    zero_ind = validation_dataset[not_c][(validation_dataset[not_c] == 0).all(axis=1)].index
                    for i in validation_dataset.index:
                        flag = True
                        for p in pull:
                            if validation_dataset.loc[i,p] == 0:
                                flag=False
                        if flag and  (i in zero_ind):
                            right_index.append(i)
            new_validation_dataset = pd.DataFrame(validation_dataset.loc[right_index, :])
            model_columns = []
            for c in new_validation_dataset.columns:
                if c in act:
                    model_columns.append(c+'_act_fact')
                if c in res:
                    model_columns.append(c+'_res_fact')
            new_validation_dataset.columns = model_columns
            validation_dataset = pd.DataFrame()
            validation_dataset = copy(new_validation_dataset)
            print('Валидационный датасет собран')
        model_dataset = create_model_dataset(ksg_for_val_data)
        model_dataset.to_csv('model_dataset.csv', index=False)
        act = [c for c in model_dataset if c.split('_')[-2] == 'act']
        res = [c for c in model_dataset if c.split('_')[-2] == 'res']
        print('Валидируем ресурсы')
        df_perc_agg_res, df_final_volume_res, df_final_style_res, fig_dict_res, not_perc_res, norm_perc_res = validate_resources(model_dataset, validation_dataset, act, res)
        print('Валидация ресурсов по ведомости')
        df_vedom, not_perc_vedom, norm_perc_vedom = get_res_ved_stat(brave, ksg_for_val_data, act)
        print('Нарезка данных на окна')
        df, df_wind_val = window_zero(validation_dataset)
        df, df_wind_model = window_zero(model_dataset)
        for i in df_wind_val.index:
            for c in act:
                df_wind_val.loc[i, c.split('_')[0]+'_real_time_act'] = df_wind_val.loc[i, 'Window length'] - df_wind_val.loc[i,c.split('_')[0]+'_act_fact_zero_lil'] - df_wind_val.loc[i,c.split('_')[0]+'_act_fact_zero_big']
        for i in df_wind_model.index:
            for c in act:
                df_wind_model.loc[i, c.split('_')[0]+'_real_time_act'] = df_wind_model.loc[i, 'Window length'] - df_wind_model.loc[i,c.split('_')[0]+'_act_fact_zero_lil'] - df_wind_model.loc[i,c.split('_')[0]+'_act_fact_zero_big']
        print('Валидация среднедневных объёмов работ')
        df_volume_stat, dist_dict, norm_volume_perc, not_volume_perc = validate_works_vol(model_dataset, validation_dataset, act)
        print('Валидация времени')
        df_time_stat, time_plot_dict, norm_time_perc, not_time_perc = validate_time(df_wind_model, df_wind_val, act)
        print('Валидация последовательностей')
        seq_history = pd.read_pickle('val_datasets/works_messoyaha_clustered_15kdict_and_glue_work_series_less_14_day.pkl')
        df_seq_stat, df_color_seq, norm_perc_seq, not_perc_seq = get_all_seq_statistic(seq_history, ksg_for_val_data)
        print('Получение общих статистик по работам и ресурсам')
        work_res_common_perc = get_statistic_for_properties_and_all_stat(norm_perc_res, norm_perc_vedom, norm_volume_perc, norm_time_perc,  norm_perc_seq, not_perc_res, not_perc_vedom, not_volume_perc, not_time_perc, not_perc_seq)
        plan_statistic = get_plan_statistic(norm_perc_res, norm_perc_vedom, norm_volume_perc, norm_time_perc,  norm_perc_seq, not_perc_res, not_perc_vedom, not_volume_perc, not_time_perc, not_perc_seq)
        
        return df_perc_agg_res, df_final_volume_res, df_final_style_res, fig_dict_res, df_vedom, df_volume_stat, dist_dict, df_time_stat, time_plot_dict, df_seq_stat, df_color_seq, work_res_common_perc, plan_statistic
        
    def validate_plan(self):
        result_dict = dict()
        ksg_for_val = open(self.plan, encoding='utf8')
        ksg_for_val_data = json.load(ksg_for_val)
        regime = True
        for el in ksg_for_val_data['activities']:
            if el['activity_name'] == 'Окончание работ по марке' or el['activity_name'] == 'Начало работ по марке':
                regime = False
                break
        if regime:
            # try:
            df_perc_agg_res, df_final_volume_res, df_final_style_res, fig_dict_res, df_vedom, df_volume_stat, dist_dict, df_time_stat, time_plot_dict, df_seq_stat, df_color_seq, work_res_common_perc, plan_statistic = self.validate(self.plan)
            result_dict['Object 0'] = {'Отношения ресурсов к работам':df_perc_agg_res, 'Пулы работ объёмы':df_final_volume_res, 'Пулы работ цвета':df_final_style_res, 'Данные для графиков ресурсов': fig_dict_res, 'Ресурсная ведомость':df_vedom, 'Статистика по выработке':df_volume_stat, 'Данные для графиков выработок':dist_dict, 'Статистика по времени работ':df_time_stat, 'Данные для графиков времени': time_plot_dict, 'Таблица связей': df_seq_stat, 'Таблица связей цвета':df_color_seq, 'Статистика итоговая по работам и ресурсам':work_res_common_perc, 'Итоговая статистика плана':plan_statistic}
            # except:
            #     result_dict['Object 0'] = 'No validation'
        else:
            new_plan_path = self.plan[0:len(self.plan)-5]
            paths = []
            act_dict = dict()
            block_id = dict()
            ind_act = dict()
            label = 0
            for i, el in enumerate(ksg_for_val_data['activities']):
                act_dict[el['activity_id']] = el['activity_name']
                if el['activity_name'] == 'Окончание работ по марке':
                    label += 1
                elif el['activity_name'] == 'Начало работ по марке':
                    label += 1
                else:
                    block_id[el['activity_id']] = label
                    ind_act[el['activity_id']] = i
            block_id['0000000'] = label+1
            json_file = {'activities':[]}
            label = block_id[list(block_id.keys())[0]]
            for k in block_id.keys():
                if block_id[k] == label:
                    ind_of_act = ind_act[k]
                    new_des_act = []
                    for el in ksg_for_val_data['activities'][ind_of_act]['descendant_activities']:
                        if el[0] in block_id.keys(): 
                            if act_dict[el[0]] != 'Окончание работ по марке' and act_dict[el[0]] != 'Начало работ по марке': 
                                if block_id[k] == block_id[el[0]]:
                                    new_des_act.append(el)
                    ksg_for_val_data['activities'][ind_of_act]['descendant_activities'] = new_des_act
                    json_file['activities'].append(ksg_for_val_data['activities'][ind_of_act])
                    label = block_id[k]
                else:
                    with open(new_plan_path+str(label)+'.json', "w") as outfile:
                        json.dump(json_file, outfile)
                    paths.append(new_plan_path+str(label)+'.json')
                    if k == '0000000':
                        break
                    else:   
                        json_file = {'activities':[]}
                        ind_of_act = ind_act[k]
                        new_des_act = []
                        for el in ksg_for_val_data['activities'][ind_of_act]['descendant_activities']:
                            if el[0] in block_id.keys(): 
                                if act_dict[el[0]] != 'Окончание работ по марке' and act_dict[el[0]] != 'Начало работ по марке': 
                                    if block_id[k] == block_id[el[0]]:
                                        new_des_act.append(el)
                        ksg_for_val_data['activities'][ind_of_act]['descendant_activities'] = new_des_act
                        json_file['activities'].append(ksg_for_val_data['activities'][ind_of_act])
                        label = block_id[k]
            for id, p in enumerate(paths):
               
                df_perc_agg_res, df_final_volume_res, df_final_style_res, fig_dict_res, df_vedom, df_volume_stat, dist_dict, df_time_stat, time_plot_dict, df_seq_stat, df_color_seq, work_res_common_perc, plan_statistic = self.validate(p)
                result_dict['Object '+str(id)] = {'Отношения ресурсов к работам':df_perc_agg_res, 'Пулы работ объёмы':df_final_volume_res, 'Пулы работ цвета':df_final_style_res, 'Данные для графиков ресурсов': fig_dict_res, 'Ресурсная ведомость':df_vedom, 'Статистика по выработке':df_volume_stat, 'Данные для графиков выработок':dist_dict, 'Статистика по времени работ':df_time_stat, 'Данные для графиков времени': time_plot_dict, 'Таблица связей': df_seq_stat, 'Таблица связей цвета':df_color_seq, 'Статистика итоговая по работам и ресурсам':work_res_common_perc, 'Итоговая статистика плана':plan_statistic}
                # except:
                #     result_dict['Object '+str(id)] = 'No validation'
        return result_dict

