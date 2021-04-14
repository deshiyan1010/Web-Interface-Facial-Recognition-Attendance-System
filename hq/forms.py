from django import forms
from hq.models import Person, PersonImage,PersonBuffer

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('id_number','name')

class PersonImageForm(forms.ModelForm):

    class Meta:
        model = PersonImage
        fields = ('pictures',)

class PersonBufferForm(forms.Form):
    list_of_people = forms.ModelChoiceField(queryset=PersonBuffer.objects.all().order_by('name'),to_field_name="id_number")
    class Meta:
        model = Person
        fields = ('list_of_people',)
        