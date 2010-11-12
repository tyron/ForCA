from operator import itemgetter

@auth.requires_login()
def home():  
 
    if auth.has_membership('Professor') and not request.vars:
        prof_id = get_prof_id()
        redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
    else:

        if request.vars:
            aluno_id = request.vars['aluno_id']
        else: 
            aluno_id = get_aluno_id()
            request.vars['aluno_id'] = aluno_id

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
        len_evals_all = len(get_posted_evals(aluno_id))
        karma_avg = get_karma_avg(aluno_id)
        grade_avg = grade_average(avaliacoes)        
        
        #Lista das últimas avaliações do aluno        
        raw_evals = avaliacoes.select(orderby=~db.avaliacoes.timestamp_eval, limitby=(0,3))
        evals = refine_evals(raw_evals)        
        
        #Lista das últimas avaliações do aluno, que foram respondidas        
        avaliacoes = db((db.avaliacoes.aluno_id==aluno_id) & (db.avaliacoes.reply!=None))
        raw_evals = avaliacoes.select(orderby=~db.avaliacoes.timestamp_reply, limitby=(0,3))
        evals_replyed = refine_evals(raw_evals)
        
        #Lista das avaliações favoritas do user logado no momento
        if perfil_proprio:
            #raw_favoritos = db((db.favoritos.user_id==session.auth.user.id)&(db.avaliacoes.id==db.favoritos.avaliacao_id)).select(db.avaliacoes.ALL)
            #evals_favorited = refine_evals(raw_favoritos)
            evals_favorited = get_favorite_evals(session.auth.user.id)
        else:
            evals_favorited = []

        return dict(aluno=aluno, perfil_proprio=perfil_proprio, evals=evals, evals_replyed=evals_replyed, evals_favorited=evals_favorited,\
                                len_evals_all=len_evals_all, karma_avg=karma_avg, grade_avg=grade_avg, page=page, per_page=10)

@auth.requires_membership('Aluno')
def favorites():
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0

    limitby = (page*10, (page+1)*11)
    if 'aluno_id' in request.vars:
        user_id = get_aluno_user_id(request.vars['aluno_id'])
    else:
        user_id = session.auth.user.id
    favorite_evals = db((Favoritos.user_id==user_id)&(Avaliacoes.id==Favoritos.avaliacao_id)).select(Avaliacoes.ALL, limitby=limitby)
    refined_favorites = refine_evals(favorite_evals)
    return dict(evals=refined_favorites, page=page, per_page=10)

