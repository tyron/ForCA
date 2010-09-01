db = DAL('postgres://forca:xx@localhost/forca')

#Tabela Alunos
db.define_table(
		'alunos',
<<<<<<< HEAD
		Field('email', 'string', length=64, required=True, notnull=True,
			requires=IS_EMAIL()),
		Field('name', 'string', length=128),
		Field('password', 'password', length=32, required=True, notnull=True),
		migrate='alunos.table')
=======
		#Field('auth_user_id', db.auth_user,
		#	requires = IS_IN_DB(db, db.auth_user.id, '')),
		Field('email', 'string', length=64, required=True, notnull=True, unique=True,
			requires = IS_EMAIL()),
		Field('full_name', 'string', length=128, required=True, notnull=True),
		Field('short_name', 'string', length=32),
		Field('password', 'password', length=32, required=True, notnull=True),
		Field('grade', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('picture', 'upload'),
		migrate="alunos.migrate")
>>>>>>> 20cdeaa28fd2b5d916b4dbfb6967adcb03198501

#Tabela Disciplinas
db.define_table(
		'disciplinas',
		Field('name', 'string', length=128, required=True, notnull=True),
<<<<<<< HEAD
		Field('code', 'string', length=8, required=True, notnull=True),
		migrate='disciplinas.table')
=======
		Field('short_name', 'string', length=32),
		Field('code', 'string', length=8, required=True, notnull=True, unique=True),
		migrate="disciplinas.migrate")
>>>>>>> 20cdeaa28fd2b5d916b4dbfb6967adcb03198501

#Tabela Professores
db.define_table(
		'professores',
		#Field('auth_user_id', db.auth_user,
		#	requires = IS_IN_DB(db, db.auth_user.id, '')),
		Field('email', 'string', length=64, required=True, notnull=True, unique=True,
			requires = IS_EMAIL()),
		Field('full_name', 'string', length=128, required=True, notnull=True),
		Field('short_name', 'string', length=32),
		Field('password', 'password', length=32),
		Field('grade', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('picture', 'upload'),
<<<<<<< HEAD
		migrate='professores.table')
=======
		migrate="professores.migrate")
>>>>>>> 20cdeaa28fd2b5d916b4dbfb6967adcb03198501

#Tabela Avaliacoes
db.define_table(
		'avaliacoes',
		Field('aluno_id', db.alunos, required=True, notnull=True,
			writable = False, readable = False,
			requires = IS_IN_DB(db, db.alunos.id, '')),
		Field('disciplina_id', db.disciplinas, required=True, notnull=True,
			writable = False, readable = False,
			requires = IS_IN_DB(db, db.disciplinas.id, '')),
		Field('professor_id', db.professores, required=True, notnull=True,
			writable = False, readable = False,
			requires = IS_IN_DB(db, db.professores.id, '')),
		Field('year', 'integer', length=4,
			requires = IS_INT_IN_RANGE(1970,9999)),
		Field('semester', 'boolean'),
		Field('grade', 'integer', length=1, required=True, notnull=True,
			requires = IS_INT_IN_RANGE(1,5)),
<<<<<<< HEAD
		Field('geral_grade', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('geral_comment', 'string', length=2048),
		Field('didatica_grade', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('didatica_comment', 'string', length=2048),
		Field('dinamica_grade', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('dinamica_comment', 'integer', length=2048),
		Field('avaliacao_grade', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('avaliacao_comment', 'string', length=2048),
		Field('disponibilidade_grade', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('disponibilidade_comment', 'string', length=2048),
		migrate='avaliacoes.table')
=======
		Field('comment', 'string', length=4096),
		Field('karma', 'integer', length=8, default='0'),
		Field('reply', 'string', length=4096),
		migrate="avaliacoes.migrate")

#Tabela Karma
db.define_table(
		'karmas',
		Field('aluno_id', db.alunos, required=True, notnull=True,
			requires = IS_IN_DB(db, db.alunos.id, '')),
		Field('avaliacao_id', db.avaliacoes, required=True, notnull=True,
			requires = IS_IN_DB(db, db.avaliacoes.id, '')),
		Field('value', 'boolean'),
		migrate="karma.migrate")
>>>>>>> 20cdeaa28fd2b5d916b4dbfb6967adcb03198501

