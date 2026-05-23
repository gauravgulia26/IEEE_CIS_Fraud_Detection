import sys
from rich.traceback import install

install()


def get_error_details(error: Exception, error_detail: sys):
    """
    Extract detailed info about exception
    """
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = f"""
    Error occurred in script: {file_name}
    Line number: {line_number}
    Error message: {str(error)}
    """

    return error_message


class CustomException(Exception):
    def __init__(self, error: Exception, error_detail: sys):
        super().__init__(error)
        self.error_message = get_error_details(error, error_detail)

    def __str__(self):
        return self.error_message
