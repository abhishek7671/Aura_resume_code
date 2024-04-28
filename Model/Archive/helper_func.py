import re
from trial.Resume_Scoring import create_skill_set, add_newruler_to_pipeline, extract_nlp

def update_progress_bar(val=1):
    '''
        Author: XYZ

        Description: This function will show progress of scoring in terminal.

        params: val=1(default 1): updates progress once each step completed successfully.

        return: progress_bar
    '''
    global pbar
    pbar.update(val)

def convert_list(string_skills):
    list_skill =list(re.split(',', string_skills))
    return list_skill

def skill_validation(skills):
    add_newruler_to_pipeline("SkillFile.jsonl")
    mds_extracted = convert_list(skills)
    print(mds_extracted)
    skill_set = extract_nlp(mds_extracted)
    skill_set_mds = create_skillset_list(skill_set)
    return skill_set_mds

def create_skillset_list(texts):
    '''Create a dictionary containing a set of the extracted skills. Name is key, matching skillset is value'''
    skillsets = [create_skill_set(text) for text in texts]
    result=[]
    for skillset in skillsets:
        if skillset != {*()} :
            result.append(skillset)
    return result

def text_urllib_encoding(encoding_text):
    """
    this function is for encoding the file name to send in sas url
    :param encoding_text:
    :return:
    """
    from urllib.parse import quote
    # from urllib.parse import urlparse
    return quote(encoding_text)