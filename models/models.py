from datetime import datetime

if request.env.web2py_runtime_gae:
    db = DAL('gae')
    session.connect(request, response, db)
else:
    db = DAL('postgres://forca:xx@localhost/forca')

#Tabela Alunos
db.define_table(
        'alunos',
        Field('user_id', 'integer', length=32),
        Field('email', 'string', length=64, required=True, notnull=True, unique=True,
            requires = IS_EMAIL()),
        Field('full_name', 'string', length=128, required=True, notnull=True),
        Field('short_name', 'string', length=32),
        Field('grade', 'string', length=1, writable=False, readable=False,
            requires = IS_IN_SET(['A', 'B', 'C', 'D', 'FF'])),
        migrate='alunos.table')

#Tabela Disciplinas
db.define_table(
        'disciplinas',
        Field('name', 'string', length=128, required=True, notnull=True),
        Field('short_name', 'string', length=32),
        Field('code', 'string', length=8, required=True, notnull=True, unique=True),
        Field('resume', 'text'),
        migrate='disciplinas.table')

#Tabela Professores
db.define_table(
        'professores',
        Field('user_id', 'integer', length=32),
        Field('email', 'string', length=64, required=True, notnull=True, unique=True,
            requires = IS_EMAIL()),
        Field('full_name', 'string', length=128, required=True, notnull=True),
        Field('short_name', 'string', length=32),
        Field('grade', 'string', length=2, writable=False, readable=False,
            requires = IS_IN_SET(['A', 'B', 'C', 'D', 'FF'], zero=None)),
        Field('site','string',length=64,readable=False),
        Field('picture', 'upload'),
        migrate='professores.table')

#Tabela Avaliacoes
db.define_table(
        'avaliacoes',
        Field('aluno_id', db.alunos, required=True, notnull=True,
            writable = False, readable = False),
        Field('disciplina_id', db.disciplinas, required=True, notnull=True,
            readable = False,
            requires = IS_IN_DB(db, db.disciplinas.id, '%(name)s')),
        Field('professor_id', db.professores, required=True, notnull=True,
            readable = False,
            requires = IS_IN_DB(db, db.professores.id, '%(full_name)s')),
        Field('year', 'integer', length=4, default=datetime.now().year, 
            requires = IS_IN_SET(range(1990, datetime.now().year+1), zero=None)),
        Field('semester', 'integer', length=1, default=(1 if datetime.now().month <= 6 else 2),
            requires = IS_IN_SET(['1', '2'], zero=None)),
        Field('grade', 'string', length=2, readable=False,
            requires = IS_IN_SET(['A', 'B', 'C', 'D', 'FF'], zero=None)),
        Field('comment', 'text'),
        Field('karma', 'integer', length=8, default='0', writable=False, readable=False),
        Field('reply', 'text', readable=False),
        Field('anonimo', 'boolean', required=True, default=False, writable=True, readable=True),
        Field('timestamp_eval', 'datetime', length=32, default=datetime.now(), readable=False),
        Field('timestamp_reply', 'datetime', length=32, readable=False),
        migrate='avaliacoes.table')

db.avaliacoes.aluno_id.requires = [
    IS_IN_DB(db, db.alunos.id, '%(full_name)s',
        error_message = 'Aluno não cadastrado em nossa base de dados'),
    IS_NOT_IN_DB(db(
        (db.avaliacoes.disciplina_id == request.vars.disciplina_id) &
        (db.avaliacoes.professor_id == request.vars.professor_id)),
    'avaliacoes.aluno_id',
    error_message = 'Você já postou uma avaliação para este professor nesta disciplina')
]

#Tabela Prof x Disc
db.define_table(
        'profs_discs',
        Field('professor_id', db.professores, required=True, notnull=True,
            readable = False,
            requires = IS_IN_DB(db, db.professores.id, '%(full_name)s')),
        Field('disciplina_id', db.disciplinas, required=True, notnull=True,
            readable = False,
            requires = IS_IN_DB(db, db.disciplinas.id, '%(name)s')),
        Field('count', 'integer', default='1', writable=False, readable=False), 
        migrate='profs_discs.table')

db.profs_discs.professor_id.requires = [
    IS_NOT_IN_DB(db(
        (db.profs_discs.disciplina_id == request.vars.disciplina_id) &
        (db.profs_discs.professor_id == request.vars.professor_id)),
    'profs_discs.professor_id',
    error_message = 'Voce já adiciou este professor para esta disciplina')
]

#Tabela Karma
db.define_table(
        'karmas',
        Field('aluno_id', db.alunos, required=True, notnull=True,
            requires = IS_IN_DB(db, db.alunos.id, '')),
        Field('avaliacao_id', db.avaliacoes, required=True, notnull=True,
            requires = IS_IN_DB(db, db.avaliacoes.id, '')),
        Field('value', 'integer', length=1,
            requires = IS_IN_SET([-1, 1], zero=None)),
        migrate='karmas.table')
