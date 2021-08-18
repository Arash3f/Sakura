from django.shortcuts import redirect, render
from admin_panel_store_materials import models
from admin_panel_store_materials import forms
from django.http import HttpResponse
import xlwt
from django.db.models import Q, Sum

# Create your views here.

def panel_materials(request):
    materials = models.materials.objects.all()
    if request.method == "POST":
        id = request.POST['id']
        if id != "":
            materials = materials.filter(id=id)
    data = {
        "materials":materials
    }
    return render(request, 'admin_panel_store_materials/materials.html',context=data)

def materials_edit(request , pk ):
    materials = models.materials.objects.get(id = pk)
    
    if request.method == "POST":
        form = forms.materials_edit_form(request.POST, instance=materials)
        if form.is_valid():
            journals = models.journal.objects.filter(materials = materials)
            if journals.count() == 0 :
                form.save()
            else:
                form.add_error("name", " ابتدا تمامی اطلاعات این کالا را در دفتر روزنامه پاک کنید .")
    else:
        form = forms.materials_edit_form(instance=materials)
    context={"form":form}
    return render(request , "admin_panel_store_materials/materials_edit.html" , context)

def materials_remove(request , pk ):
    materials = models.materials.objects.get(id = pk)
    journals = models.journal.objects.filter(materials=materials)
    if not journals :
        materials.delete()
    return redirect("panel_materials" )

def materials_add(request ):
    form = forms. materials_add_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("panel_materials" )
        else:
            form.add_error("name", "قبلا کالایی با این کد ساخته شده است")
    context={"form":form}
    return render(request , "admin_panel_store_materials/materials_add.html" , context)

def export_materials_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="materials.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('materials')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['کد کالا', 'نام کالا' , ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = models.materials.objects.all().values_list('id', 'name' ,)
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
    return render(request, 'admin_panel_store_materials/document.html',context=data)

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
            materials = models.materials.objects.get(id=code[i] , name=name[i])
            models.journal.objects.create(document = document , materials = materials ,description = description[i] ,debtor=debtor[i].replace(",",""),creditor=creditor[i].replace(",",""))
        return redirect("panel_document" )

    if models.document.objects.all().count()!=0 :
        document_last_id = models.document.objects.latest('id').id +1
    else:
        document_last_id = 0
    materials = models.materials.objects.all()
    context={
        'document_last_id': document_last_id,

        'materials': materials,
    }
    return render(request , "admin_panel_store_materials/document_add.html" , context)

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
            materials = models.materials.objects.get(id=code[i] , name=name[i])
            models.journal.objects.create(document = document , materials = materials ,description = description[i] ,debtor=debtor[i].replace(",",""),creditor=creditor[i].replace(",",""))
        
        return redirect("panel_document" )

    document =models.document.objects.get(id=pk)
    journals =  document.journals.all()
    materials = models.materials.objects.all()
    data = {
        "document":document ,
        "journals":journals ,
        'materials': materials,

    }
    return render(request , "admin_panel_store_materials/document_edit.html" , data)

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

def check_materials(request ):
    if request.method == "POST":
        id = request.POST['id']
        if id == "":
            materials = models.materials.objects.all()
            sum_debtors =models.journal.objects.aggregate(Sum('debtor'))['debtor__sum']
            sum_creditors = models.journal.objects.aggregate(Sum('creditor'))['creditor__sum']
            result = sum_debtors - sum_creditors
        else:
            if models.materials.objects.filter(id = id).exists():
                materials = models.materials.objects.filter(id = id)
                sum_debtors =models.journal.objects.filter(materials=materials[0]).aggregate(Sum('debtor'))['debtor__sum']
                sum_creditors = models.journal.objects.filter(materials=materials[0]).aggregate(Sum('creditor'))['creditor__sum']
                result = sum_debtors - sum_creditors
            else:
                return render(request, 'admin_panel_store_materials/check_materials.html')
    else:
        materials = models.materials.objects.all()
        sum_debtors =models.journal.objects.aggregate(Sum('debtor'))['debtor__sum']
        sum_creditors = models.journal.objects.aggregate(Sum('creditor'))['creditor__sum']
        if not sum_debtors == None :
            result = sum_debtors - sum_creditors
        else:
            result = 0

    journals_list = []
    for materials in materials :
        new_dic = {}
        debtors = 0
        creditors = 0
        journals = models.journal.objects.filter(materials=materials)
        for journal in journals :
            debtors += journal.debtor
            creditors += journal.creditor
        new_dic["code"] = materials.id
        new_dic["name"] = materials.name
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
    return render(request, 'admin_panel_store_materials/check_materials.html',context=data)

def export_check_materials_xls(request):
    
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

    materials = models.materials.objects.all()


    sum_debtors =models.journal.objects.aggregate(Sum('debtor'))['debtor__sum']
    sum_creditors = models.journal.objects.aggregate(Sum('creditor'))['creditor__sum']
    item_list = []
    sum_debtors = 0
    sum_creditors = 0

    for material in materials :
        list=[]
        list.append(material.id)
        list.append(material.name)
        if models.journal.objects.filter(materials=material).exists():
            debtor =models.journal.objects.filter(materials=material).aggregate(Sum('debtor'))['debtor__sum']
            creditor = models.journal.objects.filter(materials=material).aggregate(Sum('creditor'))['creditor__sum']
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
                if i.journals.filter(materials_id=id).exists():
                    list.append(i)
            document = list

    data = {
        "documents":document
    }
    return render(request, 'admin_panel_store_materials/report_one.html',context=data)