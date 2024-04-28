import os
from threading import Lock, Thread
import time
from datetime import datetime, timedelta
import json
import utils.config as cf

mutex = Lock()
LOCAL_BLOB_PATH = os.path.abspath(os.path.curdir)+"/ResumeProcess/saved_resume_files"


def get_output_file(job_id=None):
    if not job_id:
        return os.path.join(cf.upload_folder, f"{os.getpid()}_status.json")
    else:
        return os.path.join(cf.upload_folder, f"{job_id}_status.json")


def write_json(status, percent, file_name, mode="w", error_code=0):
    th = Thread(target=target_fun,args=(status,percent,file_name,mode,error_code))
    th.start()


def target_fun(status, percent, file_name, mode="w", error_code=0):
    mutex.acquire()
    output_file = get_output_file()
    with open(output_file, mode) as fp:
        json.dump({"job_id": os.getpid(),
                   "Status": status,
                   "File": file_name,
                   "Percent": percent,
                   "Error_code": error_code}, fp)
    mutex.release()
    if status != "Completed":
        time.sleep(1)
 