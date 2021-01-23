import paramiko
# Install the Python paramiko package : sudo apt-get install python-paramiko

import string
import StringIO
import os
import os.path
import glob
import socket

#import DumpObject                   # custom function to dump out an object

def dump_out_object(the_object, maxlen=100, lindent=25, maxspew=9000, msg=None):

    if msg:
        print(msg)

    DumpObject.dumpObj(the_object, maxlen, lindent, maxspew)


################################################################################
#  remoteCMDRunner
#  Run commands on a remote system using Paramiko package (MUST be installed on host)
#
#  Basic Usage to run a remote command :
#
# host = 'hostname | IPAddress'
# username = 'userID'
# password = 'somepassword'
#
# RemoteCMDObj = remoteCMDRunner(True) # debug turned on
#
# if RemoteCMDObj.connectToHost(host, username, password):
#    cmd_line = 'ls -la'
#
#    if RemoteCMDObj.runRemoteCMD(cmd_line, False, True):
#        output_string = RemoteCMDObj.getOutputAsString()
#        print output_string
#
#    RemoteCMDObj.closeRemoteConnection()
#
################################################################################


class remoteCMDRunner():

################################################################################
# Parameters :
#  debug : boolean = flag for DEBUG output in the class
#
# Returns :
#  True - connection success
#  False - connection failure
################################################################################

    def __init__(self, debug=False):
        """Constructor"""

        self.debug = debug
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.SFTP_port = 22
        self.BUFFER_SIZE = 1024                         # std output buffer size
        self.host = None
        self.user_name = None
        self.password = None


################################################################################
#  connectToHost
#  Establish a connection to the remote system.
#
# Parameters :
#  host : string = the name OR IP of host
#  user : string = user name on remote system
#  password : string = password for above user
#
# Returns :
#  True - connection success
#  False - connection failure
################################################################################

    def connectToHost(self, host, user, password):
        """Establish a connection to the remote system."""

        return_value = False

        self.host = host                     # save passed in variables to class
        self.user_name = user
        self.password = password

        try:                                 # connect to remote host
            if self.debug:
                print("RemoteCMDRun::connectToHost - Connecting to host : %s  %s/%s") % (self.host, self.user_name, self.password)

            return_value = self.ssh.connect(self.host, username=self.user_name, password=self.password)

            return_value = True

            if self.debug:
                print("connected to host : %s") % self.host

        except Exception, err_message:
            print("\n*** remoteCMDRunner.connectToHost :: Connection Error ***\n")
            print("Connection Parameters :\nHost     : %s\nUser     : %s\nPassword : %s\n") % (host, user, password)
            print(err_message)
            print

        return return_value


################################################################################
#  runRemoteCMD
#
#  run a command on the remote system
#  MUST perform a successful connectToHost command first.
#
# *** Note : There is NO CONTEXT between any commands sent to a host.
#            Each command needs to be a complete set of commands.
#            Combine multiple Unix commands together with a semi-colon.
#         EX : cd /tmp/;runAcommand
#
# Parameters :
#  command_line : string = the full command line to be run on remote system
#  show_output : boolean = flag to show command output to screeen
#  show_error : boolean = flag to show command error to screeen
#
# Returns :
#  True - command ran without error
#  False - command generated an error
################################################################################

    def runRemoteCMD(self, command_line, show_output=False, show_error=True):
        """run a command on the remote system"""

        self.std_output = ""
        self.std_error = ""

        try:
            self.channel = self.ssh.get_transport().open_session()              # open channel
            self.channel.settimeout(10800)

            self.channel.exec_command(command_line)  # Execute the given command

            contents = StringIO.StringIO()           # To capture Data. Need to
            error = StringIO.StringIO()              # read the entire buffer to caputure output

            while not self.channel.exit_status_ready():

                if self.channel.recv_ready():                   # get std output
                    data = self.channel.recv(self.BUFFER_SIZE)
#                        print("Inside stdout")

                    while data:
                        contents.write(data)
                        data = self.channel.recv(self.BUFFER_SIZE)          # write output to contents


                if self.channel.recv_stderr_ready():             # get std error

                    error_buff = self.channel.recv_stderr(self.BUFFER_SIZE)

                    while error_buff:
                        error.write(error_buff)
                        error_buff = self.channel.recv_stderr(self.BUFFER_SIZE) # write output to error_buff


            exit_status = not bool(self.channel.recv_exit_status())             # get exit status (0 | 1)

            self.channel.close()                             # close the channel

        except socket.timeout:
            raise socket.timeout


        self.std_output = contents.getvalue()         # assign class variables
        self.std_error = error.getvalue()             # : std_output & std_error

        if show_output:                               # show command output
            print(self.getOutputAsString())

        if show_error:                                    # show error to screen
            error_string = self.getErrorAsString()

            if len(error_string):                            # any errors found?
                print("\nERROR Running Remote Command : ")
                print(error_string)

        # if self.debug:
        #     print("\nstd_output = \n%s\n") % self.std_output
        #     print("\nexit_status = %s\n") % exit_status

        return exit_status


################################################################################
#  getOutputAsString
#  return the class variable self.std_output as a string.
#
# Returns :
#  string : self.std_output as a string
################################################################################

    def getOutputAsString(self):
        """return the class variable self.std_output as a string."""

        return self.std_output


################################################################################
#  getErrorAsString
#  return the class variable self.std_error as a string.
#
# Returns :
#  string : self.std_error as a string
################################################################################

    def getErrorAsString(self):
        """return the class variable self.std_error as a string."""

        return self.std_error


################################################################################
#  connectToSFTP
#   - present the user_name / password to host for SFTP connection
#
# Returns :
#  True : connection success
#  False : connection failed
################################################################################

    def connectToSFTP(self):
        """present the user_name / password to host for SFTP connection"""

        return_value = False

        try:
            self.transport = paramiko.Transport((self.host, self.SFTP_port))         # Open a transport
            self.transport.connect(username=self.user_name, password=self.password)  # Auth

            self.sftp = paramiko.SFTPClient.from_transport(self.transport)           # create transport

            if self.debug:
                print("\nSFTP Connection Opened : %s %s/%s") % (self.host, self.user_name, self.password)

            return_value = True

        except Exception, error_message:
            print("\n*** ERROR RemoteCMDRun::connectToSFTP - error connecting to : %s = %s\n") % (self.host, error_message)


        return return_value


################################################################################
#  closeSFTPConnection
#   - close an open SFTP connection
#
# Returns :
#  True : connection closed
#  False : connection close
################################################################################

    def closeSFTPConnection(self):
        """close an open SFTP connection"""

        return_value = False

        if self.sftp:
            self.sftp.close()                                                    # Close connection
            self.transport.close()
            del self.sftp
            del self.transport

            return_value = True

            if self.debug:
                print("\nSFTP Connection Closed : %s\n") % self.host

        return return_value


################################################################################
#  putFileSFTP
#  Send a file from local system to a remote system
#
# Parameters :
#   file_list : list of lists - [ [local_file, remote_file], ]
#
# Returns :
#  True | False = Status of PUT on Remote system
#
################################################################################

    def putFileSFTP(self, file_list):
        """Send a file from local system to a remote system"""

        return_value = False

        if self.connectToSFTP():

            file_count = 0
            # keep a list of file get status :True|False
            file_status_list = []

            for file_item in file_list:                      # process file list
                local_file = file_item[0]
                remote_file = file_item[1]

                if not os.path.exists(local_file):                              # make sure local file exists before PUT
                    print("\n** ERROR : RemoteCMDRun::putFileSFTP - Cannot find local_file : %s") % local_file
                    file_status_list.append(False)                              # file find failure - False
                    continue

                if self.debug:
                    print("\nRemoteCMDRun::putFileSFTP - Sending file : %s TO %s:%s") % (local_file, self.host, remote_file)

                try:
                    self.sftp.put(local_file, remote_file)   # PUT - upload file
                    file_count += 1
                    file_status_list.append(True)            # PUT success- True
                except Exception, error_msg:
                    print("\n*** ERROR : RemoteCMDRun::putFileSFTP - Error during PUT : %s \n") % error_msg
                    file_status_list.append(False)          # get failure- False


            if self.debug:
                print("\nSFTP Complete - Files put = %d  file_status_list = %s\n") % (file_count, file_status_list)

            if False not in file_status_list:               # check for any failures in list - no False = sucess
                return_value = True


            self.closeSFTPConnection()               # close the SFTP connection

        return return_value


################################################################################
#  gettFileSFTP
#  GET a file from remote system to local system
#
# Parameters :
#   file_list : list of lists - [ [local_file, remote_file], ]
#
# Returns :
#  True | False = Status of GET on Remote system
#
################################################################################

    def getFileSFTP(self, file_list):
        """GET a file from remote system to local system"""

        return_value = False

        if self.connectToSFTP():

            file_count = 0
            file_status_list = []                                               # keep a list of file get status : True | False

            for file_item in file_list:                                         # process file list
                local_file = file_item[0]
                remote_file = file_item[1]

                if self.debug:
                    print("\nRemoteCMDRun::getFileSFTP - Getting file : %s:%s TO %s") % (self.host, remote_file, local_file)

                try:
                    self.sftp.get(remote_file, local_file)                      # Download file
                    file_count += 1
                    file_status_list.append(True)                               # get success - True
                except Exception, getErrorMsg:
                    print("\n*** ERROR : RemoteCMDRun::getFileSFTP - Error during GET (remote file?): %s \n") % getErrorMsg
                    file_status_list.append(False)                              # get failure - False

            if self.debug:
                print("\nSFTP Complete - Files get = %d  file_status_list = %s\n") % (file_count, file_status_list)

            if False not in file_status_list:                                   # check for any failures in list - no False = sucess
                return_value = True


            self.closeSFTPConnection()                                          # close the SFTP connection


        return return_value


################################################################################
#  getMultipleRemoteFiles
#  GET multiple files from remote system to local system
#  - MUST use connectToSFTP() BEFORE calling this.
#
# Parameters :
#   base_local_path : string =  LOCAL location to save files "/path/path/"
#   base_remote_path : string = REMOTE location of files "/path/path/*.txt" (can use file pattern)
#
# Returns :
#  True | False = Status of GET on Remote system
#
################################################################################

    def getMultipleRemoteFiles(self, base_local_path, base_remote_path):
        """GET multiple files from remote system to local system"""

        # get directory file listing of remote directory - base_remote_path
        return_value = self.runRemoteCMD("ls -1 %s" % base_remote_path, False, show_error=True)

        # get the file listing from remote system - list of path+filename
        file_list = string.split(self.std_output, "\n")
        temp_list = []

        # create the list of lists with [localFile, remoteFile] for GET on remote system
        for current_file in file_list:
            if len(current_file):
                temp_list.append([base_local_path + os.path.basename(current_file), current_file])


        if temp_list:
            return_value = self.getFileSFTP(temp_list)        # perform the GETs
        else:
            print("\n* RemoteCMDRun::getMultipleRemoteFiles - NO Remote Files to GET : %s*\n") % base_remote_path

        return return_value


################################################################################
#  putMultipleLocalFiles
#  PUT multiple files from local system to remote system
#  - MUST use connectToSFTP() BEFORE calling this.
#
# Parameters :
#   base_local_pattern : string =  LOCAL path + pattern of files "/path/path/*.txt" (can use file pattern)
#   base_remote_path : string = REMOTE location to SAVE files "/path/path/"
#   - files will be PUT on remote system with the SAME name as local.
#
# Returns :
#  True | False = Status of PUT on Remote system
#
################################################################################

    def putMultipleLocalFiles(self, base_local_pattern, base_remote_path):
        """PUT multiple files from local system to remote system"""

        return_value = False

        # get directory file listing of local directory - base_local_pattern

        try:
            file_list = glob.glob(base_local_pattern)                           # get list of files in local Directory
        except OSError, (errno, strerror):                                      # handle any sort of OS error and continue to top of loop
            print "\nI/O error(%s): %s : %s" % (errno, strerror, base_local_pattern)
            return return_value

        temp_list = []

        # create the list of lists with [localFile, remoteFile] for PUT on local system
        for the_file in file_list:
            temp_list.append([the_file, base_remote_path + os.path.basename(the_file)])

        if temp_list:
            return_value = self.putFileSFTP(temp_list)                          # perform the PUT operations
        else:
            print("\n* RemoteCMDRun::putMultipleLocalFiles - NO Local Files to PUT *\n")

        return return_value


################################################################################
#  remote_exists
#  os.path.exists for paramiko's SCP object
#
#  uses : self.sftp : sftp connection =  the currently open sftp connection
#
# Parameters :
#
#   path : string = REMOTE file location to test for existance  "/path/file.txt"
#
# Returns :
#  True | False = Status of path / file on Remote system
#
################################################################################

        def remote_exists(self, path):
            """os.path.exists for paramiko's SCP object
            """

            try:
                self.sftp.stat(path)
            except IOError, e:
                if e[0] == 2:
                    return False
                raise
            else:
                return True


################################################################################
#  closeRemoteConnection
#
#  Close the open SSH connection
#
################################################################################

    def closeRemoteConnection(self):
        """Close a Remote Connection"""

        try:
            self.ssh.close()                                                    # close the ssh session

            if self.debug:
                print("\nremoteCMDRunner.closeRemoteConnection : Closed Host : %s\n") % self.host

        except Exception, err_message:
            print("\n*** ERROR - remoteCMDRunner::closeRemoteConnection : %s") % err_message


###############################################################################
#                   M A I N L I N E
###############################################################################
def main():
    """main program logic starts here"""

    host = '172.18.1.1'
    username = 'root'
    password = 'scarecrow'

    RemoteCMDObj = remoteCMDRunner(True)

    if RemoteCMDObj.connectToHost(host, username, password):
        cmd_line = 'ls -la'

        if RemoteCMDObj.runRemoteCMD(cmd_line, False, True):    # run command

            output_string = RemoteCMDObj.getOutputAsString()    # get output & print
            print("\nOutput String = \n%s" % output_string)


        cmd_line = 'ls -1'

        if RemoteCMDObj.runRemoteCMD(cmd_line, False, True):    # run command

            output_string = RemoteCMDObj.getOutputAsString()    # get output & print
            print("\nOutput String = \n%s" % output_string)

        cmd_line = "bad command"                                # bad command test

        RemoteCMDObj.runRemoteCMD(cmd_line, False, True)        # should fail - returns False

        error_string = RemoteCMDObj.getErrorAsString()          # get error & print
        print("\nError String = \n %s" % error_string)

        RemoteCMDObj.closeRemoteConnection()

if __name__ == "__main__":
  main()
