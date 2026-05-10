from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = '__all__'

        widgets = {

            'nome': forms.TextInput(attrs={'class':'form-control'}),

            'cpf': forms.TextInput(attrs={
                'class':'form-control',
                'id':'cpf'
            }),

            'telefone': forms.TextInput(attrs={
                'class':'form-control',
                'id':'telefone'
            }),

            'email': forms.EmailInput(attrs={'class':'form-control'}),

            'departamento': forms.Select(attrs={'class':'form-select'}),

            'cargo': forms.TextInput(attrs={'class':'form-control'}),

            'salario': forms.TextInput(attrs={
                'class':'form-control',
                'id':'salario'
            }),

            'data_nascimento': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),

            'data_admissao': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),

            'cidade': forms.TextInput(attrs={'class':'form-control'}),

            'escolaridade': forms.Select(attrs={'class':'form-select'}),

            'tipo_contrato': forms.Select(attrs={'class':'form-select'}),

            'modelo_trabalho': forms.Select(attrs={'class':'form-select'}),
        }