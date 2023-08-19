from django import forms
from .models import *
from django.forms import ModelForm, TextInput, EmailField, FloatField, ChoiceField, DateField, NumberInput
from django.core.exceptions import ValidationError
import datetime

class MonthDayField(forms.DateField):
    def to_python(self, value):
        if value:
            # Verifique se a data está no formato correto (MM-DD)
            parts = value.split('/')
            if len(parts) != 2:
                raise forms.ValidationError('Os valores devem ser separado por barra ')
            
            try:
                month = int(parts[1])
                day = int(parts[0])
            except ValueError:
                raise forms.ValidationError('')

            # Crie um objeto de data com o ano atual e o mês e dia fornecidos
            today = datetime.date.today()
            year = today.year

            try:
                return datetime.date(year, month, day)
            except ValueError:
                raise forms.ValidationError('Data inválida')

        return None
    
class Add_despesa(forms.ModelForm):
    
    Prioridades = [
        ('Alta Prioridade', 'Alta Prioridade'),
        ('Media Prioridade', 'Media Prioridade'),
        ('Baixa Prioridade', 'Baixa Prioridade'),
    ]
    Status = [
    ('Pago', 'Pago'),
    ('Pendente', 'Pendente'),
    ('Vencida', 'Vencida')
    ]   
    
 
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;'}))
    status = forms.ChoiceField(choices=Status, widget=forms.Select(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;'}))
    valor = forms.DecimalField(widget=forms.TextInput(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;', 'placeholder': ' Ex: 123.12'}))
    prioridade = forms.ChoiceField(choices=Prioridades, widget=forms.Select(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;'}))
    data_entrada = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Entrada', 'type': 'date'}))
    data_vencimento = MonthDayField(widget=forms.TextInput(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;', 'placeholder': 'Formato DD-MM'}))
    parcelas = forms.IntegerField(required=False , widget=forms.NumberInput(attrs={ 'class': "form-control", 'style': 'max-width: 300px; text-align: left;', 'placeholder': 'Parcelas'}))
     
     
     
    
    class Meta: 
        model = Despesa
        fields = ['nome', 'valor', 'prioridade','data_entrada', 'data_vencimento','parcelas','status']
        
class DespesaForm(forms.ModelForm):
    prioridade = forms.ChoiceField(choices=Prioridades, widget=forms.Select(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;'}))
    status = forms.ChoiceField(choices=Status, widget=forms.Select(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;'}))
    parcelas = forms.IntegerField(required=False , widget=forms.NumberInput(attrs={ 'class': "form-control", 'style': 'max-width: 300px; text-align: left;', 'placeholder': 'Parcelas'}))
    
    class Meta:
        model = Despesa
        fields = ['nome', 'valor', 'data_vencimento', 'parcelas','prioridade', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_entrada' : forms.DateInput(attrs={'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control'}),

        }

class Add_receita (forms.ModelForm):
    
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;'}))
    valor = forms.DecimalField(widget=forms.TextInput(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;', 'placeholder': ' Ex: 123.12'}))
    data_entrada = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Entrada', 'type': 'date'}))
    
    class Meta:
        model = Receita
        fields = ['nome', 'valor','data_entrada']
        

class ReceitaForm(forms.ModelForm):
 
    class Meta:
        model = Receita
        fields = ['nome', 'valor', 'data_entrada']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_entrada' : forms.DateInput(attrs={'class': 'form-control'}),

        }
        
class CartaoForm (forms.ModelForm):
    saldo_cartao = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;'}))
    
    class Meta:
     model = Cartao_credito
     fields = ['Marca', 'saldo_cartao', 'limite']
     widgets = {
            'Marca': forms.TextInput(attrs={'class': 'form-control'}),
            'limite': forms.TextInput(attrs={'class': 'form-control'}),
            
      }
     
      
class Cartao_att(forms.ModelForm):
    
    
    class Meta: 
        model = Cartao_credito
        fields = ['Marca', 'saldo_cartao', 'limite']
        widgets = {
            'Marca': forms.TextInput(attrs={'class': 'form-control'}),
            'saldo_cartao': forms.NumberInput(attrs={'class': 'form-control'}),
            'limite' : forms.NumberInput(attrs={'class': 'form-control'}),

        }
        
class ChequeForm (forms.ModelForm):
    saldo_cheque = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'style': 'max-width: 300px; text-align: left;'}))
    
    class Meta:
     model = Cheque_esp
     fields = [ 'saldo_cheque', 'limite', 'juros','banco']
     widgets = {
            'limite': forms.TextInput(attrs={'class': 'form-control'}),
            'saldo_cheque': forms.TextInput(attrs={'class': 'form-control'}),
            'juros': forms.TextInput(attrs={'class': 'form-control'}),
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            
            
      }


    
    