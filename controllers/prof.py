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
    return dict(profs=db().select(db.professores.ALL).sort(lambda profs: rem_acentos(profs.full_name)))

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
    #Lista de avaliações
    raw_evals = get_evals(prof_id,None).select(limitby=limitby)
    evals = refine_evals(raw_evals)    
    #Lista de disciplinas lecionadas pelo professor
    raw_discs = db(db.profs_discs.professor_id==prof_id).select()
    discs = []
    for raw_disc in raw_discs:
        disc = {}
        disc['id']        = raw_disc['disciplina_id']
        disc['name']      = db(db.disciplinas.id==raw_disc['disciplina_id']).select().first().name
        evals_prof_disc   = get_evals(prof_id,raw_disc['disciplina_id'])
        #Se não tem avaliação, a nota média recebe '\' pra colocar as disciplinas sem nota no fim, ao ordenar
        #Se alguém souber um jeito sem gambiarra seria interessante, favor me contar depois (Thomas)
        if len(evals_prof_disc.select()) < 1:
            disc['grade'] = '\\'
        else:
            disc['grade'] = grade_average(evals_prof_disc) 
        discs.append(disc)
   
    return dict(prof=prof, page=page, per_page=10, evals=sorted(evals, key=itemgetter('karma'), reverse=True), discs = sorted(discs, key=itemgetter('grade'), reverse=False))

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
