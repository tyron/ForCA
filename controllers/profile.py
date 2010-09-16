@auth.requires_login()
def home():
	user_id = session.auth.user.id
	aluno_id = db(db.alunos.user_id==user_id).select().first().id
	avaliacoes = db(db.avaliacoes.aluno_id==aluno_id).select()
	return dict(name=session.auth.user.last_name, evals=avaliacoes)
