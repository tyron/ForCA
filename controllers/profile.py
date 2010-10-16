from operator import itemgetter

@auth.requires_login()
def home():  
   
    if auth.has_membership('Professor'):
        prof_id = get_prof_id()
        redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
    else:
        aluno_id = get_aluno_id()
        avaliacoes = db(db.avaliacoes.aluno_id==aluno_id)
    
    avaliacoes = db(db.avaliacoes.aluno_id==aluno_id)
    len_evals_all = len(avaliacoes.select())
    karma_avg = get_karma_avg(aluno_id)
    grade_avg = grade_average(avaliacoes)
    '''
    Lista das últimas avaliações do aluno
    '''
    raw_evals = avaliacoes.select(orderby=~db.avaliacoes.timestamp_eval, limitby=(0,3))
    evals = []
    for raw_eval in raw_evals:
        eval = {}
        eval['id']              = raw_eval['id']
        eval['prof_id']         = raw_eval['professor_id']
        eval['disc_id']         = raw_eval['disciplina_id']
        eval['aluno_user_id']   = db(db.alunos.id==raw_eval['aluno_id']).select().first().user_id
        eval['aluno_id']        = raw_eval['aluno_id']
        eval['aluno_name']      = db(db.alunos.id==raw_eval['aluno_id']).select().first().full_name
        eval['prof_name']       = db(db.professores.id==raw_eval['professor_id']).select().first().full_name
        eval['disc_name']       = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first().name
        eval['semester']        = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
        eval['grade']           = raw_eval['grade']
        eval['karma']           = raw_eval['karma']
        eval['comment']         = raw_eval['comment']
        eval['reply']           = raw_eval['reply']
        eval['anonimo']         = raw_eval['anonimo']
        eval['timestamp_eval']  = raw_eval['timestamp_eval']
        eval['timestamp_reply'] = raw_eval['timestamp_reply']
        evals.append(eval)

    '''
    Lista das últimas avaliações do aluno, que foram respondidas
    '''
    avaliacoes = db((db.avaliacoes.aluno_id==aluno_id) & (db.avaliacoes.reply!=None))
    raw_evals = avaliacoes.select(orderby=~db.avaliacoes.timestamp_reply, limitby=(0,3))
    evals_replyed = []
    for raw_eval in raw_evals:
        eval = {}
        eval['id']              = raw_eval['id']
        eval['prof_id']         = raw_eval['professor_id']
        eval['disc_id']         = raw_eval['disciplina_id']
        eval['aluno_user_id']   = db(db.alunos.id==raw_eval['aluno_id']).select().first().user_id
        eval['aluno_id']        = raw_eval['aluno_id']
        eval['aluno_name']      = db(db.alunos.id==raw_eval['aluno_id']).select().first().full_name
        eval['prof_name']       = db(db.professores.id==raw_eval['professor_id']).select().first().full_name
        eval['disc_name']       = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first().name
        eval['semester']        = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
        eval['grade']           = raw_eval['grade']
        eval['karma']           = raw_eval['karma']
        eval['comment']         = raw_eval['comment']
        eval['reply']           = raw_eval['reply']
        eval['anonimo']         = raw_eval['anonimo']
        eval['timestamp_eval']  = raw_eval['timestamp_eval']
        eval['timestamp_reply'] = raw_eval['timestamp_reply']
        evals_replyed.append(eval)
 
    return dict(name=session.auth.user.last_name, evals=evals, evals_replyed=evals_replyed, len_evals_all = len_evals_all, karma_avg=karma_avg, grade_avg=grade_avg)
