from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import Employee,role,Department
from datetime import datetime
from django.db.models import Q
from emp_app.forms import  UserForm

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    print(context)
    return render(request, 'view_all_emp.html',context)

def add_emp(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        salary=int(request.POST['salary'])
        bonus=int(request.POST['bonus'])
        phone=int(request.POST['phone'])
        dept=int(request.POST['dept'])
        role=int(request.POST['role'])
        hra=int(request.POST['hra'])
        new_emp= Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id= dept, role_id=role,hire_data=datetime.now(),hra=hra)
        new_emp.save()
        return HttpResponse("Employee added successfully")
    elif request.method=='GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception Occured! Employee Has Not be added") 

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Please Enter a valid Employee ID")
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    return render(request, 'remove_emp.html',context)

def filter_emp(request):
    if request.method=='POST':
        name=request.POST['name']
        dept=request.POST['dept']
        role=request.POST['role']
        emps=Employee.objects.all()
        if name:
            emps=emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps=emps.filter(dept__name__icontains=dept)
        if role:
             emps=emps.filter(role__name__icontains=role)
        context={
        'emps':emps
           }
        return render(request, 'view_all_emp.html',context)
    elif request.method =='GET':
       return render(request, 'filter_emp.html')
    else:
        return HttpResponse("An Exception Occured")

def base(request):
    return render(request, 'base.html')

def userview(request):
    return render(request,'userview.html')

def special(request):
    return HttpResponse("You are logged in!")

def home(request):
    return HttpResponse("You are logged in!")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return HttpResponseRedirect(reverse('userlogin'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'register.html',
                  {'user_form': user_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('base'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone failed to login")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'login.html', {})
    
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('userview'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone failed to login")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'userlogin.html', {})

def inde(request):
    emps= Employee.objects.all()
    context = {
        'emps': emps,
    }
    return render(request, 'inde.html', context)

def pay_slip(request, pk):
    emps= Employee.objects.get(id=pk)
    template_path = 'staff_payslip.html'
    context = {
        'emps': emps,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



