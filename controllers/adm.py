def create():
	form = SQLFORM(db.profs_discs)
	if form.accepts(request.vars, session):
		session.flash = 'Adicionado com sucesso!'
	return dict (form=form)
