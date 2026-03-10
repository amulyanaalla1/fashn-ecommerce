from django import forms
from .models import CustomUser, Address


class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "dob"
        ]


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone",
            "address_line",
            "city",
            "pincode"
        ]