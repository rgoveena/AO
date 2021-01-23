import sys
import requests
import json
import datetime

################################################################
##	sys.argv[1]: msstat/msdetail	 determines output
##	sys.argv[2]: api signature	  	 for api request
##	sys.argv[3]: res endpoint	 	 splice response for output	
################################################################

BROWSER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0; QA_Automation) Gecko/20100101 Firefox/65.0'
JSON_FORMAT = 'application/json'

now = datetime.datetime.now()		#to construct the host url (not perfect method because different time zones)

month = str(now.month)
if (now.month < 10):
	month = "0"+month

day = str(now.day)
if (now.day < 10):
	day = "0"+day

################################################################
##
##	RETRIEVING TOKEN FROM LOGIN TO PERFORM AUTHORIZED REQUESTS
##
################################################################

auth = {"username" : "admin",
        "password" : "Alph@or1" }

headers = {'X-Original-User-Agent'  : BROWSER_AGENT,
           'Accept'                 : JSON_FORMAT } 

login_url = "https://daily"+str(now.year)+month+day+"shore1-rundeck-smartship-v1dot2.alphaorimarine.com/v1.2/auths/login"

response = requests.post(login_url, json=auth, headers=headers, verify=False)

token = json.loads(response.text)['token']

################################################################
##
##	PERFORMING AUTHORIZED REQUEST FOR MICROSERVICES
##
################################################################

def req(url):

	headers = {'Authorization'	: "Bearer "+token }
	res = requests.get(url, headers=headers, verify=False)
	return res


def status(url):

	status = req(url).status_code
	return str(status)

def content(url):

	content = req(url).text
	return content

################################################################
##
##	MICROSERVICE COMPONENT (STATUS CODE) (DETAILS)
##
################################################################

url = "https://daily"+str(now.year)+month+day+"shore1-rundeck-smartship-v1dot2.alphaorimarine.com"		# url should be input ...

if (sys.argv[1] == 'msstat'):

	print(status(url + sys.argv[2]))

if (sys.argv[1] == 'msdetail'):

	res = (content(url+sys.argv[2])).encode('utf-8')
	response = res[(int(sys.argv[3])-8000):int(sys.argv[3])] 
	print(response)			#code breaks with a response greater than 8191 characters
	print(len(res))