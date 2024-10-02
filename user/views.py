from django.contrib import messages
from django.contrib.auth import login, logout, authenticate 
from .forms import LoginForm, RegisterForm, EditForm
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from django.shortcuts import render

# Create your views here.
class LoginView(TemplateView):

    def get(self, request):
        form = LoginForm()
        return render(request, "user/login.html", {"form":form})

    def post(self, request):
        import pdb; pdb.set_trace()
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.auth(request)
            if user is not None:
                login(request, user)
                return redirect("book:home")
            else:
                form = LoginForm(request.POST)
                return render(request, "user/login.html", {"form":form})
        else:
            return render(request, "user/login.html", {"form":form})


class LogoutView(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('user:login')


class RegisterView(TemplateView):

    def get(self, request):
        form = RegisterForm()
        return render(request=request, template_name="user/signup.html", context={"form":form})

    def post(self, request):

        form = RegisterForm(request.POST)
        if form.is_valid():
            test = form.save()
            username = form.cleaned_data.get('email')
            user = authenticate(username=username, password=test.set_password(form.cleaned_data.get('password')))
            return redirect("user:register")
        else:
            form = RegisterForm(request.POST)
            return render(request, "user/signup.html", {"form":form})


class EditUserView(TemplateView):

    def get(self, request, **kwargs):
        page_user = get_object_or_404(CustomUser, pk=request.user.pk)
        form = EditForm(instance=request.user)
        context = {
                'form': form,
                'page_user': page_user
            }
        return render(request, "user/edit-user.html",context)

    def post(self, request, *args, **kwargs):

        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = EditForm(request.POST, instance=request.user, initial=initial_data)
        page_user = get_object_or_404(CustomUser, **kwargs)
        if form.is_valid():
            update_user = form.save(commit=False)
            update_user.save()
            messages.success(request, 'Updated user details successfully.')
            return redirect("user:edituser", request.user.id)
        else:
            form = EditForm(request.POST,  initial=initial_data)
            return render(request, "user/edit-user.html", {'form':form, 'page_user':page_user})