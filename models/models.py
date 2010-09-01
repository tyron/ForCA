db = DAL('postgres://forca:xx@localhost/forca')

#Tabela Alunos
db.define_table(
		'alunos',
		Field('email', 'string', length=64, required=True, notnull=True,
			requires=IS_EMAIL()),
		Field('name', 'string', length=128),
		Field('password', 'password', length=32, required=True, notnull=True),
		migrate='alunos.table')

#Tabela Disciplinas
db.define_table(
		'disciplinas',
		Field('name', 'string', length=128, required=True, notnull=True),
		Field('code', 'string', length=8, required=True, notnull=True),
		migrate='disciplinas.table')

#Tabela Professores
db.define_table(
		'professores',
		Field('email', 'string', length=64, required=True, notnull=True,
			requires = IS_EMAIL()),
		Field('short_name', 'string', length=32),
		Field('long_name', 'string', length=128, required=True, notnull=True),
		Field('password', 'string', length=32),
		Field('rating', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('picture', 'upload'),
		migrate='professores.table')

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
		Field('semester', 'integer', length=1,
			requires = IS_INT_IN_RANGE(1,2)),
		Field('grade', 'integer', length=1, required=True, notnull=True,
			requires = IS_INT_IN_RANGE(1,5)),
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

