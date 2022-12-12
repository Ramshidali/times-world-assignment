import datetime
import json
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.decorators import role_required
from users.forms import SignInForm, SignUpForm
from users.models import Users
from users.functions import generate_form_errors, get_auto_id, get_current_role

# Create your views here.
def index(request):

    context = {
        'page_name' : 'Dashboard',
    }

    return render(request,'index.html', context)


def user_login(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]



            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request,user)
                    if User.objects.filter(id=request.user.id,is_active=True,groups__name="admin").exists() :

                        response_data = {
                            "status": "true",
                            "title": "Successfully",
                            "message": "Login Successfull",
                            "redirect": "true",
                            "redirect_url": reverse('users:admin_dashboard')
                        }

                    elif User.objects.filter(id=request.user.id,is_active=True,groups__name="staff").exists() :

                        response_data = {
                            "status": "true",
                            "title": "Successfully",
                            "message": "Login Successfull",
                            "redirect": "true",
                            "redirect_url": reverse('users:staff_dashboard')
                        }

                    elif User.objects.filter(id=request.user.id,is_active=True,groups__name="editor").exists():

                        response_data = {
                            "status": "true",
                            "title": "Successfully",
                            "message": "Login Successfull",
                            "redirect": "true",
                            "redirect_url": reverse('users:editor_dashboard')
                        }

                    elif User.objects.filter(id=request.user.id,is_active=True,groups__name="student").exists():

                        response_data = {
                            "status": "true",
                            "title": "Successfully",
                            "message": "Login Successfull",
                            "redirect": "true",
                            "redirect_url": reverse('users:student_dashboard')
                        }

                else:
                    message = "username and password incorrect"
                    response_data = {
                        "status": "false",
                        "title": "failed",
                        "message": str(message)
                    }
            else:
                message = "User not found"
                response_data = {
                    "status": "false",
                    "title": "Form validation error",
                    "message": str(message)
                }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": str(message)
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = SignInForm()

        context = {
            'page_name' : 'Login',
            'form' : form,
            "url": reverse('users:user_login')
        }

        return render(request,'registration/login.html', context)


def user_registration(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)
        role = request.POST.get('role')

        if form.is_valid():

            user_data = User.objects.create_user(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                is_active=True,
            )

            print(user_data,type(user_data))

            if Group.objects.filter(name=role).exists():
                group = Group.objects.get(name=role)
            else:
                group = Group.objects.create(name=role)

            user_data.groups.add(group)

            data = form.save(commit=False)
            data.user = user_data
            data.auto_id = get_auto_id(Users)
            data.creator = user_data
            data.updater = user_data
            data.updater = user_data
            data.date_updated = datetime.datetime.now()
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully",
                "message": "Registartion successfully Completed.",
                "redirect": "true",
                "redirect_url": reverse('users:user_login')
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": str(message)
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = SignUpForm()

    context = {
        'page_name' : 'Registration',
        'form' : form,
        "url": reverse('users:user_registration')
    }

    return render(request,'registration/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect(reverse('users:user_login'))

@login_required
@role_required(['student'])
def student_dashboard(request):

    context = {
        'page_name' : 'Student Dashboard',
    }

    return render(request,'student_dashboad.html', context)


@login_required
@role_required(['admin'])
def admin_dashboard(request):

    context = {
        'page_name' : 'Admin Dashboard',
    }

    return render(request,'admin_dashboad.html', context)


@login_required
@role_required(['editor'])
def editor_dashboard(request):

    context = {
        'page_name' : 'Editor Dashboard',
    }

    return render(request,'editor_dashboad.html', context)


@login_required
@role_required(['staff'])
def staff_dashboard(request):

    context = {
        'page_name' : 'Staff Dashboard',
    }

    return render(request,'staff_dashboad.html', context)