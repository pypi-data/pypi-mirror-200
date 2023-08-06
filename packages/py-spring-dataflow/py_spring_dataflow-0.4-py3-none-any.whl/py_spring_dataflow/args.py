import sys


def get_args():
    """
    Get command line arguments
    :return: command line arguments
    """
    return sys.argv[1:]


def get_arg(name, default=None):
    """
    Get command line argument value by name
    :param name: command line argument name
    :param default: default command line argument value
    :return: command line argument value
    """
    args = get_args()
    for arg in args:
        arg_key_value = arg.split('=', 1)
        arg_key = arg_key_value[0]
        if arg_key == name:
            if len(arg_key_value) == 1:
                return True
            else:
                value = arg_key_value[1]
                return value

    if default is not None:
        return default

    raise Exception(f'No command line argument: {name}')


def get_flag(name, default=None):
    """
    Get command line argument value by name as flag (True/False)
    :param name: command line argument name
    :param default: default command line argument value as flag
    :return: command line argument value as flag
    """
    value = get_arg(name, default)
    return is_enabled(value)


def is_enabled(flag):
    """
    Check if argument value as flag is enabled
    :param flag: argument value as flag
    :return: enabled?
    """
    if flag is True:
        return True
    elif flag is False:
        return False
    else:
        return flag.lower() in ('true', '1', 't', 'yes')
