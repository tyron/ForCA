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

def get_grade_letter(intgrade):
	grade_list = ['A', 'B', 'C', 'D', 'FF']
	return grade_list[intgrade]

def get_grade_value(strgrade):
	grade_dict = {'A': 10, 'B': 8, 'C': 6, 'D': 2, 'FF': 0}

def check_unique_eval(form):
	aluno_id      = form.vars['aluno_id']
	professor_id  = form.vars['professor_id']
	disciplina_id = form.vars['disciplina_id']
	check = db(
			(db.avaliacoes.aluno_id      == aluno_id     ) &
			(db.avaliacoes.professor_id  == professor_id ) &
			(db.avaliacoes.disciplina_id == disciplina_id))
	if check.count():
		form.errors.disciplina_id = 'Você já postou uma avaliação para este\
				professor nesta disciplina'
	return check.count() == 0
