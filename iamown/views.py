from django.shortcuts import render

from models import (
    Task,
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