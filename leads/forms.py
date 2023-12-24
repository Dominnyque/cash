from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields =(
            'last_name',
            'first_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )
class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields =(
            'category',
        )
class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    age = forms.IntegerField(min_value=0)

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organisation = request.user.userprofile)
        super (AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents            