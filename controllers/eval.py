from gluon.tools import Crud
crud = Crud(globals(), db)

def index():
	profs = db().select(db.professores.ALL, orderby=db.professores.full_name)
	return dict(profs=profs)	

@auth.requires_login()
def create():
	'''
	Função cria uma avaliação para um determinado professor.
	'''
	prof_id = request.vars['prof_id']
	prof_name = db(db.professores.id==prof_id).select().first().short_name

	form_add=SQLFORM(db.avaliacoes,
			fields = ['disciplina_id','year','semester','grade','comment'], 
			labels = {'disciplina_id':'Disciplina: ','year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: '},
			hidden = dict(aluno_id=get_aluno_id(), professor_id=prof_id))
	form_add.vars.professor_id = prof_id
	form_add.vars.aluno_id = get_aluno_id()

	if form_add.accepts(request.vars, session, onvalidation=check_unique_eval):
		session.flash = 'Avaliação realizada com sucesso'
		update_grade(prof_id)
		redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
	else:
		response.flash = 'Por favor, preencha a sua avaliação'	
	return dict(prof_name=prof_name, form_add=form_add)

@auth.requires_login()
def update():
	'''
	Função faz update de registro já existente
	'''
	prof_id = request.vars['prof_id']
	record = db.avaliacoes(request.vars['eval_id']) 
	form_up=SQLFORM(db.avaliacoes, record, 
			fields=['year','semester','grade','comment'], 
			labels={'year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: '}, showid=False, deletable=True)

	if form_up.accepts(request.vars, session):
		session.flash = 'Avaliação editada com sucesso'
		update_grade(prof_id)
		redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
	else:
		response.flash = 'Por favor, preencha a sua avaliação'	
	return dict(form_up=form_up)

def list():
    '''
    Exibe a lista de avalições (já faz o join com tabela de professores, alunos e disciplinas).
    '''
    
    evals = db((db.avaliacoes.professor_id == db.professores.id)&(db.avaliacoes.aluno_id == db.alunos.id)&(db.avaliacoes.disciplina_id == db.disciplinas.id))#Faz o join
    evals = evals.select(db.avaliacoes.grade,db.avaliacoes.comment,db.avaliacoes.reply,db.professores.full_name,db.alunos.full_name,db.disciplinas.short_name,orderby = db.professores.full_name)#Seleciona as colunas desejadas
    
    return dict(evals = evals)
