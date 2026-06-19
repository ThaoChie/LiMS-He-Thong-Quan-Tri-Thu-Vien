from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Review
from .forms import ReviewForm
from apps.catalog.models import Book


@login_required
def review_create_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if Review.objects.filter(user=request.user, book=book).exists():
        messages.warning(request, 'Bạn đã đánh giá sách này rồi.')
        return redirect('catalog:book_detail', pk=book.pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, 'Đánh giá đã được gửi!')
            return redirect('catalog:book_detail', pk=book.pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'book': book})


@login_required
def review_edit_view(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật đánh giá.')
            return redirect('catalog:book_detail', pk=review.book.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form, 'book': review.book, 'editing': True})


@login_required
def review_delete_view(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    book_pk = review.book.pk
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Đã xóa đánh giá.')
    return redirect('catalog:book_detail', pk=book_pk)
