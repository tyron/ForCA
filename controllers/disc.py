from operator import itemgetter

@auth.requires_login()
def create():
    form = SQLFORM(db.disciplinas)
    if form.accepts(request.vars, session):
        session.flash = 'ok'
    return dict(form=form)

def list():
    '''
    Exibe a lista de disciplinas
    '''
    return dict(discs=db().select(db.disciplinas.ALL).sort(lambda discs: discs.name))
    
def home():
    '''
    Lista avaliações recebidas pela disciplina
    '''
    disc_id = request.vars['disc_id']
    disc = db(db.disciplinas.id==disc_id).select(db.disciplinas.ALL).first()
    raw_evals = get_evals(None,disc_id).select()
    evals = []
    for raw_eval in raw_evals:
        eval = {}
        eval['id']            = raw_eval['id']
        eval['aluno_user_id'] = db(db.alunos.id==raw_eval['aluno_id']).select().first().user_id
        eval['aluno_id']      = raw_eval['aluno_id']
        eval['aluno_name']    = db(db.alunos.id==raw_eval['aluno_id']).select().first().full_name
        eval['prof_name']     = db(db.professores.id==raw_eval['professor_id']).select().first().full_name
        eval['semester']      = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
        eval['grade']         = raw_eval['grade']
        eval['karma']         = raw_eval['karma']
        eval['comment']       = raw_eval['comment']
        evals.append(eval)
    #Lista de professores que dão a disciplina
    raw_profs = db(db.profs_discs.disciplina_id==disc_id).select()
    profs = []
    for raw_prof in raw_profs:
        prof = {}
        prof['id']        = raw_prof['professor_id']
        prof['full_name'] = db(db.professores.id==raw_prof['professor_id']).select().first().full_name
        evals_prof_disc   = get_evals(raw_prof['professor_id'],disc_id)
        prof['grade']     = grade_average(evals_prof_disc) 
        profs.append(prof)
         
        
    return dict(disc = disc, evals = sorted(evals, key=itemgetter('karma'), reverse=True), profs = sorted(profs, key=itemgetter('grade'), reverse=False))
