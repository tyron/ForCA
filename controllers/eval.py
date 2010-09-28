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
	if 'prof_id' in request.vars:
		prof_id = request.vars['prof_id']
		prof_name = db(db.professores.id==prof_id).select().first().short_name
		form_add=SQLFORM(db.avaliacoes,
				fields = ['disciplina_id','year','semester','grade','comment'], 
				labels = {'disciplina_id':'Disciplina: ','year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: '},
				hidden = dict(aluno_id=get_aluno_id(), professor_id=prof_id))
		form_add.vars.professor_id = prof_id

	elif 'disc_id' in request.vars:
		disc_id = request.vars['disc_id']
		disc_name = db(db.disciplinas.id==disc_id).select().first().short_name
		form_add=SQLFORM(db.avaliacoes,
				fields = ['professor_id','year','semester','grade','comment'],
				labels = {'professor_id':'Professor: ','year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: '},
				hidden = dict(aluno_id=get_aluno_id(), disciplina_id=disc_id))
		form_add.vars.disciplina_id = disc_id

	form_add.vars.aluno_id = get_aluno_id()

	if form_add.accepts(request.vars, session, onvalidation=check_unique_eval):
		session.flash = 'Avaliação realizada com sucesso'
		if 'prof_id' in request.vars:
			update_grade(prof_id)
			redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
		else:
			update_grade(request.vars['professor_id'])
			redirect(URL(request.application, 'disc', 'home', vars=dict(disc_id=disc_id)))
	else:
		response.flash = 'Por favor, preencha a sua avaliação'
	if 'prof_id' in request.vars:
		return dict(prof_name=prof_name, form_add=form_add)
	else:
		return dict(disc_name=disc_name, form_add=form_add)

@auth.requires_login()
def update():
	'''
	Função faz update de registro já existente
	'''
	record = db.avaliacoes(request.vars['eval_id'])
	prof_id = record.professor_id
	form_up=SQLFORM(db.avaliacoes, record, 
			fields=['year','semester','grade','comment'], 
			labels={'year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: '}, showid=False, deletable=True)

	if form_up.accepts(request.vars, session):
		session.flash = 'Avaliação editada com sucesso'
		update_grade(prof_id)
		if 'prof_id' in request.vars:
			redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
		else:
			redirect(URL(request.application, 'disc', 'home', vars=dict(disc_id=request.vars['disc_id'])))
	else:
		response.flash = 'Por favor, preencha a sua avaliação'	
	return dict(form_up=form_up)

@auth.requires_login()
def delete():
	'''
	Função que deleta uma avaliação existente
	'''
	eval_id = request.vars['eval_id']
	eval = db.avaliacoes[eval_id]
	prof_id = eval.professor_id
	db(db.avaliacoes.id==eval_id).delete()
	db.commit()
	update_grade(prof_id)
	session.flash = 'Avaliação excluída com sucesso'
	if 'prof_id' in request.vars:
		redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=request.vars['prof_id'])))
	elif 'disc_id' in request.vars:
		redirect(URL(request.application, 'disc', 'home', vars=dict(disc_id=request.vars['disc_id'])))

def list(prof_id = None, disc_id = None):
    '''
    Exibe a lista de avalições (já faz o join com tabela de professores, alunos e disciplinas).
    '''  
    if((prof_id != None)&(disc_id != None)):
        evals = db((db.avaliacoes.professor_id == prof_id)&(db.avaliacoes.disciplina_id == disc_id)&(db.avaliacoes.professor_id == db.professores.id)&(db.avaliacoes.disciplina_id == db.disciplinas.id)&(db.avaliacoes.aluno_id == db.alunos.id))#Faz o join
    elif(prof != None):
        evals = db((db.avaliacoes.professor_id == prof_id)&(db.avaliacoes.professor_id == db.professores.id)&(db.avaliacoes.disciplina_id == db.disciplinas.id)&(db.avaliacoes.aluno_id == db.alunos.id))#Faz o join
    elif(disc_id != None):
        evals = db((db.avaliacoes.disciplina_id == disc_id)&(db.avaliacoes.professor_id == db.professores.id)&(db.avaliacoes.disciplina_id == db.disciplinas.id)&(db.avaliacoes.aluno_id == db.alunos.id))#Faz o join
    else:
        evals = db((db.avaliacoes.professor_id == db.professores.id)&(db.avaliacoes.disciplina_id == db.disciplinas.id)&(db.avaliacoes.aluno_id == db.alunos.id))#Faz o join 
         
    evals = evals.select(db.avaliacoes.grade,db.avaliacoes.comment,db.avaliacoes.reply,db.professores.full_name,db.alunos.full_name,db.disciplinas.short_name,orderby = db.professores.full_name)#Seleciona as colunas desejadas
    
    return dict(evals = evals)
