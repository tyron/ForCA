def list():
	'''
	Exibe a lista de disciplinas
	'''
	return dict(discs=db().select(db.disciplinas.ALL).sort(lambda discs: discs.name))
