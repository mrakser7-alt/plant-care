# форма добавления/редактирования растения
# ModelForm сам лепит поля из модели

from django import forms

from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        # какие поля показывать юзеру (user не тут, его выставляем во вьюхе)
        fields = [
            'name',
            'plant_type',
            'photo',
            'last_watered',
            'last_repotted',
            'is_alive',
            'notes',
        ]
        # виджеты = как рендерить поле в html
        widgets = {
            'last_watered': forms.DateInput(attrs={'type': 'date'}),
            'last_repotted': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # накидываем на все поля bootstrap-классы чтобы красиво выглядело
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-check-input')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
            else:
                field.widget.attrs.setdefault('class', 'form-control')
