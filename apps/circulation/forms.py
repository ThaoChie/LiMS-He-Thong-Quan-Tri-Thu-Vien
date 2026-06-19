from django import forms


class BorrowRequestForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': 3, 'placeholder': 'Ghi chú (tùy chọn)',
    }), label='Ghi chú')


class BorrowApproveForm(forms.Form):
    action = forms.ChoiceField(choices=[('approve', 'Duyệt'), ('reject', 'Từ chối')],
                               widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    due_days = forms.IntegerField(initial=14, min_value=1, max_value=90,
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:100px'}),
                                  label='Số ngày mượn')
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), label='Ghi chú')
