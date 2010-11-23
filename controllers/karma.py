def create(eval_id, value):
	eval = db(db.avaliacoes.id==eval_id).select().first()
	if eval.aluno_id == get_aluno_id():
		response.flash = 'Você não pode qualificar sua própria avaliação!'
		return None
	if db(
			(db.karmas.aluno_id==get_aluno_id()) & 
			(db.karmas.avaliacao_id==eval_id)
			).count():
		response.flash = 'Você já qualificou essa avaliação'
		return None
	db.karmas.insert(
			aluno_id     = get_aluno_id(),
			avaliacao_id = eval_id,
			value        = value
			)
	db.commit()
	response.flash = 'Obrigado pela sua qualificação!'
	return True

def inc_karma(eval_id, value):
	old_karma = db(db.avaliacoes.id==eval_id).select().first().karma
	db(db.avaliacoes.id==eval_id).update(
			karma = old_karma + value
			)
	db.commit()
	return old_karma+value

@auth.requires_login()
def up():
	eval_id = request.vars['eval_id']
	up = create(eval_id, 1)
	inc = inc_karma(eval_id, 1)
	return inc

@auth.requires_login()
def down():
	eval_id = request.vars['eval_id']
	down = create(eval_id, -1)
	inc = inc_karma(eval_id, -1)
	return inc
