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

def get_grade_letter(numgrade):
	if numgrade >= 9:
		return 'A'
	elif numgrade >= 7.5:
		return 'B'
	elif numgrade >= 6:
		return 'C'
	elif numgrade >= 3:
		return 'D'
	return 'FF'

def get_grade_value(strgrade):
	grade_dict = {'A': 10, 'B': 8, 'C': 6, 'D': 3, 'FF': 1}
	return grade_dict[strgrade]

def harmonic_mean(listerms):
	numterms = len(listerms)
	return numterms / sum(map(lambda x: 1.0/x, listerms))

def grade_average(eval_rows):
	raw_grades = eval_rows.select(db.avaliacoes.grade)
	if len(raw_grades) < 1:
		return None
	grades = map(lambda x: get_grade_value(x['grade']), raw_grades.as_list())
	average = get_grade_letter(harmonic_mean(grades))
	return average

def update_grade(prof_id):
	prof_evals = db(db.avaliacoes.professor_id==prof_id)
	new_grade = grade_average(prof_evals)
	db(db.professores.id==prof_id).update(grade=new_grade)
	db.commit()
	return new_grade

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

def has_karmed(aluno_id, eval_id):
	return db(
			(db.karmas.aluno_id==aluno_id) &
			(db.karmas.avaliacao_id==eval_id)
			).count()
