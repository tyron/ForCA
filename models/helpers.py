def prof_create(data):
	'''
	Adiciona o user_id ao campo da tabela 'professores'
	'''
	db(db.professores.email==data.email).update(
			user_id    = data.id
	)
	db.commit()

def aluno_create(data):
	'''
	Insere um registro na tabela 'alunos'
	'''
	db.alunos.insert(
			email      = data.email,
			full_name  = data.first_name,
			short_name = data.last_name,
			user_id    = data.id
	)
	db.commit()

def get_aluno_id():
	'''
	Retorna o aluno_id do usuario logado
	'''
	user_id = session.auth.user.id
	aluno_id = db(db.alunos.user_id == user_id).select().first().id
	return aluno_id
