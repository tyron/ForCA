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
			fields = ['disciplina_id','year','semester','grade','comment', 'anonimo'], 
			labels = {'disciplina_id':'Disciplina: ','year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: ','anonimo': 'Anonimo:'},
			hidden = dict(aluno_id=get_aluno_id(), professor_id=prof_id))
		form_add.vars.professor_id = prof_id
		form_add[0][0] = disc_biased_dropdown(prof_id)

	elif 'disc_id' in request.vars:
		disc_id = request.vars['disc_id']
		disc_name = db(db.disciplinas.id==disc_id).select().first().short_name
		form_add=SQLFORM(db.avaliacoes,
			fields = ['professor_id','year','semester','grade','comment', 'anonimo'],
			labels = {'professor_id':'Professor: ','year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: ','anonimo:': 'Anonimo:'},
			hidden = dict(aluno_id=get_aluno_id(), disciplina_id=disc_id))
		form_add.vars.disciplina_id = disc_id
		form_add[0][0] = prof_biased_dropdown(disc_id)

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
