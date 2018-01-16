from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def index(request):
    categories = Category.objects.all()
    slider = Slide.objects.filter(slide=True)
    products = Product.objects.all()
    context = {
        'categories': categories,
        'slider': slider,
        'products':products
    }
    return render(request,'shop/index.html',context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if len(username) == 12:
                a = username[:4]+username[6:]
                code = username[4] + username[5]
                branch = ["CS", "IT", "ME", "CE", "EC"]
                if code in branch and int(a):
                    pre = ['0714','0704']
                    b= username[:4]
                    if b in pre:
                        user = form.save()
                        user.refresh_from_db()  # load the profile instance created by the signal
                        user.profile.birth_date = form.cleaned_data.get('birth_date')
                        user.profile.college = form.cleaned_data.get('college')
                        user.profile.branch = form.cleaned_data.get('branch')
                        user.profile.phone = form.cleaned_data.get('phone')
                        user.save()
                        raw_password = form.cleaned_data.get('password1')
                        user = authenticate(username=user.username, password=raw_password)
                        login(request, user)
                        messages.success(request, 'Sign Up Successfull')
                        return redirect('shop:index')
                    else:
                        messages.error(request, 'Please enter correct Roll Number')
                else:
                    messages.error(request, 'Please enter correct Roll Number')
            else:
                messages.error(request, 'Please enter correct Roll Number')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:dashboard')
                else:
                    messages.error(request,'Disabled account')
            else:
                messages.error(request,'Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponse('logout successful')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('shop:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,'registration/profile_edit.html',{'user_form': user_form,'profile_form': profile_form})

@login_required
def dashboard(request):return render(request,'shop/dashboard.html',{'section': 'dashboard'})


#product list and detail
def product_list(request, category_slug=None):
    print(request.GET)
    query = request.GET.get('q')
    print(query)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if query is not None:
        products = products.filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query) |
            #Q(category__icontains=query) |
            Q(description__icontains=query),
        )
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        #category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)
    return render(request,'shop/products/product_list.html',{'category':category,'categories':categories,'products':products})

def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    return render(request,'shop/products/product_detail.html',{'product': product})

def allproducts(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request,'shop/products/allproducts.html',{'categories':categories,'products':products})