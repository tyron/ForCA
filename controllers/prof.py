#profs controller

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
	prof_name = db(db.professores.id==prof_id).select().first().full_name
	raw_evals = db(db.avaliacoes.professor_id==prof_id).select()
	evals = []
	for raw_eval in raw_evals:
		eval = {}
		eval['id']       = raw_eval['id']
		eval['aluno']    = db(db.alunos.id==raw_eval['aluno_id']).select().first()
		eval['disc']     = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first()
		eval['semester'] = str(raw_eval['year'])+'/'+str(2 if raw_eval['semester'] else 1)
		eval['grade']    = get_grade(int(raw_eval['grade']))
		eval['comment']  = raw_eval['comment']
		evals.append(eval)
	return dict(prof_id = prof_id, prof_name = prof_name, evals = evals)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


