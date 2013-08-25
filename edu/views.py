# -*- encoding: utf-8 -*- 
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from edu.models import Aluno
from edu.models import Professor
from django.template import RequestContext
from edu.models import Codigo
from edu.models import TurmaAluno

from edu.models import Colegio
from edu.models import Turma


from edu.forms import FormCodigo
from edu.forms import FormAluno

from edu.forms import FormResgate

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.http import HttpResponseRedirect


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

def cadastrar_aluno(request):
	c = RequestContext(request)
	if request.method=="POST":
		form = FormAluno(request.POST)
		if form.is_valid():
			dados = form.cleaned_data
			colegio = Colegio.objects.get(nome=dados['colegio'])
			turma = Turma.objects.get(colegio=colegio)
			novo_aluno = Aluno(username=dados['login'], first_name=dados['primeiro_nome'],
						last_name=dados['ultimo_nome'], email=dados['email'], pontos=0)
			novo_aluno.set_password(str(dados['senha']))
			novo_aluno.save()
			turma_aluno = TurmaAluno(aluno=novo_aluno, turma=turma)
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