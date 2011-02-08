@auth.requires_membership('Admin')
def index():
    alunos = db(auth.settings.table_event.id>0).select()
    return dict(alunos=alunos)
