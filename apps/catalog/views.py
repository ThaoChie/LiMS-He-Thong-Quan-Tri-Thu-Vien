from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg

from .models import Book, Category
from .forms import BookSearchForm, BookForm, CategoryForm


def book_list_view(request):
    books = Book.objects.prefetch_related('authors').select_related('category').order_by('-created_at')
    cat = request.GET.get('category')
    if cat:
        books = books.filter(category_id=cat)
    paginator = Paginator(books, 12)
    page = paginator.get_page(request.GET.get('page'))
    categories = Category.objects.all()
    return render(request, 'catalog/book_list.html', {
        'page_obj': page, 'categories': categories, 'current_cat': cat,
    })


def book_detail_view(request, pk):
    book = get_object_or_404(Book.objects.prefetch_related('authors', 'reviews__user').select_related('category', 'publisher'), pk=pk)
    reviews = book.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    user_has_reviewed = False
    user_has_borrowed = False
    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()
        from apps.circulation.models import BorrowRecord
        user_has_borrowed = BorrowRecord.objects.filter(user=request.user, book=book, status='returned').exists()
    return render(request, 'catalog/book_detail.html', {
        'book': book, 'reviews': reviews, 'avg_rating': avg_rating,
        'user_has_reviewed': user_has_reviewed, 'user_has_borrowed': user_has_borrowed,
    })


def book_search_view(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.prefetch_related('authors').select_related('category')
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        if q:
            books = books.filter(
                Q(title__icontains=q) | Q(authors__name__icontains=q) | Q(isbn__icontains=q)
            ).distinct()
        if category:
            books = books.filter(category=category)
        if status:
            books = books.filter(status=status)
    paginator = Paginator(books.order_by('-created_at'), 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'catalog/book_search.html', {'form': form, 'page_obj': page})


def _check_staff(request):
    if request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Bạn không có quyền truy cập.')
        return False
    return True


@login_required
def book_manage_view(request):
    if not _check_staff(request):
        return redirect('home')
    q = request.GET.get('q', '')
    books = Book.objects.prefetch_related('authors').select_related('category')
    if q:
        books = books.filter(Q(title__icontains=q) | Q(isbn__icontains=q))
    paginator = Paginator(books.order_by('-created_at'), 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'catalog/book_manage.html', {'page_obj': page, 'q': q})


@login_required
def book_create_view(request):
    if not _check_staff(request):
        return redirect('home')
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm sách thành công!')
            return redirect('catalog:book_manage')
    else:
        form = BookForm()
    return render(request, 'catalog/book_form.html', {'form': form, 'title': 'Thêm sách mới'})


@login_required
def book_edit_view(request, pk):
    if not _check_staff(request):
        return redirect('home')
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật sách thành công!')
            return redirect('catalog:book_manage')
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/book_form.html', {'form': form, 'title': f'Chỉnh sửa: {book.title}', 'book': book})


@login_required
def book_delete_view(request, pk):
    if not _check_staff(request):
        return redirect('home')
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        messages.success(request, 'Đã xóa sách thành công.')
    return redirect('catalog:book_manage')


@login_required
def category_manage_view(request):
    if not _check_staff(request):
        return redirect('home')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm thể loại thành công!')
            return redirect('catalog:category_manage')
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'catalog/category_manage.html', {'form': form, 'categories': categories})


@login_required
def category_edit_view(request, pk):
    if not _check_staff(request):
        return redirect('home')
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thể loại thành công!')
            return redirect('catalog:category_manage')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'catalog/category_form.html', {'form': form, 'category': category})


@login_required
def category_delete_view(request, pk):
    if not _check_staff(request):
        return redirect('home')
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Đã xóa thể loại.')
    return redirect('catalog:category_manage')
