from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import CustomLoginForm, CustomRegisterForm, ProfileUpdateForm, UserManageForm
from .models import CustomUser


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'


def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'reader'
            user.save()
            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('accounts:login')
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất thành công.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật hồ sơ thành công!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def user_list_view(request):
    if request.user.role != 'admin':
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('home')
    q = request.GET.get('q', '')
    users = CustomUser.objects.all()
    if q:
        users = users.filter(Q(username__icontains=q) | Q(email__icontains=q))
    paginator = Paginator(users.order_by('-created_at'), 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'accounts/user_list.html', {'page_obj': page, 'q': q})


@login_required
def user_edit_view(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('home')
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserManageForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cập nhật người dùng "{user_obj.username}" thành công!')
            return redirect('accounts:user_list')
    else:
        form = UserManageForm(instance=user_obj)
    return render(request, 'accounts/user_edit.html', {'form': form, 'user_obj': user_obj})


@login_required
def user_toggle_active_view(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('home')
    if request.method == 'POST':
        user_obj = get_object_or_404(CustomUser, pk=pk)
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        status = 'kích hoạt' if user_obj.is_active else 'vô hiệu hóa'
        messages.success(request, f'Đã {status} tài khoản "{user_obj.username}".')
    return redirect('accounts:user_list')
