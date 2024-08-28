from django.shortcuts import render

from .models import News


# Create your views here.
def home(request):
    news=News.objects.filter(user_id=1)

    return render(request,"common/index.html",{"news":news})

