from django.shortcuts import redirect, render
from admin_panel_store_karaj import models
from admin_panel_store_karaj import forms
from django.http import HttpResponse
import xlwt
from django.db.models import Q, Sum

# Create your views here.

def panel_product(request):
    product = models.product.objects.all()
    if request.method == "POST":
        id = request.POST['id']
        if id != "":
            product = product.filter(id=id)
    data = {
        "product":product
    }
    return render(request, 'admin_panel_store_karaj/product.html',context=data)

def product_edit(request , pk ):
    product = models.product.objects.get(id = pk)
    
    if request.method == "POST":
        form = forms.product_edit_form(request.POST, instance=product)
        if form.is_valid():
            journals = models.journal.objects.filter(product = product)
            if journals.count() == 0 :
                form.save()
            else:
                form.add_error("name", " ابتدا تمامی اطلاعات این کالا را در دفتر روزنامه پاک کنید .")
    else:
        form = forms.product_edit_form(instance=product)
    context={"form":form}
    return render(request , "admin_panel_store_karaj/product_edit.html" , context)

def product_remove(request , pk ):
    product = models.product.objects.get(id = pk)
    journals = models.journal.objects.filter(product=product)
    if not journals :
        product.delete()
    return redirect("panel_product" )

def product_add(request ):
    form = forms. product_add_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("panel_product" )
        else:
            form.add_error("name", "قبلا کالایی با این کد ساخته شده است")
    context={"form":form}
    return render(request , "admin_panel_store_karaj/product_add.html" , context)

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

def panel_document(request):
    document = models.document.objects.all()
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

    data = {
        "documents":document
    }
    return render(request, 'admin_panel_store_karaj/document.html',context=data)

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
        return redirect("panel_document" )

    if models.document.objects.all().count()!=0 :
        document_last_id = models.document.objects.latest('id').id +1
    else:
        document_last_id = 0
    product = models.product.objects.all()
    context={
        'document_last_id': document_last_id,

        'product': product,
    }
    return render(request , "admin_panel_store_karaj/document_add.html" , context)

def document_edit(request , pk ):
    document = models.document.objects.get(id = pk)
    
    if request.method == "POST":
        sum_debtor = request.POST['sum_debtor'][0].replace(",","")
        sum_creditor = request.POST['sum_creditor'][0].replace(",","")
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
        
        return redirect("panel_document" )

    document =models.document.objects.get(id=pk)
    journals =  document.journals.all()
    product = models.product.objects.all()
    data = {
        "document":document ,
        "journals":journals ,
        'product': product,

    }
    return render(request , "admin_panel_store_karaj/document_edit.html" , data)

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

def check_product(request ):
    if request.method == "POST":
        id = request.POST['id']
        if id == "":
            product = models.product.objects.all()
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
                return render(request, 'admin_panel_store_karaj/check_product.html')
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
    return render(request, 'admin_panel_store_karaj/check_product.html',context=data)

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

def report_one(request ):
    document = models.document.objects.all()
    if request.method == "POST":
        list = []
        id = request.POST['id']
        if id != "":
            for i in document :
                if i.journals.filter(product_id=id).exists():
                    list.append(i)
            document = list

    data = {
        "documents":document
    }
    return render(request, 'admin_panel_store_karaj/report_one.html',context=data)