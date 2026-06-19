from django import forms
from .models import BookProposal


class ProposalCreateForm(forms.ModelForm):
    class Meta:
        model = BookProposal
        fields = ('title', 'author_name', 'isbn', 'reason')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên sách muốn đề xuất'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên tác giả (nếu biết)'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mã ISBN (nếu biết)'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Lý do đề xuất mua sách này...'}),
        }
