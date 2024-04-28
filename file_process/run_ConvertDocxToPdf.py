from fileinput import filename
import subprocess
import os
import time

def conDocxtoPdf(folder_name,filepath):
    try:
        output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf','--outdir',"./ResumeProcess/saved_resume_files/ConvertedPdfs",folder_name+"\\"+filepath])
        time.sleep(5)
        print("folder_name filepath->>",folder_name+"\\"+filepath)
        if os.path.isfile(filepath.replace(".docx",".pdf")):
            print("Converted")
            return True
        else:
            print("Not Converted")
            return False
    except Exception as e:
        print(e)
        raise