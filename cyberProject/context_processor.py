from .settings import PASSWORD_REQUIREMENTS

def isauth_context_processor(request):
    return {
        'isAuthenticated': request.COOKIES.get('isAuthenticated'),
        'pass_policy': PASSWORD_REQUIREMENTS,
        'userName': request.COOKIES.get('userName'),
    }
