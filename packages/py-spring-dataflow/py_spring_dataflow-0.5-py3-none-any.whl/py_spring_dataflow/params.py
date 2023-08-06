from py_spring_dataflow import args


def get_params():
    params = [arg for arg in args.get_args() if arg.startswith('--')]
    return params


def get_param(name, default=None):
    """
    Get parameter value by name: --param-name=param-value
    :param name: parameter name
    :param default: default parameter value
    :return: parameter value
    """
    return args.get_arg(f'--{name}', default)


def get_flag(name, default=None):
    """
    Get parameter value by name as flag (True/False): --param-name[=true|t|1|yes]
    :param name: parameter name
    :param default: default parameter value as flag
    :return: parameter value as flag
    """
    return args.get_flag(f'--{name}', default)
