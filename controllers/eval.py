from gluon.tools import Crud
crud = Crud(globals(), db)

def index():
	profs = db().select(db.professores.ALL, orderby=db.professores.full_name)
	return dict(profs=profs)	

def create():
	'''
	Função cria uma avaliação para um determinado professor.
	'''
#
	form_add=SQLFORM(db.avaliacoes, fields=['disciplina_id','year','semester','grade','comment'], labels={'disciplina_id':'Disciplina: ','year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: '})
	form_add.vars.professor_id = request.vars['prof_id']
	form_add.vars.aluno_id = get_aluno_id()

	if form_add.accepts(request.vars, session):
		session.flash = 'Avaliação realizada com sucesso'
		redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=request.vars['prof_id'])))
	else:
		response.flash = 'Por favor, preencha a sua avaliação'	
	return dict(form_add=form_add)

def eval_list(prof_id):
	avals = db(db.avaliacoes.id==request.args(0)).select()
	#prof = db(db.professores.id==request.args(0)).select().first()
	return dict(avals=avals, prof=prof)

def update():
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
