import optparse
import unittest
import sys
import string
import datetime
import xmlrunner

import common_lib.ServerAPI as ServerAPI                                        # http request support
import common_lib.validation_lib as validation_lib                              # validation & utilities
import common_lib.DictDiffer as DictDiffer                                      # dictionary diff routines


class SimpleTestCase(unittest.TestCase):

    config_info = None                                                          # set to command-line params dict when invoked below

    @classmethod
    def setUpClass(self):
        """ Runs at the start of the test """

        self.util_lib = validation_lib.ut_validation_lib()

        print("\n ** setUpClass - Running Parameters in config_info **\n")
        print(config_info)
        print

        self.dest_host = config_info.server_ip                                  # server location
        self.dest_port = config_info.port                                       # server port
        self.username = config_info.user                                        # user name & pw
        self.password = config_info.password
        self.debug = config_info.debug_flag
        self.secure_flag = config_info.secure_flag
        self.expected_result = 'ok'

        secure_string = "s" if self.secure_flag else ""                         # set 's' for ssl or blank
        self.base_url = 'http%s://%s:%s' % (secure_string, self.dest_host, self.dest_port)     # create host string

        # create server object - used to send API requests
        self.Server_Obj = ServerAPI.Server_API(self.dest_host, self.dest_port, secure=self.secure_flag, debug_flag=self.debug)

        login_url = "api/login"
        request = self.Server_Obj.GetLoginAuthToken(self.username, self.password, login_url)

        self.util_lib.DumpData(request, "\nServer API Payload  -  Login Status\n" )

        if not request:
            message = "%s : %s" % (self.Server_Obj.status_code, self.Server_Obj.http_content)
            exit_message = "\n** Error Getting Login Token  : %s  - %s : %s  %s" % (self.base_url, self.username, self.password, message)
            sys.exit(exit_message)

        self.author_id = self.Server_Obj.get_a_uuid()                           # get a UUID to create cases

        self.user_list = []
        self.full_case_list = []
        self.full_alert_dict = {}


    @classmethod
    def tearDownClass(self):

        self.Server_Obj.DumpTimingData()                                        # print all requests made during test run


############################################################


    def test_01_get_users(self):
        """ Test GET users"""

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "v1/users"
        title = "List Users in System"

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        payload = request['result_data']
        self.util_lib.DumpData(payload, "\nALL Users Payload - %s : \n" % title)

        self.assertTrue(len(payload) == request['result_length'], "Incorrect Payload Size = %s" % request['result_length'])

        # get the details of each user - send 1 request per id

        for current_payload in payload:

            if "user_id" in current_payload:
                id = current_payload["user_id"]
                user_name = current_payload["username"]

                self.user_list.append([id, user_name])                          # save user id & name

                print("\nCase id = %s : %s\n") % (id, user_name)

                user_rest_api = "v1/users/%s" % id

                request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=user_rest_api, Show_Output=self.debug)

                if self.Server_Obj.status_code != 200:
                    self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

                success_status = request['status']

                self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

                self.util_lib.DumpData(request, "\nUser Payload - %s : \n" % id)


    def test_02_get_cases(self):
        """ Test GET Cases"""

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "v1/cases"
        title = "List Cases in System"

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))


        payload = request['result_data']

        for current_payload in payload:
            case_id = current_payload['case_id']
            case_num = current_payload['case_number']

            self.full_case_list.append([case_id, case_num])                     # save case_id & case_num


    def test_03_case_create_list_update_delete(self):
        """ Test case - create / list / update / delete """

        # create new case
        create_date = datetime.datetime.now().strftime("%Y-%m-%d")

        rest_api = "v1/cases"
        title = "CREATE/LIST/DELETE cases"

        case_title = "AUTOMATION TEST CASE"
        case_title_update = "** UPDATE AUTOMATION TEST CASE ***"

        case_description = "AUTOMATION TEST CASE DESCRIPTION"
        case_description_update = "** UPDATE AUTOMATION TEST CASE DESCRIPTION **"

        severity_value = "HIGH"
        severity_value_update = "LOW"

        v_code_value = "9998888"
        category_value = "REAL"
        status_value = "OPEN"
        system_type = "V"

        new_case_dict = {"title"        : case_title,
                         "description"  : case_description,
                         "originator"   : self.username,
                         "category"     : category_value,
                         "severity"     : severity_value,
                         "status"       : status_value,
                         "system_type"  : system_type,
                         "v_code"       : v_code_value,
                        }


        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for create
                      "Values" : new_case_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nCreate Case Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 201:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Create Success = %s" % success_status)

        self.assertTrue(success_status == "created", "Incorrect Status = %s" % success_status)

        case_id = request['case_id']
        case_number = request['case_number']

        # update dictionary - need KEYS = case_id / case_number / system_type / v_code
        update_case_dict = {"case_id"   : case_id,
                         "case_number"  : case_number,
                         "system_type"  : system_type,
                         "v_code"       : v_code_value,
                         "title"        : case_title_update,
                         "description"  : case_description_update,
                         "originator"   : self.username,
                         "category"     : category_value,
                         "severity"     : severity_value_update,
                         "status"       : status_value,
                         "modified_by"  : self.username,
                        }

        # List the content of the newly created vessel

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing

        case_rest_api = "v1/cases/%s" % case_id                                 # create url with case id

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=case_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* List Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        self.util_lib.DumpData(request, "\nList NEW Case Payload - %s : \n" % case_id)

        new_case_info_dict = request['result_data'][0]                          # save the new case listing


        # Update the newly created case

        parameters = {"Method" : self.Server_Obj.Method_PUT,                    # PUT request to update
                      "Values" : update_case_dict
                     }

        update_request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=case_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = update_request['status']
        print("\n* Update Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

        self.util_lib.DumpData(update_request, "\nUpdated Case Payload - %s : \n" % case_id)


        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing
        list_request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=case_rest_api, Show_Output=self.debug)

        success_status = list_request['status']
        print("\n* Update List Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        self.util_lib.DumpData(list_request, "\nList Update Case Payload - %s : \n" % case_id)

        update_case_info_dict = list_request['result_data'][0]                  # save the update case listing


        # Delete the newly created case

        parameters = {"Method" : self.Server_Obj.Method_DELETE}                 # DELETE request

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=case_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

        self.util_lib.DumpData(request, "\nDelete Case Payload - %s : \n" % case_id)

        # if not case_info_dict:                                                  # make sure the new case has data
        #     self.fail("Invalid NEW case_info : %s " % case_info_dict)


        field_dict = {'title'           : case_title,                          # validate fields in the case create against this dict
                      'case_id'         : case_id,
                      'case_description': case_description,
                      'created_date'    : create_date,
                      'category'        : category_value,
                      'severity'        : severity_value,
                      'status'          : status_value,
                      'system_type'     : system_type,
                      'v_code'          : v_code_value,
                      'originator'      : self.username,
                      }

        bad_list = self.util_lib.Compare_Dictionarys(new_case_info_dict, field_dict)          # store mismatched values in this list

        update_field_dict = {'title'          : case_title_update,                          # validate fields in the case create against this dict
                            'case_id'         : case_id,
                            'case_description': case_description_update,
                            'created_date'    : create_date,
                            'category'        : category_value,
                            'severity'        : severity_value_update,
                            'status'          : status_value,
                            'system_type'     : system_type,
                            'v_code'          : v_code_value,
                            'modified_by'     : self.username,
                            'modified_date'   : create_date,
                      }

        update_bad_list = self.util_lib.Compare_Dictionarys(update_case_info_dict, update_field_dict)                                                    # store mismatched values in this list

        # bad_list & update_bad_list should be empty if all fields match - otherwise fail
        self.assertTrue(len(bad_list) == 0, "Mismatched New Case Field Values :\n\n%s\n" % string.join(bad_list, "\n"))
        self.assertTrue(len(update_bad_list) == 0, "Mismatched UPDATE Case Field Values :\n\n%s\n" % string.join(update_bad_list, "\n"))


    def test_04_caselogs(self):
        """ Test GET Caselogs"""

        rest_api = "v1/caselogs"
        title = "GET Caselogs"
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))


        payload = request['result_data']
        self.util_lib.DumpData(payload, "\nCaseLogs Payload - %s : \n" % title)

        self.assertTrue(len(payload) == request['result_length'], "Incorrect Payload Size = %s" % request['result_length'])


        for current_payload in payload:                                         # get the details of each case - send 1 request per id

            if "case_log_id" in current_payload:
                id = current_payload["case_log_id"]                             # get the case id
                print("\nCase id = %s\n") % id

                case_rest_api = "v1/caselogs/%s" % id                           # create url with case id

                request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=case_rest_api, Show_Output=self.debug)

                if self.Server_Obj.status_code != 200:
                    self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

                success_status = request['status']
                print("\n* Success = %s" % success_status)

                self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

                self.util_lib.DumpData(request, "\nCaselog Payload - %s : \n" % id)


    def test_05_vesselinfos(self):
        """ Test GET vesselinfos"""

        rest_api = "v1/vesselinfos"
        title = "GET vesselinfos"
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))


        payload = request['result_data']
        self.util_lib.DumpData(payload, "\nVesselinfo Payload - %s : \n" % title)

        self.assertTrue(len(payload) == request['result_length'], "Incorrect Payload Size = %s" % request['result_length'])

        for current_payload in payload:                                         # get the details of each case - send 1 request per id

            if "vessel_info_id" in current_payload:
                id = current_payload["vessel_info_id"]                          # get the vessel id
                print("\nVessel id = %s\n") % id

                vessel_rest_api = "v1/vesselinfos/%s" % id                      # create url with vessel id

                request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=vessel_rest_api, Show_Output=self.debug)

                if self.Server_Obj.status_code != 200:
                    self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

                success_status = request['status']
                print("\n* Success = %s" % success_status)

                self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

                self.util_lib.DumpData(request, "\nVessel Payload - %s : \n" % id)


    def test_06_vesselinfos_create_list_update_delete(self):
        """ Test vesselinfos - create / list / update / delete - BUG SMAR-5072 - default date issue"""

        # create new vessel
        create_date = datetime.datetime.now().strftime("%Y-%m-%d")

        rest_api = "v1/vesselinfos"
        title = "CREATE/LIST/DELETE vesselinfos"

        vessel_name = "AUTOMATION TEST SHIP"
        last_port = "Tokyo"
        next_port = "Oakland"
        heartbeat_true = True
        speed = 12

        # create vessel with these values
        new_vessel_dict = { "asset_name"    : vessel_name,
                            "speed"         : speed,
                            "adt"           : "20/7",
                            "next_port"     : next_port,
                            "last_port"     : last_port,
                            "heartbeat"     : heartbeat_true,
                            "created_date"  : create_date,
                            "last_date_updated": create_date,
                            "imo_number"    : "99999",
                            "status"        : "UnderWay Using Engine",
                            "eta_hours"     : 20,
                            "eta_month"     : 6,
                            "merpm"         : 100.99,
                            "atd_hours"     : 14,
                            "atd_month"     : 6
                        }


        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for create
                      "Values" : new_vessel_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nCreate Vessel Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 201:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == "created", "Incorrect Status = %s" % success_status)
        vessel_id = request['vessel_info_id']                                   # save the created id

        # List the content of the newly created vessel

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing
        vessel_rest_api = "v1/vesselinfos/%s" % vessel_id                       # create url with vessel id

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=vessel_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        self.util_lib.DumpData(request, "\nList Vessel Payload - %s : \n" % vessel_id)

        vessel_info_dict = request['result_data'][0]                            # save the vessel listing

        # Delete the newly created vessel

        parameters = {"Method" : self.Server_Obj.Method_DELETE}                 # DELETE request

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=vessel_rest_api, Show_Output=self.debug)

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

        self.util_lib.DumpData(request, "\nDelete Vessel Payload - %s : \n" % vessel_id)

        field_dict = {'asset_name'      : vessel_name,                          # validate fields in the ship create against this dict
                      'speed'           : speed,
                      'vessel_info_id'  : vessel_id,
                      'created_by'      : self.username,
                      'created_date'    : create_date,
                      'modified_date'   : create_date,
                      'last_date_updated' : create_date,
                      'last_port'       : last_port,
                      'next_port'       : next_port,
                      'heartbeat'       : heartbeat_true
                      }

        bad_list = self.util_lib.Compare_Dictionarys(vessel_info_dict, field_dict)   # compare the values                                                        # store mismatched values in this list

        # bad_list should be empty if all fields match - otherwise fail
        self.assertTrue(len(bad_list) == 0, "Mismatched New Vessel Field Values :\n\n%s\n" % string.join(bad_list, "\n"))



    def test_07_get_vessels(self):
        """ Test GET vessels"""

        rest_api = "v1/vessels"
        title = "GET vessels"
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))


        try:
            payload = request['result_data']
            self.util_lib.DumpData(payload, "\nVessels Payload - %s : \n" % title)
        except Exception:
            self.fail("NO Vessels Found In System - Expecting at least 1+ Vessels to be found.  Failing This Test...")


        self.assertTrue(len(payload) == request['result_length'], "Incorrect Payload Size = %s" % request['result_length'])

        for current_payload in payload:                                         # get the details of each case - send 1 request per id

            if "vessel_id" in current_payload:
                vessel_id = current_payload["vessel_id"]                        # get the vessel id

                vessel_rest_api = "v1/vessels/%s" % vessel_id                   # create url with vessel id
                vessel_assets_api = "v1/vessels/%s/assets/" % vessel_id         # create assets url with vessel id

                request_vessel = self.Server_Obj.SendRestPayload(request_payload=parameters, url=vessel_rest_api, Show_Output=self.debug)

                success_status = request_vessel['status']
                print("\n* Success = %s" % success_status)

                self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

                self.util_lib.DumpData(request_vessel, "\nVessel Payload - %s : \n" % vessel_id)

                payload_vessel = request_vessel['result_data'][0]


                if "imo_number" in payload_vessel:
                    imo_number = current_payload["imo_number"]                 # get the imo_number

                    vessel_position_api = "v1/vessels/%s/positions/" % imo_number    # create url with imo number

                    request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=vessel_position_api, Show_Output=self.debug)

                    if self.Server_Obj.status_code != 200:
                        self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

                    success_status = request['status']
                    print("\n* Success = %s" % success_status)

                    self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

                    self.util_lib.DumpData(request, "\nVessel Position Payload - %s : %s : \n" % (vessel_id, imo_number))

                # get assets

                request_asset = self.Server_Obj.SendRestPayload(request_payload=parameters, url=vessel_assets_api, Show_Output=self.debug)

                if self.Server_Obj.status_code != 200:
                    self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

                success_status = request_asset['status']
                print("\n* Success = %s" % success_status)

                self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

                self.util_lib.DumpData(request_asset, "\nVessel Asset Payload - %s : \n" % vessel_id)


        self.util_lib.DumpData(SimpleTestCase.user_list, "\n** Users =  **\n" )

        for current_user in SimpleTestCase.user_list:

            vessel_user_api = "v1/vessels/users/%s" % current_user[0]         # create url with vessel id (current_user = [id, username])
            print("\n?? Current User = %s  : %s ?? \n") % (current_user, vessel_user_api)

            request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=vessel_user_api, Show_Output=self.debug)

            if self.Server_Obj.status_code != 200:
                self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

            success_status = request['status']
            print("\n* Success = %s" % success_status)

            self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

            self.util_lib.DumpData(request, "\n?? Vessel Users Payload - %s : VALID DATA ?? \n" % current_user)



    def test_08_users_create_list_update_delete(self):
        """ Test users - create / list / update / delete """

        # create new user
        create_date = datetime.datetime.now().strftime("%Y-%m-%d")

        rest_api = "v1/users"
        title = "CREATE/LIST/DELETE users"

        user_name = "automation"
        email = "qa@alphaori.sg"

        name = "Automation User"
        name_updated = "** UPDATED Automation User **"

        user_type = "Normal"

        mobile_phone = "1-408-111-1111"
        mobile_phone_updated = "1-408-222-2222"

        is_active = True
        company_id = "1d8d5e7a-f95f-4219-b371-7539ef3ba368"
        question = 1
        answer = "smartship"

        # create user with these values
        new_user_dict = {   "username"      : user_name,
                            "email"         : email,
                            "name"          : name,
                            "mobile"        : mobile_phone,
                            "user_type"     : user_type,
                            "is_active"     : is_active,
                            "company_id"    : company_id,
                            "file_path"     : "/Users/%s" % user_name,
                            "question"      : question,
                            "answer"        : answer,
                            "login_attempt" : 0,
                            "user_token"    : ""
                        }


        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for create
                      "Values" : new_user_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nCreate User Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 201:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == "created", "Incorrect Status = %s" % success_status)
        user_id = request['user_id']                                            # save the created id


        # update dictionary - need KEYS = case_id / case_number / system_type / v_code
        update_user_dict = {"username"      : user_name,
                            "user_id"       : user_id,
                            "email"         : email,
                            "name"          : name_updated,
                            "mobile"        : mobile_phone_updated,
                            "user_type"     : user_type,
                            "is_active"     : is_active,
                            "company_id"    : company_id,
                            "file_path"     : "/Users/%s" % user_name,
                            "question"      : question,
                            "answer"        : answer,
                            "login_attempt" : 0,
                            "user_token"    : ""
                        }


        # List the content of the newly created user

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing
        user_rest_api = "v1/users/%s" % user_id                                 # create url with user id

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=user_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        self.util_lib.DumpData(request, "\nList User Payload - %s : \n" % user_id)

        user_info_dict = request['result_data'][0]                              # save the user listing


        # Update the newly created user

        parameters = {"Method" : self.Server_Obj.Method_PUT,                    # PUT request to update
                      "Values" : update_user_dict
                     }

        update_request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=user_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = update_request['status']
        print("\n* Update Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

        self.util_lib.DumpData(update_request, "\nUpdated User Payload - %s : \n" % user_id)


        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing
        list_request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=user_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = list_request['status']
        print("\n* Update List Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        self.util_lib.DumpData(list_request, "\nList Update User Payload - %s : \n" % user_id)

        update_user_info_dict = list_request['result_data'][0]                  # save the update user listing


        # Delete the newly created user

        parameters = {"Method" : self.Server_Obj.Method_DELETE}                 # DELETE request

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=user_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

        self.util_lib.DumpData(request, "\nDelete User Payload - %s : \n" % user_id)


        bad_list = self.util_lib.Compare_Dictionarys(user_info_dict, new_user_dict)   # compare the values                                                        # store mismatched values in this list
        update_bad_list = self.util_lib.Compare_Dictionarys(update_user_info_dict, update_user_dict)

        # bad_list should be empty if all fields match - otherwise fail
        self.assertTrue(len(bad_list) == 0, "Mismatched New User Field Values :\n\n%s\n" % string.join(bad_list, "\n"))
        self.assertTrue(len(update_bad_list) == 0, "Mismatched Update User Field Values :\n\n%s\n" % string.join(update_bad_list, "\n"))


    def test_09_users_create_duplicate(self):
        """ Test users - create duplicate - should fail"""

        # create duplicate user
        create_date = datetime.datetime.now().strftime("%Y-%m-%d")

        rest_api = "v1/users"
        title = "CREATE Duplicate users - should fail"

        email = "qa@alphaori.sg"
        name = "Automation User"
        user_type = "Normal"
        mobile_phone = "1-408-111-1111"
        is_active = True
        company_id = "1d8d5e7a-f95f-4219-b371-7539ef3ba368"
        question = 1
        answer = "smartship"

        for current_user in SimpleTestCase.user_list:
            user_name = current_user[1]                                         # get an existing username - from element 1 = [id, username]

            # create a duplicate user with these values - expecting fail
            new_user_dict = {   "username"      : user_name,
                                "email"         : email,
                                "name"          : name,
                                "mobile"        : mobile_phone,
                                "user_type"     : user_type,
                                "is_active"     : is_active,
                                "company_id"    : company_id,
                                "file_path"     : "/Users/%s" % user_name,
                                "question"      : question,
                                "answer"        : answer,
                                "login_attempt" : 0,
                                "user_token"    : ""
                            }


            parameters = {"Method" : self.Server_Obj.Method_POST,               # POST request for create
                          "Values" : new_user_dict
                         }

            # run request - expect status code 400 for duplicate
            request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

            self.util_lib.DumpData(request, "\nCreate Duplicate User Payload - %s : \n" % title)

            if self.Server_Obj.status_code != 400:
                self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

            success_status = request['status']
            status_message = request['message']

            print("\n* Dupe User Create Returns = %s : %s" % (success_status, status_message))

            self.assertTrue(success_status == "bad request", "Incorrect Status = %s" % success_status)
            self.assertIn("already exist", status_message, "Incorrect error message = %s" % status_message)



    def test_10_get_cases_with_parameters(self):
        """ Test GET Cases with parameters : ?fields=count  ?status=open"""

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request
        rest_api = "v1/cases?"
        title = "List Cases in System with parameters : "

        # run requests with this parameters on cases with status and count combinations:

        status_list = ["OPEN", "CLOSED", "ACTIVE", "UNREAD"]                    # case status values

        parameter_list = ["fields=count"]
        field_list = ["fields=count&", "status="]                               # request query fields

        all_status = map(lambda x: field_list[1]+str(x), status_list)           # map all statuses
        parameter_status_list = map(lambda x: field_list[0]+str(x), all_status) # map field + status

        parameter_list.extend(all_status)                                       # extend lists
        parameter_list.extend(parameter_status_list)                            # all combinations of fields + status


        for current_parameter in parameter_list:                                # run each request value

            request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api + current_parameter, Show_Output=self.debug)

            self.util_lib.DumpData(request, "\nAPI Payload - Cases with parameters - %s : \n" % current_parameter)

            if self.Server_Obj.status_code != 200:
                self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

            success_status = request['status']
            print("\n* Success = %s" % success_status)

            self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

            payload = request['result_data']

            if 'count' in payload:                                              # get the length of the payload
                payload_len = payload['count']                                  # count only - use this
            else:
                payload_len = len(payload)                                      # otherwise - use len() of payload

            result_len = request['result_length']                               # api returned value

            self.assertEqual(payload_len, result_len, "%s :: Mismatched payload_length : %s vs %s" % (current_parameter, payload_len, result_len))

            self.util_lib.DumpData(payload, "\nAPI Payload - %s : \n" % current_parameter)


    def test_11_get_alerts_events(self):
        """ Test GET Alerts-Events"""

        rest_api = "v1/alerts-events"
        title = "GET alerts-events"
        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        payload = request['result_data']

        self.util_lib.DumpData(payload, "\nAlerts-Events Payload - %s : \n" % title)

        self.assertTrue(len(payload) == request['result_length'], "Incorrect Payload Size = %s" % request['result_length'])


        for current_payload in payload:                                         # iterate thru all alerts found

            if 'alerts_events_id' in current_payload:
                event_id = current_payload['alerts_events_id']

                temp_list = [current_payload['name'], current_payload['description'] ]

                self.full_alert_dict[event_id] = temp_list

                alert_api = "v1/alerts-events/%s" % event_id                    # the specific event id
                parameters = {"Method" : self.Server_Obj.Method_GET}            # GET request

                alert_request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=alert_api, Show_Output=self.debug)

                self.util_lib.DumpData(request, "\nAPI Payload - %s : \n" % event_id)

                if self.Server_Obj.status_code != 200:
                    self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

                success_status = alert_request['status']
                print("\n* Success = %s" % success_status)

                self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

                payload = alert_request['result_data']

                self.util_lib.DumpData(payload, "\nAlerts-Events Payload - %s : \n" % event_id)


        self.util_lib.DumpData(self.full_alert_dict, "\nAlert Event Dict : \n")



    def test_12_alerts_create_list_update_delete(self):
        """ Test alerts - create / list / update / delete - BUG SMAR-5211 : Nested Update fields are set to NONE"""

        # create new alert
        create_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        rest_api = "v1/alerts-events"
        title = "CREATE/LIST/DELETE alerts"

        user_name = "automation"
        email = "qa@alphaori.sg"

        name = "Automation Alert Test Case"
        name_updated = "** UPDATED Automation Alert Test Case **"

        description = "The Automated Alert Description"
        description_updated = "** UPDATED The Automated Alert Description **"

        is_active = True
        company_id = "1d8d5e7a-f95f-4219-b371-7539ef3ba368"

        # create alert with these values
        new_alert_dict = {"name"            : name,
                        "description"       : description,
                        "probable_causes"   : "Probable causes and suggested measures",
                        "sensor_system": { "sensor_system_number": 1,
                                           "systems"             : "Huge and Cargo",
                                           "system_url"          : "huge-and-cargo",
                                           "is_active"           : is_active
                                         },
                        "is_vessel_alert"   : False,
                        "is_active"         : is_active,
                        "alert_type": { "alert_type_number" : 1,
                                        "name"              : "Technical Alert",
                                        "is_active"         : is_active,
                                        "priority"          : 1
                                      },
                        "alert_priority": { "alert_priority_number" : 1,
                                            "name"                  : "Critical",
                                            "is_active"             : is_active
                                          },
                        "delay"     : 0,
                        "company_id": company_id,
                        "formula_string"        : "average(AUX_BOILER_EXH_GAS_OUT_TEMP, CHS_GAS_DETECTED_ALARM) > 0",
                        "ui_formula_structure"  : "[{\n\t\titemType: \"operator\",\n\t\tvalue: \"average\",\n\t\tid: \"81e464ac-6a09-4724-81a1-9e7d959c58c8\"\n\t}",
                        "imo_number"        : "9497177",
                        "last_updated_delay": 3,
                        "modified_date"     : create_date,
                        "created_date"      : create_date,
                        "modified_by"       : self.username,
                        "created_by"        : self.username
                        }


        parameters = {"Method" : self.Server_Obj.Method_POST,                   # POST request for create
                      "Values" : new_alert_dict
                     }

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=rest_api, Show_Output=self.debug)

        self.util_lib.DumpData(request, "\nCreate Alert Payload - %s : \n" % title)

        if self.Server_Obj.status_code != 201:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == "created", "Incorrect Status = %s" % success_status)
        alert_id = request['alerts_events_id']                                   # save the created id


        # update dictionary - need KEYS = case_id / case_number / system_type / v_code
#        update_alert_dict = new_alert_dict

        # change these values for update
        # update_alert_dict["name"] = name_updated
        # update_alert_dict["description"] = description_updated
        # update_alert_dict["alerts_events_id"] = alert_id
#        update_alert_dict["company_id"] = company_id

        update_alert_dict = {"name"             : name,
                            "description"       : description_updated,
                            "alerts_events_id"  : alert_id,
                            "company_id"        : company_id,
                            "probable_causes"   : "Probable causes and suggested measures",
                            "sensor_system": { "sensor_system_number": 1,
                                                "systems"             : "Huge and Cargo",
                                                "system_url"          : "huge-and-cargo",
                                                "is_active"           : is_active
                                         },
                            "is_vessel_alert"   : False,
                            "is_active"         : is_active,
                            "alert_type": { "alert_type_number" : 1,
                                            "name"              : "Technical Alert",
                                            "is_active"         : is_active,
                                            "priority"          : 1
                                      },
                            "alert_priority": { "alert_priority_number" : 1,
                                                "name"                  : "Critical",
                                                "is_active"             : is_active
                                              },
                            "delay"                 : 0,
                            "formula_string"        : "average(AUX_BOILER_EXH_GAS_OUT_TEMP, CHS_GAS_DETECTED_ALARM) > 0",
                            "ui_formula_structure"  : "[{\n\t\titemType: \"operator\",\n\t\tvalue: \"average\",\n\t\tid: \"81e464ac-6a09-4724-81a1-9e7d959c58c8\"\n\t}",
                            "imo_number"            : "9497177",
                            "last_updated_delay"    : 3,
                            "modified_date"         : create_date,
                            "modified_by"           : self.username

                        }


        # List the content of the newly created alert

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing
        alert_rest_api = "v1/alerts-events/%s" % alert_id                       # create url with alert id

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=alert_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        self.util_lib.DumpData(request, "\nList Alert Payload - %s : \n" % alert_id)

        alert_info_dict = request['result_data'][0]                             # save the alert listing


        # Update the newly created alert

        parameters = {"Method" : self.Server_Obj.Method_PUT,                    # PUT request to update
                      "Values" : update_alert_dict
                     }

        update_request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=alert_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = update_request['status']
        print("\n* Update Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

        self.util_lib.DumpData(update_request, "\nUpdated Alert Payload - %s : \n" % alert_id)


        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing
        list_request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=alert_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = list_request['status']
        print("\n* Update List Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

        self.util_lib.DumpData(list_request, "\nList Update Alert Payload - %s : \n" % alert_id)

        update_alert_info_dict = list_request['result_data'][0]                 # save the update alert listing
#        update_alert_info_dict = list_request['result_data']                 # save the update alert listing


        # Delete the newly created alert

        parameters = {"Method" : self.Server_Obj.Method_DELETE}                 # DELETE request

        request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=alert_rest_api, Show_Output=self.debug)

        if self.Server_Obj.status_code != 200:
            self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

        success_status = request['status']
        print("\n* Success = %s" % success_status)

        self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s" % success_status)

        self.util_lib.DumpData(request, "\nDelete Alert Payload - %s : \n" % alert_id)


#        bad_list = self.util_lib.Compare_Dictionarys(alert_info_dict, new_alert_dict)   # compare the values                                                        # store mismatched values in this list
#        update_bad_list = self.util_lib.Compare_Dictionarys(update_alert_info_dict, update_alert_dict)

        # bad_list should be empty if all fields match - otherwise fail
        # self.assertTrue(len(bad_list) == 0, "Mismatched New Alert Field Values :\n\n%s\n" % string.join(bad_list, "\n"))
        # self.assertTrue(len(update_bad_list) == 0, "Mismatched Update Alert Field Values :\n\n%s\n" % string.join(update_bad_list, "\n"))

#        self.util_lib.DumpData(bad_list, "\nBad_List Payload : \n")
#        self.util_lib.DumpData(update_bad_list, "\nUpdate_Bad Payload : \n")

        diffObj = DictDiffer.DictDiffer( new_alert_dict, alert_info_dict)       # compare the values
        temp_dict_new = diffObj.all_diffs()

        diffObj = DictDiffer.DictDiffer(update_alert_dict, update_alert_info_dict)   # compare the values
        temp_dict_update = diffObj.all_diffs()


        diffObj = DictDiffer.DictDiffer(alert_info_dict, update_alert_info_dict)       # compare the values
        temp_dict_list = diffObj.all_diffs()

        self.util_lib.DumpData(temp_dict_new, "\nDiffDict New Payload : \n")
        self.util_lib.DumpData(temp_dict_update, "\nDiffDict Update Payload : \n")
        self.util_lib.DumpData(temp_dict_list, "\nDiffDict List Update Payload - BUG SMAR-5211 : \n")

        self.assertFalse(temp_dict_list, "List Update Payload - BUG SMAR-5211 - Nested Values set to None")



    def test_13_user_alerts(self):
        """ Test GET users with alerts - BUG SMAR-5211 : incorrect result_length."""

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing

        bad_list = []

        for current_user in SimpleTestCase.user_list:

            alert_user_api = "v1/users/%s/alerts" % current_user[0]             # create url with alerts by user id (current_user = [id, username])
            print("\n %s  \n") % (alert_user_api)

            request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=alert_user_api, Show_Output=self.debug)

            if self.Server_Obj.status_code != 200:
                self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

            success_status = request['status']
            print("\n* Success = %s" % success_status)

            self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

            self.util_lib.DumpData(request, "\nAlert Users Payload - %s  \n" % current_user)

            payload = request['result_data']

            payload_len = len(payload)                                          # use len() of payload
            result_len = request['result_length']                               # api returned value

            if payload_len != result_len:
                bad_list.append("%s : %s vs %s" % (current_user[0], payload_len, result_len))


        self.assertTrue(len(bad_list) == 0, "Mismatched Alert Length Values :\n\n%s\n" % string.join(bad_list, "\n"))


    def test_14_user_alerts_with_parameters(self):
        """ Test GET users with alerts with parameters - BUG SMAR-5211 : incorrect result_length."""

        parameters = {"Method" : self.Server_Obj.Method_GET}                    # GET request for listing

        alert_status_list = ["is_active=true",                                  # parameters to add to query
                             "is_active=false",
                             "is_read=true",
                             "is_read=false",
                             "is_active=true&is_read=true",
                             "is_active=true&is_read=false",
                             "is_active=false&is_read=true",
                             "is_active=false&is_read=false",
                            ]

        bad_list = []

        for current_user in SimpleTestCase.user_list:

            for current_status in alert_status_list:
                alert_user_api = "v1/users/%s/alerts?%s" % (current_user[0], current_status)             # create url with alerts by user id (current_user = [id, username])
                print("\n %s - %s ?? \n") % ( current_status, alert_user_api)

                request = self.Server_Obj.SendRestPayload(request_payload=parameters, url=alert_user_api, Show_Output=self.debug)

                if self.Server_Obj.status_code != 200:
                    self.fail("%s : %s - %s" % (self.Server_Obj.status_code, self.Server_Obj.http_reason, self.Server_Obj.server_error_message))

                success_status = request['status']
                print("\n* Success = %s" % success_status)

                self.assertTrue(success_status == self.expected_result, "Incorrect Status = %s  expecting : %s" % (success_status, self.expected_result))

                self.util_lib.DumpData(request, "\nAlert Users Payload - %s : \n" % current_user[0])

                payload = request['result_data']

                payload_len = len(payload)                                      # use len() of payload
                result_len = request['result_length']                           # api returned value

                if payload_len != result_len:
                    bad_list.append("%s - %-30s : %s vs %s" % (current_user[0], current_status,  payload_len, result_len))


        self.assertTrue(len(bad_list) == 0, "Mismatched Alert Length Values :\n\n%s\n" % string.join(bad_list, "\n"))


if __name__ == '__main__':

    validation_lib_obj = validation_lib.ut_validation_lib()                     # create the validation object -

    config_info = validation_lib_obj.parse_arguments()                          # Get configuration arguments - exit on value validation failure

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    test_class = SimpleTestCase                                                 # create the test object from class above
    test_class.config_info = config_info                                        # assign the cmd-line values to the class

    tests = loader.loadTestsFromTestCase(test_class)                            # add all of the tests from class
    suite.addTest(tests)                                                        # add tests to suite

    if config_info.xml_flag:
        test_results = xmlrunner.XMLTestRunner(verbosity=3, descriptions=True).run(suite)      # run the suite with xml output
    else:
        test_results = unittest.TextTestRunner(verbosity=3).run(suite)          # run the suite

    validation_lib_obj.getRunStats(test_results)

