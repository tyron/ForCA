def prof_create(data):
	'''
	Insere um registro na tabela 'professores'
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

