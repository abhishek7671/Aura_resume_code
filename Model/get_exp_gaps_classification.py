from spacy.pipeline import EntityRuler
import nl_core_news_sm
import time
import pandas as pd
from nltk.corpus import stopwords
import dateutil 
from dateutil.parser import parse
import re
import pickle
from nltk.corpus import stopwords
from datetime import datetime
import sys
import os
import utils.indentifiers as indentifiers


# ### using classification - Method:

def clean_text(text):
    text = text.lower()
    text = [word.strip('"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~<p><h*>') for word in text.split(" ")]
    text = [word for word in text if not any(c.isdigit() for c in word)]
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    text = " ".join(text)
    return(text)


def get_tags(data,rootpath,model):
    #encode_data = data
    vectorizer = pickle.load(open(rootpath+"\Model\\"+model.split(",")[0], "rb"))                            ## loading the tfidf - pickle file ##
    loaded_model = pickle.load(open(rootpath+"\Model\\"+model.split(",")[1], 'rb'))         ## loading the classification_model pickle file ##
    doc_data = pd.DataFrame(data,columns=['Text'])
    doc_data['Text'] = doc_data['Text'].astype('str')
    doc_data['clean_text'] = doc_data['Text'].apply(lambda x: clean_text(x) )
    #tf = train_model_v1.tf
    #features_doc_data = tf.transform(doc_data.clean_text).toarray()
    features_doc_data = vectorizer.transform(doc_data.clean_text).toarray()
    test_pred = loaded_model.predict(features_doc_data)
    doc_data['prob'] = ''
    doc_data['pred']=''
    doc_data['prob'] = loaded_model.predict_proba(features_doc_data)
    doc_data['pred']= test_pred
    doc_data['predictions']=''
    for j in range(len(doc_data)):
        if doc_data['prob'][j] <= 0.385082097 and doc_data['prob'][j] >= 0.001:
            doc_data['predictions'][j] = "OO"
        elif doc_data['prob'][j] > 0.385082097:
            doc_data['predictions'][j] = "NA"  
            
    
    return [list(doc_data['Text']),list(doc_data['predictions'])]

    

    #return [encode_data,Tag_model]


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
      diff_years_revlist,start_date,end_date,experience = [],[],[],[]
      for item in data_list3:
          try:
            start_date = datetime.strptime(item[i], "%d-%m-%Y")
            end_date = datetime.strptime(item[i+1], "%d-%m-%Y")
            t_ex = end_date-start_date
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

  start_time_classi_cal = time.time()
  
  get_tags_data = get_tags(data,rootpath,ner_model)
  resume_text = pd.DataFrame({'Text':get_tags_data[0],'values':get_tags_data[1]})
  resume_text_NA = resume_text.loc[resume_text['values']!='OO']
  word_text = " ".join(resume_text_NA['Text'].astype('str'))
  
  #regex1 = r'(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[-a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+'
  #regex1 = r'(?:\d{1,2}[-/Th|St|Nd|Rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[-a-z\s,.]*(?:\d{1,2}[-/Th|St|Nd|Rd)\s,]*)+(?:\d{2,4})+'
  #regex2 = r'D\d+@#\$\sTo\sD\d+@#\$|D\d+@#\$\sTo\s[a-zA-Z]|D\d+@#\$'
  #delimiter1 = "D"
  #delimiter2 = "@#$"
  
  #word_text = word_text.lower()
  word_text=word_text.title()
  regEx = indentifiers.regex1
  result = re.findall(regEx, word_text)
  result_years=re.findall(indentifiers.regex4, word_text)
  #print("word_text-----------------:",word_text)
  datelist=[]
  #invalid_list=[]
  # lst=[]
  # #print(result) 
  # for i in result_years:
  #   if "To" in i:
  #       lst.append(i.split('To'))
  #   else:
  #       lst.append(i.split('-'))
  lst = [i.split('To') if "To" in i else i.split('-') for i in result_years]
  flat_ls = [item for sublist in lst for item in sublist]
  # for i in  flat_ls:
  #   result.append(i)
  result.extend(flat_ls)
  
  for i in result:

    if i.isnumeric():
      if int(i) <= datetime.now().year and int(i) > 1975:
        datelist.append([i,i])
    else:
      try:
        if is_date(str(i), fuzzy=False):
            dt = dateutil.parser.parse(str(i), dayfirst=True)
            if (dt.year>2022 or dt.year<=1975):
                pass
            else:
                datelist.append([i,str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)])
      except Exception as e:
        pass
  for i in datelist:
    #print(i[0])
    if i[0].isnumeric():
        dt = dateutil.parser.parse(i[1], dayfirst=True)
        if (dt.year>2022 or dt.year<=1975):
                pass
                #print("year not valid: ", i[1])
        else:
            i[1]=(str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year))
            #print("valid date" , i[1],str(dt.day),str(dt.month),str(dt.year))
  #print("datelist----------------------",datelist)
  if datelist==[]:
    duration = []
    duration.append("0")
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
  #print("datalist is---------------------",date_list)
  #print("word_text classification----------------:",word_text)
#########################33
  filtered_spch = re.findall(indentifiers.regex2, word_text)
  #print("filtered_spch is ............:",filtered_spch)
  # filtered_spch1=[]
  # for i in filtered_spch:
  #   filtered_spch1.append(i.replace(' ','').replace("To"," To "))
  filtered_spch1 = [i.replace(' ','').replace("To"," To ") for i in filtered_spch]
  filtered_spch = ','.join(filtered_spch1)
  lst=re.findall(indentifiers.regex3, word_text)
  # lst1=[]
  # for i in lst:
  #   i=i.replace(' ','')
  #   lst1.append(i.replace("–"," To "))
  #lst[i]=lst[i].replace("–","To")
  lst1 = [i.replace(' ','').replace("–"," To ") for i in lst]
  lst=','.join(lst1)
  lst_u=re.findall(indentifiers.regex5, word_text)
  # lst_U=[]
  # for i in lst_u:
  #   i=i.replace(' ','')
  #   #print(i.replace("-","To"))
  #   lst_U.append(i.replace("-"," To "))
  #lst[i]=lst[i].replace("–","To")
  lst_U = [i.replace(' ','').replace("-"," To ") for i in lst_u]
  lst_u=','.join(lst_U)
  for i in date_list:
    filtered_spch=filtered_spch.replace(i[1],i[0])
  filtered_spch = filtered_spch.split(',')
  for i in date_list:
    #print(i[0],i[1])
    lst=lst.replace(i[1],i[0])
  lst=lst.split(',')
  for i in date_list:
    #print(i[0],i[1])
    lst_u=lst_u.replace(i[1],i[0])
  lst_u=lst_u.split(',')
  #######################################
  sorted_filtered_spch=[]
#for i in filtered_spch:
  if (filtered_spch!=[''] and lst!=[''] and lst_u!=['']):
    #print("both are having elements")
    sorted_filtered_spch=lst+filtered_spch+lst_u
  elif (filtered_spch!=[''] and lst!=['']):
    sorted_filtered_spch=lst+filtered_spch
  elif (lst_u!=[''] and lst!=['']):
    sorted_filtered_spch=lst+lst_u
  elif (lst_u!=[''] and filtered_spch!=['']):
    sorted_filtered_spch=lst_u+filtered_spch
  elif filtered_spch!=['']:
    #print("filtered_spch is empty")
    sorted_filtered_spch=filtered_spch
  elif lst!=['']:
    #print("lst is empty")
    sorted_filtered_spch=lst
  elif lst_u!=['']:
    #print("lst is empty")
    sorted_filtered_spch=lst_u  
  else:
    pass
  #################################

      #sorted_filtered_spch1.append(i.split(' to '))
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
    duration = []
    duration.append("0")
    return duration
    print("Currently we are not supporting [d/m/y] format we are supporting only [d/m/y to d/m/y]")
    sys.exit()
  else:
    pass
  sorted_filtered_spch1=lst

  sorted_filtered_spch1=till_date(sorted_filtered_spch1)
  sorted_filtered_spch1=year_mapping(sorted_filtered_spch1)
  #print("sorted_filtered_spch1----------------",sorted_filtered_spch1)
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
        # print("Index out of range")
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

  # total_experience = []
  # for i in range(len(experience)):
  #     total_experience.append(experience[i][2].days)
  total_experience = [experience[i][2].days for i in range(len(experience))]
  total_exp_yrs = round(abs(sum(total_experience)/365),1)

  # Experiance_detailed_years=[]
  # for i in range(len(experience)):           
  #   Experiance_detailed_years.append([experience[i][0],experience[i][1]])
  Experiance_detailed_years = [[experience[i][0],experience[i][1]] for i in range(len(experience))]

  total_exp_yrs = [total_exp_yrs,Experiance_detailed_years]

  l,r=[],[]
  
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
  

  # total_gap = []
  # for i in range(len(gap)):
  #     total_gap.append(gap[i][2].days)
  total_gap =[gap[i][2].days for i in range(len(gap))]
  total_gap_yrs = round(abs(sum(total_gap)/365),1)

  # gap_detailed_years=[]
  # for i in range(len(gap)):
  #   gap_detailed_years.append([gap[i][0],gap[i][1]])

  gap_detailed_years = [[gap[i][0],gap[i][1]] for i in range(len(gap))]
  
  total_gap_yrs = [total_gap_yrs,gap_detailed_years]

  duration = []
  try:
        duration.append(total_exp_yrs)
        duration.append(total_gap_yrs)
  except IndexError as e:
        pass
      
  end_time_classi = time.time()
  total_time_classi = end_time_classi - start_time_classi_cal
        
  return duration