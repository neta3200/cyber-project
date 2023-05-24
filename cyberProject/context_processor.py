#populate the context when a template is rendered with a request

from .settings import PASSWORD_REQUIREMENTS


def isauth_context_processor(request):

    context_processor=    {
        'userName': request.COOKIES.get('userName'),
        'isAuthenticated': request.COOKIES.get('isAuthenticated'),
        'policy_password': PASSWORD_REQUIREMENTS,
    }

    return context_processor
