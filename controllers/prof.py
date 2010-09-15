#profs controller

def list():
	'''
	Exibe a lista de professores
	'''
	return dict(profs=db().select(db.professores.ALL).sort(lambda profs: profs.full_name))

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


