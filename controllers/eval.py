def list():
    '''
    Exibe a lista de avalições (já faz o join com tabela de professores, alunos e disciplinas).
    '''
    
    evals = db((db.avaliacoes.professor_id == db.professores.id)&(db.avaliacoes.aluno_id == db.alunos.id)&(db.avaliacoes.disciplina_id == db.disciplinas.id))#Faz o join
    evals = evals.select(db.avaliacoes.grade,db.avaliacoes.comment,db.avaliacoes.reply,db.professores.full_name,db.alunos.full_name,db.disciplinas.short_name,orderby = db.professores.full_name)#Seleciona as colunas desejadas
    
    return dict(evals = evals)
