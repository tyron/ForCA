#profs controller

def list():
	'''
	Exibe a lista de professores
	'''
	return dict(profs=db().select(db.professores.ALL).sort(lambda profs: profs.full_name))

def home():
	'''
	bla
	'''
	prof_id = request.vars['id']
	aluno_id = get_aluno_id()
	return dict(prof_id = prof_id, aluno_id = aluno_id)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


