from operator import itemgetter

@auth.requires_membership('admin')
def create():
	form = SQLFORM(db.professores)
	if form.accepts(request.vars, session):
		session.flash = 'Professor criado com sucesso'
	return dict(form=form)

@auth.requires_membership('admin')
def edit():
	prof_id = request.vars['prof_id']
	prof = db(db.professores.id==prof_id).select().first()
	form = SQLFORM(db.professores, prof)
	if form.accepts(request.vars, session):
		session.flash = 'Professor atualizado com sucesso'
		redirect(URL(request.application, 'prof', 'list'))
	return dict(form=form)

def list():
	'''
	Exibe a lista de professores
	'''
	return dict(profs=db().select(db.professores.ALL).sort(lambda profs: profs.full_name))

def home():
	'''
	Lista avaliações recebidas pelo professor
	'''
	prof_id = request.vars['prof_id']
	if len(request.args):
		page = int(request.args[0])
	else:
		page = 0
	limitby = (page*10, (page+1)*11)
	prof = db(db.professores.id==prof_id).select(db.professores.ALL).first()
	raw_evals = get_evals(prof_id,None).select(limitby=limitby)
	evals = refine_evals(raw_evals)
	return dict(prof=prof, page=page, per_page=10, evals=sorted(evals, key=itemgetter('karma'), reverse=True))

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
