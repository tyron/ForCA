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
    
def home():
    '''
    Página da disciplina
    '''
    disc_id = request.vars['disc_id']
    aluno_id = get_aluno_id()
    disc_name = db(db.disciplinas.id==disc_id).select().first().name
    evals = db(db.avaliacoes.disciplina_id==disc_id).select()
    profs = db().select(db.professores.ALL)
    return dict(disc_id = disc_id, aluno_id = aluno_id, disc_name=disc_name, evals = evals, profs = profs)
