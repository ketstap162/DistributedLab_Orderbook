from django.shortcuts import redirect


def auth_required(function):

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        return function(request, *args, **kwargs)

    return wrapper
