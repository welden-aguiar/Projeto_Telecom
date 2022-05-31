/*Select estruturado para fácil entendimento.*/

select 
	/***************HISTORICO*********************/
	ch.id_cliente_historico as id_cliente_historico,
	ch.id_cliente as id_cliente,
	ch.historico as historico,
	ch.data_cadastro as data_cadastro,
	u.name as vendedor_historico,
	/***************CLIENTE*********************/
	cli.codigo_cliente as codigo_cliente,
	cli.data_cadastro as data_cadastro_cliente,
	cli.nome_razaosocial as nome_cliente,
	cli.nome_fantasia as nome_fantasia_cliente,
	cli.tipo_pessoa as tipo_pessoa_cliente,
	oc.descricao as origem_cliente,
	cli.data_nascimento as data_nascimento_cliente,
	/***************SERVICO*********************/
	s.id_servico as id_servico,
	s.data_cadastro as data_cadastro_servico,
	s.valor as valor_servico,
	s.descricao as nome_servico,
	sn.download_contrato as download_servico,
	sn.upload_contrato as upload_servico,
	/***************CLIENTE SERVICO*********************/
	cs.id_cliente_servico as id_cliente_servico,
	cs.id_cliente_servico_associado as id_cliente_servico_associado,
	cs.numero_plano as numero_servico_cliente,
	cs.data_habilitacao as data_habilitacao_cs,
	st.descricao as descricao_tecnologia_cs,
	cs.origem as origem_cs,
	cs.id_cliente_servico_antigo as id_servico_antigo,
	cs.data_cancelamento as data_cancelamento_cs,
	(select descricao from motivo_cancelamento where cs.id_motivo_cancelamento = id_motivo_cancelamento) as motivo_cancelamento_cs, 
	fc.descricao as forma_cobranca_cs, 
	(select nome_razaosocial from empresa where fc.id_empresa = id_empresa) as empresa_cs, 
	(select descricao from servico_status where cs.id_servico_status = id_servico_status) as status_cs,
	/***************ENDERECO*********************/	
	en.id_endereco_numero as id_endereco_nk,
	cse.id_cliente_servico_endereco as id_cse,
	en.cep as cep_localidade,
	en.bairro as bairro_localidade,
	en.complemento as complemento_localidade,
	en.numero as numero_localidade,
	en.endereco as endereco_localidade,
	(select nome 
		from cidade 
		where en.id_cidade = id_cidade) as cidade_localidade,
	(select estado.nome 
		from cidade, estado 
		where cidade.id_cidade = en.id_cidade 
		and cidade.id_estado = estado.id_estado) as estado_localidade,
	(select estado.sigla
		from cidade, estado
		where cidade.id_cidade = en.id_cidade
		and cidade.id_estado = estado.id_estado) as estado_sigla	
from cliente_historico ch
left join users u on ch.id_usuario = u.id
/***************CLIENTE*********************/
left join cliente cli on cli.id_cliente = ch.id_cliente
left join origem_cliente oc on cli.id_origem_cliente = oc.id_origem_cliente
/***************CLIENTE SERVICO*********************/
left join cliente_servico cs on cs.id_cliente = ch.id_cliente
left join servico_tecnologia st on cs.id_servico_tecnologia = st.id_servico_tecnologia
left join forma_cobranca fc on cs.id_forma_cobranca = fc.id_forma_cobranca
/***************SERVICO*********************/
left join servico s on cs.id_servico = s.id_servico
left join servico_navegacao sn on cs.id_servico = sn.id_servico
/***************ENDERECO*********************/
left join cliente_servico_endereco cse on cs.id_cliente_servico = cse.id_cliente_servico
	and cse.tipo like 'instalacao'
left join endereco_numero en on cse.id_endereco_numero = en.id_endereco_numero
/***************WHERE*********************/
where ch.historico like '%Dados do Serviço%' 
or ch.historico like '%Pacote%adicionado ao serviço%' 
or ch.historico like '%Pacote%adicionado no serviço%' 
or ch.historico like '%Pacote%removido do serviço%' 
or ch.historico like '%Serviço%do cliente%migrou para o serviço%' 
or ch.historico like '%Novo serviço de número%serviço adicionado%' 
or ch.historico like '%O servico%migrou para o servico%' 
or ch.historico like '%O serviço%foi cancelado%' 
/***************ORDER BY*********************/
order by id_cliente, data_cadastro;


/*Select único.*/
 



    sql1 = "select ch.id_cliente_historico as id_cliente_historico, ch.id_cliente as id_cliente, ch.historico as historico, ch.data_cadastro as data_cadastro, u.name as vendedor_historico, cli.codigo_cliente as codigo_cliente, cli.data_cadastro as data_cadastro_cliente, cli.nome_razaosocial as nome_cliente, cli.nome_fantasia as nome_fantasia_cliente, cli.tipo_pessoa as tipo_pessoa_cliente, oc.descricao as origem_cliente, cli.data_nascimento as data_nascimento_cliente, s.id_servico as id_servico, s.data_cadastro as data_cadastro_servico, s.valor as valor_servico, s.descricao as nome_servico, sn.download_contrato as download_servico, sn.upload_contrato as upload_servico, "
    sql2 = "cs.id_cliente_servico as id_cliente_servico, cs.id_cliente_servico_associado as id_cliente_servico_associado, cs.numero_plano as numero_plano, cs.data_habilitacao as data_habilitacao_cs, st.descricao as descricao_tecnologia_cs, cs.origem as origem_cs, cs.id_cliente_servico_antigo as id_servico_antigo, cs.data_cancelamento as data_cancelamento_cs, (select descricao from motivo_cancelamento where cs.id_motivo_cancelamento = id_motivo_cancelamento) as motivo_cancelamento_cs, fc.descricao as forma_cobranca_cs, (select nome_razaosocial from empresa where fc.id_empresa = id_empresa) as empresa_cs, (select descricao from servico_status where cs.id_servico_status = id_servico_status) as status_cs, "
    sql3 = "en.id_endereco_numero as id_endereco_nk, cse.id_cliente_servico_endereco as id_cse, en.cep as cep_localidade, en.bairro as bairro_localidade, en.complemento as complemento_localidade, en.numero as numero_localidade, en.endereco as endereco_localidade, (select nome from cidade where en.id_cidade = id_cidade) as cidade_localidade, (select estado.nome from cidade, estado where cidade.id_cidade = en.id_cidade and cidade.id_estado = estado.id_estado) as estado_localidade, (select estado.sigla from cidade, estado where cidade.id_cidade = en.id_cidade and cidade.id_estado = estado.id_estado) as estado_sigla "
    sql4 = "from cliente_historico ch left join users u on ch.id_usuario = u.id left join cliente cli on cli.id_cliente = ch.id_cliente left join origem_cliente oc on cli.id_origem_cliente = oc.id_origem_cliente left join cliente_servico cs on cs.id_cliente = ch.id_cliente left join servico_tecnologia st on cs.id_servico_tecnologia = st.id_servico_tecnologia left join forma_cobranca fc on cs.id_forma_cobranca = fc.id_forma_cobranca left join servico s on cs.id_servico = s.id_servico left join servico_navegacao sn on cs.id_servico = sn.id_servico left join cliente_servico_endereco cse on cs.id_cliente_servico = cse.id_cliente_servico and cse.tipo like 'instalacao' left join endereco_numero en on cse.id_endereco_numero = en.id_endereco_numero "
    sql5 = "where ch.historico like '%Dados do Serviço%' or ch.historico like '%Pacote%adicionado ao serviço%' or ch.historico like '%Pacote%adicionado no serviço%' or ch.historico like '%Pacote%removido do serviço%' or ch.historico like '%Serviço%do cliente%migrou para o serviço%' or ch.historico like '%Novo serviço de número%serviço adicionado%' or ch.historico like '%O servico%migrou para o servico%' or ch.historico like '%O serviço%foi cancelado%' order by id_cliente, data_cadastro;"
