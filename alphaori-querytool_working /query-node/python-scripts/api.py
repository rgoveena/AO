import sys
import requests
import json

################################################################
##  sys.argv[1]: get/post               method
##  sys.argv[2]: host url               base url for request
##  sys.argv[3]: signature              api signature for request
##  sys.argv[4]: json content           content for post
################################################################

BROWSER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0; QA_Automation) Gecko/20100101 Firefox/65.0'
JSON_FORMAT = 'application/json'

################################################################
##
##  RETRIEVING TOKEN FROM LOGIN TO PERFORM AUTHORIZED REQUESTS
##
################################################################

auth = {"username" : "admin",
        "password" : "Alph@or1" }

headers = {'X-Original-User-Agent'  : BROWSER_AGENT,
           'Accept'                 : JSON_FORMAT } 

login_url = "https://"+sys.argv[2]+"/v1.2/auths/login"

response = requests.post(login_url, json=auth, headers=headers, verify=False)

token = json.loads(response.text)['token']

################################################################
##
##  PERFORMING AUTHORIZED REQUEST FOR MICROSERVICES
##
################################################################

def req(method, url):

    headers = {'X-Original-User-Agent'  : BROWSER_AGENT,
               'Accept'                 : JSON_FORMAT,
               'Authorization'          : "Bearer "+token }
    if (method == 'get'):
        res = requests.get(url, headers=headers, verify=False)
    elif (method == 'post'):
        res = requests.post(url, json=json.loads(sys.argv[4]), headers=headers, verify=False)
    return res


def status(url):

    status = req(url).status_code
    return str(status)

def content(method, url):

    content = req(method, url).text
    return content

################################################################
##
##  API COMPONENT
##
################################################################



server_url = "https://"+ sys.argv[2]+ sys.argv[3]
#print("status code: " + status(server_url))
print(content(sys.argv[1], server_url).encode('utf-8')[:8191])

