from django.db import models
import django.contrib.auth.models
from random import choice

# Create your models here.
class Aluno (django.contrib.auth.models.User):
	pontos=models.IntegerField()
	
	def __unicode__(self):
		return self.username

	def set_pontos(self):
		self.pontos=0;

	def creditar_pontos(self,codigo):
		retorno = False
		try:
			cod =Codigo.objects.get(cod=codigo)
	   		if cod: # achou o codigo.
				if cod.status==0:
					cod.status=1
					cod.aluno = self
					self.pontos+=cod.pontos
					self.save()
					cod.save()
					retorno = True
				else: #codigo ja utilizado
					pass
		except Codigo.DoesNotExist:
			pass
		return retorno

class Recompensa (models.Model):
	preco=models.IntegerField()
	descricao=models.CharField(max_length=140)
	nome=models.CharField(max_length=30)
	aluno=models.ForeignKey(Aluno, null=True)

	def __unicode__(self):
		return self.nome
 
class Professor (django.contrib.auth.models.User):
	def __unicode__(self):
		return self.username

		
	def criar_codigo(self, pts, qtd):
		l=[]
		for j in range(qtd):
			codigo=''
			novoCod = not None
			while novoCod:
				for i in range(5):
					codigo+=choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz')
				codigo+=str(pts)
				novoCod = Codigo.objects.filter(cod=codigo)
			novoCod = Codigo(cod=codigo,status=False,professor=self,pontos=pts)
			novoCod.save()
			l.append(novoCod)
		return l
	

	
class Disciplina (models.Model):
	nome=models.CharField(max_length=30)
	professor = models.ForeignKey(Professor)
	def __unicode__(self):
		return self.nome

class Codigo (models.Model):
	cod=models.CharField(max_length=15, null=False)
	status=models.BooleanField()
	professor = models.ForeignKey(Professor)
	aluno = models.ForeignKey(Aluno,null=True)
	pontos = models.IntegerField(null=False)
	def __unicode__(self):
		return self.cod


