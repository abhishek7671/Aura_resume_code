import re
import nl_core_news_sm
from spacy.pipeline import EntityRuler
import pandas as pd
from datetime import datetime
import warnings
import time
warnings.filterwarnings('ignore')
import os
import utils.indentifiers as indentifiers


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
  nlp_data = [ent.label_.upper()[6:] for ent in data.ents if 'skill' in ent.label_.lower()]
  return nlp_data

def divide(lst, n):
      p = len(lst) // n
      if len(lst)-p > 0:
          return [lst[:p]] + divide(lst[p:], n-1)
      else:
          return [lst]

def cal_time(endT,Flag):
  print("\nFlag-- ",Flag,round(endT-time.time(),2))


#regex1 = r'D\d+@#\$\s*To\s*D\d+@#\$|D\d+@#\$\s*To\s*[a-zA-Z]|D\d+@#\$\s*to\s*D\d+@#\$'
#regex2 = r'D\d+@#\$\s*–\s*D\d+@#\$|D\d+@#\$\s*–\s*[a-zA-Z]'
#regex3 = r'D\d+@#\$\s*-\s*D\d+@#\$|D\d+@#\$\s*-\s*[a-zA-Z]'
#regex4 = 'D\d+@#\$\s*To\s*D\d+@#\$|D\d+@#\$\s*To\s*[a-zA-Z]|D\d+@#\$\s*–\s*D\d+@#\$|D\d+@#\$\s*–\s*[a-zA-Z]|D\d+@#\$\s*-\s*D\d+@#\$|D\d+@#\$\s*-\s*[a-zA-Z]'
#regex5 = r'D\d+@#\$'

def skill_recency_logic(data_file,rootPath,date_list):
  #add_newruler_to_pipeline("SkillFile.jsonl",rootPath)
  #print("sssssssssssssssss--rrrrrrrrrrrrrrrrrrrrrrrrrr")
  #print("........... skill recency is ...........")
  start_time_skill_recency = time.time()
  
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

  # new_de_dic = {}
  # for i in de_seq:
  #   new_de_dic[[k for k, v in de_dic.items() if v == i][0]] = i
  
  new_de_dic = {}
  for i in de_seq:
    for k, v in de_dic.items():
      if v == i:
        new_de_dic[k] = i
  
  l1 = set(list(new_de_dic.values()))
  l2 =set(de_seq)
  if list(set(l2) - set(l1)) != []:
    #print("FAIL")
    pass

  split_para = re.split(r'\d{0,2}@#\$', string)
  de_dic_para = {}
 
  if len(split_para)-1 == len(l1):
    cnt = 1
    for i in new_de_dic.keys():
      de_dic_para[i] = split_para[cnt]
      cnt+=1
  else:
    cnt = 1
    for i in new_de_dic.keys():
      de_dic_para[i] = split_para[cnt]
      cnt+=1
    #print('FAIL')
   ### if-else looks like duplicate code?
 
  de_dic_para_df = pd.DataFrame([[k,v] for k, v in de_dic_para.items()], columns=['date_pattern', 'Para'])


  date_list_dic = {}
  for i in date_list:
    date_list_dic[i[1]] = i[0]
  ## what is content in  date_list_dic[i[0]]?
    
 
  for i in date_list_dic.keys():
    for j in de_dic_para_df.index:
      if i in de_dic_para_df['date_pattern'][j]:
        de_dic_para_df['date_pattern'][j] = de_dic_para_df['date_pattern'][j].replace(i,date_list_dic[i])
  ### replacing delimiters with dates ?
 

  de_dic_para_df['seq_date'] = ''
  for i in de_dic_para_df.index:
    de_dic_para_df['seq_date'][i] = re.findall(r'\d{0,2}-\d{0,2}-\d{4}', de_dic_para_df['date_pattern'][i])
  ### get seq_date using date regex?
 

  date_list_df = list(de_dic_para_df['seq_date'])
  try:
      date_list_df.sort(key=lambda x:datetime.strptime(x[0],'%d-%m-%Y'))
      date_list_df.sort(key=lambda x:datetime.strptime(x[1], '%d-%m-%Y'))
  except IndexError as e:
      pass
  

  de_dic_para_df['seq_id'] = 0
  cnt = 1
  for i in date_list_df:
    for j in de_dic_para_df.index:
      if i == de_dic_para_df['seq_date'][j] and de_dic_para_df['seq_id'][j] == 0:
        de_dic_para_df['seq_id'][j] = cnt
        cnt = cnt+1
 
### check the above for loop, with print statement?

  de_dic_para_df['NER'] = ''
  for i in de_dic_para_df.index:
    de_dic_para_df['NER'][i] = ','.join(set(run_nlp(de_dic_para_df['Para'][i],rootPath)))

  de_dic_para_df = de_dic_para_df.sort_values('seq_id').reset_index(drop=True)

  recency_list = divide(de_dic_para_df[de_dic_para_df['NER'] != '']['seq_id'].values,3)

  
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
      ### delete skills from medium recency (which are present in both high,medium.)?
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
  
  end_time_skillrec = time.time()
  total_time_skillrec = end_time_skillrec - start_time_skill_recency
  #print(total_time_skillrec)      
  print("????????????????skill recency function ....................",total_time_skillrec)
  #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")     

  return recency_dic_2



