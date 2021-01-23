import getopt
import json
import os
import pprint
import re
import string
import sys
import uuid
import time
import traceback
import urllib
import uuid
import base64
import textwrap
import inspect

# see http://python-requests.org/
import requests
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

################################################################################
# Name     :   ServerAPI.py
# Purpose  :   Submit requests to the Server API - REST URLs.
#
#
# Author   :   Steve Reiss
################################################################################

# Script Constants

BROWSER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/55.0'
JSON_FORMAT = 'application/json'
TEXT_FORMAT = 'text/plain'


################################################################################
#
#   Class Server_API
#
################################################################################

class Server_API:

################################################################################
#  init - create the Server_API object.
#
#  Parameters :
#   host_name : string = server name / IP
#   port : string = the server port to use
#   secure : boolean = True | False - use https | http
#   debug_flag : boolean = debug flag to show screen output
#
#  Returns :
#   None
#
#
################################################################################

    def __init__(self, host_name="localhost", port="443", secure=True, debug_flag=True):

        self.DEBUG = debug_flag

        secure_string = "s" if secure else ""                                   # set 's' for ssl or blank

        end_point_url = 'http%s://%s:%s' % (secure_string, host_name, port)     # create host string

        self.end_point_url = end_point_url                                      # the url of the endpoint
        self.auth_token = None

        self.Method_GET = "GET"                                                 # http methods
        self.Method_POST = "POST"                                               # POST + Data
        self.Method_COOKIE = "COOKIE"                                           # GET + Cookie values
        self.Method_PUT = "PUT"                                                 # PUT + Data
        self.Method_DELETE = "DELETE"                                           # DELETE

        self.url_timing_info = {}                                               # dictionary for url timing values
        self.request_count = 0
        self.status_code = 0

        self.user_name = ""                                                     # set to blank
        self.password = ""
        self.expected_result = 'ok'                                             # expected status result for requests

        self.pp = pprint.PrettyPrinter(indent=4)                                # setup prettyprinter object
        requests.packages.urllib3.disable_warnings()                            # turn off warnings in Requests package


    def get_a_uuid(self):
        """get a UUID - URL safe, Base64"""

        return str(uuid.uuid4())                                                # return a random uuid


    def get_utc_time(self):
        """get a utc timestamp : 1440176792 """

        return int(round(time.time(), 0))                                       # return current UTC timestamp


################################################################################
#  Fetch_Page   - Perform a html page fetch
#
# Parameters:
#  url            = string : the request URL (REST call for current operation)
#  parameters     = dictionary of name / value pairs :
#                     Method : GET | POST | PUT | DELETE | COOKIE
#                     = http method to use (REQUIRED)
#                     Values : dictionary of name/value pairs for POST request
#
#  custom_header  = dictionary of name/value pair : requesting function can set as needed
#  show_output    = boolean : flag to show output to screen (Default = False)
#
# Returns:
#   success = server response of JSON data in dictionary format
#   failure = boolean False - error in request / server
#
################################################################################

    def FetchPage(self, url, parameters, custom_header=None, show_output=False):

        if custom_header:
            headers = custom_header                                             # use custom header passed in
        else:
            headers = {'X-Original-User-Agent'  : BROWSER_AGENT,
                       'Accept'                 : JSON_FORMAT,                  # output in JSON
                        }

        if string.find(url, 'http:') > -1 or string.find(url, 'https:') > -1:   # are we given a full url already?
            full_url = url                                                      # use the url "as is"
        else:
            full_url = "%s/%s" % (self.end_point_url, url)                      # command url - add the end_point_url to command

        method = parameters["Method"]                                           # get the REQUIRED http Method value
        results = None
        self.status_code = 0
        self.http_reason = None
        self.http_content = None
        self.server_error_message = None

        url_extra = ""                                                          # additional string to show POST data

        try:

            self.request_count += 1                                             # increment request_count
            start_time = time.time()                                            # save start time

            if method == self.Method_GET:                                       # process a GET request

                if show_output:
                    print("\n\n\nGET URL : %s\n\n") % (full_url)
                    self.DumpData(headers, "\nHeaders : \n")
                    print

                response = requests.get(full_url, headers=headers, verify=False) # GET request - url + headers

            elif method == self.Method_COOKIE:                                  # process a GET + COOKIE request

                values_data = parameters["Values"]                              # get POST data dictionary values
                cookie_dict = values_data['cookie']                             # get the cookie value : format in dict = {"name" : "value"}

                if show_output:
                    print("\n\n\nCOOKIE GET URL : %s\n\n") % (full_url)
                    self.DumpData(headers, "\nHeaders : \n")
                    self.DumpData(cookie_dict, "\nCookie: \n")
                    print

                response = requests.get(full_url, headers=headers, cookies=cookie_dict, verify=False) # GET request - url + cookies + headers


            elif method == self.Method_DELETE:                                  # process a DELETE request

                if show_output:
                    print("\n\n\nDELETE URL : %s\n\n") % (full_url)
                    self.DumpData(headers, "Headers : ")
                    print

                response = requests.delete(full_url, headers=headers, verify=False)


            elif method == self.Method_POST:                                    # process a POST request
                values_data = parameters["Values"]                              # get POST data dictionary values

                if "body" in values_data:                                       # get the body dictionary
                    body = values_data["body"]
                else:
                    body = values_data                                          # otherwise - user Values

                try:
                    url_extra = "  action = " + values_data["msg"]["action"]    # get post keys ["msg"]["action"] - if available
                except KeyError :
                    pass

#                values_data = urllib.urlencode(values)                         # encode the POST data
#                print("** In Post ** values_data = %s") % values_data

                if show_output:
                    print("\n\n\nPOST URL : %s\n") % (full_url)

                    self.DumpData(headers, "Headers : \n")
                    self.DumpData(values_data, "Data: \n")

#                    print("\nData    : %s\n\n") % values_data

# OLD                response = requests.post(full_url, json=values_data, headers=headers, verify=False)   # POST request - url + data + headers
                response = requests.post(full_url, json=body, headers=headers, verify=False)   # POST request - url + data + headers


            elif method == self.Method_PUT:                                     # process a PUT request

                if parameters["Values"]:                                        # PUT with DATA
#                    values_data = urllib.urlencode(parameters["Values"])
                    values_data = parameters["Values"]


                    if "body" in values_data:                                   # get the body dictionary
                        body = values_data["body"]
                    else:
                        body = values_data                                      # otherwise - user Values

                    if show_output:
                        print("\n\n\nPUT URL : %s\n") % (full_url)

                        self.DumpData(headers, "Headers : \n")
                        self.DumpData(body, "\nPUT body :\n")

                    response = requests.put(full_url, data=body, headers=headers, verify=False)

                else:
                    if show_output:                                             # PUT - NO Data
                        print("\n\n\nPUT URL : %s\n") % (full_url)
                        self.DumpData(headers, "Headers : \n")

                    response = requests.put(full_url, headers=headers, verify=False)

            else:
                raise Exception('serverAPI :: FetchPage - HTTP Request method not supported: %s' % method)

            # if show_output:
            #     print("\n %2d) response = %s \ntext = %s") % (self.request_count, response.status_code, response.text)
            #     # print("response.content = %s") % response.content

            results_raw = response.text                                         # read the response from server
            self.status_code = response.status_code
            self.http_reason = response.reason
            self.http_content = response.content

            try:
                results = json.loads(results_raw)                               # convert json string response to dictionary structure

            except Exception, err_message :

                if self.DEBUG and self.status_code != 200:
                    print("\n\n\t*** serverAPI :: FetchPage : Error decoding results_raw  ***\n\n\tstatus code : %s\n\terr_message : %s\n\tcontent     : %s\n") % (response.status_code, err_message, textwrap.fill(response.content, subsequent_indent = '\t\t\t'))

                results = response.content                                      # send content

        except Exception, err_message :                                         # failure in request
            print("\n\n*** serverAPI :: FetchPage - ERROR In Request : %s\n\nURL = %s\n\nHeaders = %s\n\nMethod = %s\n\n") % (err_message, full_url, headers, method)
            self.server_error_message = err_message                             # save any server message here
            results = False

        stop_time = time.time()                                                 # save stop time
        elapsed_time = round(stop_time - start_time, 2)

        # save request info to class dict

        if len(full_url) > 80:                                                  # shorten long urls for report
            full_url = full_url[30:]

        self.url_timing_info[self.request_count] = [full_url + url_extra, elapsed_time, method, self.status_code, self.http_reason]

    #      self.DumpData(results, "\nresults\n")

        return results


################################################################################
#  DumpData   - Output data using PrettyPrinter (using Class variable : self.pp)
#
# Parameters:
#  input_data     = object/string : data to output to screen
#  title          = string : optional heading/title to print before data output
#
# Returns :
#  None
################################################################################

    def DumpData(self, input_data, title=None):

        if title:                                 # output titles - if given
            print("%s") % title

        self.pp.pprint(input_data)                # print the data to screen


################################################################################
#  DumpTimingData   - Output the URL Request timing data
#
#  self.url_timing_info = {request_count : [full_url, elapsed_time, method, status_code, http_reason]}
#
# Parameters:
#  None
#
# Returns :
#  None
################################################################################

    def DumpTimingData(self):

        if not self.url_timing_info:        # no stats to output - return
            return

        total_time = 0.0                    # accumulator for total time - float
        data_count = 0                      # data sample counter - integer
        time_list = []


        print("\n")                         # output headings
        print("%s") % ("="*80)
        print("\n\nHTTP URL Request timings for User : %s / %s\n\n") % (self.user_name, self.password)
        print("%-10s %-10s %-80s %-10s %-12s   %-10s") % ("Req#", "Method", "URL", "Status", "Reason", "Time (sec)")
        print("%10s %-10s %80s %10s %10s %12s") % ("-"*10, "-"*10, "-"*80, "-"*10, "-"*12, "-"*10)

        # output timing data

        for current_data in sorted(self.url_timing_info):
            print("%4d        %-10s %-80s %-10s %-12s %7.2f") % (current_data,
                                                              self.url_timing_info[current_data][2],
                                                              self.url_timing_info[current_data][0],
                                                              self.url_timing_info[current_data][3],
                                                              self.url_timing_info[current_data][4],
                                                              self.url_timing_info[current_data][1])
            data_count += 1
            total_time += self.url_timing_info[current_data][1]
            time_list.append(self.url_timing_info[current_data][1])

        print("\n\n")
        print("Response Time - Seconds\n")

        try:
            print("Average : %7.2f") % (total_time / data_count)    #compute avg response time
        except ZeroDivisionError:
            pass

        print("Min     : %7.2f") % (min(time_list))
        print("Max     : %7.2f") % (max(time_list))
        print("\n%s") % ("="*80)


################################################################################
#  GetLoginAuthToken   - submit the username/password to server. Get back a
#                       auth token to be used in ALL OTHER REQUESTS.
#
#  ** SETS CLASS VARIABLE : self.auth_token
#
# Parameters:
#  username     = string : email address of the user
#  password     = string : password for the above username
#  login_url    = string : location of the login url
#
# Returns :
#  True : Login was successful
#  False : Login FAILED
#
################################################################################

    def GetLoginAuthToken(self, username, password, login_url):

        self.user_name = username                                               # get the credentials passed in
        self.password = password

        return_value = False
        current_method = inspect.stack()[0][3]                                  # get the name of the current method

        headers = {'X-Original-User-Agent'  : BROWSER_AGENT,                    # set custom headers to get Auth Token
                   'Accept'                 : JSON_FORMAT
                  }

        values = {"username"  : self.user_name,                                 # parmeters to get auth token
                  "password"  : self.password}

        parameters = {"Method" : self.Method_POST,                              # setup parameters for request
                      "Values" : values}


        data_content = self.FetchPage(login_url, parameters, custom_header=headers, show_output=self.DEBUG)         # submit request to server

        if self.DEBUG:
            self.DumpData(data_content, "\nResponse : %s\n" % current_method)


        if self.status_code in [200] and data_content:

            if data_content['status'] == self.expected_result:

                self.auth_token = data_content['token']              # set the class variable

                if self.DEBUG:
                    print("\n\nServerAPI :: %s :: %s\n\n\tAPI Token = %s") % (current_method, data_content['username'], self.auth_token)

                return_value = True
            else:
                print("\n\n*** ServerAPI :: %s :: ERROR GETTING AUTHENTICATION TOKEN ** \n\n"  % current_method)     # Dump out error messages

                for item in sorted(data_content):
                    print("%-10s = %s") % (item, data_content[item])
        else:
            print("\n\n*** ServerAPI :: %s :: ERROR FROM SERVER \n\nServer status_code = %s : %s\n\nhttp_content = %s\n\n") % (current_method, self.status_code, self.http_reason, self.http_content)


        return return_value


################################################################################
#  ReAuthenticate_User   - resubmit the username/password to server. Get back a
#                   auth token to be used in ALL OTHER REQUESTS.
#
#  ** SETS CLASS VARIABLE : self.auth_token
#
# Parameters:
#  username     = string : email address of the user
#  password     = string : password for the above username
#
# Returns :
#  True : Login was successful
#  False : Login FAILED
#
################################################################################

    def ReAuthenticate_User(self):
        return self.GetAuthToken(self.user_name, self.password)


################################################################################
#  LogoutUser   -  submit a logout request to the sever
#
#
#  ** On Success -  SETS CLASS VARIABLE : self.auth_token to None
#
# Parameters:
#  none
#
# Returns :
#  True : Logout was successful
#  False : Logout FAILED
#
################################################################################

    def LogoutUser(self):

        return_value = False

        url = "logout"                                                          # command url

        headers = {'X-Original-User-Agent'  : BROWSER_AGENT,                    # set custom headers to get Auth Token
                   'Accept'                 : JSON_FORMAT
                  }

        parameters = {"Method" : self.Method_GET}                               # setup parameters for request

        data_content = self.FetchPage(url, parameters, custom_header=headers, show_output=self.DEBUG)         # submit request to server

        if self.DEBUG and self.status_code != 200:
            self.DumpData(data_content, "\nResponse : LogoutUser\n")

        if self.status_code in [200] and data_content:
            self.auth_token = None                                              # success in logout - reset auth_token
            return_value = True

            if self.DEBUG:
                print("\nUser Logged Out.\n")

        return return_value


################################################################################
#  SendRestPayload   - send a rest JSON payload to the server.
#
#
# Parameters:
#  request_payload : dictionary = a dictionary payload for the metrics call :
#
#  url = "rest/" : string = the server URL to use for the request.
#  Show_Output : Boolean = Flag to show raw output of the command (Default = False)
#
# Returns :
#  success - rest Payload in JSON dictionary format
#  failure - Error information in JSON dictionary format
#
################################################################################

    def SendRestPayload(self, request_payload={}, url="rest/", Show_Output=False):

        if "Values" in request_payload:
            value_payload = request_payload["Values"]
        else:
            value_payload = ""

        data = {'token' : self.auth_token,                                      # add in auth_token from login
                'body'  : value_payload                                         # set payload for request
               }

        parameters = {"Method" : request_payload["Method"],                     # http "Method"
                      "Values" : data }                                         # setup parameters for request

        data_content = self.FetchPage(url, parameters, show_output=Show_Output) # make the request - return payload

        if Show_Output :

            self.DumpData(data_content, "\nResponse : SendRestPayload - %s\n" % url)

            if self.status_code != 200:
                print("\n\n*** ServerAPI :: SendRestPayload :: \n\nServer status_code = %s : %s\n\nhttp_content = %s\n\n") % (self.status_code, self.http_reason, self.http_content)

        if not data_content:                                                    # error in request?
            return {}                                                           # return empty dictionary

        return data_content
