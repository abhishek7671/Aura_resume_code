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
import utils.reg_indentifiers as ident
# ### using NER - Method:
nlp = None


def add_newruler_to_pipeline(ner_model):
    global nlp
    nlp = None
    nlp = nl_core_news_sm.load()
    new_ruler = EntityRuler(nlp).from_disk(r""+os.path.dirname(os.path.realpath(__file__))+"/"+ner_model)
    #print(".....**********.path in add_newruler_to_pipline are...........",rootpath+"/"+ner_model)
    #print("new_ruler is given as ...................",new_ruler)
    nlp.add_pipe("entity_ruler",after='parser').add_patterns(new_ruler.patterns)
    return new_ruler.patterns

add_newruler_to_pipeline('DateFile.jsonl')

def extract_nlp(para_text,rootpath,ner_model):
    temp_nlp = nlp
    # add_newruler_to_pipeline(rootpath,ner_model)
    # li = []
    # for i in para_text:
    #     li.append(nlp(i))
    li = [temp_nlp(i) for i in para_text]
    return li

def create_date_set(doc):
    # out = []
    # for ent in doc.ents:
    #     if 'edu' in ent.label_.lower() or 'dob' in ent.label_.lower() :
    #         out.append([ent.text,ent.label_.upper()[4:]])
    out = [[ent.text,ent.label_.upper()[4:]] for ent in doc.ents if 'edu' in ent.label_.lower() or 'dob' in ent.label_.lower()]
    #print("================ out values are given AS ================",out)
    if out == []:
        return {}
    else:
        return out 

def create_dateset_dict(para_no, para_texts):
    datesets = [create_date_set(para_texts) for para_texts in para_texts]
    #print("*********************** under create_dateset_dict function *******************************")
    #print("dateset_dict is............................",datesets)
    #print("************************************ ABOVE VALUES ARE DIC VALUES *****************************************")
    return dict(zip(para_no, datesets))

def get_tags(data,rootpath,ner_model):
    encode_data = data
    range_list = list(range(0, len(encode_data)))
    li_1 = extract_nlp(encode_data,rootpath,ner_model)
    #print("extract_nlp values are given as..........",li_1)
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
      i,x,diff_years_revlist,start_date,end_date,start_date,experience = 0,1,[],[],[],[],[]
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
                    if (str(i[0])<str(datetime.now().year) or str(i[0])>1975):
                        dt = dateutil.parser.parse(str(i[0]), dayfirst=True)
                        i[0]=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
                    else:
                        if (str(i[1])<str(datetime.now().year) or str(i[1])>1975):
                            dt = dateutil.parser.parse(str(i[1]), dayfirst=True)
                            i[1]=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
                except:
                    pass
        except:
            if i[0].isnumeric():
                if (int(i[0])<int(datetime.now().year) or int(i[0]>1975)):
                    dt = dateutil.parser.parse(str(i[0]), dayfirst=True)
                  
                    i[0]=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
                else:
                    dt = dateutil.parser.parse(str(i[1]), dayfirst=True)
                    i[1]=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
    return lst


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

def empty_list(lst):
    duration = [['NA','NA'],['NA','NA']]
    if lst == []:
        duration.append("0")
        return sys.exit(duration)
        
    else:
        pass



def extract_valid_dates(word_text):                                                #'''  19-08-2022 , created extract_valid_dates function '''
  #''' Author : Ashwini.M, Manmeeth
  #    Description:  extracting dates from the text using regex
  #    Parameters: text
  #    return :valid dates in list format'''
  #result = re.findall(indentifiers.regex1 , word_text)                              #''' Extract dates using regex '''
  ##################### Added new regex logic 21-12-2022 #################################################################

  result,delimi,counter,dic_keys,dic_values,dic_seq,sequ= [],[],0,[],[],[],0

  for i in ident.regex_date_identifer:
    if re.findall(i,word_text) != []:
        result.append(re.findall(i,word_text))
        
        #print("results are..............",result)
        for j in re.findall(i,word_text):
            sequ += 1
            dic_keys.append(j)
            #print("dic_keys are given as...........",dic_keys)
            #dic_seq.append()
        for k in range(counter,len(dic_keys)):
            counter += 1
            dic_values.append(
                indentifiers.delimiter1 + str(counter) + indentifiers.delimiter2 + indentifiers.delimiter3 + str(sequ))
            #print("dic_keys & dict_values..",dic_keys[k],dic_values[k])
            word_text  = word_text.replace(dic_keys[k],
                                           indentifiers.delimiter1 + str(counter) + indentifiers.delimiter2 + indentifiers.delimiter3 + str(sequ))
            #print("_________________________________________________________________")
            #print("word_text is.................",word_text)
            #print("_________________________________________________________________")
            
  result = [x for x in result if x!=[]]
  data1 = pd.DataFrame(list(zip(dic_keys, dic_values)),columns=['dates_txt','delimiterss'])
  #print("dataframe is............................................................",data1.head())
  data1['delimit'] = ''
  data1['seq'] = ''

  for i in range(len(data1)):
    data1['delimit'][i] = data1['delimiterss'][i].split('s')[0]
    data1['seq'][i] = data1['delimiterss'][i].split('s')[1]
  
  flatted_result = lambda result:[element for item in result for element in flatten_list(item)] if type(result) is list else [result]
  result = flatted_result(result)
  
  
  
  ##################### Added new regex logic 21-12-2022 #################################################################
  result_years=re.findall(indentifiers.regex4, word_text)
  datelist=[]
  lst=[]
  for i in result_years:                                          #''' Split date ranges based on given string ("To","-")'''
    if "To" in i:
        lst.append(i.split('To'))  
    else:
        lst.append(i.split('-'))
    if "–" in i:                               #### Updated ( To handle 2020-till date)
        lst.append(i.split('–'))

        
  flat_ls = [item for sublist in lst for item in sublist]
  #   for i in  flat_ls:
  #     result.append(i)
  result.extend(flat_ls)
  
  for i in result:                                               
    if i.isnumeric():                                           #'''' Filtering integers with year''' 
      if int(i) <= datetime.now().year and int(i) > 1975:
        datelist.append([i,i])
      else:
        pass
    else:
      try:
        if is_date(str(i), fuzzy=False):                       #''' Convert jan-2021 to DD-01-2021'''
            dt = dateutil.parser.parse(str(i), dayfirst=True)
            if (dt.year>datetime.now().year or dt.year<=1975):
                pass
            else:
                datelist.append([i,str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)])
        else:
            pass
      except Exception as e:
        
        pass
        
  ################################################################ 04-01-2022 ##################################3
  for i in datelist:
    #print(i[0])
    if i[0].isnumeric():
        
        dt = dateutil.parser.parse(i[1], dayfirst=True)
        if (dt.year>datetime.now().year or dt.year<=1975):
                print("year not valid: ", i[1])
        else:
            i[1]=(str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year))
            #print("valid date" , i[1],str(dt.day),str(dt.month),str(dt.year))
            
  if datelist==[]:
    duration = [["NA","NA"],["NA","NA"]]
    #duration.append("0")
    return duration
    sys.exit()
  else:
    datelist
            
  data = pd.DataFrame(datelist,columns=['dates_txt','stnf_frmt'])
  lt,lt_stndfrmt,lt1 = [],[],[]
  for i in range(len(datelist)):
    lt.append(datelist[i][0])
    lt_stndfrmt.append(datelist[i][1]) 
  lt1.append(data1['dates_txt'])
  lt2 = [x for x in lt if x not in dic_keys]
  data1 = data1.append(pd.DataFrame(lt2, columns=['dates_txt']),ignore_index=True)
  data1['delimit_upd']=''
  #dt['seq_upd']=''

  for i in range(len(data1)):
    data1['delimit_upd'][i] = indentifiers.delimiter1 + str(i) + indentifiers.delimiter2
  final_df = pd.merge(data1,data, on = 'dates_txt')    
  date_list = []

  for i in range(len(final_df)):
    #print([final_df['stnf_frmt'][i],final_df['delimit_upd'][i]])
    date_list.append([final_df['stnf_frmt'][i],final_df['delimit_upd'][i]])
  for i in range(len(final_df)):
    #if datelist[i][0].isnumeric() == False:
        #print("string values:",datelist)
    word_text = word_text.replace(str(final_df['delimiterss'][i]),str(final_df['delimit_upd'][i]))
    
    if final_df['dates_txt'][i] in word_text:
        word_text = word_text.replace(str(final_df['dates_txt'][i]),str(final_df['delimit_upd'][i]))

  
  return date_list,word_text
 
 ############################# add logic to handle single dates #################################
 
reg2 = r'D\d+@#\$\s*'

def get_singledates(reg2,word_text,date_list,filtered_date_list):
    ltt = []
    for i in indentifiers.dtn.keys():
        #print("i is..........",i)
        #print("word_text is...........",word_text)
        ltt.append(re.findall(i,word_text))

    flatted_result1 = lambda result:[element for item in result for element in flatten_list(item)] if type(result) is list else [result]
    lt = flatted_result1(ltt)
    #print("----->----->"*20)
    #print(lt)
   # lt = re.findall(reg1,word_text)
    for i in range(len(lt)):
        word_text = word_text.replace(lt[i],"s_s" + str(i) + indentifiers.delimiter2)
    lt1= re.findall(reg2,word_text)
    lt1=[x.replace(' ','') for x in lt1]

    
    for i in range(len(date_list)):
        if date_list[i][1] in lt1:
            filtered_date_list.append([date_list[i][0]])
    return filtered_date_list

def single_date_process(data_list):
    #dl=[]
    for i in data_list:
        if len(i) == 1:
            i.append(i[0])
    for i in range(1,len(data_list)):
        #print("data_list is................",data_list)
        if data_list[i-1][0] == data_list[i-1][1]:
            data_list[i-1][1] = data_list[i][0]
            

    return data_list
  
######################################### add logic to handle single dates #######################333

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
            
        if (len(re.findall('D\d+@#&\s+T|D\d+@#&\s+P|D\d+@#&\s+C|D\d+@#&\s+N',i))==1):
            pass
        
        i = i.replace('&','$')
        filtered_spch1.append(i.replace(value," To "))
        #print("filtered_spch1",filtered_spch1)
    filtered_spch = ','.join(filtered_spch1)
    for i in date_list:
        filtered_spch=filtered_spch.replace(i[1],i[0])
    filtered_spch = filtered_spch.split(',')
    return filtered_spch

def flatten_list(_2d_list):                                        ### 06-09-2022 ###
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list
   


###############################3 19-12-2022 #######################  
def remove_spaces(lst):
    # result =[]
    # for i in lst:
    #     j = i.replace(' ','')
    #     result.append(j)
    result = [i.replace(' ','') for i in lst]
    return result

################ Add logic to remove overlaped dates (because of adding single dates)    ###########

def exp_overcal(experience,data_list3):
    # print("<=======+++++======>"*8)
    ### experiment-2(logic)
    rem = []

    for i in range(1,len(experience)):
        #print("...........i is",i, experience[i])
        if datetime.strptime(experience[i-1][1], "%d-%m-%Y") > datetime.strptime(experience[i][0], "%d-%m-%Y"):
            experience[i][0] = experience[i-1][1]
            if len(experience)-1 != i:
                #print("...remove the list which is having overlapping dates...........",experience[i])
                rem.append(experience[i])
            else:
                pass
        
        else:
            pass
    
    dup_data_list3=[]
    i = 0
    start_date=[]
    end_date=[]


    for item in data_list3:
        try:
            start_date = datetime.strptime(item[i], "%d-%m-%Y")
            # print(start_date)
            end_date = datetime.strptime(item[i+1], "%d-%m-%Y")
            t_ex=end_date-start_date
            #print("===>"*12)
            #print("........ number of days/duration is....................",t_ex)
            dup_data_list3.append([start_date.strftime("%d-%m-%Y"),end_date.strftime("%d-%m-%Y"),t_ex])
        except IndexError as e:
            pass
    dup_data_list3 = [x for x in dup_data_list3 if x in experience]
    
    l=[]
    r=[]
    for i in range(len(dup_data_list3)):
        try:
            #print(data_list3[i][0],data_list3[i][1])
            r.append(dup_data_list3[i][1])
            l.append(dup_data_list3[i][0])
        except IndexError as e:
            pass
    try:
        l.pop(0)
        r.pop(-1)
    except:
        pass

    gap = gap_calculation(l,r)
    # total_experience=[]
    # for i in range(len(experience)):
    #     total_experience.append(experience[i][2].days)
    total_experience =[experience[i][2].days for i in range(len(experience))]
    total_experience = sum(total_experience)
    total_exp_yrs = total_experience/365

    # total_gap = []
    # for i in range(len(gap)):
    #     total_gap.append(gap[i][2].days)
    total_gap = [gap[i][2].days for i in range(len(gap))]
    
    total_gap_yrs = sum(total_gap)/365
    total_gap_yrs
    duration = []
    try:
        duration.append(round(total_exp_yrs,1))
        duration.append(round(total_gap_yrs,1))
        duration
    except NameError as e:
        pass
    duration
    # Experiance_detailed_years=[]
    # for i in range(len(experience)):           
    #     Experiance_detailed_years.append([experience[i][0],experience[i][1]])
    Experiance_detailed_years = [[experience[i][0],experience[i][1]] for i in range(len(experience))]
    total_exp_yrs = [total_exp_yrs,Experiance_detailed_years]
    #print("===>"*8)
    #print("...... Total experience cal is (from ner model) ...............",total_exp_yrs)
    # gap_detailed_years=[]
    # for i in range(len(gap)):
    #     gap_detailed_years.append([gap[i][0],gap[i][1]])
    gap_detailed_years = [[gap[i][0],gap[i][1]] for i in range(len(gap))]
    total_gap_yrs = [total_gap_yrs,gap_detailed_years]
    #print("===>"*8)
    #print(".......... Total gap from cal is (from ner model) ...................",total_gap_yrs)

    duration = []
    try:
        duration.append(total_exp_yrs)
        duration.append(total_gap_yrs)
    except IndexError as e:
        pass
    print("............. Duration is .........",duration)
    return duration

################ Add logic to remove overlaped dates (because of adding single dates)    ###########


def get_exp_and_gap(data,rootpath,ner_model):
#   print("******************** entered into get_exp_and_gap function *********************************")
  #start_time_ner_cal = time.time()
  get_tags_data = get_tags(data,rootpath,ner_model)
  
  #print("resume_text is having tages..............")
  resume_text = pd.DataFrame({'Text':get_tags_data[0],'values':get_tags_data[1]})
  resume_text_NA = resume_text.loc[resume_text['values']!='OO']
  word_text = " ".join(resume_text_NA['Text'].astype('str'))
  word_text = re.sub("\s\s+" , " ",word_text) 
  word_text = word_text.replace("|"," ") 
  word_text=word_text.title()
  word_text = word_text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'") #### updated(adding to handle Sep’06 dates) 
  temp_wordtxt = word_text
  date_list,word_text = extract_valid_dates(word_text)
  
  ## Extract skills if resume will not contain any date durations ##
  
  if date_list == ['NA','NA'] and word_text == ['NA','NA']:
  
    sr,ner_model_skill = Skill_Recency_Logic.skill_recency_logic(temp_wordtxt,rootpath,date_list)
    duration = ['NA','NA']
    return duration,sr,ner_model_skill
  else:                                                                                  ## Extract skills if resume will contain any date durations ##

    sr,ner_model_skill = Skill_Recency_Logic.skill_recency_logic(word_text,rootpath,date_list)

    
   ## ........ Extract skills .......... ##
# Skill Recency
  
  #sr,ner_model_skill = Skill_Recency_Logic.skill_recency_logic(word_text,rootpath,date_list)

  #####################################3
 
#   filtered_date_list=[]

#   for k,v in indentifiers.dtn.items():
#     filtered_date_list.append(delimiters_to_date_conversion(k,word_text,v,date_list))
  filtered_date_list = [delimiters_to_date_conversion(k,word_text,v,date_list) for k,v in indentifiers.dtn.items()]
  
  filtered_date_list=[ele for ele in filtered_date_list if ele != ['']]
  
  ############################## 2. add logic for single date process (calling function ) ##############################

  filtered_date_list = get_singledates(reg2,word_text,date_list,filtered_date_list)
  
  ############################## 2. add logic for single date process (calling function ) ##############################
  
  sorted_filtered_spch = [] 
  sorted_filtered_spch = lambda filtered_date_list:[element for item in filtered_date_list for element in flatten_list(item)] if type(filtered_date_list) is list else [filtered_date_list]
  #print("Transformed List ", sorted_filtered_spch(filtered_date_list))
  #print("filtered_date_list is ..........................",filtered_date_list)
  #################################added new logic (19-12-2022) delimiters ################################
  
  sorted_filtered_spch1 = []
  for i in sorted_filtered_spch(filtered_date_list):                               ## date to till_date ## ## Adding exceptional cases ##
    if "To day" in i:
        i = i.replace('To day','Today')
    try:
        sorted_filtered_spch1.append(i.split(' To '))
    except:
        pass
    
  ##########################   added new logic (19-12-2022) to remove spaces eg: ['20-02-2022 ','T'] ###############
#   lt = []

#   for lst in sorted_filtered_spch1:
#     lt.append(remove_spaces(lst))
  
  lt = [remove_spaces(lst) for lst in sorted_filtered_spch1]

  #print("dates before removing spaces",lt)

  sorted_filtered_spch1= lt
  sorted_filtered_spch1

###################### commenting these code for single date calculation ###############33
#  lst=[]
#  
#  for i in range(len(sorted_filtered_spch1)):
#    try:
#        if sorted_filtered_spch1[i][1]!=' ':
#            lst.append(sorted_filtered_spch1[i])
#    except:
#        pass
#
################## commenting these code for single date calculation ###############33

  if sorted_filtered_spch1 == []:
    duration = [["NA","NA"],["NA","NA"]]
    #duration.append(["NA","NA"])
    return duration
    print("Currently we are not supporting [d/m/y] format we are supporting only [d/m/y to d/m/y]")
    sys.exit()
  else:
    pass
  #sorted_filtered_spch1=lst

  sorted_filtered_spch1=till_date(sorted_filtered_spch1)
  sorted_filtered_spch1=year_mapping(sorted_filtered_spch1)
  data_list=[]
  sorted_filtered_spch1.sort(key=lambda x:datetime.strptime(x[0], '%d-%m-%Y'))
  data_list=sorted_filtered_spch1
  #data_list=year_mapping(data_list)
  
########################### 3. add logic to handle single dates function call ####################

  single_date_process(data_list)
#   print("---"*20)
  #print("===============> data_list values are........=======>",data_list)
  ########################### 3. add logic to handle single dates function call ####################
########################### 4. add logic to handle single dates function call ####################
  
  dl = []

  for i in range(len(data_list)):

    if (datetime.strptime(data_list[i][1], "%d-%m-%Y") - datetime.strptime(data_list[i][0], "%d-%m-%Y")).days >= 0:
        dl.append(data_list[i])
    else:
        pass
  data_list = dl


########################### 4. add logic to handle single dates function call ####################
  
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

    ###################### ------- 19-12-2022 -------- added new logic to eliminate list if it contains any charecter eg: ['12-02-2010','t']['12-02-2010','D'] ###################
  
#   dl = []

#   for i in data_list:
#     for j in i:
#         if j.isalpha() == True:
#             dl.append(i)
  dl = [i for i in data_list for j in i if j.isalpha() == True]

  data_list = [x for x in data_list if x not in dl ]
        
 ###################### ------- 19-12-2022 -------- added new logic to eliminate list if it contains any charecter eg: ['12-02-2010','t']['12-02-2010','D'] ###################


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

#   total_experience = []
#   for i in range(len(experience)):
#       total_experience.append(experience[i][2].days)
  total_experience = [experience[i][2].days for i in range(len(experience))]
  total_exp_yrs = round(abs(sum(total_experience)/365),1)

#   Experiance_detailed_years=[]
#   for i in range(len(experience)):           
#     Experiance_detailed_years.append([experience[i][0],experience[i][1]])
  Experiance_detailed_years = [[experience[i][0],experience[i][1]] for i in range(len(experience))]

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
  

#   total_gap = []
#   for i in range(len(gap)):
#       if gap[i][2].days>31:
#         total_gap.append(gap[i][2].days) 
  total_gap =[gap[i][2].days for i in range(len(gap)) if gap[i][2].days>31]
  total_gap_yrs = round(abs(sum(total_gap)/365),1)

#   gap_detailed_years=[]
#   for i in range(len(gap)):
#     gap_detailed_years.append([gap[i][0],gap[i][1]])
  gap_detailed_years = [[gap[i][0],gap[i][1]] for i in range(len(gap))]
  total_gap_yrs = [total_gap_yrs,gap_detailed_years]

  duration = []
  try:
        duration.append(total_exp_yrs)
        duration.append(total_gap_yrs)
  except IndexError as e:
        pass
        
        
  if total_gap_yrs[0] < 0:

    duration = exp_overcal(experience,data_list3)

  else:

    pass
     
  return duration,sr,ner_model_skill