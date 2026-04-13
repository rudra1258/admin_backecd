from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'category', 'message', 'nps_score']
 
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating or not (1 <= rating <= 5):
            raise forms.ValidationError('Please select a rating between 1 and 5.')
        return rating
 
    def clean_nps_score(self):
        nps = self.cleaned_data.get('nps_score')
        if nps is not None and not (0 <= nps <= 10):
            raise forms.ValidationError('NPS score must be between 0 and 10.')
        return nps