from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone

from .models import PhoneNumber, ExtendedUser
import pandas as pd



def phone_number_list_view(request):
    phone_numbers = PhoneNumber.objects.all()

    if 'download' in request.GET:
        df = pd.DataFrame(list(phone_numbers.values()))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=phone_numbers.xlsx'
        df.to_excel(response, index=False)
        return response

    return render(request, 'phone_number_list.html', {'phone_numbers': phone_numbers})


def phone_number_view(request):
    if request.method == 'POST':
        student_name = request.POST['student_name']
        email = request.POST['email']
        school = request.POST['school']
        phone_number = request.POST['number']
        comments = request.POST['textarea1']
        user = request.user.username

        if PhoneNumber.objects.filter(number=phone_number).exists():
            error_message = "Phone number already exists."
        elif PhoneNumber.objects.filter(email=email).exists():
            error_message = "Email already exists."
        else:
            PhoneNumber.objects.create(student_name=student_name, email=email, school=school, number=phone_number,
                                       comments=comments,user=user,created_at=timezone.localtime())
            return render(request, 'phone_number.html', {'error_message': "Thank you, Added successfully. Please enter new contact."})

        return render(request, 'phone_number.html', {'error_message': error_message})
    return render(request, 'phone_number.html')


def success_view(request):
    return render(request, 'success.html')

def register(request):
    if request.method=='POST':
        username = request.POST['username']
        firstname = request.POST['first_name']
        password = request.POST['password']
        cpassword = request.POST['password1']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username not available")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already exists")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password,first_name=firstname,email=email)
                user.save();
                extended_user = ExtendedUser(user=user, contact_number=contact_number, password_backup=cpassword)
                extended_user.save()
                return redirect('login')

        else:
            messages.info(request,"Password not matching")
            return redirect('register')
        return redirect('/')

    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"INCORRECT USERNAME OR PASSWORD")
            return redirect('login')
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


from django.db.models import Count

def user_data_count_view(request):
    user_data_counts = PhoneNumber.objects.values('user').annotate(count=Count('user')).order_by('-count')
    return render(request, 'user_data_count.html', {'user_data_counts': user_data_counts})
