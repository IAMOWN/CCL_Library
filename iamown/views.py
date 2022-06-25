from django.shortcuts import render

from iamown.models import (
    test
)


# ####################### BASIC VIEWS #######################
def test(request):
    if request.user.is_authenticated:
        context = {
            'title': 'Cosmic Christ Love',
        }
    else:
        context = {
            'title': 'Cosmic Christ Love',
        }

    return render(request, 'iamown/tasks.html', context)