#!/usr/bin/env python
# coding: utf-8

print("#######-> Welcome to Resume Scoring Tool <-#######\n")
#from asyncio.windows_utils import PipeHandle
from cmath import exp
from hashlib import shake_128
import os, glob
import pathlib
import asyncio

from pyparsing import condition_as_parse_action

#Import Packages
try:
    import time
    import re
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    import pandas as pd
    import numpy as np
    import json
    from tqdm import tqdm as tqdm
    
    import nltk
    #print(nltk.data.find('tokenizers/punkt'))
    nltk.download('punkt')
    import datetime, time
    from file_process.Jd_extraction import start
    from math import isnan, nan
    from docx import *
    import warnings
    warnings.filterwarnings('ignore')
    from file_process.experience import get_experience
    import file_process.email_phone_ext as email_phone_ext
    #from get_exp_gaps import get_exp_and_gap
    import Model.get_exp_gaps_classification
    import Model.get_exp_gaps_ner as get_exp_gaps_ner
    import utils.config as cf
    import spacy
    spacy.load('nl_core_news_sm')
    import nl_core_news_sm
    import traceback
    import sys
    import argparse
    import PyPDF2
    import docx2txt
    from file_process.Extract_data_from_doc import get_pdf_data
    import sklearn
    from spacy.pipeline import EntityRuler
    from gensim.models import Word2Vec
    import time
    import utils.azure_conn as run_Azure_conn
    from utils.pencrypt import decrypt
    import base64
    from flask import  jsonify
    # import Model.DocFileExtraction as DocFileExtraction # currently not in use

except Exception as e:
    print(e)
    raise
    # exc_type, exc_value, exc_traceback = sys.exc_info()
    # tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
    # for i in tb_str: print(i)
    time.sleep(10)


run_mode = ''
start_time = start_time_undermain = time.time()
#Read Data Inputs
try:
    rootPath = cf.rootPath
    threshold = 84
    check = None
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
    for i in tb_str: print(i)
    time.sleep(20)
    raise

#Load Relevance Model
try:
    #model = Word2Vec.load(rootPath + r"\Model/word2vec.model")
    model = Word2Vec.load(os.path.join(os.path.abspath(os.path.curdir),"./Model/word2vec.model"))
    # df_skill50k = pd.read_csv(rootPath + r"\Model\skill2vec_50K.csv")
    # df_skill50k.drop(columns='1',inplace=True)
    # skills_list = df_skill50k.T.apply(lambda x: x.dropna().astype(str).tolist()[:-2]).tolist()
    # df_skill50k['Cleaned'] = skills_list
    # df_skill50k['Cleaned_T'] = df_skill50k.Cleaned.apply(lambda x: " ".join(x))
    # review_text = df_skill50k.Cleaned_T.apply(gensim.utils.simple_preprocess)
    # review_text_len0 = review_text[review_text.map(lambda d: len(d)) > 0]
    # review_text_len0 = review_text_len0.reset_index(drop=True)
    # model = gensim.models.Word2Vec(window=10,min_count=2,workers=4,)
    # model.build_vocab(review_text_len0,progress_per=1000)
    # model.train(review_text_len0, total_examples=model.corpus_count, epochs=model.epochs)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
    for i in tb_str: print(i)

""" might required while training """
# def word2vec_preprocess(data):
#
#     return data.lower().replace("-"," ").split(",")

def get_relevant_skills(jdskills,resumeskills,matchedskills):
    '''
        Author: XYZ

        Description: This function is used to get relevant skills that matched from profile.

        params: jdskills(list): all the skills present in job description file
                resumeskills(list): all the skills present in resume file
                matchedskills(list): all the matched skills i.e.; skills matched in resumes and job
                description file

        return: list of relevant and matched skills
    '''
    try:
        jdskills = jdskills.lower().replace(", ",",").replace("-"," ").split(",")
        resumeskills = resumeskills.lower().replace(", ",",").replace("-"," ").split(",")
        matchedskills = matchedskills.lower().replace(", ",",").replace("-"," ").split(",")
        out_li = []
        for i in jdskills:
            try:
                out_li.extend([i[0].replace('ee','j2ee') for i in model.wv.most_similar(i,topn=10)])
                #print(i,out_li)                
            except Exception as e:
                #print(e)
                pass
        
        out_li = set(out_li)
        out_l1 = [x for x in out_li if x not in set(jdskills+matchedskills)]
        out_l2 = [x for x in out_l1 if x in resumeskills]
        return out_l2
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return 'fetching skills failed!'

def extract_text_from_word(filepath):
    '''
        Author: XYZ

        Description:This function is used to extract text from word files
                    i.e job desc. file or resume. Opens and reads in a .docx file from path.

        params: filepath(str): path of folder where this file is located

        return: list - extracted text and list of extracted data i.e. each word or each digit.

    '''
    '''Opens en reads in a .docx file from path'''
    try:
        #docx_text = docx2txt.process(open(filepath,'r+b'))
        ##docx_text_list = docx_text.replace('\t', ' ').replace('\xa0','').split("\n\n")
        #docx_text_list = docx_text.replace('\t', ' ').replace('\xa0',' ')
        #docx_text_list = docx_text_list.replace('?',' ')
        #docx_text_list= re.sub('\s+',' ',docx_text_list)
        #docx_text_list=docx_text_list.split("\n\n")
        ##docx_text = docx_text.replace('\n', ' ').replace('\t', ' ').replace('\xa0','')
        #docx_text = docx_text.replace('\n', ' ').replace('\t', ' ').replace('\xa0',' ')
        #docx_text = docx_text.replace('?',' ')
        #docx_text= re.sub('\s+',' ',docx_text)
        
        docx_text = docx2txt.process(open(filepath,'r+b'))
        docx_text_list = docx_text.replace('\t', ' ').replace('\xa0',' ').split("\n\n")
        docx_text = docx_text.replace('\n', ' ').replace('\t', ' ').replace('\xa0',' ')
        return [docx_text,docx_text_list]
        #return [docx_text,docx_text_list]
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while extracting data from word"

def extract_text_from_pdf(filepath):
    '''
        Author: XYZ

        Description: This function is used to extract text from pdf file i.e. resume files
                    Opens and reads in a PDF file from path

        params: filepath(str): path of folder where pdf file is located

        return: list - extracted text and list of extracted data i.e. each word or each digit
    '''
    '''Opens and reads in a PDF file from path'''
    try:
        fileReader = PyPDF2.PdfFileReader(open(filepath,'rb'))
        page_count = fileReader.getNumPages()
        pdf_text = [fileReader.getPage(i).extractText() for i in range(page_count)]
        pdf_text = str(pdf_text).replace("\\n", "").replace('\xa0','')
        pdf_data_list = get_pdf_data(filepath)
        return [pdf_text,pdf_data_list]
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while extracting data from pdf"

def text_read(file):
    '''
            Author: XYZ

            Description: This function opens file and reads it.

            params: file(str): path of folder where .txt file is located

            return: all the text read by function.
    '''
    try:
        with open(file, 'r') as file:
            data = file.read()
        return data
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while reading file"

""" duplicate function """
# def add_newruler_to_pipeline(skill_pattern_path):
#     '''Reads in all created patterns from a JSONL file and adds it to the pipeline after PARSER and before NER'''
#     new_ruler = EntityRuler(nlp).from_disk(skill_pattern_path)
#     nlp.add_pipe("entity_ruler",after='parser').add_patterns(new_ruler.patterns)

def text_extract(path_name):
    '''
        Author: XYZ

        Description: This function is used to call functions for
                    data extraction depends upon file type.

        params: path_name: path of folder where all the files are stored.

        return: data/text extracted to process further based on file format.
    '''
    try:
        file_extension = path_name.split(".")[-1]
        if file_extension == 'docx' or file_extension == "DOCX":
            return extract_text_from_word(path_name)
        elif file_extension == 'pdf' or file_extension == "PDF":
            return extract_text_from_pdf(path_name)
        else:
            return ('Other_File_Format')
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while extracting data from resume "

async def process_files(infiles):
    tasks = []  # for storing all the tasks we will create in the next step
    for infile in infiles:
        tasks.append(asyncio.ensure_future(preprocess_Resume(infile)))
    # .gather() will collect the result from every single task from tasks list
    # here we use await to wait till all the requests have been satisfied
    all_results = await asyncio.gather(*tasks)
    # combined_list = merge_lists(all_results)
    # print(">>>>",all_results)
    return all_results

async def preprocess_Resume(resume_path):
    '''
        Author: XYZ

        Description: This function is used to preprocess resume and get required data

        params: resume_path(str): path of folder where all the resumes are stored

        return: multiple values like: name of resume, extracted data, experience,
        total experience, skill recency, email and mobile number of candidate
    '''
    text_list = []
    try:
        
        resume_names = resume_path.split('/')[-1]
        data = text_extract(resume_path)
        text_list.append(data[0])
        resume_experience_pattern1 = 'NA'
        try:
            resume_experience_pattern1 = get_experience(text_list[0])
            resume_experience_pattern2, sr,ner_skill_data = get_exp_gaps_ner.get_exp_and_gap(data[1],rootPath,"DateFile.jsonl")
            resume_experience_pattern2 = list(resume_experience_pattern2)
            # await asyncio.sleep(0.5)
        except:
            resume_experience_pattern2 = [["NA","NA"],["NA","NA"]]
            sr = {"Low_Skill_Recency":{"NA"},"Medium_Skill_Recency":{"NA"},"High_Skill_Recency":{"NA"}}
            ner_skill_data = {}
        try:
            resume_email, resume_mobile = email_phone_ext.emph(text_list[0])
        except:
            resume_email, resume_mobile = "NA" , "NA"
        run_Azure_conn.write_json(f"In Document Extraction process", 25, os.path.basename(""))
        # await asyncio.sleep(1)
        return resume_names, text_list, resume_experience_pattern1, resume_experience_pattern2, sr,ner_skill_data, resume_email, resume_mobile
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed to process resume " + str(resume_names)

def preprocess_JD(jd_path,Flag):
    '''
            Author: XYZ

            Description: preprocessing of jd file and extracting required fields from jd file

            params: jd_path(file_path): path of folder where job description file is present
                    flag(int) : flag value based on type of input

            return: multiple values like jd file name, extracted data of jd and experience from jd
    '''
    try:
        text_list = []
        jd_names = ''
        jd_names = jd_path.split('\\')[-1]
        
        if Flag == 1:
            text_list.append(JD_TEXT)
        else:
            text_list.append(text_extract(jd_path))
        jd_experience = get_experience(text_list[-1])

        if jd_experience == "NA":
            jd_experience = 1
        return jd_names, text_list, jd_experience
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        
        return "failed to process jd"

def createList_Range(r1, r2):
    '''
            Author: XYZ

            Description: This function creates range from input experience

            params: r1(int): minimum value of experience
                    r2(int): maximum value of experience

            return: list of all the years falls under given range
    '''
    return [item for item in range(r1, r2+1)]

def years_and_months(float_year):
    '''
            Author: XYZ

            Description: This function is used get float value of year to separate
                        value for months and years.

            params: float_year(float): extracted float experience years

            return: converted year and month as separate ints
    '''
    year = int(float_year)* 12
    month = int(str(float_year).split(".")[1])
    return year+month

def process_text(resume_path, jd_file, flag, MDS, SDS, excel_exp):
    '''
        Author: XYZ

        Description: This function is used to extract jd files and resume files from folder
                    and separating resume files and jd files. Parse the required data from files.

        params: mypath(file_path): path of folder where job description file and resume files is present
                flag(int) : flag value based on type of input

        return: Multiple values like parsed data of jd files and resume files, jd file path, jd and resume file list.
    '''
    #global pbar
    try:
        # total_files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        # extensions=[".pdf",".docx",".PDF"]
        # exts = tuple(extensions)
        # total_files = [f for f in total_files if f.endswith(exts)]
        #change1
        # total_files = [f for f in total_files if '~$' not in f ]
        jd_file_path_,res_text_list,res_files_list,res_exp_list,res_exp_list_p2,sr,skills_ner,res_email_list,res_mobile_list,res_exp_match_list,res_exp_score_list = [],[],[],[],[],[],[],[],[],[],[]

        ## *** JD - Text processing
        if str('jd') in jd_file.lower() and jd_file != '':
            jd_file_path_.append(os.path.join(cf.jd_File_Path,jd_file))

        if flag == 2:
            jd_file_list = jd_file
            jd_text_list = [MDS,SDS]
      
            Jd_exp = re.findall('[0-9]+',excel_exp)
            
           # print(" >>>>>>>>>>>>> ----------- JD_Exp ------------------>>>>>>>>>>>",Jd_exp)
            if len(Jd_exp)==2:
                pass
            elif len(Jd_exp)==1 and Jd_exp[0].isnumeric():
                Jd_exp = [Jd_exp[0],Jd_exp[0]]                         ## ['3','3']
       
            jd_exp_list=Jd_exp
            
            jd_file_path=jd_file_list
            #print("jd_file_path is......................",jd_file_path)
        else:
            jd_file_path = jd_file_path_[0]
            jd_file_list , jd_text_list, jd_exp_list = preprocess_JD(jd_file_path,flag)

    
        ## *** Resume - Text processing
        resumes_file_path = resume_path
        # if flag != 2:
        #     resumes_file_path.remove(jd_file_path)
        #
        if len(resumes_file_path) < 1:
            time.sleep(10)
            exit()

        temp_rp = []

        for files in resumes_file_path:
            if str('jd_') in files.lower():
                pass
            elif files.split(".")[-1] != "docx" and files.split(".")[-1] != "pdf":
                pass
            else:
                temp_rp.append(os.path.join(cf.Resumes_File_Path,files))

        # pbar = tqdm(total=len(temp_rp)+1,desc='#######-> Parsing Resumes & JD')
        # update_progress_bar()
        results = asyncio.run(process_files(temp_rp))
        for result in results:
        # for res_file_path in temp_rp:
            res_files_lst, res_text_lst, res_exp_lst, res_exp_lst_p2, sr1,ner_skill_data ,resume_email, resume_mobile = result #preprocess_Resume(res_file_path)
            ## 10-12 :  case1: 10-12 then 1.0, case2: 9-, 9.5- ,case3: 12.5- ,13-....
            ## case2: 0 to 8.4: zero, 8.5-97, 9 - 98 , 9.5 - 99
            ## Case3: 12.5- 99, 13-99.......
            
            a = 0
            b= 0
            for i in range(0,len(jd_exp_list)-1):
                a=jd_exp_list[i]
                for j in range(1,len(jd_exp_list)):
                    b=jd_exp_list[j]
            JP_exp_range=createList_Range(int(a),int(b))
            res_exp_match_lst='YES-DE'
            if res_exp_lst == 'NA':
                if res_exp_lst_p2!=['NA','NA']:
                    res_exp_lst=res_exp_lst_p2[0][0]
                    if res_exp_lst != "NA":
                        res_exp_mnth = years_and_months(float(res_exp_lst))
                        res_exp_match_lst='YES-CE'
            else:
                res_exp_mnth = years_and_months(float(res_exp_lst))
            min_years = years_and_months(float(JP_exp_range[0]))
            max_years = years_and_months(float(JP_exp_range[-1]))
            if JP_exp_range == 'NA':
                res_exp_score_lst=0
                res_exp_match_lst= 'No Exp In JD'
            elif res_exp_lst=='NA':
                res_exp_score_lst=4
                res_exp_match_lst='No Exp In Resume'
            elif res_exp_lst >=JP_exp_range[0] and res_exp_lst<= JP_exp_range[-1]:
                res_exp_score_lst=1
            elif res_exp_lst < JP_exp_range[0]:
                # if (min_years-res_exp_mnth <= 6):  # min_years=4(48),res_exp_mnth=3.6(42)
                res_exp_score_lst=2 
                # # elif (min_years-res_exp_mnth<=12 and min_years-res_exp_mnth>6):
                #     res_exp_score_lst=0.98
                # else:
                #     res_exp_match_lst='Below the range'
                #     res_exp_score_lst=0
            elif res_exp_lst > JP_exp_range[-1]:
                # if (res_exp_mnth - max_years <= 6):
                res_exp_score_lst=3
                # else:
                #     res_exp_score_lst=0.98
            else:
                res_exp_score_lst=0
                res_exp_match_lst='No EXp In Resume'

        # 5-8 year  5-8 -100%, 4,4.5-98,95; 8.5,9,-98,95;
            res_files_list.append(res_files_lst)
            res_text_list.append(res_text_lst[0])
            res_exp_list.append(res_exp_lst)
            res_exp_list_p2.append(res_exp_lst_p2)
            sr.append(sr1)
            skills_ner.append(ner_skill_data)
            res_email_list.append(resume_email)
            res_mobile_list.append(resume_mobile)
            res_exp_match_list.append(res_exp_match_lst)
            res_exp_score_list.append(res_exp_score_lst)
            #time.sleep(.1)
            #update_progress_bar()
        #pbar.close()
        return jd_file_path, jd_text_list, jd_exp_list, jd_file_list, res_files_list, res_text_list, res_exp_list, res_exp_match_list, res_exp_score_list,res_exp_list_p2,sr,skills_ner,res_email_list,res_mobile_list
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while processing Resumes and jd"

def preprocess_skills_df(skill_val):
    '''
        Author: XYZ

        Description: preprocessing the skills and extracting skills from files.

        params: skill_val(str): skill present in files

        return: skills in the files
    '''
    try:
        skill_val = re.sub(r'[^A-Za-z.+#0-9 ]', ' ', str(skill_val).strip())
        skill_ = [tok.lower() for tok in skill_val.split()]
        skill = ' '.join(skill_)
        return skill
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while preprocessing skills dataframe"

nlp = None
def add_newruler_to_pipeline(skill_pattern_path):
    '''
        Author: XYZ

        Description: Reads in all created patterns from a JSONL file and adds it to the pipeline
                    after PARSER and before NER

        params: skill_pattern_path(str/path): path for jsonl file containing skills

        return: patterns
    '''
    global nlp
    try:
        nlp = None
        nlp = nl_core_news_sm.load()
        '''Reads in all created patterns from a JSONL file and adds it to the pipeline after PARSER and before NER'''
        new_ruler = EntityRuler(nlp).from_disk(r"./Model/"+skill_pattern_path)
        nlp.add_pipe("entity_ruler",after='parser').add_patterns(new_ruler.patterns)
        return new_ruler.patterns
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while reading patterns from jsonl file"

def extract_nlp(resume_text):
    '''
        Author: XYZ

        Description: Extract required data from resume files

        params: resume_text(str): Data from files

        return: required data in the files
    '''
    try:
        # li = []
        # for i in resume_text:
        #     li.append(nlp(i))
        li = [nlp(i) for i in resume_text]
        return li
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while extracting from nlp"

def create_skill_set(doc):
    '''
        Author: XYZ

        Description: Create a set of the extracted data from resume files

        params: doc(str): extracted data

        return: set of the extracted skill data.
    '''
    '''Create a set of the extracted skill entities of a doc'''
    try:
        #print("----------------------- extracted skills from resume are-------",[ent.label_.upper()[6:] for ent in doc.ents if 'skill' in ent.label_.lower()])
        return set([ent.label_.upper()[6:] for ent in doc.ents if 'skill' in ent.label_.lower()])
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed to create set of skills"

def create_skillset_dict(resume_names, resume_texts):
    '''
        Author: XYZ

        Description: This function create a dictionary containing a set of the extracted skills.
                    Name is key, matching skillset is value

        params: resume_names(str): names of resumes to score
                resume_texts(list): list of extracted text from resume

        return: dictionary of extracted skill data.
    '''
    '''Create a dictionary containing a set of the extracted skills. Name is key, matching skillset is value'''
    try:
        skillsets = [create_skill_set(resume_text) for resume_text in resume_texts]
        return dict(zip(resume_names, skillsets))
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed to create dictionary of skills"

def match_skills(vacature_set, cv_set, resume_name):
    '''
        Author: XYZ

        Description: This function get intersection of resume skills and job offer skills
        and return match percentage

        params: vacature_set(list): list of resume skills
                cv_set(list): list of jd skills
                resume_name(str): resume file name

        return: pct_match(int/percentage): percentage of profile match
                skl_matched(list): matched skills set
    '''
    try:
        skillset_dict = cv_set
        if len(vacature_set) < 1:
            return 0, {}
        else:
            pct_match = round(len(vacature_set.intersection(cv_set[resume_name])) / len(vacature_set), 2)
            skl_matched = vacature_set.intersection(cv_set[resume_name])
            if pct_match == None:
                pct_match = 0
            if skl_matched == {}:
                skl_matched = {"None"}
            return pct_match, skl_matched
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while matching skills"

add_newruler_to_pipeline("../Model/SkillFile.jsonl")
def get_tech_skills(resumes_names_list, resume_text_list,jd_names_list, jd_text_list,flag,skill_type, skills,rs_skills):
    '''
        Author: XYZ

        Description: This function will find out mandatory skills, secondary skills from resume and jd
            and also matched skills

        params: resumes_names_list(list): list of names of all the resumes to be scored
                resume_text_list(list): list of extracted data of all the resumes that to be scored
                jd_names_list(list): list of jd file name
                jd_text_list(list) : list of text extracted from jd file
                flag(int): flag value, based of type of operation
                skill_type(str): "MAN" for mandatory skills, "SEC" for secondary skills

        return: list of resume skills, list of jd skills, list of matched skills
    '''
    # global resume_text_list_t
    # global resume_text_list_t_flag
    try:
        # resume_text_list_t = []
        # resume_text_list_t_flag = 0
        # #add_newruler_to_pipeline("skill_patternsT.jsonl")

        # add_newruler_to_pipeline("SkillFile.jsonl")
        # if resume_text_list_t_flag == 0:
        #     resume_text_list_t = extract_nlp(resume_text_list)
        #     resume_text_list_t_flag = 1

        # skillset_dict = create_skillset_dict(resumes_names_list, resume_text_list_t)

        skillset_dict = rs_skills
        if flag == 2:
            if skill_type == "MAN":
                vacature_skillset = create_skill_set(nlp(' '.join(skills)))
            else:
                vacature_skillset = create_skill_set(nlp(' '.join(skills)))
        else:
            vacature_skillset = create_skill_set(nlp(jd_text_list[0]))
        
        vacature_skillset = set([re.sub(u'\xa0','',i) for i in vacature_skillset])
        # li = []
        # for i in vacature_skillset:
        #     li.append(i.replace('\xa0',''))
        # vacature_skillset = set(li)

        match_pairs = [match_skills(vacature_skillset, skillset_dict, name) for name in skillset_dict.keys()]

        match_pairs = [i if i!= None else 0 for i in match_pairs]

        # li = []
        # for i in match_pairs:
        #     if i == None:
        #         li.append(0)
        #     else:
        #         li.append(i)
        # match_pairs = li

        return list(vacature_skillset), list(skillset_dict.keys()), list(skillset_dict.values()), match_pairs
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed to fetch tech skills"

# ### Resume Scoring based on Technical Skills and Experience
def score_adjst_tech(df_res_scoring):
    '''
        Author: XYZ

        Description: This function will score based on skills and experience

        params: df_res_scoring(dataframe-column): adding score to dataframe column

        return: rs_score(percentage): round of score i.e. percentage for each resume.
    '''
    try:
        ### 2. Weightage Experience Scoring

        #######  exp:100%, man:100%,sec:100%  ((100+100)/2*0.9)+(100*0.1))=100%
        ##secondary 5%
        ###Experiance

        weightage = [0.90,0.10,1]
        # if df_res_scoring['Mandatory_Skills_Score'] > 0.9:
        if SDS == [''] or SDS == ['None']:
            #SDS = []
            rs_score = (df_res_scoring['Mandatory_Skills_Score'] * weightage[2])
        else:
            rs_score = ((df_res_scoring['Mandatory_Skills_Score'] * weightage[0]) + (df_res_scoring['Secondary_Skills_Score'] * weightage[1]))
           
        # else:
            # rs_score = ((df_res_scoring['Mandatory_Skills_Score'] * weightage[0]) + (df_res_scoring['Exp_Score'] * weightage[1]))
        return round(rs_score*100,2)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed while scoring skills"

def _check_bold_inside_pgh(para):
    '''
        Author: XYZ

        Description: This function check for bold data inside input paragraph.

        params: para(str): paragraph

        return: boldFound(bool): True if value is bold, False if value is not bold
    '''
    try:
        boldFound = False
        for idx, run in enumerate(para.runs):
            if run.bold and idx < 6 and para.text.find(run.text) < 50 and len(run.text.strip()) > 2:
                boldFound = True
                break
        return boldFound
    except Exception as error:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "failed to find bold text"

def _header_content_split(document):
    '''
        Author: XYZ

        Description: This function will create multiple parapgraph from given file

        params: document(str): content of jd file

        return: dict of keys like mandatory skills, secondary skills and experience and
            value as extracted data from jd for each key
    '''
    try:
        Paragraph_header,Listbolds,Listbolds2,paraval = {},[],[],''
        for para in document.paragraphs:
            boldFound = _check_bold_inside_pgh(para)
            if boldFound:
                Listbolds, Listbolds1, Listbolds2 = [], [], []
                for run in para.runs:
                    word = run.text
                    if run.bold:
                        Listbolds1.append(word)
                    else:
                        Listbolds2.append(word)
                if Listbolds2:
                    paraval = ' '.join(Listbolds1)
                    Paragraph_header[paraval] = [' '.join(Listbolds2)]
                    Listbolds.append([' '.join(Listbolds2)])
                else:
                    paraval = ' '.join(Listbolds1)
                    Paragraph_header[paraval] = [paraval]
                    Listbolds.append(paraval)

            else:
                Listbolds.append(para.text) if len(para.text.strip()) > 1 else 'Value'
                if Listbolds2:
                    Listbolds2.append(para.text)
                    Paragraph_header[paraval] = [' '.join(Listbolds2)]
                else:
                    Paragraph_header[paraval] = Listbolds

        return Paragraph_header

    except Exception as error:
        print("Error in |_header_content_split|", error)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "error in header content split"

def skills_from_excel(job_description):
    try:
        Mandatory,Secondary = [],[]
        Mandatory_possibility = ['Must-Have:', 'Mandatory:', 'Must Have:', '', 'Mandatory Skills:']
        Secondary_possibility = ['Nice To Have:', 'Secondary:', 'Secondary Skills:']
        for i in job_description.values:
            i = i.lower()
            # print(i)
            for sec in Secondary_possibility:
                sec_possibility_lower = sec.lower()
                if sec_possibility_lower in i:
                    splitting_mds_sds = re.split(f"(?={sec_possibility_lower})", i)
                    Mandatory_list = splitting_mds_sds[0].replace("•", ";").replace("\xa0", "").replace("\n",
                                                                                                        "").replace(i,
                                                                                                                    "").replace("\t","")
                    Secondary_list = splitting_mds_sds[1].replace("•", ";").replace("\xa0", "").replace("\n",
                                                                                                        "").replace(i,
                                                                                                                    "").replace("\t","")
                    Mandatory_list = Mandatory_list.split(';')
                    Mandatory = [i for i in Mandatory_list if i.strip()]
                    Secondary_list = Secondary_list.split(';')
                    Secondary = [i for i in Secondary_list if i.strip()]
                    flag = 1
                elif sec_possibility_lower not in i:
                    for mand in Mandatory_possibility:
                        mand_lower = mand.lower()
                        if mand_lower in i:
                            Mandatory_list = i.replace("•", ";").replace("\xa0", "").replace("\n", "").replace(i, "").replace("\t","")
                            Mandatory_list = Mandatory_list.split(';')
                            Mandatory = [i for i in Mandatory_list if i.strip()]
            # print(Mandatory)

        return Mandatory, Secondary


    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "something is wrong with jd file"

def check_standardformat(jd_path):
    '''
        Author: XYZ

        Description: This function checks if jd file is in required format or not and will give
            appropriate output of extracted fields.

        params: mypath(path/str): path of jd file

        return: status(bool), list of mandatory skills, list of secondary skills and list of experience
    '''
    try:
        if jd_path.endswith('.docx'):
            requiredheadings=['MandatorySkills','SecondarySkills','Experience']
            #total_files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
            
            #jd_file_path_=[]
            jd_file_path_ = jd_path
            #for files in total_files:
            #    if str('jd') in files.lower():
            #        jd_file_path_.append(files)
            document = Document(jd_file_path_)
            """ Split the Header and Paragraph """
            Paragraph_header = _header_content_split(document)
            updatedresults={}
            for key in list(Paragraph_header.keys()):
                value=Paragraph_header[key]
                key=key.replace(":","").replace("\xa0","").replace(" ","")
                updatedresults[key]=value
            if set(requiredheadings).issubset(set(updatedresults)):
                return True,updatedresults['MandatorySkills'],updatedresults['SecondarySkills'],updatedresults['Experience']
            else:
                return False,[],[],[]
        elif jd_path.endswith('.xlsx'):
            excel_jd_file = pd.read_excel(jd_path, index_col=0, engine='openpyxl')
            try:
                job_description = excel_jd_file.loc["Job Description"]
                year_of_experience = excel_jd_file.loc["Years of Experience (Relevant)"]
            except:
                return 400
            Experience = []
            # yr = 'Years'.lower()
            Mandatory, Secondary = skills_from_excel(job_description)
            # print(year_of_experience.values)
            yr = year_of_experience.values
            if pd.isna(yr):
                #print("If Yr")
                Experience.append('0-1')
            else:
                #print("Else Yr")
                for years in year_of_experience.values:
                    # print(years)
                    if not isinstance(years, int):
                        years = years.lower()
                        exp = years.replace('\xa0', '').replace(' ', '').replace('years', '').replace('year','')
                    else:
                        exp = years
                    # print(exp)
                    Experience.append(exp)
                # print("check_standa...Mand", Mandatory)
                # print("check_standa...Sec", Secondary)
                # print("check_standa...Exp", Experience)
            if Mandatory and Secondary and Experience == []:
                return False, [], [], []
            else:
                return True, Mandatory, Secondary, Experience
                
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        return "Required Data is missing in Jd file."

# def update_progress_bar(val=1):
#     '''
#         Author: XYZ

#         Description: This function will show progress of scoring in terminal.

#         params: val=1(default 1): updates progress once each step completed successfully.

#         return: progress_bar
#     '''
#     global pbar
#     pbar.update(val)

JD_TEXT = ''
FLAG = 0
#pbar = ''
def main(resume_folder, job_folder, jd_input, experience, mandatory_skills, secondary_skills):
    '''
        Author: XYZ

        Description: This function call necessary functions and will score each resume one by one.
                input to this function comes from API and will provide appropriate response back.

        params: resume_folder(str): name of folder where all resumes stored that to be scored
                job_folder(str): in case of operation with 'file' name folder where jd file
                    is present. In case of 'tool' it's passed as 'None'.
                jd_input(str): mode of operation to be done either 'file' or 'tool'
                experience(str): range of experience. In case of 'file' taken from jd file, in case of
                    'tool' input from user e.g.: 3-4 years
                mandatory_skills(str): in case of 'tool', one or more skills that user finds mandatory.
                    in case of 'file' it will extracted from jd file.
                secondary_skills(str): in case of 'tool',one or more skills that user finds secondary
                    in scoring. in case of 'file' it will extracted from jd file.

        return: df_Resume_scores(pandas dataframe): dataframe holding multiple columns like profile name,
            email, phone number, matched skills, skills score, resume score, experience etc.
    '''
    # global JD_TEXT
    # global FLAG
    # global MDS
    global SDS
    # global excel_exp
    # global jd_file_exper
    #global pbar
    # global FOLDER_NAME
    # global mypath
    JOB_INPUT = job_folder
    JDID = jd_input
    excel_exp = experience
    MDS = mandatory_skills
    SDS = secondary_skills
    try:
        
        mypath = resume_folder
        if JOB_INPUT == "file":
            #print("===> JD Template")
            JDID = JDID.split("\\")[-1]
            MDS = MDS.split(',')
            SDS = SDS.split(',')
            MDS_updated, SDS_updated = [], []
            for md in MDS: MDS_updated.append(md.replace("-", ' '))
            for sd in SDS: SDS_updated.append(sd.replace("-", ' '))
            MDS, SDS = MDS_updated, SDS_updated
            FLAG = 2
            jd_file_path, jd_Text_List, jd_Exp_List, jd_file_list, res_Files_List, res_Text_List,\
            res_Exp_List, res_Exp_Match_List, res_Exp_Score_List,res_Exp_List_p2,sr,skills_ner,res_email_list,\
            res_mobile_list = process_text(
                    mypath, jd_input, FLAG, MDS, SDS, excel_exp)
        elif JDID !="" and JOB_INPUT != "tool":
            #From Ceipal
  
            JD_TEXT = start(JDID)
            FLAG = 1
            jd_file_path, jd_Text_List, jd_Exp_List, jd_file_list, res_Files_List, res_Text_List, res_Exp_List,\
            res_Exp_Match_List, res_Exp_Score_List,res_Exp_List_p2,sr,skills_ner,res_email_list,res_mobile_list = process_text(
                mypath, jd_input, FLAG, MDS, SDS, excel_exp)
        else:
            #From Tool
            MDS=MDS.split(',')
            SDS=SDS.split(',')
            MDS_updated,SDS_updated=[],[]
            for md in MDS : MDS_updated.append(md.replace("-",' '))
            for sd in SDS : SDS_updated.append(sd.replace("-",' '))
            MDS,SDS=MDS_updated,SDS_updated
            FLAG = 2
            jd_file_path, jd_Text_List, jd_Exp_List, jd_file_list, res_Files_List, res_Text_List, res_Exp_List,\
            res_Exp_Match_List, res_Exp_Score_List,res_Exp_List_p2,sr,skills_ner,res_email_list,res_mobile_list = process_text(
                mypath, jd_input, FLAG, MDS, SDS, excel_exp)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        time.sleep(10)

    run_Azure_conn.write_json(f"Extracting Mandatory & Secondary Skills and Experience", 50, os.path.basename(""))
    time.sleep(2)
    total_len = len(res_Files_List)+1
    #pbar = tqdm(total=total_len,desc='#######-> Extracting Mandatory & Secondary Skills and Experience')
    
    # if total_len%2 != 0:
    #     upd_pbar = int(total_len/2)
    # else:
    #     upd_pbar = int(total_len/2)
    jd_M_tech_skills_updt_list_, res_fileName_M_tech_list_, res_M_tech_skills_list_,\
    res_Mandatory_Skills_Score_list_ = get_tech_skills(
        res_Files_List, res_Text_List, jd_file_list, jd_Text_List, FLAG, "MAN", MDS,dict(zip(res_Files_List, skills_ner)))
    
    jd_sec_tech_skills_updt_list_, res_fileName_sec_tech_list_, res_sec_tech_skills_list_,\
    res_sec_tech_score_list_ = get_tech_skills(
        res_Files_List, res_Text_List, jd_file_list, jd_Text_List, FLAG, "SEC", SDS,dict(zip(res_Files_List, skills_ner)))
    #update_progress_bar(total_len)
    #pbar.close()
    ## *** Club Resume details File-wise
    resumes_scores = zip(res_fileName_M_tech_list_, res_Exp_List, res_Exp_Match_List,
            res_Exp_Score_List,res_Exp_List_p2,sr,res_email_list,res_mobile_list)

    ## *** DataFrame - 0 - Skills - JD Technical & Functional Skills
    run_Azure_conn.write_json(f"Sorting the resumes", 75, os.path.basename(""))
    time.sleep(2)
    #pbar = tqdm(total=total_len-1,desc='#######-> Sorting Resumes')
    skills_df = pd.DataFrame()
    skills_df['Res_Filename'] = res_fileName_M_tech_list_

    skills_df['JD_M_Tech_Skills'] = ', '.join(skill for skill in jd_M_tech_skills_updt_list_)
    skills_df['JD_Sec_Tech_Skills'] = ', '.join(skill for skill in jd_sec_tech_skills_updt_list_)

    skills_df['JD_M_Tech_Skills'].replace('', 'NA', inplace=True)
    skills_df['JD_Sec_Tech_Skills'].replace('', 'NA', inplace=True)


    ## ***  1. Dataframe 1 - Parameter Resume Mandatory Technical Skills
    M_tech_df = pd.DataFrame()
    M_tech_df['Res_Filename'] = res_fileName_M_tech_list_

    # li = []
    # for i in res_M_tech_skills_list_:
    #     li.append(','.join(i))
    li = [','.join(i) for i in res_M_tech_skills_list_]
    res_M_tech_skills_list_ = li

    M_tech_df['Resume_M_Tech_Skills'] = res_M_tech_skills_list_
    M_tech_df['Resume_M_Tech_Skills'] = M_tech_df['Resume_M_Tech_Skills'].apply(
        lambda x: np.nan if len(x) == 0 else x)
    M_tech_df['Matched_Mandatory_Skills'] = ''
    M_tech_df['Mandatory_Skills_Score'] = ''
    for i in M_tech_df.index:
        M_tech_df['Matched_Mandatory_Skills'][i] = ",".join(res_Mandatory_Skills_Score_list_[i][1])
        if M_tech_df['Matched_Mandatory_Skills'][i] == '':
            M_tech_df['Matched_Mandatory_Skills'][i] = 'NA'
        M_tech_df['Mandatory_Skills_Score'][i] = res_Mandatory_Skills_Score_list_[i][0]


    ## ***  2. Dataframe 2 - Parameter Resume Secondary Technical Skills
    Sec_tech_df = pd.DataFrame()
    Sec_tech_df['Res_Filename'] = res_fileName_sec_tech_list_

    # li = []
    # for i in res_sec_tech_skills_list_:
    #     li.append(','.join(i))
    li = [','.join(i) for i in res_sec_tech_skills_list_]
    res_sec_tech_skills_list_ = li

    Sec_tech_df['Resume_Sec_Tech_Skills'] = res_sec_tech_skills_list_
    Sec_tech_df['Resume_Sec_Tech_Skills'] = Sec_tech_df['Resume_Sec_Tech_Skills'].apply(
        lambda x: np.nan if len(x) == 0 else x)
    Sec_tech_df['Matched_Sec_Tech_Skills'] = ''
    Sec_tech_df['Secondary_Skills_Score'] = ''
    for i in Sec_tech_df.index:
        Sec_tech_df['Matched_Sec_Tech_Skills'][i] = ",".join(res_sec_tech_score_list_[i][1])
        if Sec_tech_df['Matched_Sec_Tech_Skills'][i] == '':
            Sec_tech_df['Matched_Sec_Tech_Skills'][i] = 'NA'
        Sec_tech_df['Secondary_Skills_Score'][i] = res_sec_tech_score_list_[i][0]
    
    ## ***  4. Dataframe 4 - Parameter Experience
    exp_df = pd.DataFrame(data=resumes_scores, columns=['Res_Filename', 'Exp_Years', 'Exp_Match', 'Exp_Score','Total_and_Gaps','Skills_Recency','Email','Mobile'])
    for exdf in exp_df.index:
        if exp_df['Skills_Recency'][exdf] == ['NA', 'NA']:
            exp_df['Skills_Recency'][exdf] = {"Low_Skill_Recency":{"NA"},"Medium_Skill_Recency":{"NA"},"High_Skill_Recency":{"NA"}}
    
    exp_df[['Total_Exp_With_Years','Total_Gaps_With_Years']] = pd.DataFrame(exp_df.Total_and_Gaps.tolist(), index= exp_df.index)
    
    df_Resume_scores = pd.DataFrame()
  
    df_Resume_scores = skills_df.merge((M_tech_df.merge(Sec_tech_df, on='Res_Filename', how='outer')).merge(exp_df, on='Res_Filename',how='outer'),
                                       on='Res_Filename', how='outer')
    df_Resume_scores.rename(columns={'Res_Filename': 'Candidate'}, inplace=True)

    df_Resume_scores['Resume_M_Tech_Skills'].fillna(value='NA', inplace=True)
    df_Resume_scores['Resume_Sec_Tech_Skills'].fillna(value='NA', inplace=True)

    df_Resume_scores['Mandatory_Skills_Score'].fillna(value=0.0, inplace=True)
    df_Resume_scores['Secondary_Skills_Score'].fillna(value=0.0, inplace=True)
    # it_value = mypath.split("\\")[-2]

    ## *** Compute Overall Resume Score based on Parameters ==> Tech (100%) / Exp Scores (=0.1)
    df_Resume_scores['Resume_Score'] = df_Resume_scores.apply(score_adjst_tech, axis=1)
    df_Resume_scores['Resume_skills'] = df_Resume_scores[['Resume_M_Tech_Skills']].apply(lambda x: ', '.join(x[x != 'NA']), axis = 1)
    df_Resume_scores['Resume_Sec_Tech_Skills']=df_Resume_scores[['Resume_Sec_Tech_Skills']].apply(lambda x: ', '.join(x[x != 'NA']), axis = 1)
    df_Resume_scores['JD_Secondary_skills'] = df_Resume_scores[['JD_Sec_Tech_Skills']].apply(lambda x: ', '.join(x[x != 'NA']), axis = 1)
    df_Resume_scores['Matched_Secondary_skills'] = df_Resume_scores[['Matched_Sec_Tech_Skills']].apply(lambda x: ', '.join(x[x != 'NA']), axis = 1)
    df_Resume_scores['JD_Mandatory_skills'] = df_Resume_scores[['JD_M_Tech_Skills']].apply(lambda x: ', '.join(x[x != 'NA']), axis = 1)
   
    df_Resume_scores['Resume_Score'].fillna(value=0, inplace=True)
    try:
        if JDID == "None":
            df_Resume_scores.insert(1, 'JD_ID', jd_file_list.split('.')[0])
        else:
            df_Resume_scores.insert(1, 'JD_ID', JDID)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        time.sleep(10)

    df_Resume_scores['Resume_Score'].fillna(value=0, inplace=True)

    df_Resume_scores['JD_Rel_Res_Skills'] = ''
    for i in df_Resume_scores.index:
        df_Resume_scores['JD_Rel_Res_Skills'][i] = get_relevant_skills(df_Resume_scores['JD_Mandatory_skills'][i],
                                                                       df_Resume_scores['Resume_skills'][i],
                                                                       df_Resume_scores['Matched_Mandatory_Skills'][i]
                                                                       )
    for i in df_Resume_scores.index:
        df_Resume_scores['JD_Rel_Res_Skills'][i] = ",".join(df_Resume_scores['JD_Rel_Res_Skills'][i])
        if df_Resume_scores['JD_Rel_Res_Skills'][i] == '':
            df_Resume_scores['JD_Rel_Res_Skills'][i] = 'NA'
        df_Resume_scores['JD_Rel_Res_Skills'][i] = df_Resume_scores['JD_Rel_Res_Skills'][i].replace("rest","rest- API")
    
    df_Resume_scores = df_Resume_scores[
        ['Candidate', 'Email','Mobile','JD_ID', 'JD_Mandatory_skills', 'Resume_skills', 'Matched_Mandatory_Skills', 'Mandatory_Skills_Score', 'JD_Secondary_skills','Matched_Secondary_skills'
        ,'Secondary_Skills_Score', 'Exp_Years', 'Exp_Match', 'Exp_Score', 'Resume_Score','Total_Exp_With_Years','Total_Gaps_With_Years','Skills_Recency','JD_Rel_Res_Skills']]
    
    df_Resume_scores.sort_values(by=['Exp_Score'], ascending=True,inplace =True)  
    df_Resume_scores = df_Resume_scores.groupby('Exp_Score').apply(lambda g: g.sort_values('Resume_Score', ascending=False))
    # print("..........................columns are.................",df_Resume_scores.columns)
    
    df_Resume_scores.reset_index(drop=True, inplace=True)
    df_Resume_scores = df_Resume_scores.drop('Skills_Recency', axis=1).join(pd.DataFrame(df_Resume_scores.Skills_Recency.values.tolist()))

    mask = df_Resume_scores['Matched_Secondary_skills'].str.len() == 0
    df_Resume_scores['Matched_Secondary_skills'] = df_Resume_scores['Matched_Secondary_skills'].mask(mask, df_Resume_scores['Matched_Secondary_skills'].str.replace('', 'NA'))

    df_Resume_scores['Temp1'] = df_Resume_scores['Matched_Mandatory_Skills'].str.split(',') + df_Resume_scores['Matched_Secondary_skills'].str.split(',')
    #df_Resume_scores['Temp2'] = df_Resume_scores['Matched_Mandatory_Skills'].str.split(',') + df_Resume_scores['Matched_Secondary_skills'].str.split(',')
    
    for skill_rec in ['Low_Skill_Recency','Medium_Skill_Recency','High_Skill_Recency']:
        df_Resume_scores[skill_rec] = [set(x[0]) & x[1] for x in zip(df_Resume_scores['Temp1'], df_Resume_scores[skill_rec])]

    df_Resume_scores = df_Resume_scores.drop('Temp1', axis=1)

    for skill_rec in ['Low_Skill_Recency','Medium_Skill_Recency','High_Skill_Recency']:
        df_Resume_scores[skill_rec] = [','.join(map(str, l)) for l in df_Resume_scores[skill_rec]]
    for skill_rec in ['Low_Skill_Recency','Medium_Skill_Recency','High_Skill_Recency']:
        mask = df_Resume_scores[skill_rec].str.len() == 0
        df_Resume_scores[skill_rec] = df_Resume_scores[skill_rec].mask(mask, df_Resume_scores[skill_rec].str.replace('', 'NA'))
    df_Resume_scores['Resume_Score'] = [str(row) + '%' for row in df_Resume_scores['Resume_Score']]
    df_Resume_scores = df_Resume_scores.assign(Sl_No=[1 + i for i in range(len(df_Resume_scores))])[
        ['Sl_No'] + df_Resume_scores.columns.tolist()]
    df_rs_cols = df_Resume_scores.columns
    
    df_Resume_scores['score_'] = df_Resume_scores['Resume_Score'].apply(lambda x: str(x).replace('%', '')).astype('float')
    df_Resume_scores_ = df_Resume_scores.style.apply(
        lambda x: ['background-color: lime'] * df_Resume_scores.shape[1] if (x['Need_Exp_Review'] == "YES") else [''] *
                                                                                                                 df_Resume_scores.shape[
                                                                                                                     1],
        axis=1)
    df_Resume_scores_ = df_Resume_scores.style.apply(
        lambda x: ['background-color: lime'] * df_Resume_scores.shape[1] if (x['score_'] >= 75.0) else [''] *
                                                                                                       df_Resume_scores.shape[
                                                                                                           1], axis=1)
    #update_progress_bar(total_len-1)
    #pbar.close()
    
    print("\n#######-> Generating resultant file.")
    ### Write Output to Excel file
    datetime_ = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    jd_file_name = os.path.basename(jd_file_path)
    jd_file_name = os.path.splitext(jd_file_name)[0]
    try:
        if JDID == "None":
            output_file_name = jd_file_list.split('.')[0]
        else:
            output_file_name = JDID
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for i in tb_str: print(i)
        time.sleep(10)

    # df_Resume_scores_.to_excel('{}_{}.xlsx'.format(output_file_name, datetime_),
    #                            index=False, columns=df_rs_cols)
    
    end_time = time.time()
    total_time = end_time - start_time
            
    return df_Resume_scores

def change_filename(filename, job_id):
    splitted_file_name = filename.split('.')
    new_filename = ".".join(splitted_file_name[:-1])+ "_" + str(job_id)+ "." +splitted_file_name[-1]
    return new_filename


def extract_candidate_name(candidate_name):
    conditions = [("naukri", "Naukri"),
                  ("linkedin", "Linkedin"),
                  ("mt", "MT"),
                  ("mouritech", "Mouritech"),
                  ("resume", "Resume")]
    name = candidate_name
    for condition in conditions:
        if condition[0] in name.lower():
            name = name.replace(condition[1], "").replace(condition[0], "")
    name = name.replace('_', '').replace(' ', '')
    name_parts = re.findall('[A-Z][a-z\s]*', name)
    name = ' '.join(name_parts)
    return name.split('[')[0] if '[' in name else name

def get_skill_process(req_data):
    start = time.time()
    today = datetime.datetime.now()
    start_time = today.strftime("%m-%d-%Y %I:%M:%S %p")
    job_folder = 'file'
    jd_input = ''
    resume_folder = req_data["resume_folder"]
 
    enc_files = req_data['resfile']
    enc_file_names = resume_folder
 
    files = []
    org_input_file = []
    for i in range(0, len(enc_file_names)):
        # dec_file = decrypt(enc_files[i], cf.SECRET_KEY)
        # print(dec_file)
        # dec_file_data = base64.b64decode((dec_file.split('base64,')[-1]))
        dec_file_data = base64.b64decode((enc_files[i].split('base64,')[-1]))
        if enc_file_names[i].startswith('~$'):
            pass
        else:
            org_input_file.append(enc_file_names[i])
            file = open(os.path.join(cf.Resumes_File_Path, enc_file_names[i]), 'wb')
            file.write(dec_file_data)
            file.close()
            files.append(file)
    mandatory_skills = ''
    secondary_skills = ''
    experience = ''
    resp, entry_time, exit_time = process_file(org_input_file, job_folder, jd_input, experience, mandatory_skills,
                                               secondary_skills)
    module_run_time = exit_time - entry_time
    overall_end_time = time.time() - start
    if not resp.empty:
        resp['Total_exp_cal'] = ''
        resp['Total_Exp_With_Years_lst'] = ''
        for i in range(len(resp)):
 
            if type(resp['Total_Exp_With_Years'][i]) == "NA":
                resp['Total_exp_cal'][i] = "NA"
 
            elif type(resp['Total_Exp_With_Years'][i]) == list:
                resp['Total_exp_cal'][i] = resp['Total_Exp_With_Years'][i][0]
 
            else:
                print("........................entered into else condition")
                resp['Total_exp_cal'][i] = 'NA'
               
        resp['Candidate'] = resp['Candidate'].apply(extract_candidate_name)
        resp['name'] = resp['Candidate']
 
        output_obj = {
            'overall_run_time': overall_end_time,
            'result': resp.to_dict(orient='records')
        }
        filtered_results = []
        for result in output_obj["result"]:
            filtered_result = {
                "Candidate": result["Candidate"],
                "Email": result["Email"],
                "Exp_Years": result["Exp_Years"],
                "Mobile": result["Mobile"],
                "Total_exp_cal": result["Total_exp_cal"],
                "Resume_skills": result["Resume_skills"]
            }
            filtered_results.append(filtered_result)
        resultant = {
            'overall_run_time': overall_end_time,
            'result': filtered_results
        }
        return resultant


def bg_process(req_data):
    try:
        start = time.time()
        today = datetime.datetime.now()
        start_time = today.strftime("%m-%d-%Y %I:%M:%S %p")
        job_folder = 'file'
        jd_input = ''
        resume_folder = req_data["resume_folder"]
 
        enc_files = req_data['resfile']
        enc_file_names = resume_folder
 
        files = []
        org_input_file = []
        dec_file_data = None  # Initialize dec_file_data outside the loop
        for i in range(0, len(enc_file_names)):
            dec_file_data = base64.b64decode((enc_files[i].split('base64,')[-1]))
            if enc_file_names[i].startswith('~$'):
                pass
            else:
                org_input_file.append(enc_file_names[i])
                file = open(os.path.join(cf.Resumes_File_Path, enc_file_names[i]), 'wb')
                file.write(dec_file_data)
                file.close()
                files.append(file)
 
        mandatory_skills = ','.join(req_data['mandatory_skills'])  
        secondary_skills = ','.join(req_data['secondary_skills'])  
        experience = req_data['experience']
        job_input = req_data.get('job_input', '')
        jd_input = req_data.get('jd_input', '')  
 
        resp, entry_time, exit_time = process_file(org_input_file, job_folder, jd_input, experience, mandatory_skills, secondary_skills)
        module_run_time = exit_time - entry_time
        overall_end_time = time.time() - start
 
        if not resp.empty:
            resp['Total_exp_cal'] = ''
            resp['Total_Exp_With_Years_lst'] = ''
            for i in range(len(resp)):
                if type(resp['Total_Exp_With_Years'][i]) == "NA":  
                    resp['Total_exp_cal'][i] = "NA"
                elif type(resp['Total_Exp_With_Years'][i]) == list:
                    resp['Total_exp_cal'][i] = resp['Total_Exp_With_Years'][i][0]
                else:
                    print("........................entered into else condition")
                    resp['Total_exp_cal'][i] = 'NA'
 
            # Calculate Low_Skill_Recency
            jd_mandatory_skills = resp['JD_Mandatory_skills'].str.split(',').fillna('')
            jd_secondary_skills = resp['JD_Secondary_skills'].str.split(',').fillna('')
            combined_skills = jd_mandatory_skills + jd_secondary_skills
            low_skill_recency = combined_skills.apply(lambda x: ','.join(x)).str.upper()
            resp['Low_Skill_Recency'] = low_skill_recency
 
            if resp['JD_Mandatory_skills'][0] == '':
                jd_man_skill_count = 0
            else:
                jd_man_skill_count = len(resp['JD_Mandatory_skills'][0].split(','))
            if resp['JD_Secondary_skills'][0] == '':
                jd_sec_skill_count = 0
            else:
                jd_sec_skill_count = len(resp['JD_Secondary_skills'][0].split(','))
            resp['mandatory_skill_score'] = resp['Mandatory_Skills_Score'].apply(
                lambda x: str(int(round(x * jd_man_skill_count, 0))) + "/" + str(jd_man_skill_count))
            resp['secondary_skill_score'] = resp['Secondary_Skills_Score'].apply(
                lambda x: str(int(round(x * jd_sec_skill_count, 0))) + "/" + str(jd_sec_skill_count))
            resp['JD_Rel_Res_Skills'] = resp['JD_Rel_Res_Skills'].str.upper()
 
            resp['Candidate'] = resp['Candidate'].apply(extract_candidate_name)
            resp['name'] = resp['Candidate']
 
            resp['exp_details'] = ""
 
            output_obj = {
                'overall_run_time': overall_end_time,
                'result': resp.to_dict(orient='records')
            }
 
            return output_obj
 
    except Exception as e:
        return jsonify({
            "Status": "Something went wrong while processing the request",
            "Error": str(e),
            "Error_code": 1
        })

def process_file(org_file_list, job_folder, jd_input, experience, mandatory_skills, secondary_skills):
    start_time = time.time()
    try:
        resp = main(org_file_list, job_folder, jd_input, experience, mandatory_skills, secondary_skills)
        run_Azure_conn.write_json("Completed", 100, os.path.basename(""))
        return resp, start_time, time.time()
    except Exception as e:
        print(traceback.format_exc())
        run_Azure_conn.write_json(f"Error {traceback.format_exc()}" ,25, os.path.basename(""), "w", 1)
        return None, start_time, time.time()


def convert_list(string_skills):
    list_skill =list(re.split(',', string_skills))
    return list_skill

def skill_validation(skills):
    add_newruler_to_pipeline("../Model/SkillFile.jsonl")
    mds_extracted = convert_list(skills)
    #print("mds_extracted are.........................................",mds_extracted)
    skill_set = extract_nlp(mds_extracted)
    skill_set_mds = create_skillset_list(skill_set)
    return skill_set_mds


def create_skillset_list(texts):
    dct ={}
    # result = []
    for text in texts:
        for ent in text.ents:
            if "skill" in ent.label_.lower():
                dct[ent.label_.upper()[6:]] = ent
                
    # for i in dct.values():
    #     result.append(str(i))
    result = [str(i) for i in dct.values()]
    return result