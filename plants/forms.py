from django import forms

from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name',
            'species',
            'photo',
            'watering_interval_days',
            'last_watered',
            'notes',
        ]
        widgets = {
            'last_watered': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = 'form-control'
            if isinstance(field.widget, forms.ClearableFileInput):
                css = 'form-control'
            field.widget.attrs.setdefault('class', css)
