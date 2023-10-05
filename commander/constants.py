ZERO = 0
MIN_PORT_RANGE = 0
MAX_PORT_RANGE = 65536
LOCAL_HOST = "localhost"
LOCAL_HOST_VALUE = "127.0.0.1"
MIN_QUEUE_SIZE = 5


# MENU Constants
MENU_BANNER = "===================================== \\ COMMANDER PROGRAM // ====================================="
MENU_CLOSING_BANNER = ("==================================================================================="
                       "===============")
SERVER_INFO_MSG = "[+] Commander server is listening on: {}"
INVALID_INPUT_MENU_ERROR = "[+] ERROR: Invalid input was provided to menu: {}"
INITIAL_VICTIM_IP_MSG = "[+] Victim IP (from argument): {}"
INITIAL_VICTIM_PORT_MSG = "[+] Victim Port (from argument): {}"
INITIATE_VICTIM_CONNECTION_MSG = "[+] Now initiating a connection to the victim..."
SUCCESSFUL_VICTIM_CONNECTION_MSG = "[+] Successfully connected to a victim: {}"
ERROR_VICTIM_CONNECTION_MSG = "[+] ERROR: A connection error to victim has occurred: {}"
MENU_SELECTION_PROMPT_MSG = "[+] Enter any number above to perform any of the following actions displayed: "
INVALID_MENU_SELECTION_PROMPT = "[+] INVALID INPUT: Please enter a valid option: "
COMMANDER_SERVER_SOCKET_CREATION_ERROR_MSG = "[+] ERROR: An error has occurred while creating server socket: {}"
MENU_ITEM_ONE = "1 - Start Keylogger"
MENU_ITEM_TWO = "2 - Stop Keylogger"
MENU_ITEM_THREE = "3 - Transfer Keylog Program to Victim"
MENU_ITEM_FOUR = "4 - Get Keylog File from Victim"
MENU_ITEM_FIVE = "5 - Disconnect from Victim"
MENU_ITEM_SIX = "6 - Transfer a file to a Victim"
MENU_ITEM_SEVEN = "7 - Get a file from a Victim"
MENU_ITEM_EIGHT = "8 - Run program"
MENU_ITEM_NINE = "9 - Watch file"
MENU_ITEM_TEN = "10 - Watch directory"
MENU_ITEM_ELEVEN = "11 - Uninstall"
PERFORM_MENU_ITEM_ONE = 1
PERFORM_MENU_ITEM_TWO = 2
PERFORM_MENU_ITEM_THREE = 3
PERFORM_MENU_ITEM_FOUR = 4
PERFORM_MENU_ITEM_FIVE = 5
PERFORM_MENU_ITEM_SIX = 6
PERFORM_MENU_ITEM_SEVEN = 7
PERFORM_MENU_ITEM_EIGHT = 8
PERFORM_MENU_ITEM_NINE = 9
PERFORM_MENU_ITEM_TEN = 10
PERFORM_MENU_ITEM_ELEVEN = 11
MIN_MENU_ITEM_VALUE = 1
MAX_MENU_ITEM_VALUE = 11
MENU_ACTION_START_MSG = "[+] ACTION SELECTED: Now performing menu item: {}..."

# MENU ITEM 5 - DISCONNECT Constants
DISCONNECT_FROM_VICTIM_MSG = "[+] DISCONNECTING FROM VICTIM: Now disconnecting from victim {}..."
DISCONNECT_FROM_VICTIM_SUCCESS = "[+] DISCONNECT SUCCESSFUL: Disconnection was successful!"


# DESTINATION IP/PORT Constants
NO_ARG_ERROR = "[+] NO_ARG_ERROR: No arguments were passed in!"
INVALID_DST_IP_ADDRESS_ARG_ERROR = ("[+] ERROR: Invalid format for the destination IP address was provided "
                                    "(-d option): {}")
INVALID_FORMAT_DST_PORT_NUMBER_ARG_ERROR = "[+] ERROR: Invalid format provided for the destination port (-p option): {}"
INVALID_DST_PORT_NUMBER_RANGE = ("[+] ERROR: The value provided for destination port (-p option) is not "
                                 "valid: (not between 0 and 65536)")
NO_DST_IP_ADDRESS_SPECIFIED_ERROR = "[+] ERROR: No destination IP Address (-d option) was specified!"
NO_DST_PORT_NUMBER_SPECIFIED_ERROR = "[+] ERROR: No destination port number (-p option) was specified!"


# SOURCE IP/PORT Constants
INVALID_SRC_IP_ADDRESS_ARG_ERROR = ("[+] ERROR: Invalid format for the source IP address was provided "
                                    "(-s or --src_ip option): {}")
INVALID_FORMAT_SRC_PORT_NUMBER_ARG_ERROR = ("[+] ERROR: Invalid format provided for the source port (-c or --src_port "
                                            "option): {}")
INVALID_SRC_PORT_NUMBER_RANGE = ("[+] ERROR: The value provided for source port (-c or --src_port option) is not "
                                 "valid: (not between 0 and 65536)")
NO_SRC_IP_ADDRESS_SPECIFIED_ERROR = "[+] ERROR: No source IP Address (-s or --src_ip option) was specified!"
NO_SRC_PORT_NUMBER_SPECIFIED_ERROR = "[+] ERROR: No source port number (-c or --src_port option) was specified!"
