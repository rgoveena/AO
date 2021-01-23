*** Settings ***

Library     RequestsLibrary
Library     Collections
Library     json
Library     String


Suite Teardown      Delete All Sessions

*** Variables ***

${SERVER}           ahab:3000                                                   # server + port to connect
${SERVER_URL}       http://${SERVER}                                            # full server url 
${LOGIN_URL}        /api/login                                                  # API to get login token
${SERVICE_NAME}     server_check                                                # name of connection
${USER}             admin                                                       # username in system
${PASSWORD}         1                                                           # password for username



*** Test Cases ***

Get Login Token
    [Documentation]     Heartbeat Test of SMARTShip - get login token via API request
    [Tags]  post    Heartbeat   token

    # setup request headers & login info
    ${headers}=     Create Dictionary   accept=application/json  X-Original-User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/55.0
    ${data_dict}=   Create Dictionary   username=${USER}     password=${PASSWORD}
  
    ${string_json}=     json.dumps  ${data_dict}                                # convert dict to json value - double quoted key/value pairs
    
    # create the http session
    Create session   ${SERVICE_NAME}    ${SERVER_URL}   headers=${headers}   debug=2   max_retries=1

    # send the POST request to server - get back response -
    # BUG SMAR-4990 - happens when string_json has double-quotes around key/value pairs
    
#    ${response}=    Post Request     ${SERVICE_NAME}    ${LOGIN_URL}    data=${string_json}  headers=${headers}  allow_redirects=False
#    ${response}=    Post Request     ${SERVICE_NAME}    ${LOGIN_URL}    params=${string_json}  headers=${headers}  allow_redirects=False

    # bug workaround - use single quoted dictionary values with params instead of data
    ${response}=    Post Request     ${SERVICE_NAME}    ${LOGIN_URL}    params=${data_dict}  headers=${headers}  allow_redirects=False

    Log  ${response.text}
  
    Should be equal as numbers   ${response.status_code}     200
    ...  Expected a status code of 200 but got ${response.status_code}


    ${json_response}=  To JSON   ${response.content}    

    # get the status key from the response - expecting value ok
    ${status_value}=  Get From Dictionary     ${json_response}    status

    Should Be Equal As Strings  ${status_value}     ok      msg=Expecting status value 'ok' - got ${status_value}
    
    # validate the fetched token

    Dictionary Should Contain Key   ${json_response}    token       msg=Cannot Get Token from response

    # get all keys from jsone_response
    ${dict_keys_list}=       Get Dictionary Keys     ${json_response}

    # these are the expected keys for the payload
    ${expected_keys_list}=    Create List   login_attempt  login_time  status  token   user_id   user_role   username

    Lists Should Be Equal   ${dict_keys_list}    ${expected_keys_list}          # compare returned keys against expected keys


    ${token_value}=     Get From Dictionary     ${json_response}    token       # get the token value from json_response
    ${token_length}=    Get Length   ${token_value}

    # validate the length of token
    Should Be True      ${token_length} > 619                                   # token is 620 chars
