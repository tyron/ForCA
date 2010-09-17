from gluon.tools import Crud
crud = Crud(globals(), db)

def index():
	profs = db().select(db.professores.ALL, orderby=db.professores.full_name)
	return dict(profs=profs)	

def aval_add():
	form_add=SQLFORM(db.avaliacoes, _action="aval_list")
	if form_add.accepts(request.vars, session):
		response.flash = 'Avaliação realizada com sucesso'
	else:
		response.flash = 'Por favor, preencha a sua avaliação'
	form_add.aluno_id = request.vars['id']
	return dict(form_add=form_add)

def aval_list():
	avals = db(db.avaliacoes.id==request.args(0)).select()
	prof = db(db.professores.id==request.args(0)).select().first()
	return dict(avals=avals, prof=prof)

def aval_up():
	record = db.avaliacoes(request.args(0)) 
	form_up=SQLFORM(db.avaliacoes, request.args(0), deletable=True)
	if form_up.accepts(request.vars, session):
		response.flash = 'Avaliação editada com sucesso'
	return dict(form_up=form_up)

def list():
    '''
    Exibe a lista de avalições (já faz o join com tabela de professores, alunos e disciplinas).
    '''
    
    evals = db((db.avaliacoes.professor_id == db.professores.id)&(db.avaliacoes.aluno_id == db.alunos.id)&(db.avaliacoes.disciplina_id == db.disciplinas.id))#Faz o join
    evals = evals.select(db.avaliacoes.grade,db.avaliacoes.comment,db.avaliacoes.reply,db.professores.full_name,db.alunos.full_name,db.disciplinas.short_name,orderby = db.professores.full_name)#Seleciona as colunas desejadas
    
    return dict(evals = evals)
