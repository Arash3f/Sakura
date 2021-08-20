from django.shortcuts import render
from accounts.models import users

def level_one(view_func):
    def wrap(request, *args, **kwargs):
        try :
            user = request.user
            user = users.objects.get(user=user)
        except:
            return render(request, "404.html")
        if user.accessibility != "0":
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "404.html")
    return wrap

def level_two(view_func):
    def wrap(request, *args, **kwargs):
        try :
            user = request.user
            user = users.objects.get(user=user)
        except:
            return render(request, "404.html")
        if user.accessibility == "2" or user.accessibility == "3":
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "404.html")
    return wrap

def level_three(view_func):
    def wrap(request, *args, **kwargs):
        try :
            user = request.user
            user = users.objects.get(user=user)
        except:
            return render(request, "404.html")
        if user.accessibility == "3" :
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "404.html")
    return wrap