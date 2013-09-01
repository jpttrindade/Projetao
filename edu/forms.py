# -*- encoding: utf-8 -*- 
from django.forms import ModelForm
from edu.models import Codigo
from edu.models import Aluno, Colegio, Turma
from django import forms
from django.contrib.auth.models import User
#from django.utils.translation import ugettext as _

class FormCodigo(forms.Form):
	pontos = forms.IntegerField()
	qtd = forms.IntegerField()

class FormResgate(forms.Form):
	codigo = forms.CharField()



class FormAluno(forms.Form):
	primeiro_nome = forms.CharField(widget=forms.TextInput, label='Primeiro Nome');
	ultimo_nome = forms.CharField(widget=forms.TextInput, label='Último Nome');
	login = forms.CharField(max_length=30, min_length=4);
	email = forms.EmailField(max_length=75)
	senha = forms.CharField(widget=forms.PasswordInput, min_length=5)
	confirme_senha = forms.CharField(widget=forms.PasswordInput, min_length=5)

	def __init__(self, *args, **kwargs):
		super(FormAluno, self).__init__(*args, **kwargs)
		self.fields['colegio'] = forms.ModelChoiceField(queryset=Colegio.objects.all(), empty_label="Selecione")
		#self.fields['turma'] = forms.ModelChoiceField(queryset=Turma.objects.all())
	# 	pass
	def clean_login(self):
		if User.objects.filter(username=self.cleaned_data['login']).count():
			raise forms.ValidationError('login já cadastrado!')
		return self.cleaned_data['login']

	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data['email']).count():
			raise forms.ValidationError('Email já cadastrado!')
		return self.cleaned_data['email']
	
	def clean_senha(self):
		if self.cleaned_data['senha'] != self.data['confirme_senha']:
			raise forms.ValidationError('Senhas não conferem!')
		return self.cleaned_data['senha']

class FormTurma(forms.Form):

	def __init__(self, user=None, *args, **kwargs):
		super(FormTurma, self).__init__(*args,**kwargs)
		self._user = user
		aluno = Aluno.objects.get(id=self._user.id)
		self.fields['turma'] = forms.ModelChoiceField(queryset=aluno.turma.all())