from .models import StudyMaterial,Subject
from django import forms

class StudyMaterialForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        empty_label="Select Subject Name",
        widget=forms.Select(attrs={'class': 'form-select mb-3', 'required': True})
    )

    class Meta:
        model = StudyMaterial
        fields = ["subject","title", "description", "file" ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control mb-3"}),
            "description": forms.TextInput(attrs={"class": "form-control mb-3"}),
            "file": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        teacher_course = kwargs.pop('teacher_course', None)
        super(StudyMaterialForm, self).__init__(*args, **kwargs)
        if teacher_course:
            self.fields['subject'].queryset = Subject.objects.filter(course=teacher_course).order_by('subject')
        else:
            self.fields['subject'].queryset = Subject.objects.none()

