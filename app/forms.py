from django import forms
from app import models


class domainForm(forms.ModelForm):
    class Meta:
        model = models.domain
        fields="__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class accountForm(forms.ModelForm):
    class Meta:
        model = models.account
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class domainsiteForm(forms.ModelForm):
    class Meta:
        model = models.domainsite
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class nameserverForm(forms.ModelForm):
    class Meta:
        model = models.nameserver
        fields = "__all__"
        exclude = ['domainsite']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class recordForm(forms.ModelForm):
    class Meta:
        model = models.record
        # fields = ['hostrecord','type','recordvalue','status']
        fields = "__all__"
        exclude = ['main_domain']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            # self.fields['main_domain'].choices = [(self.instance.main_domain.pk, self.instance.main_domain.name)]