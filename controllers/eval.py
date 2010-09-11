from gluon.tools import Crud
crud = Crud(globals(), db)

def aval_add():
	return dict(form_add=crud.create(db.avaliacoes), message=("Avaliação realizada com sucesso"))
