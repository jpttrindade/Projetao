## funcao recebe uma lista de codigos e coloca eles num txt
def escreve_codigos(nome,lista):
	f=open(nome,'w')
	for cod in lista:
		f.write(cod.cod '\t')
	f.close()
	pass
