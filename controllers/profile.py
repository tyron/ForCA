from operator import itemgetter

@auth.requires_login()
def home():  
   
    if auth.has_membership('Professor'):
            prof_id = get_prof_id()
            redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
    else:

        if request.vars:
            aluno_id = request.vars['aluno_id']
        else: 
            aluno_id = get_aluno_id()
            
        #Verifica se quem ta acessando a página é o próprio aluno ou alguém de fora
        if int(aluno_id) == get_aluno_id():
            perfil_proprio = True
        else: 
            perfil_proprio = False
       
        if len(request.args):
            page = int(request.args[0])
        else:
            page = 0
            
        limitby = (page*10, (page+1)*11)

        aluno = db(db.alunos.id==aluno_id).select(db.alunos.ALL).first()
        avaliacoes = db(db.avaliacoes.aluno_id==aluno_id)
        len_evals_all = len(avaliacoes.select(limitby=limitby))
        karma_avg = get_karma_avg(aluno_id)
        grade_avg = grade_average(avaliacoes)
        '''
        Lista das últimas avaliações do aluno
        '''
        raw_evals = avaliacoes.select(orderby=~db.avaliacoes.timestamp_eval, limitby=(0,3))
        evals = refine_evals(raw_evals)

        '''
        Lista das últimas avaliações do aluno, que foram respondidas
        '''
        avaliacoes = db((db.avaliacoes.aluno_id==aluno_id) & (db.avaliacoes.reply!=None))
        raw_evals = avaliacoes.select(orderby=~db.avaliacoes.timestamp_reply, limitby=(0,3))
        evals_replyed = refine_evals(raw_evals)

        return dict(aluno=aluno, perfil_proprio=perfil_proprio, evals=evals, evals_replyed=evals_replyed, len_evals_all = len_evals_all,\
                    karma_avg=karma_avg, grade_avg=grade_avg, page=page, per_page=10)
