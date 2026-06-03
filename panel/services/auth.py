from django.contrib.auth.forms import AuthenticationForm


def build_login_context(error=None):
    return {
        'form': AuthenticationForm,
        'error': error,
    }
