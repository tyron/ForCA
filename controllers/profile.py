@auth.requires_login()
def home():
	if auth.has_membership('Professor'):
		prof_id = get_prof_id()
		redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
	else:
		aluno_id = get_aluno_id()
		avaliacoes = db(db.avaliacoes.aluno_id==aluno_id).select()
	return dict(name=session.auth.user.last_name, evals=avaliacoes)
