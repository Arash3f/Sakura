from django.shortcuts import get_object_or_404, redirect, render
from admin_panel_accounting import models
from admin_panel_accounting import forms
from django.http import HttpResponse
import xlwt
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from admin_panel import decorators
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage


@login_required
@decorators.level_one
def panel_accounting(request):
    account = models.account.objects.all().order_by("id")
    if request.method == "POST":
        id = request.POST['id']
        if id != "":
            account = account.filter(id=id).order_by("id")

    paginator = Paginator(account ,6 )
    page = request.GET.get('page')

    try:
        account = paginator.page(page)
    except PageNotAnInteger:
        account = paginator.page(1)
    except EmptyPage:
        account = paginator.page(paginator.num_pages)

    data = {
        "accounts":account
    }
    return render(request, 'admin_panel_accounting/account.html',context=data)

@login_required
@decorators.level_three
def account_edit(request , pk ):
    account = models.account.objects.get(id = pk)
    
    if request.method == "POST":
        form = forms.account_edit_form(request.POST, instance=account)
        if form.is_valid():
            journals = models.journal2.objects.filter(account = account)
            if journals.count() == 0 :
                form.save()
                return redirect("admin_panel_accounting:panel_accounting" )
            else:
                form.add_error("name", " ابتدا تمامی اطلاعات این حساب را در دفتر روزنامه پاک کنید .")
    else:
        form = forms.account_edit_form(instance=account)
    context={"form":form}
    return render(request , "admin_panel_accounting/account_edit.html" , context)

@login_required
@decorators.level_three
def account_remove(request , pk ):
    account = models.account.objects.get(id = pk)
    journals = models.journal2.objects.filter(account=account)
    if not journals :
        account.delete()
    return redirect("admin_panel_accounting:panel_accounting" )

@login_required
@decorators.level_two
def account_add(request ):
    form = forms. account_add_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("admin_panel_accounting:panel_accounting" )
        else:
            form.add_error("name", "قبلا حسابی با این کد ساخته شده است")
    context={"form":form}
    return render(request , "admin_panel_accounting/account_add.html" , context)

@login_required
@decorators.level_one
def export_accounts_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="account.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('accounts')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['کد حساب', 'نام حساب' , ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = models.account.objects.all().order_by("id").values_list('id', 'name' ,)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    # rtl :
    ws.cols_right_to_left = True
    wb.save(response)
    return response

#  document :
@login_required
@decorators.level_one
def panel_document(request):
    document = models.document.objects.all().order_by("id")
    if request.method == "POST":
        id = request.POST['id']
        date = request.POST['date']
        description = request.POST['description']
        if date == "":
            if description == "":
                if id == "" :
                    pass
                else : 
                    document = models.document.objects.filter(id = id)
            else:
                if id == "" :
                    document = models.document.objects.filter(description__icontains = description).order_by("id")
                else:
                    document = models.document.objects.filter(Q(description__icontains = description)|Q(id = id)).order_by("id")
        else:
            if description == "":
                if id == "" :
                    document = models.document.objects.filter(date = date).order_by("id")
                else : 
                    document = models.document.objects.filter(Q(id = id)|Q(date = date)).order_by("id")
            else:
                if id == "" :
                    document = models.document.objects.filter(Q(description__icontains = description)|Q(date = date)).order_by("id")
                else :
                    document = models.document.objects.filter(Q(description__icontains = description)|Q(id = id)|Q(date = date)).order_by("id")
    paginator = Paginator(document ,6 )
    page = request.GET.get('page')

    try:
        document = paginator.page(page)
    except PageNotAnInteger:
        document = paginator.page(1)
    except EmptyPage:
        document = paginator.page(paginator.num_pages)
    data = {
        "documents":document
    }
    return render(request, 'admin_panel_accounting/document.html',context=data)

@login_required
@decorators.level_two
def document_add(request ):
    if request.method == "POST":
        sum_debtor = request.POST['sum_debtor'][0].replace(",","")
        sum_creditor = request.POST['sum_creditor'][0].replace(",","")
        if sum_debtor != sum_creditor or sum_debtor=="0" or sum_creditor=="0":
            return redirect("document_add" )
        document_id = request.POST['document_id']
        document_date= request.POST['document_date']
        document_description= request.POST['document_description']
        code= request.POST.getlist('code')
        name= request.POST.getlist('name')
        description= request.POST.getlist('description')
        debtor= request.POST.getlist('debtor')
        creditor= request.POST.getlist('creditor')

        document = models.document.objects.create(id = document_id , date = document_date , description = document_description)
        for i in range(len(code)):
            if code[i]=="" or name[i]=="":
                break
            account = models.account.objects.get(id=code[i] , name=name[i])
            models.journal2.objects.create(document = document , account = account ,description = description[i]  ,debtor=debtor[i].replace(",",""),creditor=creditor[i].replace(",",""))
        return redirect("admin_panel_accounting:panel_document" )

    if models.document.objects.all().count()!=0 :
        document_last_id = models.document.objects.latest('id').id +1
    else:
        document_last_id = 0
    accounts = models.account.objects.all()
    context={
        'document_last_id': document_last_id,

        'accounts': accounts,
    }
    return render(request , "admin_panel_accounting/document_add.html" , context)

@login_required
@decorators.level_three
def document_edit(request , pk ):
    document = models.document.objects.get(id = pk)
    
    if request.method == "POST":
        sum_debtor = request.POST['sum_debtor'][0].replace(",","")
        sum_creditor = request.POST['sum_creditor'][0].replace(",","")
        if sum_debtor != sum_creditor or sum_debtor=="0" or sum_creditor=="0":
            return redirect("document_edit" )
        document_id = request.POST['document_id']
        document_date= request.POST['document_date']
        document_description= request.POST['document_description']
        code= request.POST.getlist('code')
        name= request.POST.getlist('name')
        description= request.POST.getlist('description')
        debtor= request.POST.getlist('debtor')
        creditor= request.POST.getlist('creditor')
        document = models.document.objects.get(id = document_id )
        document.date = document_date
        document.description = document_description
        document.save()

        journals =  document.journals.all().delete()

        for i in range(len(code)):
            if code[i]=="" or name[i]=="":
                break
            account = models.account.objects.get(id=code[i] , name=name[i])
            models.journal2.objects.create(document = document , account = account ,description = description[i] ,debtor=debtor[i].replace(",",""),creditor=creditor[i].replace(",",""))
        
        return redirect("admin_panel_accounting:panel_document" )

    document =models.document.objects.get(id=pk)
    journals =  document.journals.all()
    accounts = models.account.objects.all()
    data = {
        "document":document ,
        "journals":journals ,
        'accounts': accounts,

    }
    return render(request , "admin_panel_accounting/document_edit.html" , data)

@login_required
@decorators.level_three
def document_remove(request , pk ):
    document = get_object_or_404(models.document, id = pk)
    document.delete()
    return redirect("admin_panel_accounting:panel_document" )

@login_required
@decorators.level_one
def export_document_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="document.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('documents')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["سند","تاریخ","شرح"]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = models.document.objects.all().order_by("id").values_list('id', 'date' ,'description')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    # rtl :
    ws.cols_right_to_left = True
    wb.save(response)
    return response

@login_required
@decorators.level_one
def check_accounts(request ):
    if request.method == "POST":
        id = request.POST['id']
        if id == "":
            accounts = models.account.objects.all().order_by("id")
            sum_debtors =models.journal2.objects.aggregate(Sum('debtor'))['debtor__sum']
            sum_creditors = models.journal2.objects.aggregate(Sum('creditor'))['creditor__sum']
            result = sum_debtors - sum_creditors
        else:
            if models.account.objects.filter(id = id).exists():
                accounts = models.account.objects.filter(id = id)
                sum_debtors =models.journal2.objects.filter(account=accounts[0]).aggregate(Sum('debtor'))['debtor__sum']
                sum_creditors = models.journal2.objects.filter(account=accounts[0]).aggregate(Sum('creditor'))['creditor__sum']
                result = sum_debtors - sum_creditors
            else:
                return render(request, 'admin_panel_accounting/check_accounts.html')
    else:
        accounts = models.account.objects.all().order_by("id")
        sum_debtors =models.journal2.objects.aggregate(Sum('debtor'))['debtor__sum']
        sum_creditors = models.journal2.objects.aggregate(Sum('creditor'))['creditor__sum']
        if not sum_debtors == None :
            result = sum_debtors - sum_creditors
        else:
            result = 0

    journals_list = []
    for account in accounts :
        new_dic = {}
        debtors = 0
        creditors = 0
        journals = models.journal2.objects.filter(account=account)
        for journal in journals :
            debtors += journal.debtor
            creditors += journal.creditor
        new_dic["code"] = account.id
        new_dic["name"] = account.name
        new_dic["debtors"] = debtors
        new_dic["creditors"] = creditors
        new_dic["re_amount"] = debtors - creditors
        journals_list.append(new_dic)

    data = {
        "journals_list":journals_list,
        "sum_debtors":sum_debtors,
        "sum_creditors":sum_creditors,
        "result":result,
    }
    return render(request, 'admin_panel_accounting/check_accounts.html',context=data)

@login_required
@decorators.level_one
def export_check_accounts_xls(request):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="journals.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('journal')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['کد', 'نام حساب' ,'گردش بدهکار', 'گردش بستانکار' , 'مانده' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    accounts = models.account.objects.all().order_by("id")


    sum_debtors =models.journal2.objects.aggregate(Sum('debtor'))['debtor__sum']
    sum_creditors = models.journal2.objects.aggregate(Sum('creditor'))['creditor__sum']
    item_list = []
    sum_debtors = 0
    sum_creditors = 0

    for account in accounts :
        list=[]
        list.append(account.id)
        list.append(account.name)
        if models.journal2.objects.filter(account=account).exists():
            debtor =models.journal2.objects.filter(account=account).aggregate(Sum('debtor'))['debtor__sum']
            creditor = models.journal2.objects.filter(account=account).aggregate(Sum('creditor'))['creditor__sum']
            sum_debtors += int(debtor)
            sum_creditors += int(creditor)
            list.append(debtor)
            list.append(creditor)
            result = debtor - creditor
            if result < 0:
                list.append("("+str(result*-1)+")")
            else:
                list.append(result)

        else:
            list.append(0)
            list.append(0)
            list.append(0)
        item_list.append(list)
    list=[]
    list.append("-")
    list.append("-")
    list.append(sum_debtors)
    list.append(sum_creditors)
    result = sum_debtors - sum_creditors
    if result < 0:
        list.append("("+str(result*-1)+")")
    else:
        list.append(result)
    
    item_list.append(list)
    for i in item_list:
        row_num += 1
        for col_num in range(len(i)):
            ws.write(row_num, col_num, i[col_num], font_style)
    ws.cols_right_to_left = True
    wb.save(response)
    return response

@login_required
@decorators.level_one
def report_one(request ):
    journals = []
    id = 0
    if request.method == "POST":
        id = request.POST['id']
        journals = models.journal2.objects.filter(account__id = id ).order_by("document__date")

    data = {
        "journals":journals,
        "id" : id ,
    }
    return render(request, 'admin_panel_accounting/report_one.html',context=data)

@login_required
@decorators.level_one
def export_check_report_xls(request , pk):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(str(pk))
    # Sheet header, first row
    row_num = 0
    col_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['تاریخ سند' , 'شماره سند' ,'شرح','بدهکار','بستانکار','مانده در خط' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = models.journal2.objects.filter(account__id = pk ).order_by("document__date")
    result = 0
    for row in rows:
        row_num += 1
        col_num = 0
        ws.write(row_num, col_num, str(row.document.date), font_style)
        col_num += 1
        ws.write(row_num, col_num, row.document.pk, font_style)
        col_num += 1
        ws.write(row_num, col_num, row.description, font_style)
        col_num += 1
        ws.write(row_num, col_num, row.debtor, font_style)
        col_num += 1
        ws.write(row_num, col_num, row.creditor, font_style)
        col_num += 1
        result += row.debtor - row.creditor
        if result < 0 :
            style = xlwt.easyxf('pattern: pattern solid, fore_color red;')
            ws.write(row_num, col_num, "("+str(result * -1)+")", style)
        else :
            ws.write(row_num, col_num, result, font_style)
    # rtl :
    ws.cols_right_to_left = True
    wb.save(response)
    return response
