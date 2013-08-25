# -*- coding: utf-8 -*- 
from django.db import models
import django.contrib.auth.models
from random import choice

# Create your models here.
class Colegio(models.Model):
	nome=models.CharField(max_length=16)
	def __unicode__(self):
		return self.nome

class Aluno (django.contrib.auth.models.User):
	turma = models.ManyToManyField('Turma',through='TurmaAluno')
	pontos=models.IntegerField(default=0)
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

class Professor (django.contrib.auth.models.User):
	turma = models.ManyToManyField('Turma',through='TurmaProfessor')
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



class TurmaAluno (models.Model): # -- verificar o que deve ser único..
	aluno=models.ForeignKey(Aluno)
	turma=models.ForeignKey('Turma')

class TurmaProfessor (models.Model):
	disciplina = models.CharField(max_length=16)
	professor=models.ForeignKey(Professor)
	turma = models.ForeignKey('Turma')
	def __unicode__(self):
		return "%s:%s" % (self.professor.username , self.turma.nome)

class Turma (models.Model):
	nome=models.CharField(max_length=16)
	colegio = models.ForeignKey(Colegio)
	def __unicode__(self):
		return self.nome
 
class Codigo (models.Model):
	cod=models.CharField(max_length=15)
	status=models.BooleanField(default=False)
	aluno = models.ForeignKey(Aluno,null=True,blank=True)
	atividade = models.ForeignKey('AtividadeColegio')
	turmaprof = models.ForeignKey('TurmaProfessor')
	# atividade = models.ForeignKey('AtvTurmaProf',null=True,blank=True)
	def __unicode__(self):
		return self.cod

class Atividade (models.Model):
	nome = models.CharField(max_length=16)
	colegio = models.ManyToManyField(Colegio,through='AtividadeColegio')
	# turma_professor = models.ManyToManyField(TurmaProfessor,through='AtvTurmaProf')
	def __unicode__(self):
		return self.nome

class AtividadeColegio (models.Model):
	atividade = models.ForeignKey(Atividade)
	colegio = models.ForeignKey(Colegio)
	pontos = models.IntegerField()
	def __unicode__(self):
		return "%s: (%s) %spts" % (self.colegio.nome, self.atividade.nome, self.pontos)

##### Classes Deprecated #####

# class AtvTurmaProf (models.Model):
# 	atividade = models.ForeignKey(Atividade)
# 	turmaprof = models.ForeignKey(TurmaProfessor)
# 	pontos = models.IntegerField()
