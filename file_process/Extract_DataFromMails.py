import requests
import json
import os
# import pandas as pd
from datetime import datetime
from dateutil import tz
import re
import utils.config as cf
import PyPDF2
from pyhtml2pdf import converter
# from db_connection import db_connect,insert_data
from utils.SQL_CONN import *
import pytz

def get_auth_token():

    url = f"https://login.microsoftonline.com/{cf.Outlook_Tenant_ID}/oauth2/v2.0/token"
    payload = f'grant_type=client_credentials&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&client_id={cf.Outlook_client_ID}&client_secret={cf.Outlook_Client_secret}'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'fpc=ApPtiUiaiC9Np5n3T3Rk9tHV5HfGAQAAAG6kh9gOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    jsonData = response.json()
    access_token = jsonData['access_token']
    # print("access_token " + str(access_token))
    return access_token

def Download_attachments(auth_token,Mail_uniqueid,target_folderpath):
    try:
        get_attachments_list = "https://graph.microsoft.com/v1.0/users/resumescoring@mouritech.org/mailFolders/Inbox/Messages/{0}/attachments".format(
            Mail_uniqueid)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }

        list0fattachments = requests.request("GET", get_attachments_list, headers=headers)
        for attachment in json.loads(list0fattachments.content)['value']:
            if not attachment['isInline']:
                file_name = attachment['name']
                attachment_id = attachment['id']
                download_attachment_url = "https://graph.microsoft.com/v1.0/users/resumescoring@mouritech.org/mailFolders/Inbox/Messages/{0}/attachments/{1}/$value".format(Mail_uniqueid,attachment_id)
                attachment_content = requests.request("GET", download_attachment_url, headers=headers)
                print("saving the file")
                with open(os.path.join(target_folderpath,file_name),'wb') as _f:
                    _f.write(attachment_content.content)
                print("Successfully downloaded file " + str('"'+file_name+'"'))
        return (200,str(os.path.join(target_folderpath,file_name)))
    except Exception as e:
        print("Exception occurred while downloading the file "+str(e))
        return (201,str(e))

def WriteToCSV(Target_folderpath,inputs):
    inputs_df = pd.DataFrame(inputs, index=[0])
    db_file_path = os.path.join(Target_folderpath,"db.csv")
    if os.path.exists(db_file_path):
        existing_data = pd.read_csv(db_file_path,index_col=False)
        # updated_data = existing_data.append(inputs_df, ignore_index=True)
        updated_data = pd.concat(existing_data,inputs_df)
        updated_data = updated_data.astype(str)
        updated_data.drop_duplicates(inplace=True,keep='last')
        updated_data.to_csv(db_file_path, index=False)
    else:
        inputs_df.to_csv(db_file_path,index=False)

def UTCtoLocaltime(utcvalue):
    # from_zone = tz.tzutc()
    utc = datetime.strptime(utcvalue, '%Y-%m-%dT%H:%M:%SZ')
    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=pytz.utc)
    # Convert time zone
    central = utc.astimezone(pytz.timezone('Asia/Calcutta'))

    return central

#input format 2023-02-27 20:00:00
def LocaltimetoUTC(localtimestamp):
    # localtimestamp = '2023-02-27 20:00:00'
    localtimestamp = datetime.strptime(localtimestamp, '%Y-%m-%d %H:%M:%S')
    localtimestamp = localtimestamp.replace(tzinfo=pytz.timezone('Asia/Calcutta'))
    to_zone = tz.tzutc()
    utc = localtimestamp.astimezone(to_zone)
    FilterAfterDate_UTC = utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    return FilterAfterDate_UTC

def get_employeedetails(mail_body):
    string_pattern = re.compile(r'^[\n]*(.*)-(.*)', re.MULTILINE)
    Employee_details = re.findall(string_pattern, mail_body)
    values_dict ={}
    for value in Employee_details:
        values_dict[value[0].strip()] =value[1].strip()
    return values_dict

def Dice_Mails(result,auth_token,target_folderpath):
    Applicant_name,Job_Title,KeySkills,resume_path,MailID,MobileNumber,\
        NoticePeriod,Education,Location,Experience,DateOfMailReceived = '','','','','','','','','','',''
    Mail_uniqueid = result['id']
    Mail_Subject = result['subject']
    list_ofdetails_applicant = Mail_Subject.split("-")
    Job_Title = list_ofdetails_applicant[0].strip()
    Job_Id = list_ofdetails_applicant[-1].strip()
    Applicant_name = list_ofdetails_applicant[1].split('has')[0].strip()
    DateOfMailReceived_UTC = UTCtoLocaltime(result['receivedDateTime'])
    DateOfMailReceived = datetime(DateOfMailReceived_UTC.year, DateOfMailReceived_UTC.month,
                                  DateOfMailReceived_UTC.day, DateOfMailReceived_UTC.hour,
                                  DateOfMailReceived_UTC.minute, DateOfMailReceived_UTC.second)
    mail_body = result['bodyPreview']
    Details_from_mailbody = get_employeedetails(mail_body)
    if 'Location' in Details_from_mailbody.keys():
        Location = Details_from_mailbody['Location']
    if result['hasAttachments']:
        resume_path = Download_attachments(auth_token, Mail_uniqueid, target_folderpath)
        if resume_path[0] == 201:
            print("Failed to download the file")
            exit()

    # applicant_details = {'Applicant_name': Applicant_name, 'Job_Id': Job_Id, 'Job_Title': Job_Title,
    #                      'Resume_path': resume_path[1], 'DateOfMailReceived': DateOfMailReceived,
    #                      'Source': 'Dice'}

    applicant_details = {'Applicant_Name':Applicant_name,'Job_Title':Job_Title,'Keyskills':KeySkills,'Resume_Path':resume_path[1],'Mail_ID':MailID,
                         'Mobile_Number':MobileNumber,'Notice_Period':NoticePeriod,'Education':Education,'Location':Location,'Experience':Experience,'DateOfMailReceived':str(DateOfMailReceived),'Source': 'Dice'}

    cursor = connect_db()
    columns_and_datatypes = {'Applicant_Name': ['varchar', 255], 'Job_Title': ['varchar', 255],
                             'Keyskills': ['varchar', 255],
                             'Resume_Path': ['varchar', 255], 'Mail_ID': ['varchar', 255],
                             'Mobile_Number': ['varchar', 255],
                             'Notice_Period': ['varchar', 255], 'Education': ['varchar', 255],
                             'Location': ['varchar', 255],
                             'Experience': ['varchar', 255], 'DateOfMailReceived': ['varchar', 255],
                             'Source': ['varchar', 255]}
    if not check_if_tableExists(cursor,'dbo', 'Mail_Info'):
        create_table(cursor,'dbo', 'Mail_Info', columns_and_datatypes)
    insert_data(cursor, applicant_details, 'Mail_Info')
    return applicant_details

def Naukari_Mails(result,auth_token,target_folderpath):
    Applicant_name, Job_Title, KeySkills, resume_path, MailID, MobileNumber, \
        NoticePeriod, Education, Location, Experience, DateOfMailReceived = '', '', '', '', '', '', '', '', '', '', ''
    result_content = result['body']['content']
    Mail_uniqueid = result['id']
    if result['hasAttachments']:
        resume_path = Download_attachments(auth_token, Mail_uniqueid, target_folderpath)
        if resume_path[0] == 201:
            print("Failed to download the file")
            exit()
    else:
        exit()
    with open("../Model/html_file.html", 'w') as file:
        file.write(result_content)
    current_path = os.getcwd()
    DateOfMailReceived_UTC = UTCtoLocaltime(result['receivedDateTime'])
    DateOfMailReceived = datetime(DateOfMailReceived_UTC.year, DateOfMailReceived_UTC.month,
                                  DateOfMailReceived_UTC.day, DateOfMailReceived_UTC.hour,
                                  DateOfMailReceived_UTC.minute, DateOfMailReceived_UTC.second)
    converter.convert(os.path.join(current_path,"html_file.html"), "email_pdf.pdf")
    fileReader = PyPDF2.PdfReader(open(os.path.join(current_path,"email_pdf.pdf"), 'rb'))
    page_count = len(fileReader.pages)
    pdf_text = [fileReader.pages[i].extract_text() for i in range(page_count)]
    if type(pdf_text) is list:
        pdf_text = pdf_text[0]
    key_words = ['Location', 'Past Experience', 'Notice Period', 'Education', 'Keyskills', 'Shortl ist']
    key_words_values = {}
    for key_word in range(0, len(key_words) - 1):
        idx1 = pdf_text.index(key_words[key_word])
        idx2 = pdf_text.index(key_words[key_word + 1])
        key_value = pdf_text[idx1:idx2]
        if key_words[key_word] in key_value:
            key_words_values[key_words[key_word]] = key_value.replace(key_words[key_word], '').replace("\n",
                                                                                                            "").strip()
        else:
            key_words_values[key_words[key_word]] = key_value
    if 'Location' in key_words_values.keys():
        Location = key_words_values['Location']
    if 'Notice Period' in key_words_values.keys():
        NoticePeriod = key_words_values['Notice Period']
    if 'Education' in key_words_values.keys():
        Education = key_words_values['Education']
        if '+ See all' in Education: Education = Education.replace('+ See all', '')
    if 'Keyskills' in key_words_values.keys():
        KeySkills = key_words_values['Keyskills']
    idx_last = pdf_text.index(key_words[-1])
    filtered_text = pdf_text[:idx_last]
    split_by_newline = filtered_text.split("\n")
    Applicant_name = split_by_newline[4]
    Job_Title = split_by_newline[5]
    phone_regex = re.compile("(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$")
    phone_nummatch = re.search(phone_regex, filtered_text)
    if phone_nummatch != None:
        # key_words_values['Mobile_Number'] = phone_nummatch.group()
        MobileNumber = phone_nummatch.group()
    else:
        # key_words_values['Mobile_Number'] = ""
        MobileNumber = ""
    exp_years_regex = r"(\d+(?:-\d+)?\+?)\s*(Years?)"
    exp_month_regex = r"(\d+(?:-\d+)?\+?)\s*(Months?)"
    for line in split_by_newline:
        if 'years' in line.lower() or 'months' in line.lower():
            line_with_exp = line
            break
    match_year = re.search(exp_years_regex, line_with_exp)
    match_month = re.search(exp_month_regex, line_with_exp)
    if match_year != None:
        experience_years = match_year.group()
    else:
        experience_years = ""
    if match_month != None:
        experience_months = match_month.group()
    else:
        experience_months = ""
    Experience = experience_years + " " + experience_months
    package = split_by_newline[7].split(experience_months)[-1]
    # key_words_values['Experience'] = experience
    # key_words_values['Package'] = package
    Mail_Id = re.findall('\S+@\S+.+', filtered_text)
    if Mail_Id != []:
        Mail_Id = Mail_Id[0]
    else:
        Mail_Id = ""
    # key_words_values['Applicant_name'] = Applicant_name
    # key_words_values['Job_Title'] = Job_Title
    key_words_values = {'Applicant_Name': Applicant_name, 'Job_Title': Job_Title, 'Keyskills': KeySkills,
                         'Resume_Path': resume_path[1], 'Mail_ID': Mail_Id,
                         'Mobile_Number': MobileNumber, 'Notice_Period': NoticePeriod, 'Education': Education,
                         'Location': Location, 'Experience': Experience, 'DateOfMailReceived': str(DateOfMailReceived),
                         'Source': 'Naukari'}
    # WriteToCSV(target_folderpath, key_words_values)
    # cursor = db_connect('dbo', 'Mail_Info')
    # insert_data(cursor, key_words_values)
    cursor = connect_db()
    columns_and_datatypes = {'Applicant_Name': ['varchar', 255], 'Job_Title': ['varchar', 255],
                             'Keyskills': ['varchar', 255],
                             'Resume_Path': ['varchar', 255], 'Mail_ID': ['varchar', 255],
                             'Mobile_Number': ['varchar', 255],
                             'Notice_Period': ['varchar', 255], 'Education': ['varchar', 255],
                             'Location': ['varchar', 255],
                             'Experience': ['varchar', 255], 'DateOfMailReceived': ['varchar', 255],
                             'Source': ['varchar', 255]}
    if not check_if_tableExists(cursor,'dbo', 'Mail_Info'):
        create_table(cursor,'dbo', 'Mail_Info', columns_and_datatypes)
    insert_data(cursor, key_words_values, 'Mail_Info')
    return key_words_values

def Linkedin_Mails(result,auth_token,target_folderpath):
    target_folderpath = os.path.join(target_folderpath,'Model')
    Applicant_name, Job_Title, KeySkills, resume_path, MailID, MobileNumber, \
        NoticePeriod, Education, Location, Experience, DateOfMailReceived = '', '', '', '', '', '', '', '', '', '', ''
    Mail_uniqueid = result['id']
    if result['hasAttachments']:
        resume_path = Download_attachments(auth_token, Mail_uniqueid, target_folderpath)
        if resume_path[0] == 201:
            print("Failed to download the file")
            exit()
    result_content = result['body']['content']
    with open(os.path.join(target_folderpath,"html_file.html"), 'w') as file:
        file.write(result_content)
    DateOfMailReceived_UTC = UTCtoLocaltime(result['receivedDateTime'])
    DateOfMailReceived = datetime(DateOfMailReceived_UTC.year, DateOfMailReceived_UTC.month,
                                  DateOfMailReceived_UTC.day, DateOfMailReceived_UTC.hour,
                                  DateOfMailReceived_UTC.minute, DateOfMailReceived_UTC.second)
    print(1)
    converter.convert(os.path.join(os.getcwd(),"html_file.html"), "email_pdf.pdf")
    fileReader = PyPDF2.PdfReader(open(os.path.join(os.getcwd(),"email_pdf.pdf"), 'rb'))
    page_count = len(fileReader.pages)
    pdf_text = [fileReader.pages[i].extract_text() for i in range(page_count)]
    if type(pdf_text) is list:
        pdf_text = pdf_text[0]
    if 'Your job' and 'has a new applicant!' in result['bodyPreview']:
        start_index = result['bodyPreview'].index('Your job') + 9
        end_index = result['bodyPreview'].index('has a new applicant!') - 2
        Job_Title =  result['bodyPreview'][start_index:end_index]
    key_words = ['Current experience', 'Past experience', 'Education', 'Skills matching your job', 'Highlight']
    key_words_values = {}
    for key_word in range(0, len(key_words) - 1):
        idx1 = pdf_text.index(key_words[key_word])
        idx2 = pdf_text.index(key_words[key_word + 1])
        Location_value = pdf_text[idx1:idx2]
        if key_words[key_word] in Location_value:
            key_words_values[key_words[key_word]] = Location_value.replace(key_words[key_word], '').replace("\n",
                                                                                                            "").strip()
        else:
            key_words_values[key_words[key_word]] = Location_value
    if 'Past experience' in key_words_values.keys():
        Experience = key_words_values['Past experience']
    if 'Education' in key_words_values.keys():
        Education = key_words_values['Education']
        if '+ See all' in Education: Education=Education.replace('+ See all','')
    filtered_text = pdf_text[pdf_text.index("applicant!"):].replace("applicant!\n", "")
    Applicant_name = filtered_text.split("\n")[0]
    filter_keyskills = pdf_text[pdf_text.index(Applicant_name) + len(Applicant_name) + 1:pdf_text.index(
        'View full application')]
    key_skills = filter_keyskills.split("\n")[:-2]
    # key_words_values['Candinate_Name'] = Applicant_name
    # key_words_values['key_Skills'] = "".join(key_skills)
    KeySkills = "".join(key_skills)
    key_words_values = [{'Applicant_Name': Applicant_name, 'Job_Title': Job_Title, 'Keyskills': KeySkills,
                        'Resume_Path': resume_path[1], 'Mail_ID': MailID,
                        'Mobile_Number': MobileNumber, 'Notice_Period': NoticePeriod, 'Education': Education,
                        'Location': Location, 'Experience': Experience, 'DateOfMailReceived': str(DateOfMailReceived),
                        'Source': 'LinkedIn'}]
    # WriteToCSV(target_folderpath,key_words_values)
    # cursor = db_connect('dbo', 'Mail_Info')
    # insert_data(cursor, key_words_values)
    df = pd.DataFrame.from_dict(key_words_values, orient='columns')
    cursor = connect_db()
    columns_and_datatypes = {'Applicant_Name': ['varchar', 255], 'Job_Title': ['varchar', 255],
                             'Keyskills': ['varchar', 255],
                             'Resume_Path': ['varchar', 255], 'Mail_ID': ['varchar', 255],
                             'Mobile_Number': ['varchar', 255],
                             'Notice_Period': ['varchar', 255], 'Education': ['varchar', 255],
                             'Location': ['varchar', 255],
                             'Experience': ['varchar', 255], 'DateOfMailReceived': ['varchar', 255],
                             'Source': ['varchar', 255]}
    if not check_if_tableExists(cursor,'dbo', 'Mail_Info'):
        create_table(cursor,'dbo', 'Mail_Info', columns_and_datatypes)
    insert_data(df, 'dbo.Mail_Info')
    return key_words_values

def Read_email(auth_token,response,target_folderpath,Mail_source):
    try:
        if Mail_source == 'naukri':
            Naukari_Mails(response,auth_token,target_folderpath)
        elif Mail_source == 'dice':
            Dice_Mails(response,auth_token, target_folderpath)
        elif Mail_source == 'linkedin':
            Linkedin_Mails(response,auth_token,target_folderpath)
        else:
            print("Didn't recognize the mail source type")
    except Exception as e:
        print(e)


'''
Final code
From_mailid = 'applicant@dice.com'
if From_mailid == 'jobs-listings@linkedin.com':
    Mail_source = 'linkedin'
elif From_mailid == 'info@naukri.com':
    Mail_source = 'naukri'
elif From_mailid == 'applicant@dice.com':
    Mail_source = 'dice'
'''


# # Dice Mails input
# Target_folderpath = 'D:\Dice_Mails\Attachments_downloaded'
# FilterAfterDate = '2023-01-16 18:00:00'
# FilterBeforeDate = '2023-01-16 19:00:00'
# From_mailid = 'jeevanap.in@mouritech.com'
# Mail_source = 'dice'

# # Nukari  Mails input
# Target_folderpath = 'D:\Dice_Mails\Attachments_downloaded'
# FilterAfterDate = '2023-02-27 16:00:00'
# FilterBeforeDate = '2023-02-27 17:00:00'
# From_mailid = 'jeevanap.in@mouritech.com'
# Mail_source = 'naukri'


# Linkedin  Mails input
# Target_folderpath = 'D:\Dice_Mails\Attachments_downloaded'
# # Target_folderpath = ''
# FilterAfterDate = '2023-02-27 20:00:00'
# FilterBeforeDate = '2023-02-27 21:00:00'
# From_mailid = 'jeevanap.in@mouritech.com'
# Mail_source = 'linkedin'
# JobID = ''
# Job_Title = ''

import sched, time

def auto_monitoring(scheduler):
    print("Started dicemails code")
    # schedule the next call first
    # scheduler.enter(60, 1, auto_monitoring, (scheduler,))
    # FilterBeforeDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    # FilterAfterDate = datetime.now() - datetime.timedelta(seconds=5)
    auth_token = get_auth_token()
    FilterAfterDate = '2023-02-27 20:00:00'
    FilterBeforeDate = '2023-02-27 21:00:00'
    FilterAfterDatetime = LocaltimetoUTC(FilterAfterDate)
    FilterBeforeDatetime = LocaltimetoUTC(FilterBeforeDate)
    url = "https://graph.microsoft.com/v1.0/users/resumescoring@mouritech.org/mailFolders/Inbox/Messages?$filter=receivedDateTime ge {0} and receivedDateTime le {1}".format(
        FilterAfterDatetime, FilterBeforeDatetime)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/json'
    }
    target_folderpath =''
    if target_folderpath == '':
        target_folderpath = os.getcwd()
    # response = requests.request("GET", url, headers=headers)
    response = requests.get(url,headers=headers)
    response_json = response.json()
    for i in range(0, len(json.loads(response.content)['value'])):
        result = json.loads(response.content)['value'][i]
        # From_mailid = result['from']['emailAddress']['address']
        # if not result['hasAttachments']:
        #     continue
        # if From_mailid == 'jobs-listings@linkedin.com':
        #     Mail_source = 'linkedin'
        #     Read_email(auth_token, response, target_folderpath, Mail_source)
        # elif From_mailid == 'info@naukri.com':
        #     Mail_source = 'naukri'
        #     Read_email(auth_token, response, target_folderpath, Mail_source)
        # elif From_mailid == 'applicant@dice.com':
        #     Mail_source = 'dice'
        #     Read_email(auth_token, response, target_folderpath, Mail_source)
        # else:
        #     print('Mail Soure not defined')
        From_mailid = 'jeevanap.in@mouritech.com'
        if From_mailid == 'jeevanap.in@mouritech.com':
            Mail_source = 'linkedin'
            Read_email(auth_token, result, target_folderpath, Mail_source)

# print("1-",datetime.now())
# my_scheduler = sched.scheduler(time.time, time.sleep)
# my_scheduler.enter(60, 1, auto_monitoring, (my_scheduler,))
# my_scheduler.run()
# print("2-",datetime.now())

# auto_monitoring(1)


# x = LocaltimetoUTC('2023-02-27 20:00:00')
# print(x)
# print(UTCtoLocaltime(str(x)))