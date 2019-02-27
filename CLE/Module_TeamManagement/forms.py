from django import forms
from Module_TeamManagement.models import *

class TrailheadForm(forms.ModelForm):
    class Meta:
        model = Trailmix_Information
        fields = ( 'link','course', )

# class InstructorToolsForm(forms.Form):
#     tools = forms.ChoiceField(choices=[('Trailhead','Tableau','Kahoot')])

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=8)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if len(phone_number) != 8:
            raise forms.ValidationError("This is not a valid number")
        return phone_number

class VerificationCodeForm(forms.Form):
    login_code = forms.CharField(max_length=6)
