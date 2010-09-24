#profs controller

def list():
    '''
    Exibe a lista de professores
    '''
    return dict(profs=db().select(db.professores.ALL).sort(lambda profs: profs.full_name))

def home():
    '''
    Perfil do professor
    '''
    prof_id = request.vars['prof_id']
    aluno_id = get_aluno_id()
    prof_name = db(db.professores.id==prof_id).select().first().full_name
    avals = db(db.avaliacoes.professor_id==prof_id).select()
    discs = db().select(db.disciplinas.ALL)
    return dict(prof_id = prof_id, aluno_id = aluno_id, prof_name=prof_name, avals = avals, discs = discs)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
