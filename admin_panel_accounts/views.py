import xlwt
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from accounts.models import users
from admin_panel_accounts import forms
import datetime

def panel_accounts(request):
    user = users.objects.all()
    data = {
        "users":user
    }
    return render(request, 'admin_panel_accounts/accounts.html',context=data)
    
def user_detail(request , pk ):
    user = users.objects.get(user__pk = pk)
    data = {
        "user":user
    }
    return render(request , "admin_panel_accounts/detail.html" , data)

def user_edit(request , pk ):
    user = users.objects.get(pk = pk)
    
    if request.method == "POST":
        form = forms.users_edit_form(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = forms.users_edit_form(instance=user)
    context={"form":form}
    return render(request , "admin_panel_accounts/edit.html" , context)

def user_remove(request , pk ):
    user = User.objects.get(pk = pk)
    user.delete()
    return redirect("panel_accounts" )


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'First name', 'Last name', 'Email address', 'is_active' , 'is_staff' , 'is_superuser' , 'Date joined' , ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email', 'is_active' , 'is_staff' , 'is_superuser' , 'date_joined' ,)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if type(row[col_num]) == datetime.datetime :
                date = row[col_num].strftime("%Y/%m/%d")
                ws.write(row_num, col_num, date, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
