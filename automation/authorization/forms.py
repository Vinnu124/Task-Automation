from django import forms
from .models import autho

class login_form(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    class Meta:
        model = autho
        fields = ['username','email','password']


class signup_form(forms.ModelForm):
    create_username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create Username'}))
    enter_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    create_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = autho
        fields = []  # Include the fields here

    def clean(self):
        cleaned_data = super().clean()
        intial_pass = cleaned_data.get("create_password")
        final_pass = cleaned_data.get("confirm_password")

        if intial_pass != final_pass:
            raise forms.ValidationError("Make sure the password is the same")

    # def save(self, commit=True):
    #     instance = super(signup_form, self).save(commit=False)
    #     instance.password = self.cleaned_data['create_password']
    #     if commit:
    #         instance.save()
    #     return instance
