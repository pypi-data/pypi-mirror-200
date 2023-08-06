from py_spring_dataflow import params


def get_execution_id():
    """
    Get unique ID for task's run
    :return: unique ID for task's run
    """
    return params.get_param('spring.cloud.task.executionid')


def get_name():
    """
    Get name for task
    :return: name for task
    """
    return params.get_param('spring.cloud.task.name')
