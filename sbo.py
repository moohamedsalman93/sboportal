import requests
from bs4 import BeautifulSoup
import re
import telepot

t='2132333797:AAHH6w_57uJVRzq_Dz97Rdl92pFGwWIyNE'
rid=867862142
bot = telepot.Bot(t)

session = requests.Session()

url = "https://www.sboportal.org.in/"
cookie_pattern = re.compile(r'(XSRF-TOKEN|laravel_session)=([^;]+)')
csrf_token = ''
initial_cookie = ''

def loginGet():
    global csrf_token
    global initial_cookie

    try:
        response = session.get(url + 'login')
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
        initial_cookie = {m.group(1): m.group(
            2) for m in cookie_pattern.finditer(response.headers['Set-Cookie'])}
    except Exception as e:
        bot.sendMessage(rid,'inLoginGet')

def loginAction():
    global initial_cookie
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in initial_cookie.items()]),
        "X-Csrf-Token": csrf_token,
        "Origin": "https://www.sboportal.org.in",
        "Referer": "https://www.sboportal.org.in/login",
        "Host": "www.sboportal.org.in",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    }
    data = {
        "profile_id": "",
        "password": "@"
    }

    try:
        response = session.post(url + 'loginaction', headers=headers, data=data)
        # print(response.text)
        initial_cookie = {m.group(1): m.group(
            2) for m in cookie_pattern.finditer(response.headers['Set-Cookie'])}
        print('login true')
    except Exception as e:
        bot.sendMessage(rid,'inLogin')

def getBalance():
    global initial_cookie  # Add this line
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in initial_cookie.items()]),
        "Referer": "https://www.sboportal.org.in/",
        "Host": "www.sboportal.org.in",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    }

    try:
        response = session.get(url + 'dashboard', headers=headers)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        getTheValue=soup.find_all('div' ,class_='media-body')
        taskBalance=getTheValue[1].find('h3').text
        # bot.sendMessage(rid,'taskBalnce :' + taskBalance)
        print(taskBalance)
        
    except Exception as e:
        bot.sendMessage(rid,'ingetBalance')
   
def getcode(articleUrl):
    print('entered get code')
    code = ''
    try:
        with requests.Session() as temp_session:
            response = temp_session.get(articleUrl)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            code_div = soup.find('div', id='coderesult')
            if code_div:
                code = code_div.text.strip()
                print(code)
            else:
                print('no code div 86')

        headers = {
            "Cookie": "; ".join([f"{key}={value}" for key, value in initial_cookie.items()]),
            "X-Csrf-Token": csrf_token,
            "Origin": "https://www.sboportal.org.in",
            "Referer": "https://www.sboportal.org.in/articledetail/2",
            "Host": "www.sboportal.org.in",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
        }

        data = {
            "videoid": "2",
            "code": code
        }

        response = session.post(url + 'articledetail/2/articlesubmitform', headers=headers, data=data)
        print(response.text)
        getBalance()

    except Exception as e:
        bot.sendMessage(rid, 'inSubmit')

def articleInitial():
    getBalance()
    print('entered article')
    global initial_cookie  # Add this line
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in initial_cookie.items()]),
        "X-Csrf-Token": csrf_token,
        "Origin": "https://www.sboportal.org.in",
        "Referer": "https://www.sboportal.org.in/articlelistnew",
        "Host": "www.sboportal.org.in",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }

    try:
        response = session.get(url + 'articledetail/2', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        a_tag = soup.find('a', class_='btn btn-primary d-none viewarticlelink')

        if a_tag:
            href = a_tag['href']
            print('link founded')
            getcode(href)
        else:
            print("The <a> tag was not found.")
        
    except Exception as e:
        print('error in article')
        bot.sendMessage(rid,'inartical')
  

# def submit_video():
#     video=['qg','qw','rA','rQ','rg']
#     count=1

#     for i in video:
#         headers = {
#             "Cookie": "; ".join([f"{key}={value}" for key, value in initial_cookie.items()]),
#             "X-Csrf-Token": csrf_token,
#             "Origin": "https://www.sboportal.org.in",
#             "Referer": f"https://www.sboportal.org.in/videodetail/{i}==",
#             "Host": "www.sboportal.org.in",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
#         }
#         data = {
#             "videoid":f"{i}%3D%3D"
#         }

#         try:
#             response = session.post(url + 'videosubmitform', headers=headers, data=data)
            # print(response.text)
#             bot.sendMessage(rid,f"v-{count} {response.text}")
#         except Exception as e:
#             bot.sendMessage(rid,"in video")
#             print("An error occurred:", e)

#         count+=1




loginGet()
loginAction()
# submit_video()
articleInitial()
session.close()
