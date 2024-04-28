#!/usr/bin/env python
# coding: utf-8

# In[21]:


import requests
import json
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from html.parser import HTMLParser


# In[22]:


email="veeranjaneyuluk.in@mouritech.com"
password="Mouri@123"
api_key="cabb9e71e4f6ba5e8512d8d14b89df7e08bac98d0195ac7717"


# In[23]:


def get_tokens(email,password,api_key):
    payload={'email':email,'password':password,'api_key':api_key}
    url="https://api.ceipal.com/api_authentication/"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    return response.json()


# In[24]:


def get_PageContent(url,auth_token):
    retry_count = 0
    max_retry_count = 3
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+auth_token
    resp = requests.get(url, headers=headers)
    if resp.status_code== 200:
        return resp
    else:
        while retry_count<max_retry_count:
            tokens=get_tokens(data,url)
            auth_token=tokens['access_token']
            retry_count=retry_count+1


# In[25]:


def all_jds(auth_token):
    final_result=[]
    jd_first_url="https://api.ceipal.com/job-postings/"
    jds_first=get_PageContent(jd_first_url,auth_token).json()
    final_result=final_result+jds_first['results']
    for i in range(2,jds_first['num_pages']+1):
        jd_url="https://api.ceipal.com/job-postings/?page="+str(i)
        jds=get_PageContent(jd_url,auth_token).json()
        final_result=final_result+jds['results']
    return final_result


# In[26]:


def get_req_id(final_result,job_code,auth_token):
    req_id = next(jd['id'] for jd in final_result if job_code==jd['job_code'])
    req_url="https://api.ceipal.com/job-postings/"+req_id
    req_content=get_PageContent(req_url,auth_token).json()
    return req_content


# In[27]:


class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data


# In[28]:


def start(job_code):
    try:
        tokens=get_tokens(email,password,api_key)
        auth_token=tokens['access_token']
        final_result=all_jds(auth_token)
        req_content=get_req_id(final_result,job_code,auth_token)
        data = req_content["requistion_description"]
        f = HTMLFilter()
        f.feed(data)
        return f.text
    except exception as E:
        return "Exception occured as followed ------->" + str(E)


# In[29]:


# job_code="MT-2022-3762"
# print(start(job_code))


# In[ ]:




