# !pip install PyMuPDF

import time
from spacy.pipeline import EntityRuler
import nl_core_news_sm
import pandas as pd
from nltk.corpus import stopwords
import dateutil 
from dateutil.parser import parse
import re
#import datetime
from datetime import datetime
import sys
import os
import utils.indentifiers as indentifiers
import warnings
warnings.filterwarnings('ignore')
import Model.Skill_Recency_Logic as Skill_Recency_Logic
# ### using NER - Method:
nlp = None


def add_newruler_to_pipeline(rootpath,ner_model):
    global nlp
    nlp = None
    nlp = nl_core_news_sm.load()
    new_ruler = EntityRuler(nlp).from_disk(rootpath+"\Model\\"+ner_model)
    nlp.add_pipe("entity_ruler",after='parser').add_patterns(new_ruler.patterns)
    return new_ruler.patterns

def extract_nlp(para_text,rootpath,ner_model):
    add_newruler_to_pipeline(rootpath,ner_model)
    li = []
    for i in para_text:
        li.append(nlp(i))
    return li

def create_date_set(doc):
    out = []
    for ent in doc.ents:
        if 'edu' in ent.label_.lower() or 'dob' in ent.label_.lower() :
            out.append([ent.text,ent.label_.upper()[4:]])
    if out == []:
        return {}
    else:
        return out 

def create_dateset_dict(para_no, para_texts):
    datesets = [create_date_set(para_texts) for para_texts in para_texts]
    return dict(zip(para_no, datesets))

def get_tags(data,rootpath,ner_model):
    encode_data = data
    range_list = list(range(0, len(encode_data)))
    li_1 = extract_nlp(encode_data,rootpath,ner_model)
    dateset_dict = create_dateset_dict(range_list, li_1)
    dateset_dict = {i:dateset_dict[i] for i in dateset_dict if dateset_dict[i] != {}}
    Tag_model = ["NA"] * len(encode_data)
    for i in dateset_dict.keys():
        Tag_model[i] = "OO"
    return [encode_data,Tag_model]

#Regex Model
def is_date(string, fuzzy=False):
  """
  Return whether the string can be interpreted as a date.

  :param string: str, string to check for date
  :param fuzzy: bool, ignore unknown tokens in string if True
  """
  try: 
      parse(string, fuzzy=fuzzy)
      return True

  except ValueError:
      return False

def dup(lst):
      data_list1=([i for z,i in enumerate(lst) if i not in lst[:z]])
      return data_list1

def date_mapping(data_list1):
    for i in range(len(data_list1)):
        for j in range(i + 1, len(data_list1)):
            try:
                if datetime.strptime(data_list1[i][0], "%d-%m-%Y") == datetime.strptime(data_list1[j][0], "%d-%m-%Y"):
                    data_list1[i][1]=data_list1[j][1]
                elif datetime.strptime(data_list1[i][0], "%d-%m-%Y")> datetime.strptime(data_list1[j][0], "%d-%m-%Y"):
                    if (datetime.strptime(data_list1[i][1], "%d-%m-%Y") > datetime.strptime(data_list1[j][0], "%d-%m-%Y")):
                        data_list1[i][0]=data_list1[j][0]
                elif datetime.strptime(data_list1[i][0], "%d-%m-%Y")< datetime.strptime(data_list1[j][0], "%d-%m-%Y"):
                    if datetime.strptime(data_list1[j][0], "%d-%m-%Y")<datetime.strptime(data_list1[i][1], "%d-%m-%Y"):
                        data_list1[j][0]=data_list1[i][0]
                else:
                        pass
            except IndexError as e:
                pass
    return data_list1

def map_right(data_list1):                                                ## Add try,except 
      for i in range(len(data_list1)):
          for j in range(i + 1, len(data_list1)):
            try:
                if datetime.strptime(data_list1[i][0], "%d-%m-%Y") == datetime.strptime(data_list1[j][0], "%d-%m-%Y"):
                    data_list1[i][1]=data_list1[j+1][1]
            except:
                pass
      return data_list1

def map_left(data_list1):                                            ## Add try,except 
      for i in range(len(data_list1)):
          for j in range(i + 1, len(data_list1)):
            try:
                if datetime.strptime(data_list1[i][1], "%d-%m-%Y") == datetime.strptime(data_list1[j][1], "%d-%m-%Y"):
                    data_list1[i][0]=data_list1[i+1][0]
            except:
                pass
      return data_list1

def calculate_experience(data_list3):
      i = 0
      x=1
      diff_years_revlist = []
      start_date=[]
      end_date=[]
      start_date=[]
      experience=[]
      for item in data_list3:

          try:
            start_date = datetime.strptime(item[i], "%d-%m-%Y")
            end_date = datetime.strptime(item[i+1], "%d-%m-%Y")
            t_ex=end_date-start_date
            experience.append([start_date.strftime("%d-%m-%Y"),end_date.strftime("%d-%m-%Y"),t_ex])
          except:
            pass
      lst=[]
      for item in data_list3:
        try:
            lst.append(item[i])
            lst.append(item[i+1])
        except:
            pass
      lst.pop(0)
      lst.pop(-1)
      return experience

def year_mapping(lst):
    for i in lst:
        try:
            if str(i[1])!=' ':
              
                try:
                    if (str(i[0])<2022 or str(i[0])>1975):
                        dt = dateutil.parser.parse(str(i[0]), dayfirst=True)
                        i[0]=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
                    else:
                        if (str(i[1])<2022 or str(i[1])>1975):
                            dt = dateutil.parser.parse(str(i[1]), dayfirst=True)
                            i[1]=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
                except:
                    pass
        except:
            if i[0].isnumeric():
                if (int(i[0])<2022 or int(i[0]>1975)):
                    dt = dateutil.parser.parse(str(i[0]), dayfirst=True)
                  
                    i[0]=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
                else:
                    dt = dateutil.parser.parse(str(i[1]), dayfirst=True)
                    i[1]=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
    return lst
def till_date(lst):
    for i in lst:
        try:
            if i[1]=='T':
                i[1]=datetime.today().strftime('%d-%m-%Y')
            elif i[1]=='P':
                i[1]=datetime.today().strftime('%d-%m-%Y')
            elif i[1]=='C':
                i[1]=datetime.today().strftime('%d-%m-%Y')
            else:
                pass
        except:
            pass
    return lst

def gap_calculation(l_lst,r_lst):

    gap=[]
    for i in range(len(l_lst)):
        try:
            start_date = datetime.strptime(l_lst[i], "%d-%m-%Y")
            end_date = datetime.strptime(r_lst[i], "%d-%m-%Y")
            t_ex=start_date - end_date
            gap.append([start_date.strftime("%d-%m-%Y"),end_date.strftime("%d-%m-%Y"),t_ex])
   
        except:
            pass
    return gap

def get_exp_and_gap(data,rootpath,ner_model):

  start_time_ner_cal = time.time()
  get_tags_data = get_tags(data,rootpath,ner_model)
  resume_text = pd.DataFrame({'Text':get_tags_data[0],'values':get_tags_data[1]})
  resume_text_NA = resume_text.loc[resume_text['values']!='OO']
  word_text = " ".join(resume_text_NA['Text'].astype('str'))
  word_text=word_text.title()
  regEx = indentifiers.regex1
  result = re.findall(regEx, word_text)
  result_years=re.findall(indentifiers.regex4, word_text)
  
  datelist=[]
  #invalid_list=[]
  lst=[]

#print(result) 
  for i in result_years:
    if "To" in i:
        lst.append(i.split('To'))
    else:
        lst.append(i.split('-'))
  flat_ls = [item for sublist in lst for item in sublist]
  for i in  flat_ls:
    result.append(i)

  for i in result:

    if i.isnumeric():
      if int(i) <= datetime.now().year and int(i) > 1975:
        datelist.append([i,i])
      else:
        pass
    else:
      try:
        if is_date(str(i), fuzzy=False):
            dt = dateutil.parser.parse(str(i), dayfirst=True)
            if (dt.year>2022 or dt.year<=1975):
                pass
            else:
                datelist.append([i,str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)])
        else:
            pass
      except Exception as e:
        
        pass
  for i in datelist:
    
    if i[0].isnumeric():
        dt = dateutil.parser.parse(i[1], dayfirst=True)
        if (dt.year>2022 or dt.year<=1975):
                pass
                
        else:
            i[1]=(str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year))
            
            

  if datelist==[]:
    duration = [["NA","NA"],["NA","NA"]]
    #duration.append("0")
    return duration
    sys.exit()
  else:
    datelist

  date_list = []
  for i in range(0,len(datelist)):
    if datelist[i][0].isnumeric():
        pass
    else:
        word_text = word_text.replace(datelist[i][0], indentifiers.delimiter1 + str(i) + indentifiers.delimiter2)
        date_list.append([datelist[i][1], indentifiers.delimiter1 + str(i) + indentifiers.delimiter2])
  
  for i in range(0,len(datelist)):
    if datelist[i][0].isnumeric():
        word_text = word_text.replace(datelist[i][0], indentifiers.delimiter1 + str(i) + indentifiers.delimiter2)
        date_list.append([datelist[i][1], indentifiers.delimiter1 + str(i) + indentifiers.delimiter2])
 
# Skill Recency
  
  sr = Skill_Recency_Logic.skill_recency_logic(word_text,rootpath,date_list)

  #####################################3
  filtered_spch = re.findall(indentifiers.regex2, word_text)

  filtered_spch1=[]
  for i in filtered_spch:
    i=i.replace(' ','')
    filtered_spch1.append(i.replace("To"," To "))
  filtered_spch = ','.join(filtered_spch1)
  lst=re.findall(indentifiers.regex3, word_text)
  lst1=[]
  for i in lst:
    i=i.replace(' ','')
    lst1.append(i.replace("–"," To "))
#lst[i]=lst[i].replace("–","To")
  lst=','.join(lst1)
  lst_u=re.findall(indentifiers.regex5, word_text)
  lst_U=[]
  for i in lst_u:
    i=i.replace(' ','')
    
    lst_U.append(i.replace("-"," To "))
#lst[i]=lst[i].replace("–","To")
  lst_u=','.join(lst_U)
  for i in date_list:
    filtered_spch=filtered_spch.replace(i[1],i[0])
  filtered_spch = filtered_spch.split(',')
  for i in date_list:
    
    lst=lst.replace(i[1],i[0])
  lst=lst.split(',')
  for i in date_list:
    
    lst_u=lst_u.replace(i[1],i[0])
  lst_u=lst_u.split(',')
  #######################################
  sorted_filtered_spch=[]
#for i in filtered_spch:
  if (filtered_spch!=[''] and lst!=[''] and lst_u!=['']):
    
    sorted_filtered_spch=lst+filtered_spch+lst_u
  elif (filtered_spch!=[''] and lst!=['']):
    sorted_filtered_spch=lst+filtered_spch
  elif (lst_u!=[''] and lst!=['']):
    sorted_filtered_spch=lst+lst_u
  elif (lst_u!=[''] and filtered_spch!=['']):
    sorted_filtered_spch=lst_u+filtered_spch
  elif filtered_spch!=['']:
    
    sorted_filtered_spch=filtered_spch
  elif lst!=['']:
    
    sorted_filtered_spch=lst
  elif lst_u!=['']:
    
    sorted_filtered_spch=lst_u  
  else:
    pass
  #################################
  sorted_filtered_spch1 = []
  for i in sorted_filtered_spch:                               ## date to till_date ## ## Adding exceptional cases ##
    try:
        sorted_filtered_spch1.append(i.split(' To '))
    except:
        pass
      #sorted_filtered_spch1.append(i.split(' to '))
  
  lst=[]
  
  for i in range(len(sorted_filtered_spch1)):
    try:
        if sorted_filtered_spch1[i][1]!=' ':
            lst.append(sorted_filtered_spch1[i])
    except:
        pass
  if lst == []:
    duration = [["NA","NA"],["NA","NA"]]
    #duration.append(["NA","NA"])
    return duration
    print("Currently we are not supporting [d/m/y] format we are supporting only [d/m/y to d/m/y]")
    sys.exit()
  else:
    pass
  sorted_filtered_spch1=lst

  sorted_filtered_spch1=till_date(sorted_filtered_spch1)
  sorted_filtered_spch1=year_mapping(sorted_filtered_spch1)
  data_list=[]
  sorted_filtered_spch1.sort(key=lambda x:datetime.strptime(x[0], '%d-%m-%Y'))
  data_list=sorted_filtered_spch1
  #data_list=year_mapping(data_list)
  
  try:
    start_date = datetime.strptime(data_list[0][0], "%d-%m-%Y")
    end_date = datetime.strptime(data_list[1][0], "%d-%m-%Y")
    age=end_date-start_date
    if age.days>8000:
        data_list=data_list[1:]
    else:
        pass
  except IndexError as e:
        
        pass

  try:
    data_list.sort(key=lambda x:datetime.strptime(x[0], '%d-%m-%Y'))
    data_list.sort(key=lambda x:datetime.strptime(x[1], '%d-%m-%Y'))
  except IndexError as e:
        pass
  
  data_list2 = []
  for i in range(len(data_list)):
      data_list2=dup(data_list)
      data_list2=map_right(data_list2)
  
  try:
        data_list2.sort(key=lambda x:datetime.strptime(x[0], '%d-%m-%Y'),reverse=True)
        data_list2.sort(key=lambda x:datetime.strptime(x[1], '%d-%m-%Y'),reverse=True)
  except IndexError as e:
        pass

  data_list3 = []
  for i in range(len(data_list2)):
      data_list3=dup(data_list2)
      data_list3=map_left(data_list3)

  try:
        data_list3.sort(key=lambda x:datetime.strptime(x[0], '%d-%m-%Y'))
        data_list3.sort(key=lambda x:datetime.strptime(x[1], '%d-%m-%Y'))
        
  except IndexError as e:
        pass
#  for i in data_list3:
#    data_list3=dup(data_list3)
#    data_list3=date_mapping(data_list3)
  for i in range(len(data_list3)):                             ## updated overlaping logic ###
    data_list3=dup(data_list3)
    for j in range(len(data_list3)):
        data_list3=date_mapping(data_list3)

#
  experience = calculate_experience(data_list3)

  total_experience = []
  for i in range(len(experience)):
      total_experience.append(experience[i][2].days)
  total_experience = sum(total_experience)
  total_exp_yrs = round(abs(total_experience/365),1)

  Experiance_detailed_years=[]
  for i in range(len(experience)):           
    Experiance_detailed_years.append([experience[i][0],experience[i][1]])

  total_exp_yrs = [total_exp_yrs,Experiance_detailed_years]

  l=[]
  r=[]
  for i in range(len(data_list3)):              ## Add
    try:
        r.append(data_list3[i][1])
        l.append(data_list3[i][0])
    except:
        pass
  try:
    l.pop(0)
    r.pop(-1)
  except:
    pass

  gap = gap_calculation(l,r)
  

  total_gap = []
  for i in range(len(gap)):
      if gap[i][2].days>31:
        total_gap.append(gap[i][2].days) 
  total_gap = sum(total_gap)
  total_gap_yrs = round(abs(total_gap/365),1)

  gap_detailed_years=[]
  for i in range(len(gap)):
    gap_detailed_years.append([gap[i][0],gap[i][1]])
  
  total_gap_yrs = [total_gap_yrs,gap_detailed_years]

  duration = []
  try:
        duration.append(total_exp_yrs)
        duration.append(total_gap_yrs)
  except IndexError as e:
        pass
        
  end_time_ner = time.time()
  total_time_ner = end_time_ner - start_time_ner_cal
  print(total_time_ner)      
  print("????????????????under get_exp_and_gap function ....................",total_time_ner)
  print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")     
  return duration,sr