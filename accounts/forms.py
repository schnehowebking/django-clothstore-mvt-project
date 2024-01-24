
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, AuthenticationForm, UserChangeForm
from django import forms
from .constants import GENDER
from django.contrib.auth.models import User
from .models import *

class UserRegistrationForm(UserCreationForm):
    
    gender = forms.ChoiceField(choices=GENDER)
    mobile_no = forms.CharField(max_length=12)
    class Meta:
        model = User
        fields = ['first_name', 'last_name',  'email', 'gender','mobile_no', 'username', 'password1', 'password2']
        
    def save(self, commit=True):
        our_user = super().save(commit=False) 
        if commit == True:
            
            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            email = self.cleaned_data.get('email')
            username = self.cleaned_data.get('username')
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            gender = self.cleaned_data.get('gender')
            mobile_no = self.cleaned_data.get('mobile_no')

            if password1 != password2:
                raise forms.ValidationError({'error': "Password Doesn't Matched"})
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError({'error': "Email Already Exists"})
            
            our_user.is_active = False
            our_user.save()

            Customer.objects.create(
                user = our_user,
                gender = gender,
                mobile_no = mobile_no
            )
           
        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'w-100 form-control border-1 py-1'
                    
                ) 
            })


class UserUpdateForm(forms.ModelForm):
    image = forms.ImageField()
    gender = forms.ChoiceField(choices=GENDER)
    mobile_no = forms.CharField(max_length=12)

    class Meta:
        model = User
        fields = ['image', 'first_name', 'last_name', 'gender', 'mobile_no', 'email']

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit:
            # Handle image upload
            image = self.cleaned_data.get('image')
            if image:
                our_user.image = image
            our_user.save()
            

            customer = our_user.user
            customer.first_name = self.cleaned_data.get('first_name')
            customer.last_name = self.cleaned_data.get('last_name')
            customer.email = self.cleaned_data.get('email')
           
            customer.save()

        return our_user

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-100 form-control border-1 py-1'
            })

        # Set initial values
        if self.instance:
            self.initial['image'] = self.instance.image
            self.initial['gender'] = self.instance.gender
            self.initial['mobile_no'] = self.instance.mobile_no
            self.initial['first_name'] = self.instance.user.first_name
            self.initial['last_name'] = self.instance.user.last_name
            self.initial['email'] = self.instance.user.email


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'w-100 form-control border-1 py-1'
                )
            })




class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'w-100 form-control border-1 py-1'
                )
            })



class AddBalanceForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=12, decimal_places=2)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'w-100 form-control border-1 py-1'
                )
            })


