import logging
from sys import _getframe

from django.http import HttpResponse
# from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile

# # do not import any app related stuff here
# # for specific app utils, please create utils.py in your app directory
# # functions here will be used project-wide, may be in multiples apps

# logger = logging.getLogger(__name__)


def test_user(user, allow_staff=True, allow_other=True):
    """Tests user if is_active, is_staff, is_superuser
    Returns boolean status, True/False"""
    if user.is_active:
        if user.is_superuser:
            logger.debug(  # prints class and function name
                f"{_getframe().f_code.co_name} {user} is a superuser."
            )
            return True
        elif user.is_staff and allow_staff:
            logger.debug(  # prints class and function name
                f"{_getframe().f_code.co_name} {user} is a staff."
            )
            return True
        else:  # test for other
            logger.debug(  # prints class and function name
                f"{_getframe().f_code.co_name} {user} is a other."
            )
            return allow_other

    # user not active
    logger.debug(  # prints class and function name
        f"{_getframe().f_code.co_name} {user} is not active."
    )
    return False


# def render_pdf(request, template, context, file_name: str):
#     html_string = render_to_string(
#         template, context
#     )
#     html = HTML(
#         string=html_string,
#         base_url=request.build_absolute_uri()
#     )
#     result = html.write_pdf()

#     # Creating http response
#     response = HttpResponse(content_type='application/pdf;')
#     response['Content-Disposition'] = f"inline; filename={file_name}.pdf"
#     response['Content-Transfer-Encoding'] = 'binary'
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())
#     return response
