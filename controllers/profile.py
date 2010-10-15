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
    len_evals = len(avaliacoes.select())
    karma_avg = get_karma_avg(aluno_id)
    grade_avg = grade_average(avaliacoes)
    '''
    Lista das últimas avaliações do aluno
    '''
    raw_evals = avaliacoes.select()
    evals = []
    counter = 0
    for raw_eval in raw_evals:
        eval = {}
        eval['id']            = raw_eval['id']
        eval['prof_id']       = raw_eval['professor_id']
        eval['disc_id']       = raw_eval['disciplina_id']
        eval['aluno_user_id'] = db(db.alunos.id==raw_eval['aluno_id']).select().first().user_id
        eval['aluno_id']      = raw_eval['aluno_id']
        eval['aluno_name']    = db(db.alunos.id==raw_eval['aluno_id']).select().first().full_name
        eval['prof_name']     = db(db.professores.id==raw_eval['professor_id']).select().first().full_name
        eval['disc_name']     = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first().name
        eval['semester']      = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
        eval['grade']         = raw_eval['grade']
        eval['karma']         = raw_eval['karma']
        eval['comment']       = raw_eval['comment']
        eval['reply']         = raw_eval['reply']
        eval['anonimo']       = raw_eval['anonimo']
        eval['timestamp']     = raw_eval['timestamp']
        evals.append(eval)
        counter = counter+1
        if counter>2:
            break
    '''
    Lista das últimas avaliações do aluno, que foram respondidas
    '''
    avaliacoes = db((db.avaliacoes.aluno_id==aluno_id) & (db.avaliacoes.reply!=None))
    raw_evals = avaliacoes.select()
    evals_replyed = []
    counter = 0
    for raw_eval in raw_evals:
        eval = {}
        eval['id']            = raw_eval['id']
        eval['prof_id']       = raw_eval['professor_id']
        eval['disc_id']       = raw_eval['disciplina_id']
        eval['aluno_user_id'] = db(db.alunos.id==raw_eval['aluno_id']).select().first().user_id
        eval['aluno_id']      = raw_eval['aluno_id']
        eval['aluno_name']    = db(db.alunos.id==raw_eval['aluno_id']).select().first().full_name
        eval['prof_name']     = db(db.professores.id==raw_eval['professor_id']).select().first().full_name
        eval['disc_name']     = db(db.disciplinas.id==raw_eval['disciplina_id']).select().first().name
        eval['semester']      = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
        eval['grade']         = raw_eval['grade']
        eval['karma']         = raw_eval['karma']
        eval['comment']       = raw_eval['comment']
        eval['reply']         = raw_eval['reply']
        eval['anonimo']       = raw_eval['anonimo']
        eval['timestamp']     = raw_eval['timestamp']
        evals_replyed.append(eval)
        counter = counter+1
        if counter>2:
            break    
 
    return dict(name=session.auth.user.last_name, evals = sorted(evals, key=itemgetter('timestamp'), reverse=True), evals_replyed= sorted(evals_replyed, key=itemgetter('timestamp'), reverse=True), len_evals=len_evals, karma_avg=karma_avg, grade_avg=grade_avg)
