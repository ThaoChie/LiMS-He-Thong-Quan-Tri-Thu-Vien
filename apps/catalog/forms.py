from django import forms
from .models import Book, Category, Author, Publisher


class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Tìm theo tên sách, tác giả, ISBN...',
    }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False, empty_label='Tất cả thể loại',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'Tất cả trạng thái')] + Book.STATUS_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'isbn', 'authors', 'category', 'publisher',
                  'publication_year', 'description', 'cover_image', 'pdf_file',
                  'total_copies', 'available_copies', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'authors': forms.CheckboxSelectMultiple(),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'publisher': forms.Select(attrs={'class': 'form-select'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên thể loại'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Mô tả'}),
        }
