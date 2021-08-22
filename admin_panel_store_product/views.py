from django.shortcuts import get_object_or_404, redirect, render
from admin_panel_store_product import models
from admin_panel_store_product import forms
from django.http import HttpResponse
import xlwt
from django.db.models import Q, Sum
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from admin_panel import decorators
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
@decorators.level_one
def panel_product(request):
    product = models.product.objects.all()
    if request.method == "POST":
        id = request.POST['id']
        if id != "":
            product = product.filter(id=id).order_by("id")
    
    paginator = Paginator(product ,6 )
    page = request.GET.get('page')

    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    return render(request, 'admin_panel_store_product/product.html',context=data)

@login_required
@decorators.level_three
def product_edit(request , pk ):
    product = models.product.objects.get(id = pk)
    
    if request.method == "POST":
        form = forms.product_edit_form(request.POST, instance=product)
        if form.is_valid():
            journals = models.journal.objects.filter(product = product)
            if journals.count() == 0 :
                form.save()
                return redirect("admin_panel_product:panel_product" )
            else:
                form.add_error("name", " ابتدا تمامی اطلاعات این کالا را در دفتر روزنامه پاک کنید .")
    else:
        form = forms.product_edit_form(instance=product)
    context={"form":form}
    return render(request , "admin_panel_store_product/product_edit.html" , context)

@login_required
@decorators.level_three
def product_remove(request , pk ):
    product = models.product.objects.get(id = pk)
    journals = models.journal.objects.filter(product=product)
    if not journals :
        product.delete()
    return redirect("admin_panel_product:panel_product" )

def product_add(request ):
    form = forms. product_add_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("admin_panel_product:panel_product" )
        else:
            form.add_error("name", "قبلا کالایی با این کد ساخته شده است")
    context={"form":form}
    return render(request , "admin_panel_store_product/product_add.html" , context)

@login_required
@decorators.level_one
def export_product_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="product.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('product')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['کد کالا', 'نام کالا' , ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = models.product.objects.all().values_list('id', 'name' ,)
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
                    document = models.document.objects.filter(description__icontains = description)
                else:
                    document = models.document.objects.filter(Q(description__icontains = description)|Q(id = id))
        else:
            if description == "":
                if id == "" :
                    document = models.document.objects.filter(date = date)
                else : 
                    document = models.document.objects.filter(Q(id = id)|Q(date = date))
            else:
                if id == "" :
                    document = models.document.objects.filter(Q(description__icontains = description)|Q(date = date))
                else :
                    document = models.document.objects.filter(Q(description__icontains = description)|Q(id = id)|Q(date = date))
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
    return render(request, 'admin_panel_store_product/document.html',context=data)

@login_required
@decorators.level_two
def document_add(request ):
    if request.method == "POST":
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
            product = models.product.objects.get(id=code[i] , name=name[i])
            models.journal.objects.create(document = document , product = product ,description = description[i] ,debtor=debtor[i].replace(",",""),creditor=creditor[i].replace(",",""))
        return redirect("admin_panel_product:panel_document" )

    if models.document.objects.all().count()!=0 :
        document_last_id = models.document.objects.latest('id').id +1
    else:
        document_last_id = 0
    product = models.product.objects.all()
    context={
        'document_last_id': document_last_id,

        'product': product,
    }
    return render(request , "admin_panel_store_product/document_add.html" , context)

@login_required
@decorators.level_three
def document_edit(request , pk ):
    document = models.document.objects.get(id = pk)
    
    if request.method == "POST":
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
            product = models.product.objects.get(id=code[i] , name=name[i])
            models.journal.objects.create(document = document , product = product ,description = description[i] ,debtor=debtor[i].replace(",",""),creditor=creditor[i].replace(",",""))
        
        return redirect("admin_panel_product:panel_document" )

    document =models.document.objects.get(id=pk)
    journals =  document.journals.all()
    product = models.product.objects.all()
    data = {
        "document":document ,
        "journals":journals ,
        'product': product,

    }
    return render(request , "admin_panel_store_product/document_edit.html" , data)

@login_required
@decorators.level_three
def document_remove(request , pk ):
    document = get_object_or_404(models.document, id = pk)
    document.delete()
    return redirect("admin_panel_product:panel_document" )

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
    rows = models.document.objects.all().values_list('id', 'date' ,'description')
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
def check_product(request ):
    if request.method == "POST":
        id = request.POST['id']
        if id == "":
            product = models.product.objects.all().order_by("id")
            sum_debtors =models.journal.objects.aggregate(Sum('debtor'))['debtor__sum']
            sum_creditors = models.journal.objects.aggregate(Sum('creditor'))['creditor__sum']
            result = sum_debtors - sum_creditors
        else:
            if models.product.objects.filter(id = id).exists():
                product = models.product.objects.filter(id = id)
                sum_debtors =models.journal.objects.filter(product=product[0]).aggregate(Sum('debtor'))['debtor__sum']
                sum_creditors = models.journal.objects.filter(product=product[0]).aggregate(Sum('creditor'))['creditor__sum']
                result = sum_debtors - sum_creditors
            else:
                return render(request, 'admin_panel_store_product/check_product.html')
    else:
        product = models.product.objects.all()
        sum_debtors =models.journal.objects.aggregate(Sum('debtor'))['debtor__sum']
        sum_creditors = models.journal.objects.aggregate(Sum('creditor'))['creditor__sum']
        if not sum_debtors == None :
            result = sum_debtors - sum_creditors
        else:
            result = 0

    journals_list = []
    for product in product :
        new_dic = {}
        debtors = 0
        creditors = 0
        journals = models.journal.objects.filter(product=product)
        for journal in journals :
            debtors += journal.debtor
            creditors += journal.creditor
        new_dic["code"] = product.id
        new_dic["name"] = product.name
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
    return render(request, 'admin_panel_store_product/check_product.html',context=data)

@login_required
@decorators.level_one
def export_check_product_xls(request):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="journals.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('journal')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['کد', 'نام کالا' ,'گردش وارده', 'گردش صادره' , 'مانده' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    product = models.product.objects.all()


    sum_debtors =models.journal.objects.aggregate(Sum('debtor'))['debtor__sum']
    sum_creditors = models.journal.objects.aggregate(Sum('creditor'))['creditor__sum']
    item_list = []
    sum_debtors = 0
    sum_creditors = 0

    for material in product :
        list=[]
        list.append(material.id)
        list.append(material.name)
        if models.journal.objects.filter(product=material).exists():
            debtor =models.journal.objects.filter(product=material).aggregate(Sum('debtor'))['debtor__sum']
            creditor = models.journal.objects.filter(product=material).aggregate(Sum('creditor'))['creditor__sum']
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
        journals = models.journal.objects.filter(product__id = id ).order_by("document__date")

    data = {
        "journals":journals,
        "id" : id ,
    }
    return render(request, 'admin_panel_store_product/report_one.html',context=data)

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
    columns = ['تاریخ سند' , 'شماره سند' ,'شرح','وارده','صادره','مانده در خط' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = models.journal.objects.filter(account__id = pk ).order_by("document__date")
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