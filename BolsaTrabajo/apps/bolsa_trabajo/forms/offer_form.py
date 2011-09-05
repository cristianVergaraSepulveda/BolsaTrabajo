#-*- coding: UTF-8 -*-

from django import forms

from bolsa_trabajo.models import OfferLevel


class OfferForm(forms.Form):
    title = forms.CharField(label='Título')
    description = forms.CharField(widget=forms.Textarea(), label='Descripción del trabajo')
    liquid_salary = forms.IntegerField(label='Sueldo líquido (0 si se requiere pretensión de salario)')
    available_slots = forms.IntegerField(label='Número de puestos disponibles (0 si son indeterminados)')
    level = forms.ModelMultipleChoiceField(queryset=OfferLevel.objects.all(), label='Nivel (puede seleccionar más de uno manteniendo apretada la tecla Control)', required = True)
    tags = forms.CharField(label='Palabras clave separadas por coma (e.g. "MySQL, CakePHP")', required=True)

    def clean(self):
        """
        verifies that liquid_salary is higher than the minimum selected offer level requires
        """

        cleaned_data = self.cleaned_data

        if 'level' not in cleaned_data:  # nothing to do
            return cleaned_data

        levels = cleaned_data['level']
        liquid_salary = cleaned_data['liquid_salary']

        selected_levels = OfferLevel.objects.filter(id__in=levels)
        minimum_salary = min((level.minimum_salary for level in selected_levels))

        if liquid_salary > 0 and liquid_salary < minimum_salary:
            msg = u"El sueldo mínimo debe ser mayor a %s para este nivel de oferta" % minimum_salary
            self._errors["liquid_salary"] = self.error_class([msg])

        return cleaned_data

    @staticmethod
    def create_from_offer(offer):
        form = OfferForm()
        form.fields['title'].initial = offer.title
        form.fields['description'].initial = offer.description
        form.fields['liquid_salary'].initial = offer.liquid_salary
        form.fields['available_slots'].initial = offer.available_slots
        form.fields['level'].initial = [level.id for level in offer.level.all()]
        form.fields['tags'].initial = ', '.join([tag.name for tag in offer.tags.all()])
        return form
