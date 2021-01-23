<<<<<<< HEAD
import optparse
import unittest
import sys
import string
import datetime

import common_lib.ServerAPI as ServerAPI
import common_lib.validation_lib as validation_lib
#import common_lib.server_config as server_config


################################################################################
# parse_arguments
#
#  Setup and validate the command-line arguements for the script
#
#  Returns :
#  structure of the command-line args
<<<<<<< HEAD
#  
=======
#
>>>>>>> b39f43628b6a8e9fdf6cf34e607460e7aff7758e
################################################################################
def parse_arguments(show_help=False):
    """ Option parser - Setup command-line options"""

    usage_text = "Usage: %prog  [--debug] [--help]"
    description_text = "Alpha Ori API testing."
    version_text = "%prog  v1.0 September 2017"
    epilog_text = "(c) 2017 Alpha Ori Ltd"

    # create option parser object
    parser = optparse.OptionParser(usage=usage_text,
                                   version=version_text,
                                   description=description_text,
                                   epilog=epilog_text)

    # general parameters
    general_opts = optparse.OptionGroup(parser, 'General Parameters', 'Running options :',)

    general_opts.add_option("--server", action="store",
                            dest="server_ip", default="ahab",
                            help="The Address of the Server.")

    general_opts.add_option("--port", action="store",
                            dest="port", default="3001",
                            help="The port")

    general_opts.add_option("--user", action="store",
                            dest="user", default="admin",
                            help="The User name")

    general_opts.add_option("--password", action="store",
                            dest="password", default="1",
                            help="The password")

    general_opts.add_option("--debug", action="store_true", dest="debug_flag",
                            default=False, help="Run script in debug mode - increased screen output. DEFAULT = False.")


    parser.add_option_group(general_opts)                                       # add general options

    (options, args) = parser.parse_args()

    if show_help:                                                               # if --help on cmd-line, show help exit
        parser.print_help()


    return options                                                              # send back all of the options


class SimpleTestCase(unittest.TestCase):

    config_info = None                                                          # set to command-line params dict when invoked below

    @classmethod
    def setUpClass(self):
        """ Runs at the start of the test """

        print("\n ** setUpClass - config_info **\n")
        print config_info

#        self.server_config_obj = server_config.server_config()
        self.util_lib = validation_lib.ut_validation_lib()

#        self.config_info_dict = self.util_lib.get_config("ahab_database.ini")
#        self.util_lib.DumpOutObject(self)

        self.dest_host = config_info.server_ip                                  # server location
        self.dest_port = config_info.port                                       # server port
        self.username = config_info.user                                        # user name & pw
        self.password = config_info.password
        self.debug = config_info.debug_flag

        self.secure_flag = False
        
        self.expected_result = 'ok'
        self.base_url = "http://%s:%s" % (self.dest_host, self.dest_port)

        # create server object - used to send API requests
        self.Server_Obj = ServerAPI.Server_API(self.dest_host, self.dest_port, secure=self.secure_flag, debug_flag=self.debug)

        login_url = "api/login"

        request = self.Server_Obj.GetLoginAuthToken(self.username, self.password, login_url)

        self.util_lib.DumpData(request, "\nServer API Payload  -  Login Status\n" )

        if not request:
            message = "%s : %s" % (self.Server_Obj.status_code, self.Server_Obj.http_content)
            exit_message = "\n** Error Getting Login Token  : %s  - %s : %s  %s" % (self.base_url, self.username, self.password, message)
            sys.exit(exit_message)

#        self.assertTrue(request, "Incorrect Login Status = %s" % request)

        self.author_id = self.Server_Obj.get_a_uuid()                           # get a UUID to create cases

        self.user_list = []


    @classmethod
    def tearDownClass(self):

        self.Server_Obj.DumpTimingData()


###############################################################################################################################################
    
    def test_001_get_system(self):
        """ Test GET Systems"""
    
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "api/get/getSystems"
        title = "List Systems in System"
    
        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)
    
        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)
    
        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))
    
        success_status = request['status']
        print("\n* Success = %s" % success_status)
    
        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

###############################################################################################################################################
###############################################################################################################################################

    def test_002_get_securityquestions(self):
        """ Test GET Security Questions"""
    
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "api/get/SecurityQuestions"
        title = "get Security Questions from System"
    
        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)
    
        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)
    
        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))
    
        success_status = request['status']
        print("\n* Success = %s" % success_status)
    
        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

###############################################################################################################################################
###############################################################################################################################################

    def test_003_get_caselogs(self):
        """ Test GET Case Logs"""
    
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "api/caselogs"
        title = "get Case Logs from System"
    
        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)
    
        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)
    
        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))
    
        success_status = request['status']
        print("\n* Success = %s" % success_status)
    
        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

###############################################################################################################################################
###############################################################################################################################################

    def test_004_get_roles(self):
        """ Test GET Roles"""
    
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "api/get/getRoles"
        title = "get Roles from System"
    
        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)
    
        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)
    
        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))
    
        success_status = request['status']
        print("\n* Success = %s" % success_status)
    
        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

##############################################################################################################################################
<<<<<<< HEAD
    def test_011_getallactivealertbyuser(self):
        """ Get All Active Alerts By User """
    
=======
def test_020_getallactivealertsbyuser(self):
        """ Get All Active Alerts By User """
    
        # create new vessel
>>>>>>> b39f43628b6a8e9fdf6cf34e607460e7aff7758e
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getAllActiveAlertByUser"
        title = "Get All Active Alerts By User"
<<<<<<< HEAD
=======
    
        #vessel_name = "AUTOMATION TEST SHIP"
        #last_port = "Tokyo"
        #next_port = "Oakland"
        #heartbeat_true = True
>>>>>>> b39f43628b6a8e9fdf6cf34e607460e7aff7758e

        # create active Alerts with these values
        activealerts_dict = { "name": "NotificationId",
                "tableID": 81008,
                "columnID": 1,
                "dataTypeID": 23,
                "dataTypeSize": 4,
                "dataTypeModifier": -1,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : activealerts_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetAllActiveAlertByUser Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)
<<<<<<< HEAD
        
##############################################################################################################################################
    def test_012_getallunreadalertbyuser(self):
        """ Get All Unread Alerts By User """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getAllUnreadAlertByUser"
        title = "Get All Unread Alerts By User"

        # create Unread Alerts with these values
        unreadalerts_dict = { "name": "AlertsEventXId",
                "tableID": 81055,
                "columnID": 1,
                "dataTypeID": 23,
                "dataTypeSize": 4,
                "dataTypeModifier": -1,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : unreadalerts_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetAllUnreadAlertByUser Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)
##############################################################################################################################################
    def test_013_getallalertbyuser(self):
        """ Get All Alerts By User """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getAllAlertByUser"
        title = "Get All Alerts By User"

        # create All Alerts with these values
        allalerts_dict = {   "name": "AlertsEventXId",
                "tableID": 81055,
                "columnID": 1,
                "dataTypeID": 23,
                "dataTypeSize": 4,
                "dataTypeModifier": -1,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : allalerts_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetAllAlertByUser Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)
        
##############################################################################################################################################
=======

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)
    
    
>>>>>>> b39f43628b6a8e9fdf6cf34e607460e7aff7758e
############################################################## Main ##########################################################################
##############################################################################################################################################
if __name__ == '__main__':

    config_info = parse_arguments()                                             # Get configuration arguments - exit on value validation failure

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    test_class = SimpleTestCase                                                 # create the test object from class above
    test_class.config_info = config_info                                        # assign the cmd-line values to the class
    
    tests = loader.loadTestsFromTestCase(test_class)                            # add all of the tests from class
    suite.addTest(tests)                                                        # add tests to suite
<<<<<<< HEAD
    print("\nno of test cases")
    print(suite.countTestCases)
=======

>>>>>>> b39f43628b6a8e9fdf6cf34e607460e7aff7758e
    unittest.TextTestRunner(verbosity=2).run(suite)                             # run the suite
=======
import optparse
import unittest
import sys
import string
import datetime

import common_lib.ServerAPI as ServerAPI
import common_lib.validation_lib as validation_lib
#import common_lib.server_config as server_config


################################################################################
# parse_arguments
#
#  Setup and validate the command-line arguements for the script
#
#  Returns :
#  structure of the command-line args
#
################################################################################
def parse_arguments(show_help=False):
    """ Option parser - Setup command-line options"""

    usage_text = "Usage: %prog  [--debug] [--help]"
    description_text = "Alpha Ori API testing."
    version_text = "%prog  v1.0 September 2017"
    epilog_text = "(c) 2017 Alpha Ori Ltd"

    # create option parser object
    parser = optparse.OptionParser(usage=usage_text,
                                   version=version_text,
                                   description=description_text,
                                   epilog=epilog_text)

    # general parameters
    general_opts = optparse.OptionGroup(parser, 'General Parameters', 'Running options :',)

    general_opts.add_option("--server", action="store",
                            dest="server_ip", default="ahab",
                            help="The Address of the Server.")

    general_opts.add_option("--port", action="store",
                            dest="port", default="3001",
                            help="The port")

    general_opts.add_option("--user", action="store",
                            dest="user", default="admin",
                            help="The User name")

    general_opts.add_option("--password", action="store",
                            dest="password", default="1",
                            help="The password")

    general_opts.add_option("--debug", action="store_true", dest="debug_flag",
                            default=False, help="Run script in debug mode - increased screen output. DEFAULT = False.")


    parser.add_option_group(general_opts)                                       # add general options

    (options, args) = parser.parse_args()

    if show_help:                                                               # if --help on cmd-line, show help exit
        parser.print_help()


    return options                                                              # send back all of the options


class SimpleTestCase(unittest.TestCase):

    config_info = None                                                          # set to command-line params dict when invoked below

    @classmethod
    def setUpClass(self):
        """ Runs at the start of the test """

        print("\n ** setUpClass - config_info **\n")
        print config_info

#        self.server_config_obj = server_config.server_config()
        self.util_lib = validation_lib.ut_validation_lib()

#        self.config_info_dict = self.util_lib.get_config("ahab_database.ini")
#        self.util_lib.DumpOutObject(self)

        self.dest_host = config_info.server_ip                                  # server location
        self.dest_port = config_info.port                                       # server port
        self.username = config_info.user                                        # user name & pw
        self.password = config_info.password
        self.debug = config_info.debug_flag

        self.secure_flag = False
        
        self.expected_result = 'ok'
        self.base_url = "http://%s:%s" % (self.dest_host, self.dest_port)

        # create server object - used to send API requests
        self.Server_Obj = ServerAPI.Server_API(self.dest_host, self.dest_port, secure=self.secure_flag, debug_flag=self.debug)

        login_url = "api/login"

        request = self.Server_Obj.GetLoginAuthToken(self.username, self.password, login_url)

        self.util_lib.DumpData(request, "\nServer API Payload  -  Login Status\n" )

        if not request:
            message = "%s : %s" % (self.Server_Obj.status_code, self.Server_Obj.http_content)
            exit_message = "\n** Error Getting Login Token  : %s  - %s : %s  %s" % (self.base_url, self.username, self.password, message)
            sys.exit(exit_message)

#        self.assertTrue(request, "Incorrect Login Status = %s" % request)

        self.author_id = self.Server_Obj.get_a_uuid()                           # get a UUID to create cases

        self.user_list = []


    @classmethod
    def tearDownClass(self):

        self.Server_Obj.DumpTimingData()


###############################################################################################################################################
    
    def test_001_get_system(self):
        """ Test GET Systems"""
    
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "api/get/getSystems"
        title = "List Systems in System"
    
        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)
    
        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)
    
        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))
    
        success_status = request['status']
        print("\n* Success = %s" % success_status)
    
        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

###############################################################################################################################################
###############################################################################################################################################

    def test_002_get_securityquestions(self):
        """ Test GET Security Questions"""
    
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "api/get/SecurityQuestions"
        title = "get Security Questions from System"
    
        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)
    
        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)
    
        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))
    
        success_status = request['status']
        print("\n* Success = %s" % success_status)
    
        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

###############################################################################################################################################
###############################################################################################################################################

    def test_003_get_caselogs(self):
        """ Test GET Case Logs"""
    
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "api/caselogs"
        title = "get Case Logs from System"
    
        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)
    
        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)
    
        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))
    
        success_status = request['status']
        print("\n* Success = %s" % success_status)
    
        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

###############################################################################################################################################
###############################################################################################################################################

    def test_004_get_roles(self):
        """ Test GET Roles"""
    
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "api/get/getRoles"
        title = "get Roles from System"
    
        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)
    
        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)
    
        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))
    
        success_status = request['status']
        print("\n* Success = %s" % success_status)
    
        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

##############################################################################################################################################
    def test_011_getallactivealertbyuser(self):
        """ Get All Active Alerts By User """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getAllActiveAlertByUser"
        title = "Get All Active Alerts By User"

        # create active Alerts with these values
        activealerts_dict = { "name": "NotificationId",
                "tableID": 81008,
                "columnID": 1,
                "dataTypeID": 23,
                "dataTypeSize": 4,
                "dataTypeModifier": -1,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : activealerts_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetAllActiveAlertByUser Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)
##############################################################################################################################################
    
    def test_012_getallunreadalertbyuser(self):
        """ Get All Unread Alerts By User """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getAllUnreadAlertByUser"
        title = "Get All Unread Alerts By User"

        # create unread Alerts with these values
        unreadalerts_dict = { "name": "AlertsEventXId",
                "tableID": 81055,
                "columnID": 1,
                "dataTypeID": 23,
                "dataTypeSize": 4,
                "dataTypeModifier": -1,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : unreadalerts_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetAllUnreadAlertByUser Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)
##############################################################################################################################################
    
    def test_013_getallalertbyuser(self):
        """ Get All Alerts By User """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getAllAlertByUser"
        title = "Get All Alerts By User"

        # create All Alerts with these values
        allalerts_dict = {  "name": "AlertsEventXId",
                "tableID": 81055,
                "columnID": 1,
                "dataTypeID": 23,
                "dataTypeSize": 4,
                "dataTypeModifier": -1,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : allalerts_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetAllAlertByUser Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)
##############################################################################################################################################
    def test_014_getreportconfigroles(self):
        """ Get Report Config Roles """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getReportConfigRoles"
        title = "Get Report Config Roles "

        # create config roles with these values
        configroles_dict = { "name": "id",
                "tableID": 97058,
                "columnID": 3,
                "dataTypeID": 23,
                "dataTypeSize": 4,
                "dataTypeModifier": -1,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : configroles_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetReportConfigRoles Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)
##############################################################################################################################################
       
        def test_015_setalertack(self):
          """ Set Alert Acknowledgement """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/setAlertAck"
        title = "Set Alert Acknowledgement "

        # Set Alert Acknowledgement with these values
        alertack_dict = {     "name": "error",
        "length": 248,
        "severity": "ERROR",
        "code": "23502",
        "detail": "Failing row contains (null, null, null, 158339, f, null, 2017-09-21 00:00:00).",
        "schema": "smartship",
        "table": "alertack",
        "column": "notificationxid",
        "file": "execMain.c",
        "line": "1734",
        "routine": "ExecConstraints"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : alertack_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nsetAlertAck Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

##############################################################################################################################################
        def test_016_getacknowledgements(self):
          """ Get Acknowledgements """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getAcknowledgements"
        title = "Get Acknowledgements "

        # Set Alert Acknowledgement with these values
        getack_dict = { "name": "acknote",
                "tableID": 81116,
                "columnID": 6,
                "dataTypeID": 25,
                "dataTypeSize": -1,
                "dataTypeModifier": -1,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : getack_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetAcknowledgements Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)
##############################################################################################################################################
        def test_017_getvesselmarkers(self):
          """ Get Vessel Markers """
    
        create_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    
        rest_api = "api/post/getVesselmarkers"
        title = "Get Vessel Markers  "

        # Set Alert Acknowledgement with these values
        getvesselmarkers_dict = { "name": "GPS_GLL_LATTITUDE_Normal_10",
                "tableID": 0,
                "columnID": 0,
                "dataTypeID": 1043,
                "dataTypeSize": -1,
                "dataTypeModifier": 24,
                "format": "text"
                        }

        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for getting the values
                      "Values" : getvesselmarkers_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\ngetVesselmarkers Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        #self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

##############################################################################################################################################
############################################################## Main ##########################################################################
##############################################################################################################################################
if __name__ == '__main__':

    config_info = parse_arguments()                                             # Get configuration arguments - exit on value validation failure

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    test_class = SimpleTestCase                                                 # create the test object from class above
    test_class.config_info = config_info                                        # assign the cmd-line values to the class
    
    tests = loader.loadTestsFromTestCase(test_class)                            # add all of the tests from class
    suite.addTest(tests)                                                        # add tests to suite

    unittest.TextTestRunner(verbosity=2).run(suite)                             # run the suite
>>>>>>> 8c6104466bb6f5a13caa2319c09aee51bb059e06
