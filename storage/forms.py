from django import forms


class ObjectForm(forms.Form):
    name = forms.CharField(label='파일 이름',
                           widget=forms.TextInput(attrs={
                               'class': 'form-input',
                               'placeholder': '파일 이름으로 URL이 생성됩니다.',
                           }))
    file = forms.FileField(label='업로드할 파일',
                           widget=forms.FileInput(attrs={
                               'class': 'form-input'
                           }))
