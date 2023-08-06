from py_spring_dataflow import params


def get_url():
    """
    Get datasource's url
    :return: datasource's url
    """
    return params.get_param('spring.datasource.url')


def get_username():
    """
    Get datasource's username
    :return: datasource's username
    """
    return params.get_param('spring.datasource.username')


def get_password():
    """
    Get datasource's password
    :return: datasource's password
    """
    return params.get_param('spring.datasource.password')


def get_driver_class_name():
    """
    Get datasource's driver class name
    :return: datasource's driver class name
    """
    return params.get_param('spring.datasource.driverClassName')
