from operator import itemgetter

@auth.requires_membership('admin')
def create():
	form = SQLFORM(db.professores)
	if form.accepts(request.vars, session):
		session.flash = 'Professor criado com sucesso'
	return dict(form=form)

@auth.requires_membership('admin')
def edit():
	prof_id = request.vars['prof_id']
	prof = db(db.professores.id==prof_id).select().first()
	form = SQLFORM(db.professores, prof)
	if form.accepts(request.vars, session):
		session.flash = 'Professor atualizado com sucesso'
		redirect(URL(request.application, 'prof', 'list'))
	return dict(form=form)

def list():
	'''
	Exibe a lista de professores
	'''
	return dict(profs=db().select(db.professores.ALL).sort(lambda profs: profs.full_name))

def home():
	'''
	Lista avaliações recebidas pelo professor
	'''
	prof_id = request.vars['prof_id']
	prof = db(db.professores.id==prof_id).select(db.professores.ALL).first()
	raw_evals = get_evals(prof_id,None).select()
	evals = []
	for raw_eval in raw_evals:
		eval = {}
		eval['id']            = raw_eval['id']
		eval['aluno_user_id'] = db(db.alunos.id==raw_eval['aluno_id']).select().first().user_id
		eval['aluno_id']      = raw_eval['aluno_id']
		eval['aluno_name']    = db(db.alunos.id==raw_eval['aluno_id']).select().first().full_name
		eval['prof_id']       = raw_eval['professor_id']
		eval['disc_name']     = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first().name
		eval['semester']      = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
		eval['grade']         = raw_eval['grade']
		eval['karma']         = raw_eval['karma']
		eval['comment']       = raw_eval['comment']
		eval['reply']         = raw_eval['reply']
		eval['anonimo']       = raw_eval['anonimo']
		evals.append(eval)
	return dict(prof = prof, evals = sorted(evals, key=itemgetter('karma'), reverse=True))

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
