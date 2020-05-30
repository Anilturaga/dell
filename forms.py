from django import forms  
from dell.models import history 
  
class CustomerForm(forms.ModelForm):  
    class Meta:  
        model = history
        fields = "__all__"  