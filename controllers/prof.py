#profs controller

@auth.requires_login()
def create():
	form = SQLFORM(db.professores)
	if form.accepts(request.vars, session):
		session.flash = 'ok'
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
	raw_evals = db(db.avaliacoes.professor_id==prof_id).select()
	evals = []
	for raw_eval in raw_evals:
		eval = {}
		eval['id']       = raw_eval['id']
		eval['aluno_user_id'] = db(db.alunos.id==raw_eval['aluno_id']).select().first().user_id
		eval['aluno_name']    = db(db.alunos.id==raw_eval['aluno_id']).select().first().full_name
		eval['disc_name']     = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first().name
		eval['semester'] = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
		eval['grade']    = raw_eval['grade']
		eval['comment']  = raw_eval['comment']
		evals.append(eval)
	return dict(prof = prof, evals = evals)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


