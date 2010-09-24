@auth.requires_login()
def create():
	form = SQLFORM(db.disciplinas)
	if form.accepts(request.vars, session):
		session.flash = 'ok'
	return dict(form=form)

def list():
	'''
	Exibe a lista de disciplinas
	'''
	return dict(discs=db().select(db.disciplinas.ALL).sort(lambda discs: discs.name))
