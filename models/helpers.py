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

#########################################
#              Aluno getters            #
#########################################

def get_aluno_id():
    '''
    Retorna o aluno_id do usuario logado
    '''
    try:
        user_id = session.auth.user.id
        aluno_id = db(db.alunos.user_id == user_id).select().first().id
        return aluno_id
    except:
        return 0

def get_aluno_full_name(aluno_id):
    '''
    Retorna o nome completo do aluno referenciado por aluno_id
    '''
    aluno = db(db.alunos.id==aluno_id).select().first()
    return aluno.full_name

def get_posted_evals(aluno_id):
    '''
    Retorna todas as avaliacoes postadas por um aluno
    '''
    aluno_evals = db(db.avaliacoes.aluno_id==aluno_id).select()
    return aluno_evals

def get_karma_avg(aluno_id):
    '''
    Retorna a soma de karmas recebidos pelas avaliacoes
    postadas pelo aluno referenciado por aluno_id
    '''
    aluno_evals = get_posted_evals(aluno_id)
    karmas = []
    for eval in aluno_evals:
        if eval.karma:
            karmas.append(eval.karma)
    return sum(karmas)

#########################################
#              Prof getters             #
#########################################

def get_prof_id():
    '''
    Retorna o professor_id do usuario logado
    '''
    try:
        user_id = session.auth.user.id
        prof_id = db(db.professores.user_id == user_id).select().first().id
        return prof_id
    except:
        return 0

def get_prof_name(prof_id):
    '''
    Retorna o nome completo do professor referenciado por prof_id
    '''
    prof = db(db.professores.id==prof_id).select().first()
    return prof.full_name

def get_prof_id_from_email(prof_email):
    '''
    Retorna o id no datastore do professor cujo e-mail eh prof_email
    '''
    prof = db(db.professores.email==prof_email).select().first()
    return prof.id

#########################################
#              Disc getters             #
#########################################

def get_disc_name(disc_id):
    '''
    Retorna o nome da disciplina referenciada por disc_id
    '''
    disc = db(db.disciplinas.id==disc_id).select().first()
    return disc.name

def get_disc_id_from_code(disc_code):
    '''
    Retorna o id no datastore da disciplina cujo codigo eh disc_code
    '''
    disc = db(db.disciplinas.code==disc_code).select().first()
    return disc.id

#########################################
#              Eval getters             #
#########################################

def get_evals(prof_id = None, disc_id = None):
    '''
    Exibe a lista de avalições (já faz o join com tabela de professores, alunos e disciplinas).
    '''
    if((prof_id != None)&(disc_id != None)):
        evals = db((db.avaliacoes.professor_id == prof_id)&(db.avaliacoes.disciplina_id == disc_id))
    elif(prof_id != None):
        evals = db(db.avaliacoes.professor_id == prof_id)
    elif(disc_id != None):
        evals = db(db.avaliacoes.disciplina_id == disc_id)
    else:
        evals = db(db.avaliacoes.aluno_id == get_aluno_id())
    return evals

def refine_evals(raw_evals):
    '''
    Retorna uma lista de avaliações com campos refinados - referências resolvidas, campos tratados, etc
    '''
    evals = []
    for raw_eval in raw_evals:
        eval = {}
        eval['id']               = raw_eval['id']
        eval['prof_id']          = raw_eval['professor_id']
        eval['disc_id']          = raw_eval['disciplina_id']
        eval['aluno_user_id']    = db(db.alunos.id==raw_eval['aluno_id']).select().first().user_id
        eval['aluno_id']         = raw_eval['aluno_id']
        eval['aluno_name']       = db(db.alunos.id==raw_eval['aluno_id']).select().first().full_name
        eval['aluno_short_name'] = db(db.alunos.id==raw_eval['aluno_id']).select().first().short_name
        eval['prof_name']        = db(db.professores.id==raw_eval['professor_id']).select().first().full_name
        eval['prof_short_name']  = db(db.professores.id==raw_eval['professor_id']).select().first().short_name
        eval['disc_name']        = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first().name
        eval['disc_short_name']  = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first().short_name
        eval['semester']         = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
        eval['grade']            = raw_eval['grade']
        eval['karma']            = raw_eval['karma']
        eval['comment']          = raw_eval['comment']
        eval['reply']            = raw_eval['reply']
        eval['anonimo']          = raw_eval['anonimo']
        eval['timestamp_eval']   = raw_eval['timestamp_eval']
        eval['timestamp_reply']  = raw_eval['timestamp_reply']
        evals.append(eval)
    return evals

def get_refined_evals(prof_id=None, disc_id=None):
    '''
    Seleciona as avaliações dados um prof_id ou disc_id e as refina, devolvendo avaliações tratadas
    '''
    raw_evals = get_evals(prof_id, disc_id).select()
    evals = refine_evals(raw_evals)
    return evals

#########################################
#           Funções auxiliares          #
#########################################
def rem_acentos(str):
    '''
    Remove acentuação de uma string. Exemplo Não faça -> Nao faca
    '''
    from unicodedata import normalize
    return normalize('NFKD', str.decode('utf-8')).encode('ASCII', 'ignore')
    
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
    
def update_timestamp_eval(eval_id):
    db(db.avaliacoes.id==eval_id).update(timestamp_eval=datetime.now())
    db.commit()

def update_timestamp_reply(eval_id):
    db(db.avaliacoes.id==eval_id).update(timestamp_reply=datetime.now())
    db.commit()

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


def update_profs_discs(prof_id, disc_id):
    prof_disc = db((db.profs_discs.professor_id==prof_id)&(db.profs_discs.disciplina_id==disc_id)).select().first()
    if not prof_disc:
        db.profs_discs.insert(professor_id=prof_id, disciplina_id=disc_id)
        return 0
    count = prof_disc.count
    db(db.profs_discs.id==prof_disc.id).update(count = count+1)
    db.commit()
    return count + 1

#########################################
# Biased dropdowns: the pretty way      #
#########################################

def disc_biased_dropdown(prof_id):
    rows = db().select(db.disciplinas.id, db.disciplinas.name,
            left = db.profs_discs.on(
                (db.disciplinas.id==db.profs_discs.disciplina_id)&
                (db.profs_discs.professor_id==prof_id)),
            orderby=db.profs_discs.professor_id|db.disciplinas.name)
    key = [row.id for row in rows]
    value = [row.name for row in rows]
    form = SQLFORM.factory(
            Field('disciplina_id', label="Disciplina", requires=IS_IN_SET(key,value,zero=None)))
    return form[0][0]

def prof_biased_dropdown(disc_id):
    rows = db().select(db.professores.id, db.professores.full_name,
            left = db.profs_discs.on(
                (db.professores.id==db.profs_discs.professor_id)&
                (db.profs_discs.disciplina_id==disc_id)),
            orderby=db.profs_discs.disciplina_id|db.professores.full_name)
    key = [row.id for row in rows]
    value = [row.full_name for row in rows]
    form = SQLFORM.factory(
            Field('professor_id', label="Professor", requires=IS_IN_SET(key,value,zero=None)))
    return form[0][0]

#########################################
# Biased dropdowns: the GAE way         #
#########################################

def gae_disc_biased_dropdown(prof_id):
    discs = db(db.disciplinas.id>0).select(db.disciplinas.ALL)
    profs_discs = db(db.profs_discs.id>0).select(db.profs_discs.ALL).as_list()
    pds = map(lambda x: {'professor_id': x['professor_id'], 'disciplina_id': x['disciplina_id']}, profs_discs)
    results = []
    for disc in discs:
        dictkey = {'professor_id': int(prof_id), 'disciplina_id': disc.id}
        if dictkey in pds:
            results.append([disc.id, disc.name, profs_discs[pds.index(dictkey)]['count']])
        else:
            results.append([disc.id, disc.name, 0])
    key = [res[0] for res in sorted(sorted(results, key=lambda x: rem_acentos(x[1])), key=lambda x: x[2], reverse=True)]
    value = [res[1] for res in sorted(sorted(results, key=lambda x: rem_acentos(x[1])), key=lambda x: x[2], reverse=True)]
    form = SQLFORM.factory(
            Field('disciplina_id', label="Disciplina", requires=IS_IN_SET(key, value, zero=None)))
    return form[0][0]

def gae_prof_biased_dropdown(disc_id):
    profs = db(db.professores.id>0).select(db.professores.ALL)
    profs_discs = db(db.profs_discs.id>0).select(db.profs_discs.ALL).as_list()
    pds = map(lambda x: {'professor_id': x['professor_id'], 'disciplina_id': x['disciplina_id']}, profs_discs)
    results = []
    for prof in profs:
        dictkey = {'disciplina_id': int(disc_id), 'professor_id': prof.id}
        if dictkey in pds:
            results.append([prof.id, prof.full_name, profs_discs[pds.index(dictkey)]['count']])
        else:
            results.append([prof.id, prof.full_name, 0])
    key = [res[0] for res in sorted(sorted(results, key=lambda x: rem_acentos(x[1])), key=lambda x: x[2], reverse=True)]
    value = [res[1] for res in sorted(sorted(results, key=lambda x: rem_acentos(x[1])), key=lambda x: x[2], reverse=True)]
    form = SQLFORM.factory(
            Field('professor_id', label="Professor", requires=IS_IN_SET(key, value, zero=None)))
    return form[0][0]
