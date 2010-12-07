from gluon.tools import Auth, Mail

if request.env.web2py_runtime_gae:
	db = DAL('gae')
	session.connect(request, response, db)
else:
	db = DAL('postgres://forca:xx@localhost/forca')

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
		Field('reset_password_key', length=512,
			writable=False, readable=False, default=''),
		Field('registration_id', length=512,
			writable=False, readable=False, default=''))

forca_auth = db[auth.settings.table_user_name]
forca_auth.first_name.requires = \
		IS_NOT_EMPTY(error_message = auth.messages.is_empty)
forca_auth.last_name.requires = \
		IS_NOT_EMPTY(error_message = auth.messages.is_empty)
forca_auth.password.requires = \
		 [IS_LENGTH(minsize=2, error_message='A senha deve ter pelo menos 2 caracteres'), CRYPT()]
forca_auth.email.requires = \
		[IS_EMAIL(forced='inf\.ufrgs\.br', 
			error_message = 'O e-mail deve ser @inf.ufrgs.br'),
				IS_NOT_IN_DB(db, forca_auth.email)]

#auth settings
auth.settings.table_user = forca_auth
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.create_user_groups = False
auth.settings.register_next = URL(request.application, 'default', 'user/login')

auth.define_tables()

if not auth.id_group('Aluno'):
	auth.add_group('Aluno', 'Aluno do Instituto de Informática')
if not auth.id_group('Professor'):
	auth.add_group('Professor', 'Professor do Instituto de Informática')
if not auth.id_group('Admin'):
	auth.add_group('Admin', 'Administrador do sistema')

#definicao de categoria por email
def is_professor(form):
	email = form.vars.email
	if len(db(db.professores.email==email).select()) > 0:
		auth.add_membership(auth.id_group('Professor'), int(form.vars.id))
		prof_create(form.vars)
	else:
		auth.add_membership(auth.id_group('Aluno'), int(form.vars.id))
		aluno_create(form.vars)

auth.settings.register_onaccept.append(is_professor)

#definicao das configuracoes de e-mail
mail = Mail(globals())

#mail.settings.server = 'smtp.gmail.com:587' or 'gae'
#mail.settings.server = 'gae'
mail.settings.server = 'logging'
mail.settings.login = None or 'forcaufrgs@gmail.com:f0rc4!@#'
mail.settings.sender = 'forcaufrgs@gmail.com'

auth.settings.mailer = mail
auth.messages.verify_email = 'Clique no link http://' + \
		request.env.http_host + \
		URL(r=request,f='user',args=['verify_email']) + \
		'/%(key)s para confirmar seu cadastro.'
auth.messages.reset_password = 'Clique no link http://' + \
		request.env.http_host + \
		URL(r=request,f='user',args=['reset_password']) + \
		'/%(key)s para redefinir sua senha.'

#mensagens do auth
auth.messages.submit_button = 'Enviar'
auth.messages.verify_password = 'Confirmação de senha'
auth.messages.delete_label = 'Marque para excluir'
auth.messages.function_disabled = 'Função desabilitada'
auth.messages.access_denied = 'Acesso negado'
auth.messages.registration_verifying = 'Cadastro ainda não verificado'
auth.messages.registration_pending = 'Acesse o link de confirmação no seu e-mail para completar o cadastro'
auth.messages.logged_in = 'Logado'
auth.messages.email_sent = 'Acesse o link de confirmação no seu e-mail para completar o cadastro'
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
auth.messages.reset_password_subject = 'ForCA - Redefinição de senha'
auth.messages.invalid_reset_password = 'Redefinição de senha inválida'
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


