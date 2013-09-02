# -*- encoding: utf-8 -*- 
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from edu.models import *

from django.template import RequestContext


from edu.forms import FormCodigo
from edu.forms import FormAluno
from edu.forms import FormTurma


from edu.forms import FormResgate

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.views import generic
from django.db.models import *


@login_required
def index(request):
	c = RequestContext(request)
	usuario = Aluno.objects.filter(id = request.user.id)
	if usuario: # usuario é um aluno
		c['aluno'] = usuario[0]
		#c['nome'] = request.user.username
		return 	resgatar_codigo(request)
	else :
		usuario = Professor.objects.filter(id = request.user.id)	
		if usuario: #usuario é um professor
			c['professor'] = usuario[0]
			
			return render_to_response("index_professor.html", c)
		else:
			return render_to_response("index_adm.html", c)


@login_required
def gerar_codigo(request):
	c = RequestContext(request)
	if request.method == "POST":
		form = FormCodigo(request.POST, request.FILES)
		lista = request.POST.getlist("list")
		if form.is_valid():
			dados = form.cleaned_data
			prof = Professor.objects.get(id=request.user.id)
			lista_codigos = prof.criar_codigo(dados['pontos'], dados['qtd'])
			if lista_codigos:
				c['lista_codigos'] = lista_codigos
				c['professor'] = prof
				return render_to_response("mostrar_codigos.html", c)
		elif lista:
			# Crie o objeto HttpResponse com o cabeçalho de PDF apropriado.
		   	response = HttpResponse(mimetype='application/pdf')
		   	response['Content-Disposition'] = 'attachment; filename=codigos.pdf'
			gerar_PDF(response, lista)
			return response
		else:
			form = FormCodigo() 
	else:
		prof = get_object_or_404(Professor, id=request.user.id)
		form = FormCodigo() 
		c['professor'] = prof
	c['form'] = form

	return render_to_response("gerar_codigo.html", c)

@login_required
def resgatar_codigo(request):
	c = RequestContext(request)
	usuario = get_object_or_404(Aluno, id=request.user.id)
	if request.method=="POST":	
		form = FormResgate(request.POST, request.FILES);
		if form.is_valid():
			dados = form.cleaned_data
			if usuario.creditar_pontos(dados['codigo']):
				pass 
			else:
				pass

	c['aluno'] = usuario
	form = FormResgate()	
	c['form'] = form
	return render_to_response("index_aluno.html", c)

# @login_required
# def ranking(request):
# 	c=RequestContext(request)
# 	if request.method="POST":
# 		pass

# 	else:
# 		aluno = Aluno,objects.get(id=request.user.id)
# 		if(aluno != null)
# 			ranking = Aluno.objects.filter(turma=aluno.turma)
# 			c['ranking'] = ranking

# 	return render_to_response("ranking.html", c)	
@login_required		
def ranking_view(request):
	###
	c = RequestContext(request)
	c['aluno'] = request.user
	c['passa'] = True
	if request.method=="POST":
		form = FormTurma(user=request.user, data=request.POST);
		if form.is_valid():
			dados = form.cleaned_data

########## joao paulo mexendo aqui ###############################################################################
			turma = dados['turma']
			colegio = turma.colegio

				#lista com os dicionarios: {nome_aluno, nome_atividade, total_pontos}
			lista_aluno_atividade_pontos = Codigo.objects.filter(turmaprof__turma=turma).exclude(aluno=None).values('aluno__username', 'atividade__atividade__nome').annotate(pontos=Sum('atividade__pontos')).order_by('aluno', 'atividade', '-pontos')
			print lista_aluno_atividade_pontos
				#lista de todas as atividades de um determinado colegio			
			lista_atividades_colegio = AtividadeColegio.objects.filter(colegio=colegio).order_by('-atividade')
			print lista_atividades_colegio
			c['lista_atividades_colegio'] = lista_atividades_colegio
				#numero de atividades de um determinado colegio
			qtd_atividades_colegio = len(lista_atividades_colegio)

			
			lista_dicionario_aluno_potuacao_atividade=[]

				#lista q vai conter as N pontuações referentes as N atividades de um determinado aluno
			lista_aluno_pontacao_atividades = [];

			
				#variavel auxiliar no for. 
			if lista_aluno_atividade_pontos:
				nome_anterior = str(lista_aluno_atividade_pontos[0]['aluno__username'])
				proxima_atividade = 0

				for i in range(len(lista_aluno_atividade_pontos)): #para cada conjunto de valores na lista de dicionarios
					nome_atual = str(lista_aluno_atividade_pontos[i]['aluno__username'])
					if nome_atual == nome_anterior: #verifica se o dicionario atual ainda é do aluno anterior
						for j in range(len(lista_atividades_colegio)): #loop para as N atividades do colegio
							if str(lista_aluno_atividade_pontos[i]['atividade__atividade__nome']) == str(lista_atividades_colegio[j].atividade.nome):
								lista_aluno_pontacao_atividades+=[lista_aluno_atividade_pontos[i]['pontos']]
								proxima_atividade+=1		
								break;
							else:
								if j == proxima_atividade:
									lista_aluno_pontacao_atividades+=[0]
					else:
						lista_dicionario_aluno_potuacao_atividade += [{'nome': nome_anterior, 'pontos': lista_aluno_pontacao_atividades+[sum(lista_aluno_pontacao_atividades)]}]
						lista_aluno_pontacao_atividades = [];
						proxima_atividade = 0
						for j in range(len(lista_atividades_colegio)): #loop para as N atividades do colegio
							if str(lista_aluno_atividade_pontos[i]['atividade__atividade__nome']) == str(lista_atividades_colegio[j].atividade.nome):
								lista_aluno_pontacao_atividades+=[lista_aluno_atividade_pontos[i]['pontos']]
								proxima_atividade+=1
								break;							
							else:
								if j == proxima_atividade:							
									lista_aluno_pontacao_atividades+=[0]
					nome_anterior = nome_atual	
				else:
					lista_dicionario_aluno_potuacao_atividade += [{'nome': nome_anterior, 'pontos': lista_aluno_pontacao_atividades+[sum(lista_aluno_pontacao_atividades)]}]

				#c['lista_alunos'] = Aluno.objects.filter(turma=turma)	
			c['lista_alunos'] = lista_dicionario_aluno_potuacao_atividade

####################################################################################################################	
	else:
		print request.user.id
		form = FormTurma(user=request.user)
		c['form']=form
		c['passa'] = False

	return render_to_response("aluno_ranking.html", c)


class RankingView(generic.ListView):
	template_name = "aluno_ranking.html"
	context_object_name = 'alunos'

	def get_queryset(self):

		##verifica se eh professor:

		# usuario = Professor.objects.get(id=self.request.user.id)
		# if(usuario == null):
		# 	usuario = Aluno.objects.get(id=self.request.user.id)
		# 	turma = TurmaAluno.objects.get(aluno=usuario).turma
		# else:
		# 	turma=TurmaProfessor.objects.get(professor=usuario).turma
		turma = Turma.objects.get(nome=self.request.session['turma'])
		return Aluno.objects.filter(turma=turma)




def cadastrar_aluno(request):
	c = RequestContext(request)
	if request.method=="POST":
		form = FormAluno(request.POST)
		if form.is_valid():
			dados = form.cleaned_data
			colegio = Colegio.objects.get(nome=dados['colegio'])
			turma = Turma.objects.filter(colegio=colegio)

			novo_aluno = Aluno(username=dados['login'], first_name=dados['primeiro_nome'],
						last_name=dados['ultimo_nome'], email=dados['email'], pontos=0)
			novo_aluno.set_password(str(dados['senha']))
			novo_aluno.save()
			turma_aluno = TurmaAluno(aluno=novo_aluno, turma=turma[0])
			turma_aluno.save()

			return HttpResponseRedirect('/login/')
		c['form']= form
	else:
		c['form'] = FormAluno()
	
	return render_to_response("cadastro_aluno.html", c)


def gerar_PDF(response, lista):
	qtd_codigos = len(lista)  # 6 x 30 = 180 codigos por pagina
	qtd_paginas = qtd_codigos*1.0/180

	# Crie o objeto PDF, usando o objeto response como seu "arquivo".
	p = canvas.Canvas(response)
	# Desenhe coisas no PDF. Aqui é onde a geração do PDF acontece.
	# Veja a documentação do ReportLab para a lista completa de
	# funcionalidades.
	
	p.drawString(250, 825, "PRIZE")

	x = 40
	y = 775
	for codigo in lista:
		p.drawString(x, y, codigo)
		y-=25
	# Feche o objeto PDF, e está feito.
	p.showPage()
	p.save()


def get_turmas(request):
	turma = TurmaAluno.objects.filter()
