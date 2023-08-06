import os


def get_env(name, default=None):
    """
    Get environment variable value by name
    :param name: environment variable name
    :param default: default environment variable value
    :return: environment variable value
    """
    value = os.getenv(name)
    if value is not None:
        return value

    if default is not None:
        return default

    raise Exception(f'No environment variable: {name}')
