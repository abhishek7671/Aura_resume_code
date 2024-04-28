import re
import nl_core_news_sm
from spacy.pipeline import EntityRuler
import pandas as pd
from datetime import datetime
#from Model.get_exp_gaps_ner import delimiters_to_date_conversion
#from Model.get_exp_gaps_ner import flatten_list
#from Model.get_exp_gaps_ner import till_date
import warnings
import time
warnings.filterwarnings('ignore')
import os
import utils.indentifiers as indentifiers
import numpy as np


'''Function to initilize Entity Ruler'''
nlp = None
def add_newruler_to_pipeline(skill_pattern_path,rootPath):
    global nlp
    nlp = None
    nlp = nl_core_news_sm.load()
    '''Reads in all created patterns from a JSONL file and adds it to the pipeline after PARSER and before NER'''
    new_ruler = EntityRuler(nlp).from_disk("./Model/"+skill_pattern_path)
    nlp.add_pipe("entity_ruler",after='parser').add_patterns(new_ruler.patterns)
    return new_ruler.patterns

'''Calling the function to initilize Entity Ruler'''
add_newruler_to_pipeline("SkillFile.jsonl",r""+os.path.dirname(os.path.realpath(__file__)))

def create_skill_set(doc):
    '''Create a set of the extracted skill entities of a doc'''
    return set([ent.label_.upper()[6:] for ent in doc.ents if 'skill' in ent.label_.lower()])


def run_nlp(data,rootPath):
  data = nlp(data)
  #print("data is.......",data)
  nlp_data = [ent.label_.upper()[6:] for ent in data.ents if 'skill' in ent.label_.lower()]
  return nlp_data

############################################################################################################
def delimiters_to_date_conversion(reg,word_text,value,date_list):
    filtered_spch1=[]
    lst1=[]
    filtered_spch = re.findall(reg, word_text)

    for i in filtered_spch:
       
        i = i.replace('$','&')
        if (len(re.findall('D\d+@#&\s+D\d+@#&',i))!=1):
            if (len(re.findall('D\d+@#&\s+T|D\d+@#&\s+P|D\d+@#&\s+C|D\d+@#&\s+N',i))==1):
                
                pass
            else:
                i=i.replace(' ','')
        else:
            
            pass
            
        if (len(re.findall('D\d+@#&\s+T|D\d+@#&\s+P|D\d+@#&\s+C|D\d+@#&\s+N',i))==1):
            pass
            
        else:
           
            pass
        
        i = i.replace('&','$')
        filtered_spch1.append(i.replace(value," To "))
        
    filtered_spch = ','.join(filtered_spch1)
    for i in date_list:
        filtered_spch=filtered_spch.replace(i[1],i[0])
    filtered_spch = filtered_spch.split(',')
    return filtered_spch

def flatten_list(_2d_list):                                        ### 06-09-2022 ###
    flat_list = []
   
    for element in _2d_list:
        if type(element) is list:
           
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def till_date(lst):
    for i in lst:
        try:
            if (i[1] == 'T')|(i[1] == 'Till')|(i[1] == 'till')|(i[1] == 'TILL')|(i[1] == 'Today')|(i[1] == 'today')|(i[1] == 'TODAY')|(i[1] == 'To day'):
                i[1]=datetime.today().strftime('%d-%m-%Y')
            elif (i[1] == 'P')|(i[1] == 'Present')|(i[1] == 'present')|(i[1] == 'PRESENT')|(i[1] == 'Now')|(i[1] == 'N'):
                i[1]=datetime.today().strftime('%d-%m-%Y')
            elif (i[1] == 'C')|(i[1] == 'Current')|(i[1] == 'current')|(i[1] == 'CURRENT'):
                i[1]=datetime.today().strftime('%d-%m-%Y')
            else:
                pass
        except:
            pass
    return lst 

#############################################################################################################

#def divide(lst, n):
#      p = len(lst) // n
#      if len(lst)-p > 0:
#          return [lst[:p]] + divide(lst[p:], n-1)
#      else:
#          return [lst]
#################### ------------- Add new logic -------------- ##############################

def divide_func(lst,n):
    r = len(lst) % n
    q = len(lst)//n
    if r > 0:
        h = q+1
        r = r-1
        h=h-1
        
        
        if r > 0:
            
            m = q+1
            l = q
        else:
            
            m = q
            l = q
    else:
       
        h=q
        m=q
        l=q
    return [np.array(lst[:h]),np.array(lst[h:][:m]),np.array(lst[h:][m:])]

#################### ------------- Add new logic -------------- ##############################

def cal_time(endT,Flag):
  print("\nFlag-- ",Flag,round(endT-time.time(),2))


def skill_recency_logic(data_file,rootPath,date_list):

  start_time_skill_recency = time.time()
  if date_list == ["NA","NA"]:
    ner_skill_data = set(run_nlp(data_file,rootPath))
    recency_dic_2 = {"Low_Skill_Recency":{"NA"},"Medium_Skill_Recency":{"NA"},"High_Skill_Recency":{"NA"}}
    return recency_dic_2,ner_skill_data
  else:
     #pass
    raw_data = data_file
    date_list = date_list
    li_regex = [indentifiers.regex2, indentifiers.regex3, indentifiers.regex5, indentifiers.regex6, indentifiers.regex7,
                indentifiers.regex8, indentifiers.regex9]
    string = raw_data
    date_li_regex = []
    for i in li_regex:
      check_regex = re.findall(i,string)
      for j in check_regex:
        string = string.replace(j," ")
      date_li_regex = date_li_regex + check_regex
 
    string = raw_data

    cnt = 0
    de_dic = {}

    for i in set(date_li_regex):
      string = string.replace(i,str(cnt)+"@#$")
      de_dic[i] = str(cnt)+"@#$"
      cnt = cnt + 1

    de_seq = re.findall(r'\d{0,2}@#\$',string)
  ############----------- Add logic to not remove duplicate dates --------- ############
    lt_val =[]
    lt_key =[]
#new_dict={}

    for k,v in de_dic.items():
      for i in range(len(date_li_regex)):
          if date_li_regex[i] == k:
              lt_key.append(k)
              lt_val.append(v)
    new_tup =list(zip(lt_val,lt_key))
  
    # keys =[]
    # for i in range(len(new_tup)):
    #   keys.append(new_tup[i][0])
    keys = [new_tup[i][0] for i in range(len(new_tup))]

    l1 = set(keys)
    l2 =set(de_seq)
    if list(set(l2) - set(l1)) != []:
    #print("FAIL")
      pass
    split_para = re.split(r'\d{0,2}@#\$', string)
    de_dic_para_df=pd.DataFrame()
    de_dic_para_df['seq_no'] = pd.Series(de_seq)
    de_dic_para_df['Para'] = ''
    de_dic_para_df['date_pattern']=''
    for i in range(len(de_dic_para_df)):
      de_dic_para_df['Para'][i] = split_para[1:][i]
    
    for i in range(len(de_dic_para_df)):
      for k in range(len(new_tup)):
          if de_dic_para_df['seq_no'][i] == new_tup[k][0]:
              de_dic_para_df['date_pattern'][i] =  new_tup[k][1]


  ### groupby date_pattern
    de_dic_para_df = de_dic_para_df.groupby(['date_pattern'], as_index = False).agg({'Para': ' '.join})

    filtered_date_list=[]
    tst = []

    for k,v in indentifiers.dtn.items():
      for i in range(len(de_dic_para_df['date_pattern'])):
        tst.append(de_dic_para_df['date_pattern'][i])
        filtered_date_list.append(delimiters_to_date_conversion(k,de_dic_para_df['date_pattern'][i],v,date_list))

    flatted_result = lambda result:[element for item in result for element in flatten_list(item)] if type(result) is list else [result]
    flat_lst = flatted_result(filtered_date_list)
  #print("................ flat_lst are in skill_recency...............",flat_lst)
  
    d = {}                                              ### create dictionary of k,v pair to sort the dates ###
    for i,j in zip(tst,flat_lst):
      d.setdefault(i, []).append(j)
    dic = {k: [x for x in v if x] for k, v in d.items()}
    dt = pd.DataFrame()
    dt['dt_key']=pd.Series(dic.keys())
    dt['dt_value']=pd.Series(dic.values())
  
    de_dic_para_df['date_update']=''
    for i in range(len(dt)):
      for j in range(len(de_dic_para_df)):
          if dt['dt_key'][i] == de_dic_para_df['date_pattern'][j]:
              de_dic_para_df['date_update'][j] = dt['dt_value'][i]
            
  #########---------- Single date extraction bug fix (not extracting single dates for sr) ------------- #############
    for i in range(len(de_dic_para_df)):
      if (de_dic_para_df['date_pattern'][i] == '') or (de_dic_para_df['date_update'][i] == []):
          de_dic_para_df = de_dic_para_df.drop(i)
      else:
          pass

    de_dic_para_df.reset_index(inplace=True)

  #########---------- Single date extraction bug fix (not extracting single dates) ------------- #############           
            
    de_dic_para_df['date_split']=""

    for i in range(len(de_dic_para_df['date_update'])):
      de_dic_para_df['date_split'][i] = de_dic_para_df['date_update'][i][0].split(" To ")
  
  
    m =[x for x in de_dic_para_df['date_split']]
    de_dic_para_df['date_split'] = pd.Series(till_date([[s.strip() for s in inner] for inner in m]))
 # print("....... data frame is..................",de_dic_para_df.head(3))


  ################ ----------------- Add logic --------------- ######################

    date_list_dic = {}
    for i in date_list:
      date_list_dic[i[1]] = i[0]
 
    for i in date_list_dic.keys():
      for j in de_dic_para_df.index:
        if i in de_dic_para_df['date_pattern'][j]:
          de_dic_para_df['date_pattern'][j] = de_dic_para_df['date_pattern'][j].replace(i,date_list_dic[i])
 
############# ------------ Add NER model --------------- ###########
  #de_dic_para_df.loc[len(de_dic_para_df.index)] = ['',split_para[0],'',"TEMP"]
  #for cnt_i in range(cnt-1,len(split_para)):
  #  de_dic_para_df.loc[len(de_dic_para_df.index)] = ['',split_para[cnt_i],'',"TEMP"]
  
    df_para_lst=[]
    for k in range(len(de_dic_para_df['Para'])):
      df_para_lst.append(de_dic_para_df['Para'][k])

    dictionary_row = {"Para":"".join([x for x in split_para if x not in df_para_lst]),"date_split":"TEMP"}
    de_dic_para_df = de_dic_para_df.append(dictionary_row, ignore_index=True)

    de_dic_para_df['NER'] = ''
    for i in de_dic_para_df.index:
      de_dic_para_df['NER'][i] = ','.join(set(run_nlp(de_dic_para_df['Para'][i],rootPath)))

    ner_skill_data = de_dic_para_df[de_dic_para_df['NER'] != '']['NER'].values
    ner_skill_data = set([item for sublist in [x.split(",") for x in ner_skill_data] for item in sublist])
  
    de_dic_para_df = de_dic_para_df[de_dic_para_df['date_split']!='TEMP']
  
  ############### ---------------  Add logic ------------------ ##################
    de_dic_para_df['final_dates_end']=''

    for i in range(len(de_dic_para_df)):
      de_dic_para_df['final_dates_end'][i] = de_dic_para_df['date_split'][i][1]
    
    de_dic_para_df['final_dates_end'] = pd.to_datetime(de_dic_para_df['final_dates_end'],format='%d-%m-%Y')
    de_dic_para_df = de_dic_para_df.sort_values(by='final_dates_end')
    de_dic_para_df.reset_index(inplace=True)
  
    de_dic_para_df['seq_id']=''                      ####### create sequence id ########
    for i in range(len(de_dic_para_df)):
      de_dic_para_df['seq_id'][i] = i
    
 # print("********************")
 # print(".............. Data frame is..............",de_dic_para_df.head(7))
 
  ############### ---------------  Add logic ------------------ ##################

    recency_list = divide_func(de_dic_para_df[de_dic_para_df['NER'] != '']['seq_id'].values,3)

    recency_dic = {0:"",1:"",2:""}
    cnt = 0
    for i in recency_list:
      recency_dic[cnt] = ",".join(de_dic_para_df[de_dic_para_df['seq_id'].isin(list(i))]['NER'].values)
      cnt = cnt + 1

    for i in recency_dic.keys():
      recency_dic[i] = set(recency_dic[i].lower().split(","))
 
  
    cnt = 2
    while cnt > 0:
      if cnt == 2:
        del_ele = recency_dic[cnt].intersection(recency_dic[cnt-1])
        for i in del_ele:
          recency_dic[cnt-1].remove(i)
        del_ele = recency_dic[cnt].intersection(recency_dic[cnt-2])
        for i in del_ele:
          recency_dic[cnt-2].remove(i)
        cnt = cnt - 1
      elif cnt == 1:
        del_ele = recency_dic[cnt].intersection(recency_dic[cnt-1])
        for i in del_ele:
          recency_dic[cnt-1].remove(i)
        cnt = cnt - 1
      else:
        pass
 
    recency_dic_1 = {"0":"Low_Skill_Recency","1":"Medium_Skill_Recency","2":"High_Skill_Recency"}
    recency_dic_2 = {}

    for i in recency_dic.keys():
      recency_dic_2[recency_dic_1[str(i)]] = set(list(map(lambda x: x.upper().replace(" ","-"), recency_dic[i])))
  
    #end_time_skillrec = time.time()
    #total_time_skillrec = end_time_skillrec - start_time_skill_recency
  
    return recency_dic_2,ner_skill_data