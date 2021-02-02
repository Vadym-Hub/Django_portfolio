from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module


class CourseModelForm(forms.ModelForm):
    """
    Базовая форма модели Course/
    """

    class Meta:
        model = Course
        fields = ['subject', 'title', 'slug', 'overview']


ModuleFormSet = inlineformset_factory(Course, Module,
                                      fields=['title', 'description'],
                                      extra=1,
                                      can_delete=True)


class CourseEnrollForm(forms.Form):
    """
    Форма для записи на курсы.
    """
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)
