from django.shortcuts import render


def response_error(request, status_code, message):
    return render(
        request,
        "error.html",
        context={
            "status_code": status_code,
            "message": message,
        },
        status=status_code,
    )
