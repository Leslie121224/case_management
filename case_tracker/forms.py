from django import forms
from .models import Case

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["case_number", "department", "circuit_diagram", "model_type", "business_case_number", "software_version", "status"]
