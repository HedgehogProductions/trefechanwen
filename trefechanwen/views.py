from django.shortcuts import render

# Create your views here.


def index(request):
    """
    View function for home page.
    """

    return render(
        request,
        'index.html',
        context={},
    )

def cottage(request):
    """
    View function for cottage page.
    """

    return render(
        request,
        'cottage.html',
        context={},
    )

def barn(request):
    """
    View function for barn page.
    """

    return render(
        request,
        'barn.html',
        context={},
    )

def availability(request):
    """
    View function for availability page.
    """

    return render(
        request,
        'availability.html',
        context={},
    )

def localinfo(request):
    """
    View function for local info page.
    """

    return render(
        request,
        'localinfo.html',
        context={},
    )

def contact(request):
    """
    View function for contact page.
    """

    return render(
        request,
        'contact.html',
        context={},
    )
