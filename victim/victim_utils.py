import constants


def is_file_openable(file_path):
    try:
        with open(file_path, 'r') as file:
            pass
        return True
    except IOError as e:
        print(constants.FILE_CANNOT_OPEN_ERROR.format(file_path, e))
        return False
    