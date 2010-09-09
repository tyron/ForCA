from gluon.tools import Mail, Auth

db = DAL('postgres://forca:xx@localhost/forca')

#Tabela Alunos
db.define_table(
		'alunos',
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
		migrate='alunos.table')

#Tabela Disciplinas
db.define_table(
		'disciplinas',
		Field('name', 'string', length=128, required=True, notnull=True),
		Field('short_name', 'string', length=32),
		Field('code', 'string', length=8, required=True, notnull=True, unique=True),
		migrate='disciplinas.table')

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
		Field('semester', 'boolean'),
		Field('grade', 'integer', length=1, required=True, notnull=True,
			requires = IS_INT_IN_RANGE(1,5)),
		Field('comment', 'string', length=4096),
		Field('karma', 'integer', length=8, default='0'),
		Field('reply', 'string', length=4096),
		migrate='avaliacoes.table')

#Tabela Karma
db.define_table(
		'karmas',
		Field('aluno_id', db.alunos, required=True, notnull=True,
			requires = IS_IN_DB(db, db.alunos.id, '')),
		Field('avaliacao_id', db.avaliacoes, required=True, notnull=True,
			requires = IS_IN_DB(db, db.avaliacoes.id, '')),
		Field('value', 'boolean'),
		migrate='karmas.table')

#Tabelas de cadastro e login de usuarios

auth = Auth(globals(), db)

db.define_table(
		auth.settings.table_user_name,
		Field('first_name', length=128, default='', label="Nome completo"),
		Field('last_name', length=128, default='', label="Nome para exibição"),
		Field('email', length=128, default='', unique=True),
		Field('password', 'password', length=512,
			readable=False, label='Senha'),
		Field('registration_key', length=512,
			writable=False, readable=False, default=''),
		Field('reset_password_pkey', length=512,
			writable=False, readable=False, default=''),
		Field('registration_id', length=512,
			writable=False, readable=False, default=''))

forca_auth = db[auth.settings.table_user_name]
forca_auth.first_name.requires = \
		IS_NOT_EMPTY(error_message = auth.messages.is_empty)
forca_auth.last_name.requires = \
		IS_NOT_EMPTY(error_message = auth.messages.is_empty)
forca_auth.password.requires = \
		[IS_STRONG(), CRYPT()]
forca_auth.email.requires = \
		[IS_EMAIL(error_message = auth.messages.invalid_email),
				IS_NOT_IN_DB(db, forca_auth.email)]

#auth settings
auth.settings.table_user = forca_auth
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False

auth.define_tables()

#definicao das configuracoes de e-mail
mail = Mail(globals())
#mail.settings.server = 'smtp.gmail.com:465'
mail.settings.server = 'logging'
mail.settings.sender = 'forcaufrgs@gmail.com'
mail.settings.login = 'forcaufrgs@gmail.com:f0rc4!@#'
auth.settings.mailer = mail

#mensagens do auth
auth.messages.submit_button = 'Enviar'
auth.messages.verify_password = 'Confirmação de senha'
auth.messages.delete_label = 'Marque para excluir:'
auth.messages.function_disabled = 'Função desabilitada'
auth.messages.access_denied = 'Acesso negado'
auth.messages.registration_verifying = 'Cadastro ainda não verificado'
auth.messages.logged_in = 'Logado'
auth.messages.email_sent = 'E-mail enviado'
auth.messages.unable_to_send_email = 'Não foi possível enviar o e-mail'
auth.messages.email_verified = 'E-mail verificado'
auth.messages.logged_out = 'Deslogado'
auth.messages.registration_successful = 'Cadastro realizado com sucesso'
auth.messages.invalid_email = 'E-mail inválido'
auth.messages.unable_send_email = 'Não foi possível enviar o e-mail'
auth.messages.invalid_login = 'Login inválido'
auth.messages.invalid_user = 'Usuário inválido'
auth.messages.is_empty = "Não pode estar vazio"
auth.messages.mismatched_password = "Os campos de senha não conferem"
auth.messages.verify_email_subject = 'ForCA - Verificação de e-mail'
auth.messages.username_sent = 'Seu nome de usuário foi enviado por e-mail'
auth.messages.new_password_sent = 'Uma nova senha foi enviada para o seu e-mail'
auth.messages.password_changed = 'A senha foi trocada'
auth.messages.retrieve_password = 'Sua senha é: %(password)s'
auth.messages.retrieve_password_subject = 'Recuperação de senha'
auth.messages.reset_password_subject = 'Password reset'
auth.messages.invalid_reset_password = 'Invalid reset password'
auth.messages.profile_updated = 'Profile updated'
auth.messages.new_password = 'New password'
auth.messages.old_password = 'Old password'
auth.messages.register_log = 'User %(id)s Registered'
auth.messages.login_log = 'User %(id)s Logged-in'
auth.messages.logout_log = 'User %(id)s Logged-out'
auth.messages.profile_log = 'User %(id)s Profile updated'
auth.messages.verify_email_log = 'User %(id)s Verification email sent'
auth.messages.retrieve_username_log = 'User %(id)s Username retrieved'
auth.messages.retrieve_password_log = 'User %(id)s Password retrieved'
auth.messages.reset_password_log = 'User %(id)s Password reset'
auth.messages.change_password_log = 'User %(id)s Password changed'
auth.messages.add_group_log = 'Group %(group_id)s created'
auth.messages.del_group_log = 'Group %(group_id)s deleted'
auth.messages.add_membership_log = None
auth.messages.del_membership_log = None
auth.messages.has_membership_log = None
auth.messages.add_permission_log = None
auth.messages.del_permission_log = None
auth.messages.has_permission_log = None
auth.messages.label_first_name = 'Nome completo'
auth.messages.label_last_name = 'Nome para exibição'
auth.messages.label_username = 'Nome de usuário'
auth.messages.label_email = 'E-mail'
auth.messages.label_password = 'Senha'
auth.messages.label_registration_key = 'Chave de registro'
auth.messages.label_reset_password_key = 'Chave de recuperação de senha'
auth.messages.label_registration_id = 'Identificador de registro'
auth.messages.label_role = 'Categoria'
auth.messages.label_description = 'Descrição'
auth.messages.label_user_id = 'ID do usuário'
auth.messages.label_group_id = 'ID do grupo'
auth.messages.label_name = 'Nome'
auth.messages.label_table_name = 'Nome da tabela'
auth.messages.label_record_id = 'ID do registro'
auth.messages.label_time_stamp = 'Timestamp'
auth.messages.label_client_ip = 'IP do cliente'
auth.messages.label_origin = 'Origem'
auth.messages.label_remember_me = "Lembrar-me (por 30 dias)"

