from django import forms
from .models import check

class checkForm(forms.Form):
    check_img=forms.ImageField(label='Cheque Image(Front)')
    back_check_img=forms.ImageField(label='Cheque Image(Back)')