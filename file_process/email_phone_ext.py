import re
import time

def emph(text):
    '''
        Author: XYZ

        Description: This function is used to extract candidate's email address and phone number.

        params: text(list): list of extracted content from resume

        return: phone number and email of candidate
    '''
    start_time = time.time()
   
   
    emailRegex = re.compile(r'[a-zA-Z0-9-_\.]+\s*@\s*[a-zA-Z-\.\s*]*\.(\s*c\s*o\s*m|edu|net|org|in|cc)')  ## added new regex to extract mail.ids with space also , ash12 @ gmail.com##
    #phoneRegex = re.compile(r'(\+?(\b[0-9]{2}|[0-9]{1})?[-. ]?\(?[2-9][0-9]{2}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}\b)|(\+?(\b[0-9]{2}|[0-9]{1})?[-. ]?\(?[2-9][0-9]{4}\)?[-. ]?[0-9]{5}\b)|(\+?(\b[0-9]{2}|[0-9]{1})?[-. ][ ]?\(?[2-9][0-9]{3}\)?[-. ][ ]?[0-9]{3}[-. ][ ]?[0-9]{3}\b)|(\+?(\b[0-9]{2}|[0-9]{1})?[-. ]?\(?[2-9][0-9]{3}\)?[ ][-. ]?[0-9]{3}[ ][-. ]?[0-9]{3}\b)')
    phoneRegex = re.compile(r'(\+?(\b[0-9]{2}|[0-9]{1})?[-. ]?\(?[2-9][0-9]{2}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}\b)|(\+?(\b[0-9]{2}|[0-9]{1})?[-. ]?\(?[2-9][0-9]{4}\)?[-. ]?[0-9]{5})|(\+?(\b[0-9]{2}|[0-9]{1})?[-. ]?\(?[2-9][0-9]{4}\)?[-. ]?[0-9]{5}\b)|(\+?(\b[0-9]{2}|[0-9]{1})?[-. ][ ]?\(?[2-9][0-9]{3}\)?[-. ][ ]?[0-9]{3}[-. ][ ]?[0-9]{3}\b)|(\+?(\b[0-9]{2}|[0-9]{1})?[-. ]?\(?[2-9][0-9]{3}\)?[ ][-. ]?[0-9]{3}[ ][-. ]?[0-9]{3}\b)|(\+?(\b[0-9]{2}|[0-9]{1})?[-. ]?\(?[2-9][0-9]{3}\)?[-. ]?[0-9]{2}[-. ]?[0-9]{2}[-. ]?[0-9]{2}\b)')

    emailmatch = emailRegex.finditer(text)
    phonematch = phoneRegex.finditer(text)

    emails=[]
    for match in emailmatch:
        test = match.group(0)
        emails.append(test)
    
    phnums=[]
    for match in phonematch:
        test = match.group(0)
        phnums.append(test)
    if emails != []:
        if len(str(emails[0])) <= 1:
            email_data = 'NA'
        else:
            email_data = emails[0]
    
    if emails == []: email_data = "NA"
    
    if phnums != []:
        if len(str(phnums[0])) <= 1:
            phone_data = 'NA'
        else:
            phone_data = phnums[0]
    else:
        phone_data = "NA"
        

    return email_data,phone_data