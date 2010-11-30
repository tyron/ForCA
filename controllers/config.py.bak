@auth.requires_login()
def index():
    '''
    Retorna elementos necessários para a página de configurações do perfil
    '''
    aluno = get_aluno_id()
    professor = get_prof_id()
    if aluno != 0:     
        form_add=SQLFORM(db.alunos,
            fields = ['reply_warning'], 
            labels = {'reply_warning':'Notificar por e-mail quando algum professor responder minha avaliação: '},
            hidden = dict(id=aluno))

    return dict(form_add=form_add)
