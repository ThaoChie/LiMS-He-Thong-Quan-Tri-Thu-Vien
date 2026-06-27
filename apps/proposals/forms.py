from django import forms
from .models import BookProposal


class ProposalCreateForm(forms.ModelForm):
    class Meta:
        model = BookProposal
        fields = ('isbn', 'title', 'author_name', 'reason')
        widgets = {
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mã ISBN (Bắt buộc - VD: 9786041234567)', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên sách muốn đề xuất', 'required': True}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên tác giả'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Lý do đề xuất mua sách này...', 'required': True}),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn:
            raise forms.ValidationError("Mã ISBN là bắt buộc.")
        clean_code = ''.join(filter(str.isalnum, isbn))
        if len(clean_code) not in [10, 13]:
            raise forms.ValidationError("Mã ISBN phải gồm 10 hoặc 13 ký tự.")
        return clean_code

