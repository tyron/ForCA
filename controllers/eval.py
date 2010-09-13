from gluon.tools import Crud
crud = Crud(globals(), db)

#request.vars.professor_id

def aval_add():
	form_add=crud.create(db.avaliacoes, message="Avaliação realizada com sucesso", next=URL('aval_list'))
	return dict(form_add=form_add)

def aval_list():
	avals=crud.select(db.avaliacoes, db.avaliacoes.professor_id==1)
	return dict(avals=avals)
