import getopt
import sys
import constants
import ipaddress


def parse_arguments():
    # Initialization
    destination_ip, destination_port = "", ""

    # GetOpt Arguments
    arguments = sys.argv[1:]
    opts, user_list_args = getopt.getopt(arguments, 'd:p:')

    if len(opts) == constants.ZERO:
        sys.exit(constants.NO_ARG_ERROR)

    for opt, argument in opts:
        if opt == '-d':  # For destination IP
            try:
                destination_ip = str(ipaddress.ip_address(argument))
            except ValueError as e:
                sys.exit(constants.INVALID_IP_ADDRESS_ARG_ERROR.format(e))

        if opt == '-p':  # For destination port
            try:
                destination_port = int(argument)
                if not (constants.MIN_PORT_RANGE < destination_port < constants.MAX_PORT_RANGE):
                    sys.exit(constants.INVALID_PORT_NUMBER_RANGE)
            except ValueError as e:
                sys.exit(constants.INVALID_FORMAT_PORT_NUMBER_ARG_ERROR.format(e))

    # Check if Server IP and Port was specified
    if len(destination_ip) == constants.ZERO:
        sys.exit(constants.NO_IP_ADDRESS_SPECIFIED_ERROR)

    if len(str(destination_port)) == constants.ZERO:
        sys.exit(constants.NO_PORT_NUMBER_SPECIFIED_ERROR)

    return destination_ip, destination_port


if __name__ == '__main__':
    parse_arguments()
