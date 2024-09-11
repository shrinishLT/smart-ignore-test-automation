import requests
import os 
import re

CURL = """
curl --location 'https://api.lambdatest.com/automation/smart-ui/v2/upload' --header 'Authorization: Basic aGFpZGVyazppN3ZGNXI2NklZZ3NnRTlIcDV0NmhacWQ1UGtRWDAyMUZncFdSQzcwbXAwU2hiRmgxUg==' --form 'projectToken="1639932#0e56f45c-cea1-4e34-9516-affc23534dd8#testing-api"' --form 'buildName="smartui-build"' --form 'screenshotNames="null"' --form 'files=@"null"'
"""

API_URL = re.search(r"curl --location '(.*?)'", CURL)
AUTH_TOKEN = re.search(r"--header 'Authorization: Basic (.*?)'", CURL)
PROJECT_TOKEN = re.search(r"--form 'projectToken=\"(.*?)\"'", CURL)


# check from where to where you want to upload
START = 1
END = 17
TYPE = 'compare' ## change with 'compare' or  'base'
BUILD_NAME = 'B3'

IMAGE_DIR = f"./input/{TYPE}/"

def generate_screenshot_names():
    return ",".join([f"s{i}" for i in range(START, END + 1)])

def list_images():
    images = [os.path.join(IMAGE_DIR, f"{TYPE}{i}.png") for i in range(START, END + 1)]
    return images


def upload_to_lambdatest():
    url = API_URL
    headers = {
        "Authorization": f"Basic {AUTH_TOKEN}"
    }
    
    form_data = {
        "projectToken": PROJECT_TOKEN,
        "buildName": BUILD_NAME,
        "screenshotNames": generate_screenshot_names(),
    }
    
    # Get all image paths from the directory based on TYPE and range
    images = list_images()
    files = [('files', (os.path.basename(img), open(img, 'rb'))) for img in images]

    try:
        response = requests.post(url, headers=headers, data=form_data, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        for _, (_, file_obj) in files:
            file_obj.close()


upload_to_lambdatest()
