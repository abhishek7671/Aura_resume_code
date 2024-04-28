from docx import *
import os, sys
import traceback


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
        return str(error)

def _header_content_split(document):
    '''
        Author: XYZ

        Description: This function will create multiple parapgraph from given file

        params: document(str): content of jd file

        return: dict of keys like mandatory skills, secondary skills and experience and
            value as extracted data from jd for each key
    '''
    try:
        Paragraph_header = {}
        Listbolds = []
        Listbolds2 = []
        paraval = ''
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
        return str(error)


def check_standardformat(jd_path):
    '''
        Author: XYZ

        Description: This function checks if jd file is in required format or not and will give
            appropriate output of extracted fields.

        params: mypath(path/str): path of jd file

        return: status(bool), list of mandatory skills, list of secondary skills and list of experience
    '''
    requiredheadings=['MandatorySkills','SecondarySkills','Experience']
    # total_files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    jd_file_path_=[]
    # for files in total_files:
        # if str('jd') in files.lower():
    jd_file_path_.append(jd_path)
    document = Document(jd_file_path_[0])
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

