from admin_panel.forms import login_form
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def login(request):
    form = login_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request , user)
                return redirect("panel" )
            form.add_error(None, "incorect data")
    else:
        if request.user.is_authenticated:
            return render(request , "admin_panel/panel.html" )
    context={"form":form}
    return render(request , "admin_panel/panel_login.html" , context)

def logout_user(request):
    logout(request)
    return redirect("panel_login" )

@login_required(login_url='/admin_panel/login')
def panel(request):
    return render(request, 'admin_panel/panel.html')