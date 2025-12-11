from django import forms
from .models import FinancialTracker

class GoalForm(forms.ModelForm):
    class Meta:
        model = FinancialTracker
        fields = ['name', 'target_amount', 'deadline']


class UpdateSavingsForm(forms.ModelForm):
    class Meta:
        model = FinancialTracker
        fields = ['current_amount']
        widgets = {
            'current_amount': forms.NumberInput(attrs={
                'class': 'form-control figma-input',
                'placeholder': 'Enter new saved amount'
            })
        }