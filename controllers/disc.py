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
    return dict(discs=db().select(db.disciplinas.ALL).sort(lambda discs: rem_acentos(discs.name)))
    
def home():
    '''
    Lista avaliações recebidas pela disciplina
    '''
    disc_id = request.vars['disc_id']
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    limitby = (page*10, (page+1)*11)

    result_query, defaults = get_filter_query(db(Avaliacoes.disciplina_id == disc_id))

    fields = {}

    fields['prof'] = get_prof_dropdown(default=defaults['prof_id'])
    fields['year'] = get_year_dropdown(default=defaults['year'])
    fields['grade'] = get_grade_dropdown(default=defaults['grade'])

    evals_disc = db(Avaliacoes.disciplina_id == disc_id)

    disc = db(db.disciplinas.id==disc_id).select().first()
    disc_grade = grade_average(evals_disc)
    #Lista de avaliações
    raw_evals = result_query.select(limitby=limitby)
    evals = refine_evals(raw_evals)
    #Lista de professores que dão a disciplina
    raw_profs = db(db.profs_discs.disciplina_id==disc_id).select()
    profs = []
    for raw_prof in raw_profs:
        prof = {}
        prof['id']        = raw_prof['professor_id']
        prof['full_name'] = db(db.professores.id==raw_prof['professor_id']).select().first().full_name
        evals_prof_disc   = get_evals(raw_prof['professor_id'],disc_id)
        #Se não tem avaliação, a nota média recebe '\' pra colocar os professores sem nota no fim, ao ordenar
        #Se alguém souber um jeito sem gambiarra seria interessante, favor me contar depois (Thomas)
        if len(evals_prof_disc.select()) < 1:
            prof['grade'] = '\\'
        else:
            prof['grade'] = grade_average(evals_prof_disc) 
        profs.append(prof)

    return dict(disc = disc, disc_grade = disc_grade, evals = sorted(evals, key=itemgetter('karma'), reverse=True), fields=fields,
            page=page, per_page=10, profs = sorted(sorted(profs, key=lambda x: rem_acentos(x['full_name'])), key=lambda x: x['grade'], reverse=False))
