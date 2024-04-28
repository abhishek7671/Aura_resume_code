import re
from nltk.tokenize import sent_tokenize
#from doc_to_text import file_reader
import time
import unicodedata


def string_to_number(text):
    '''
        Author: XYZ

        Description: This function will convert numbers in text format i.e. zero-nineteen
            to digits i.e. 0-19

        params: text(str) extracted possible text part that might be experience

        return: converted text to numbers
    '''
    #     print(text)
    dct={'zero':'0','one':'1','two':'2','three':'3','four':'4',
     'five':'5','six':'6','seven':'7','eight':'8','nine':'9',
        'ten':'10','eleven':'11','twelve':'12','thirteen':'13',
         'fourteen':'14','fifteen':'15','sixteen':'16',
         'seventeen':'17','eighteen':'18','nineteen':'19'}

    text_lists = str(text).lower().split()
    for item in text_lists:
        if item in dct.keys():
            dct_value = dct[item]
            text = text.replace(item,dct_value) 
    return text
# Getting Exp from resumes using keyword year and yrs
# Limitations: Ex: 0-5 years in JD matches with Zero and above experience
def get_experience(text): 

    '''
        Author: XYZ

        Description: This function will extract experience of candidate from resume

        params: text(list) list of extracted content of resume

        return: range of years of experience
    '''
    #print(">>>>>>>>>>>>>>>>>>>>>>> entered into grt_experience function >>>>>>>>>>>>>>>>>>>>>>")
    #print("text is...........",text)

    
    def is_pua(c):
        return unicodedata.category(c) == 'Co'

    #content = "This\uf0b7 is a \uf0a7string \uf0c7with private \uf0b7use are\uf0a7as blocks\uf0d7."
    text = "".join(text).encode().decode('unicode_escape') 
    text = "".join([char for char in text if not is_pua(char)])

    #print(".......................... text is...........",text)
    text = text.replace("\\uf0b7",'').replace("plus","+") 
    text = sent_tokenize(text) #['10-12year']
    text = sum([re.split('[\t\n]',i) for i in text],[])
    text = [i.split('and') for i in text]
    
    try:
        text =sum(text,[])
    except Exception:
        pass  

    #print("..........................text issssssssss...........",text)

################# ............. updated code ............. #####################
#    import unicodedata

#    def is_pua(c):
#        return unicodedata.category(c) == 'Co'

    #content = "This\uf0b7 is a \uf0a7string \uf0c7with private \uf0b7use are\uf0a7as blocks\uf0d7." 

#    text = "".join([char for char in text[0] if not is_pua(char)])
    #text = [text]
    #print("..........................text is...........",text)
################# ............. updated code ............. #####################
    match_string = "year"
    match_string2 = "yr"
    match_string_mn = "months"
    matched_sent = [" ".join(i.lower().split()) for i in text if match_string in i.lower() or match_string2 in i.lower()]
 

    #print("<======><------>"*12)
    #print("................. matched_sent while converting into lower case is. ......................",matched_sent)
    #cls
    #print("<======><------>"*12)
    matched_sent = [string_to_number(i) for i in matched_sent]
    #print("................. matched_sent is ......................",matched_sent)
    expr_match = [re.findall(r"\d+\s*"+"to"+"\s*"+"\d+\s*"+"year|\d+\s*"+"-"+"\s*"+"\d+\s*"+"year|\d+\s*"+"."+"\s*"+"\d+\s*"+"year|\d+\s*"+"to"+"\s*"+"\d+\s*"+"yr|\d+\s*"+"-"+"\s*"+"\d+\s*"+"yr|\d+\s*"+"."+"\s*"+"\d+\s*"+"yr|\d+\s*"+"year|\d+\s*"+"-"+"\s*"+"years|\d+\s*.\s*\d+\s*\W\s*year|\d+\s*\W\s*years|\d+\s*\W\s*year|\d+\s*"+"yr|\d+\s*"+"-"+"\s*"+"yr|\d+\s*.\s*\d+\s*\W\s*yr|\d+\s*\W\s*yr|\d+.\d\s*to\s*\d+.\d+\s*"+"years|\d+.\d\s*to\s*\d+.\d+\s*"+"yrs|\d+.\d\s*-\s*\d+.\d+\s*"+"years|\d+.\d\s*-\s*\d+.\d+\s*"+"yrs|\d+.\d\s*to\s*\d+.\d+\s*"+"years|\d+.\d\s*to\s*\d+.\d+\s*"+"yrs|\d+.\d+\s*-\s*\d+\s*"+"years|\d+\s*-\s*\d+.\d+\s*"+"years|\d+.\d+\s*-\s*\d+\s*"+"yrs|\d+\s*-\s*\d+.\d+\s*"+"yrs|\d+.\d+\s*to\s*\d+\s*"+"yrs|\d+\s*to\s*\d+.\d+\s*"+"yrs|\d+.\d+\s*to\s*\d+\s*"+"years|\d+\s*to\s*\d+.\d+\s*"+"years",i)for i in matched_sent]
    #print(".........................................................................................")
    #print(".....................expr_match is....................",expr_match)

    expr_match = sum(expr_match, [])
    #print(".....................expr_match second call is....................",expr_match)
    # value_append = []
    # for i in expr_match:
    #     value_append.append(i.split()[0].strip("+"))
    value_append = [i.split()[0].strip("+") for i in expr_match]

    ##### ----------------  Add Logic to extract over all months also ---------------- #####
    matched_sent_mn = [" ".join(i.lower().split()) for i in text if match_string_mn in i.lower()]
    #print("................. matched_sent while converting into lower case is. ......................",matched_sent_mn)
    matched_sent_mn = [string_to_number(i) for i in matched_sent_mn]
    #print("................. matched_sent is ......................",matched_sent_mn)
    exp_match_mnth = [re.findall(r"\d+\s*"+"to"+"\s*"+"\d+\s*"+"months|\d+\s*"+"-"+"\s*"+"\d+\s*"+"months|\d+\s*"+"."+"\s*"+"\d+\s*"+"months|\d+\s*.\s*\d+\s*\W\s*months|\d+\s*\W\s*months|\d+\s*\W\s*months",i)for i in matched_sent_mn]

    #print(".....................expr_match is....................",exp_match_mnth)
    exp_match_mnth = sum(exp_match_mnth, [])
    # value_append_mn = []
    # for i in exp_match_mnth:
    #     value_append_mn.append(i.split()[0].strip("+"))
    value_append_mn = [i.split()[0].strip("+") for i in exp_match_mnth]
    
    if value_append_mn == []:
        value_append_mn = "NA"
    else:
        pass

    #print("......... value_append_mn issssssssss......",value_append_mn)

    float_values = []
    for i in value_append:
        try:
            if "-" in i and len(i)>4:
                float_values.append(float(i.lower().split("-")[0]))
            elif "yr" in i and "-" in i:
                # print("*************",i)
                float_values.append(float(i.lower().split("-")[0]))
            elif "yr" in i and "to" in i:
                float_values.append(float(i.lower().split("to")[0]))
            elif "year" in i and "-" in i:
                float_values.append(float(i.lower().split("-")[0]))
            elif "year" in i and "to" in i:
                float_values.append(float(i.lower().split("to")[0]))
            elif "year" in i and len(i)>4:
                if "year" in i and "+" in i:
                    #print(" *************** i is.........",i)
                    float_values.append(float(i.lower().split("+")[0]))
                else:
                    float_values.append(float(i.lower().split("year")[0]))
            elif "yr" in i and "+" in i:
                float_values.append(float(i.lower().split("+")[0]))
            elif "yr" in i:
                float_values.append(float(i.lower().split("yr")[0]))
            elif "to" in i:
                float_values.append(float(i.lower().split("to")[0])) 
            elif "+" in i:
                float_values.append(float(i.lower().split("+")[0]))
            elif "-" in i:
                float_values.append(float(i.lower().split("-")[0]))
            else:
                float_values.append(float(i))
        except:
            float_values = [0]
    float_values.sort(reverse = True)
    total_exprns = "NA"
    
    for exp_val in float_values:
        if exp_val < 30.0:
            total_exprns = exp_val
            break   
    #print(".......... total_exp isssssssss.........",total_exprns) 
    if total_exprns != "NA"and value_append_mn != "NA":
        #print("*****************************************")
        final_exp = round(float(str(total_exprns))+float(value_append_mn[0])/12,1)
        #print("total experience under if cond issssssss...........********* ......",final_exp)
    elif total_exprns == "NA" and value_append_mn != "NA":
        final_exp = round(float(int(value_append_mn[0])/12),2)
        #print("total experience under elif cond issssssss...........********* ......",final_exp)
    elif total_exprns != "NA"and value_append_mn == "NA" :
        final_exp = total_exprns
        #print("total experience under elif-elif cond issssssss...........********* ......",final_exp)
    else:
        final_exp = "NA"

   # print("total experience issssssss...........********* ......",str(total_exprns)+value_append_mn[0])
    return final_exp
