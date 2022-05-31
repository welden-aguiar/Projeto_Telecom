############################################################################
# Projeto Novácia                                                          #
# Autor: Welden Souza de Aguiar                                            #
# Iniciado em: 26/01/2022                                                  #
# Terminado em:                                                            #
############################################################################
# Descrição do Script: Este script é utilizando para realizar limpeza e    #
# transformação nos dados do histórico do cliente e adicionar informações  #
# aos dados de históricos de pacotes e algumas tranformações.              #
############################################################################

# Bibliotecas
import pandas as pd
import getpass
import logging
import time
from datetime import datetime


# Contabilizar tempo de execução
inicio = time.time()
path='/home/dwadmin/telecom/comercial'


# Declarar variáveis globais
user = getpass.getuser()
int_nan = int(999999999)
data_nan = "2199-01-01"
data_ini = "1965-01-01"
data_fim = "2030-12-31"


# Configurar o Logger
user = getpass.getuser()
log_format='%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=f"{path}/syslog.log",
                    filemode='a',
                    level = logging.INFO,
                    format=log_format)
logger = logging.getLogger(user)

try:

    logger.info("INFO - Início da transformação e preparação para carga.")

    # Limpar e transformar histórico do cliente
    historico_cliente = pd.read_csv(f"/home/{user}/dados_hubsoft/dados_transformados.csv", sep=';', dtype=object)
    historico_cliente['id_cliente'] = historico_cliente['id_cliente'].astype(int)
    historico_cliente['numero_plano'] = historico_cliente['numero_plano'].astype(int)
    #cliente = historico_cliente['id_cliente'].unique()

    # Transformações
    historico_cliente['data_cadastro'] = pd.to_datetime(historico_cliente['data_cadastro']).dt.strftime('%Y-%m-%d')


    ### SERVICOS VENDIDOS ###

        # Gerando e manipulando arquivo de serviços vendidos
    servicos_cliente = pd.DataFrame(historico_cliente.loc[historico_cliente['historico'].str.contains('Dados do Serviço', na=False)])
    servicos_cliente = servicos_cliente.join(servicos_cliente["historico"].str.split(';', expand=True))
    servicos_cliente = servicos_cliente.rename(columns={
        0:'dados', 1:'data_venda', 2:'validade_p', 3:'vendedor', 4:'status', 
        5:'anotacoes_p', 6:'fatura_p', 7:'agrupamento_p', 8:'forma_cobranca', 9:'vencimento_p', 
        10:'tipo_cobranca_p', 11:'taxa_instalacao_p'
    })
        # dividir coluna dados 
    split_dados = servicos_cliente["dados"].str.split(':', expand=True)
        # preencher nome_servico
    servicos_cliente['nome_servico'] = split_dados[0].str.split('\) ', expand=True).get(1).str.split(' no momento', expand=True).get(0).replace({'\'' : ''}, regex=True)
    servicos_cliente = servicos_cliente.drop(columns=['dados'])
        # preencher valor
    if 3 in split_dados.columns:
        split_dados.loc[split_dados[3].str.contains('R\$', na=False), 'valor'] = split_dados[3].str.split('\$ ', expand=True).get(1)
    if 5 in split_dados.columns:
        split_dados.loc[split_dados[5].str.contains('R\$', na=False), 'valor'] = split_dados[5].str.split('\$ ', expand=True).get(1)
    servicos_cliente['valor'] = round(split_dados['valor'].astype(float), 2)
        # preencher numero_servico
    servicos_cliente['numero_servico_cliente'] = split_dados[0].str.split(' ', expand=True).get(3).str.strip('()').astype(int)
        # limpar memória
    split_dados = 0
        # preencher promocoes_ativas
    servicos_cliente['promocoes_ativas'] = 'NENHUM'
    if 12 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[12].str.contains('Promoções Ativadas', na=False), 'promocoes_ativas'] = servicos_cliente[12]
    if 13 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[13].str.contains('Promoções Ativadas', na=False), 'promocoes_ativas'] = servicos_cliente[13]
    if 14 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[14].str.contains('Promoções Ativadas', na=False), 'promocoes_ativas'] = servicos_cliente[14]
    if 15 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[15].str.contains('Promoções Ativadas', na=False), 'promocoes_ativas'] = servicos_cliente[15]
    if 16 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[16].str.contains('Promoções Ativadas', na=False), 'promocoes_ativas'] = servicos_cliente[16]
    if 17 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[17].str.contains('Promoções Ativadas', na=False), 'promocoes_ativas'] = servicos_cliente[17]
    if 18 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[18].str.contains('Promoções Ativadas', na=False), 'promocoes_ativas'] = servicos_cliente[18]
    servicos_cliente['promocoes_ativas'] = (servicos_cliente['promocoes_ativas'].replace({'Promoções Ativadas: ':'', 'Promoções ativadas: ':'', '\[':'', '\]':''}, regex=True))
        # preencher valor_instalacao
    servicos_cliente['valor_instalacao'] = '0.0'
    if 12 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[12].str.contains('R\$', na=False), 'valor_instalacao'] = servicos_cliente[12]
    if 13 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[13].str.contains('R\$', na=False), 'valor_instalacao'] = servicos_cliente[13]
    if 14 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[14].str.contains('R\$', na=False), 'valor_instalacao'] = servicos_cliente[14]
    if 15 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[15].str.contains('R\$', na=False), 'valor_instalacao'] = servicos_cliente[15]
    if 16 in servicos_cliente.columns:
        servicos_cliente.loc[servicos_cliente[16].str.contains('R\$', na=False), 'valor_instalacao'] = servicos_cliente[16]
    servicos_cliente.loc[servicos_cliente['taxa_instalacao_p'].str.contains('R\$', na=False), 'valor_instalacao'] = servicos_cliente['taxa_instalacao_p']
    servicos_cliente.loc[servicos_cliente['valor_instalacao'].str.contains('R\$', na=False), 'valor_instalacao'] = (servicos_cliente.loc[servicos_cliente['valor_instalacao'].str.contains('R\$', na=False), 'valor_instalacao']).str.split('R\$ ', expand=True).get(1)
    servicos_cliente['valor_instalacao'] = servicos_cliente['valor_instalacao'].astype(float)
        # Preencher demais colunas
    servicos_cliente['status'] = servicos_cliente['status'].str.split(': ', expand=True).get(1)
    servicos_cliente['vendedor'] = servicos_cliente['vendedor'].str.split(': ', expand=True).get(1)
    servicos_cliente['forma_cobranca'] = servicos_cliente['forma_cobranca'].str.split(': ', expand=True).get(1)
    servicos_cliente['data_venda'] = pd.to_datetime(servicos_cliente['data_venda'].str.rsplit(': ', expand=True).get(1), format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    servicos_cliente['id_transacao'] = (servicos_cliente.index).astype(int)
    servicos_cliente['tipo_transacao'] = 'VENDA'
    servicos_cliente['tipo_produto'] = 'SERVIÇO'
    servicos_cliente['motivo_cancelamento'] = servicos_cliente['motivo_cancelamento_cs']
    servicos_cliente['id_dev'] = ((servicos_cliente['id_cliente'] * 1000) + servicos_cliente['numero_servico_cliente']).astype(int)
    servicos_cliente['valor_soma_pacotes'] = float(0.0)
    servicos_cliente['valor_venda'] = float(0.0)
        # Editar data_venda
    servicos_cliente.loc[(servicos_cliente['data_venda'] < data_ini) | (servicos_cliente['data_venda'] > data_fim), 'data_venda'] = data_nan
        # Retirar duplicadas vindas do bando de dados
    servicos_cliente = servicos_cliente.loc[servicos_cliente['numero_plano'] == servicos_cliente['numero_servico_cliente']]
        # Ordenar servico_cliente
    servicos_cliente = servicos_cliente.sort_values(by=['id_dev'])  
        # Limpar colunas desnecessárias
    servicos_cliente = servicos_cliente.drop(columns={'validade_p', 'anotacoes_p', 'fatura_p', 'agrupamento_p', 'vencimento_p', 'taxa_instalacao_p', 'tipo_cobranca_p', 12, 13, 14, 15, 16, 17, 18})


    ### PACOTES ###

        ### CALCULAR PACOTES ADICIONADOS DURANTE A VENDA ###

    pacotes_durante = historico_cliente.loc[historico_cliente['historico'].str.contains('Pacote', na=False)]
    pacotes_durante = pacotes_durante.loc[pacotes_durante['historico'].str.contains('adicionado ao serviço', na=False)]
    pacotes_durante = pacotes_durante.loc[pacotes_durante['historico'].str.contains('durante o cadastro', na=False)]
    pacotes_durante['nome_pacote'] = pacotes_durante['historico'].str.split('\) ', expand=True).get(0).str.split('\(', expand=True).get(1)
    pacotes_durante['numero_servico_cliente'] = pacotes_durante['historico'].str.split('\) ', expand=True).get(1).str.split('\(', expand=True).get(1).astype(int)
    pacotes_durante['valor_pacote_durante_cadastro'] = pacotes_durante['historico'].str.split('R\$ ', expand=True).get(1).astype(float)
    pacotes_durante['id_dev'] = (pacotes_durante['id_cliente'] * 1000) + pacotes_durante['numero_servico_cliente']
    pacotes_durante = pacotes_durante.loc[pacotes_durante['numero_plano'] == pacotes_durante['numero_servico_cliente']]
    pacotes_durante = round(pacotes_durante.groupby(by=['id_dev'])['valor_pacote_durante_cadastro'].sum(), 2)
    pacotes_durante = pacotes_durante.rename_axis(['id_dev']).reset_index()

        ### CALCULAR PACOTES ADICIONADOS APÓS A VENDA ###

    pacotes_apos = historico_cliente.loc[historico_cliente['historico'].str.contains('Pacote', na=False)]
    pacotes_apos = pacotes_apos.loc[pacotes_apos['historico'].str.contains('adicionado no serviço', na=False)]
    pacotes_apos['numero_servico_cliente'] = pacotes_apos['historico'].str.split('\(', expand=True).get(2).str.split('\)', expand=True).get(0).astype(int)
    pacotes_apos = (pacotes_apos.loc[pacotes_apos['numero_servico_cliente'] == pacotes_apos['numero_plano']])
    pacotes_apos['valor_pacotes_apos_cadastro'] = pacotes_apos['historico'].str.split('R\$ ', expand=True).get(1).str.split(' ', expand=True).get(0).astype(float)
    pacotes_apos['id_dev'] = ((pacotes_apos['id_cliente'] * 1000) + pacotes_apos['numero_servico_cliente']).astype(int)
    pacotes_apos = round((pacotes_apos[['id_dev', 'valor_pacotes_apos_cadastro']]).groupby(by='id_dev')['valor_pacotes_apos_cadastro'].sum().rename_axis(['id_dev']).reset_index(), 2)

        ### CALCULAR PACOTES REMOVIDOS APÓS A VENDA ###

    pacotes_removidos = historico_cliente.loc[historico_cliente['historico'].str.contains('Pacote', na=False)]
    pacotes_removidos = pacotes_removidos.loc[pacotes_removidos['historico'].str.contains('removido do serviço', na=False)]
    pacotes_removidos['numero_servico_cliente'] = pacotes_removidos['historico'].str.split('\(', expand=True).get(2).str.split('\)', expand=True).get(0).astype(int)
    pacotes_removidos = (pacotes_removidos.loc[pacotes_removidos['numero_servico_cliente'] == pacotes_removidos['numero_plano']])
    pacotes_removidos['valor_soma_removidos'] = pacotes_removidos['historico'].str.split('R\$ ', expand=True).get(1).str.split(' ', expand=True).get(0).astype(float)
    pacotes_removidos['id_dev'] = (pacotes_removidos['id_cliente'] * 1000) + pacotes_removidos['numero_servico_cliente']
    pacotes_removidos = round((pacotes_removidos[['id_dev', 'valor_soma_removidos']]).groupby(by='id_dev')['valor_soma_removidos'].sum().rename_axis(['id_dev']).reset_index(), 2)
    
        ### ADICIONAR OS PACOTES ADICIONADOS DURANTE A VENDA AOS SERVICOS_CLIENTES ###

    servicos_cliente.loc[servicos_cliente['id_dev'].isin(pacotes_durante['id_dev']), 'valor_soma_pacotes'] = list(round(pacotes_durante['valor_pacote_durante_cadastro'] ,2))
    servicos_cliente['valor_venda'] = round(servicos_cliente['valor'] + servicos_cliente['valor_soma_pacotes'], 2)


    ### TROCA DE TITULARIDADE ###

        # verificar os clientes com troca de titularidade
    troca_titularidade = historico_cliente.loc[historico_cliente['historico'].str.contains('Serviço', na=False)]
    troca_titularidade = troca_titularidade.loc[troca_titularidade['historico'].str.contains('do cliente', na=False)]
    troca_titularidade = troca_titularidade.loc[troca_titularidade['historico'].str.contains('migrou para o serviço', na=False)]
        # separar dados de serviços remetente e destinatário, e criar o id_dev_destinatario
    troca_titularidade['numero_servico_remetente'] = troca_titularidade['historico'].str.split('\(', expand=True).get(1).str.split('\)', expand=True).get(0).astype(int)
    troca_titularidade['codigo_cliente_remetente'] = troca_titularidade['historico'].str.split('\(', expand=True).get(2).str.split('\)', expand=True).get(0).astype(int)
    troca_titularidade['numero_servico_destinatario'] = troca_titularidade['historico'].str.split('\(', expand=True).get(3).str.split('\)', expand=True).get(0).astype(int)
    troca_titularidade = troca_titularidade.loc[troca_titularidade['numero_servico_destinatario'] == troca_titularidade['numero_plano']]
    troca_titularidade['id_dev_destinatario'] = (troca_titularidade['id_cliente'] * 1000) + troca_titularidade['numero_servico_destinatario']

    validador = True
    while validador:

            # buscar nos serviços o id do remetente que condiz com o código do remetente para criar o id_dev_remetente
            # OBS: no DataFrame troca_titularidade ficaram os dados dos clientes destinatário
        id_cliente_remetente = servicos_cliente[['codigo_cliente', 'id_cliente']].astype(int)
        id_cliente_remetente = id_cliente_remetente.drop_duplicates()
        troca_titularidade = troca_titularidade.merge(id_cliente_remetente, how='left', left_on='codigo_cliente_remetente', right_on='codigo_cliente', suffixes=['', '_merge_remetente'])
        troca_titularidade = troca_titularidade.drop(columns='codigo_cliente_merge_remetente').rename(columns={'id_cliente_merge_remetente':'id_cliente_remetente'})
        troca_titularidade_sem_servicos = troca_titularidade.loc[troca_titularidade['id_cliente_remetente'].isna()]
        troca_titularidade_sem_servicos = troca_titularidade_sem_servicos.drop(columns='id_cliente_remetente')
        troca_titularidade = troca_titularidade.loc[~troca_titularidade['id_cliente_remetente'].isna()]
        troca_titularidade['id_cliente_remetente'] = troca_titularidade['id_cliente_remetente'].astype(int)
        troca_titularidade['id_dev_remetente'] = (troca_titularidade['id_cliente_remetente'] * 1000) + troca_titularidade['numero_servico_remetente']

            # criar serviço do cliente destinatario
            # OBS: neste ponto será necessário alterar alguns dados do cliente destinatário, para isso será necessário buscar também alguns dados do remetente.
        servico_destinatario = troca_titularidade
        servico_destinatario = servico_destinatario.rename(columns={'id_dev_destinatario':'id_dev'})
            # buscar o valor do servico no momento da troca de titularidade
        valor_servico_destinatario = historico_cliente.loc[historico_cliente['historico'].str.contains('Novo serviço de número', na=False)]
        valor_servico_destinatario = valor_servico_destinatario.loc[valor_servico_destinatario['historico'].str.contains('serviço adicionado', na=False)]
        valor_servico_destinatario['numero_servico_cliente'] = valor_servico_destinatario['historico'].str.split('\)', expand=True).get(0).str.split('\(', expand=True).get(1).astype(int)
        valor_servico_destinatario['valor'] = valor_servico_destinatario['historico'].str.split('R\$ ', expand=True).get(1).astype(float)
        valor_servico_destinatario = valor_servico_destinatario.loc[valor_servico_destinatario['numero_servico_cliente'] == valor_servico_destinatario['numero_plano']]       
        valor_servico_destinatario['id_dev'] = (valor_servico_destinatario['id_cliente'] * 1000) + valor_servico_destinatario['numero_servico_cliente']
        valor_servico_destinatario = valor_servico_destinatario[['id_dev', 'valor']]
        valor_servico_destinatario = valor_servico_destinatario.drop_duplicates(subset=['id_dev'])        
            # preencher o valor do servico destinatario
        servico_destinatario = servico_destinatario.merge(valor_servico_destinatario, how='left', on='id_dev')
            # será necessário buscar os valores dos pacotes adicionados ao servico remetente durante o cadastro do serviço.
            # preencher os valores dos pacotes adicionados durante o cadastro do servico remetente
        servico_destinatario = servico_destinatario.merge(pacotes_durante, how='left', left_on='id_dev_remetente', right_on='id_dev')
        servico_destinatario = servico_destinatario.drop(columns='id_dev_y').rename(columns={'id_dev_x':'id_dev'})
        servico_destinatario['id_dev'] = servico_destinatario['id_dev'].astype(int)
        servico_destinatario['valor_pacote_durante_cadastro'].fillna(0.0, inplace=True)
            # preencher o valor dos pacotes adicionados após o cadastro no serviço inicial
        servico_destinatario = servico_destinatario.merge(pacotes_apos, how='left', left_on='id_dev_remetente', right_on='id_dev')
        servico_destinatario = servico_destinatario.drop(columns='id_dev_y').rename(columns={'id_dev_x':'id_dev'})
        servico_destinatario['id_dev'] = servico_destinatario['id_dev'].astype(int)
        servico_destinatario['valor_pacotes_apos_cadastro'].fillna(0.0, inplace=True)
            # adicionar o valor dos pacotes removidos após o cadastro no serviço inicial
        servico_destinatario = servico_destinatario.merge(pacotes_removidos, how='left', left_on='id_dev_remetente', right_on='id_dev')
        servico_destinatario = servico_destinatario.drop(columns='id_dev_y').rename(columns={'id_dev_x':'id_dev'})
        servico_destinatario['id_dev'] = servico_destinatario['id_dev'].astype(int)
        servico_destinatario['valor_soma_removidos'].fillna(0.0, inplace=True)
            # calcular o valor da troca de titularidade
        servico_destinatario['valor_soma_pacotes'] = round(servico_destinatario['valor_pacote_durante_cadastro'] + servico_destinatario['valor_pacotes_apos_cadastro'] - servico_destinatario['valor_soma_removidos'], 2)
        servico_destinatario['valor_venda'] = round(servico_destinatario['valor'] + servico_destinatario['valor_soma_pacotes'], 2)
            # preencher demais colunas
        servico_destinatario['data_venda'] = servico_destinatario['data_cadastro']
        servico_destinatario['vendedor'] = servico_destinatario['vendedor_historico']
        servico_destinatario['status'] = servico_destinatario['status_cs']
        servico_destinatario['forma_cobranca'] = servico_destinatario['forma_cobranca_cs']
        servico_destinatario['numero_servico_cliente'] = servico_destinatario['numero_plano']
        servico_destinatario['promocoes_ativas'] = 'NENHUM'
        servico_destinatario['valor_instalacao'] = 0.0
        servico_destinatario['id_transacao'] = servicos_cliente['id_transacao'].iloc[-1] + servico_destinatario.index
        servico_destinatario['tipo_transacao'] = 'TROCA DE TITULARIDADE'
        servico_destinatario['tipo_produto'] = 'SERVIÇO'
        servico_destinatario['motivo_cancelamento'] = servico_destinatario['motivo_cancelamento_cs']   
            # ordenar e remover colunas desnecessárias
        colunas = list(servicos_cliente.columns.astype(str))
        servico_destinatario = servico_destinatario[colunas]
            # preencher o servicos_cliente com os servicos de troca de titularidade
        servicos_cliente = pd.concat([ servicos_cliente ,servico_destinatario ], ignore_index=True)
            # adicionar troca_titularidade_sem_servicos ao troca_titularidade para preencher com os valores faltantes
        troca_titularidade = troca_titularidade_sem_servicos

        servico_destinatario.to_csv(f"/home/{user}/dados_hubsoft/servico_destinatario.csv", sep=";", index=False)    
        servicos_cliente.to_csv(f"/home/{user}/dados_hubsoft/servicos_cliente.csv", sep=";", index=False)    

        if not troca_titularidade_sem_servicos.empty:
            validador = True

        if troca_titularidade_sem_servicos.empty:
            validador = False


    ### MUDANÇA DE PLANO ###

    mudanca_plano = historico_cliente.loc[historico_cliente['historico'].str.contains('O servico', na=False)]
    mudanca_plano = mudanca_plano.loc[mudanca_plano['historico'].str.contains('migrou para o servico', na=False)]
    mudanca_plano['numero_servico_cliente_inicial'] = mudanca_plano['historico'].str.split('\)', expand=True).get(0).str.split('\(', expand=True).get(1).astype(int)
    mudanca_plano['numero_servico_cliente_final'] = mudanca_plano['historico'].str.split('\)', expand=True).get(1).str.split('\(', expand=True).get(1).astype(int)
    mudanca_plano['id_cliente'] = mudanca_plano['id_cliente'].astype(int)
    mudanca_plano = mudanca_plano.loc[mudanca_plano['numero_plano'] == mudanca_plano['numero_servico_cliente_inicial']]
    mudanca_plano['id_dev_inicial'] = (mudanca_plano['id_cliente'] * 1000) + mudanca_plano['numero_servico_cliente_inicial']
    mudanca_plano['id_dev_final'] = (mudanca_plano['id_cliente'] * 1000) + mudanca_plano['numero_servico_cliente_final']
    #data_cancelamento_mudanca_plano = mudanca_plano[['id_dev_inicial', 'data_cadastro']]
    #data_cancelamento_mudanca_plano = data_cancelamento_mudanca_plano.rename(columns={'id_dev_inicial':'id_dev', 'data_cadastro':'data_cancelamento'})
    #data_cancelamento_mudanca_plano.to_csv(f"/home/{user}/dados_hubsoft/data_cancelamento_mudanca_plano.csv", sep=";", index=False)
    
        # data_cancelamento
    #servicos_cliente = servicos_cliente.merge(data_cancelamento_mudanca_plano, how='left', on='id_dev')

        # tipo_transacao
    mudanca_plano = mudanca_plano.merge(servicos_cliente[['id_dev', 'download_servico']], how='left', left_on='id_dev_final', right_on='id_dev', suffixes=['', '_final']).drop(columns='id_dev')
    mudanca_plano.loc[mudanca_plano['download_servico'] < mudanca_plano['download_servico_final'], 'tipo_transacao'] = "UPGRADE DE BANDA"
    mudanca_plano.loc[mudanca_plano['download_servico'] > mudanca_plano['download_servico_final'], 'tipo_transacao'] = "DOWNGRADE DE BANDA" 
    mudanca_plano.loc[mudanca_plano['download_servico'] == mudanca_plano['download_servico_final'], 'tipo_transacao'] = "MUDANÇA DE PLANO SEM ALTERAÇÃO DE BANDA" 
    servicos_cliente.loc[(servicos_cliente['id_dev'].isin(mudanca_plano['id_dev_final']), 'tipo_transacao')] = list(mudanca_plano['tipo_transacao'])

    servicos_cliente.to_csv(f"/home/{user}/dados_hubsoft/servicos_cliente_em_mudanca.csv", sep=";", index=False)


    # A data do cancelamento será usada a data_cancelamento_cs do sistema e não será excluido para posteriores usos
    '''### CANCELAMENTOS ###

    servicos_cancelados = historico_cliente.loc[historico_cliente['historico'].str.contains('O serviço', na=False)]
    servicos_cancelados = servicos_cancelados.loc[servicos_cancelados['historico'].str.contains('foi cancelado', na=False)]
    servicos_cancelados['numero_servico_cliente'] = servicos_cancelados['historico'].str.split('\)', expand=True).get(0).str.split('\(', expand=True).get(1).astype(int)
    servicos_cancelados['id_cliente'] = servicos_cancelados['id_cliente'].astype(int)
    servicos_cancelados = servicos_cancelados.loc[servicos_cancelados['numero_plano'] == servicos_cancelados['numero_servico_cliente']]
    servicos_cancelados['id_dev'] = (servicos_cancelados['id_cliente'] * 1000) + servicos_cancelados['numero_servico_cliente']
    servicos_cancelados = servicos_cancelados[['id_dev', 'data_cadastro']]
    servicos_cancelados = servicos_cancelados.drop_duplicates(subset='id_dev', keep='last')
    servicos_cancelados = servicos_cancelados.sort_values(by='id_dev')
        # modificar a data de cancelamento do servicos_cliente
    servicos_cliente.loc[servicos_cliente['id_dev'].isin(servicos_cancelados['id_dev']), 'data_cancelamento'] = list(servicos_cancelados['data_cadastro'])

    servicos_cliente.to_csv(f"/home/{user}/dados_hubsoft/servicos_cliente_em_cancelados.csv", sep=";", index=False)'''


    ### SERVIÇOS VINCULADOS ###

    servicos_cliente[['id_cliente_servico', 'id_cliente_servico_associado']] = servicos_cliente[['id_cliente_servico', 'id_cliente_servico_associado']].astype(int)
    id_cs_associado = list(servicos_cliente.loc[servicos_cliente['id_cliente_servico_associado'] != int_nan, 'id_cliente_servico_associado'])
    id_transacao = servicos_cliente.loc[servicos_cliente['id_cliente_servico'].isin(id_cs_associado), ['id_cliente_servico', 'id_transacao']]
    servicos_associados = servicos_cliente.merge(id_transacao, how='left', left_on='id_cliente_servico_associado', right_on='id_cliente_servico')
    servicos_cliente.loc[servicos_cliente['id_cliente_servico_associado'] != int_nan, 'id_transacao'] = servicos_associados.loc[servicos_associados['id_cliente_servico_associado'] != int_nan, 'id_transacao_y'].astype(int)


    ### ULTIMOS AJUSTES EM SERVICOS_CLIENTE ###

    servicos_cliente = servicos_cliente.rename(columns={'data_cancelamento_cs':'data_cancelamento'})
    servicos_cliente['data_carga'] = datetime.now().date()
    servicos_cliente['id_venda_sk'] = list(servicos_cliente.index.astype(int))
    servicos_cliente['valor_instalacao'].fillna(0.0, inplace=True)


    ### EXPORTAR DADOS PRONTOS EM CSV ###
    servicos_cliente.to_csv(f"/home/{user}/dados_hubsoft/servicos_cliente.csv", sep=";", index=False)
    logger.info("SUCESSO - Dados Transformados!")


    ### DIMENSÃO CLIENTE ###

    logger.info("INFO - Início da preparação para carga!")

    servicos_cliente[['id_cliente', 'codigo_cliente']] = servicos_cliente[['id_cliente', 'codigo_cliente']].astype(int)
    servicos_cliente[['nome_cliente', 'nome_fantasia_cliente', 'tipo_pessoa_cliente', 'origem_cliente']] = servicos_cliente[['nome_cliente', 'nome_fantasia_cliente', 'tipo_pessoa_cliente', 'origem_cliente']].apply(lambda x: x.astype(str).str.upper())
    cliente = servicos_cliente.drop_duplicates(subset='id_cliente')
    colunas_dim_cliente = [
        'id_cliente_nk', 'data_cadastro_cliente', 'nome_cliente', 'nome_fantasia_cliente', 'tipo_pessoa_cliente',
        'origem_cliente', 'data_nascimento_cliente', 'codigo_cliente', 'data_carga_cliente'
    ]
    dim_cliente = pd.DataFrame(columns=colunas_dim_cliente)
    dim_cliente [[
        'id_cliente_nk', 'data_cadastro_cliente', 'nome_cliente', 'nome_fantasia_cliente', 'tipo_pessoa_cliente',
        'origem_cliente', 'data_nascimento_cliente', 'codigo_cliente', 'data_carga_cliente'
    ]] = cliente [[
        'id_cliente', 'data_cadastro_cliente', 'nome_cliente', 'nome_fantasia_cliente', 'tipo_pessoa_cliente',
        'origem_cliente', 'data_nascimento_cliente', 'codigo_cliente', 'data_carga'
    ]]
    dim_cliente = dim_cliente.sort_values(by='id_cliente_nk')
    dim_cliente.to_csv(f"/home/{user}/dados_hubsoft/dimensao_cliente.csv", sep=";", index=False)


    ### DIMENSÃO ENDEREÇO ###

    servicos_cliente['id_endereco_nk'] = servicos_cliente['id_endereco_nk'].astype(int)
    servicos_cliente[['cep_localidade', 'estado_sigla', 'estado_localidade', 'cidade_localidade', 'bairro_localidade', 'endereco_localidade', 'complemento_localidade']] = servicos_cliente[['cep_localidade', 'estado_sigla', 'estado_localidade', 'cidade_localidade', 'bairro_localidade', 'endereco_localidade', 'complemento_localidade']].apply(lambda x: x.astype(str).str.upper())
    endereco = servicos_cliente.drop_duplicates(subset='id_endereco_nk')
    colunas_dim_endereco = [
        'id_endereco_nk', 'cep', 'sigla_uf', 'estado', 'cidade',
        'bairro', 'endereco', 'complemento', 'data_carga_endereco'
    ]
    dim_endereco = pd.DataFrame(columns=colunas_dim_endereco)
    dim_endereco[[
        'id_endereco_nk', 'cep', 'sigla_uf', 'estado', 'cidade',
        'bairro', 'endereco', 'complemento', 'data_carga_endereco'
    ]] = endereco[[
        'id_endereco_nk', 'cep_localidade', 'estado_sigla', 'estado_localidade', 'cidade_localidade',
        'bairro_localidade', 'endereco_localidade', 'complemento_localidade', 'data_carga'
    ]]
    dim_endereco = dim_endereco.sort_values(by='id_endereco_nk')
    dim_endereco.to_csv(f"/home/{user}/dados_hubsoft/dimensao_endereco.csv", sep=";", index=False)


    ### DIMENSÃO PRODUTO ###

    servicos_cliente[['id_servico', 'download_servico', 'upload_servico']] = servicos_cliente[['id_servico', 'download_servico', 'upload_servico']].astype(int)
    servicos_cliente[['nome_servico', 'tipo_produto']] = servicos_cliente[['nome_servico', 'tipo_produto']].apply(lambda x: x.astype(str).str.upper())
    servicos_cliente['valor_servico'] = servicos_cliente['valor_servico'].astype(float)
    produto = servicos_cliente.drop_duplicates(subset='id_servico')
    colunas_produto = [
        'id_produto_nk', 'data_cadastro_produto', 'nome_produto', 'valor_produto', 'download_produto', 
        'upload_produto', 'tipo_produto', 'data_carga_produto'
    ]
    dim_produto = pd.DataFrame(columns=colunas_produto)
    dim_produto[[
        'id_produto_nk', 'data_cadastro_produto', 'nome_produto', 'valor_produto', 'download_produto', 
        'upload_produto', 'tipo_produto', 'data_carga_produto'
    ]] = produto[[
        'id_servico', 'data_cadastro_servico', 'nome_servico', 'valor_servico', 'download_servico',
        'upload_servico', 'tipo_produto', 'data_carga'
    ]]
    dim_produto = dim_produto.sort_values(by='id_produto_nk')
    dim_produto.to_csv(f"/home/{user}/dados_hubsoft/dimensao_produto.csv", sep=";", index=False) 

    
    ### TABELA FATO VENDA ###

    servicos_cliente[['status', 'descricao_tecnologia_cs', 'vendedor', 'origem_cliente', 'motivo_cancelamento', 'tipo_transacao', 'tipo_produto', 'forma_cobranca', 'empresa_cs']] = servicos_cliente[['status', 'descricao_tecnologia_cs', 'vendedor', 'origem_cliente', 'motivo_cancelamento', 'tipo_transacao', 'tipo_produto', 'forma_cobranca', 'empresa_cs']].apply(lambda x: x.astype(str).str.upper())
    fato = servicos_cliente [[ 
        "id_cliente", "id_endereco_nk", "id_servico", "data_venda", "id_venda_sk", "id_transacao",
        "valor_venda", "status", "data_venda", "data_habilitacao_cs", "descricao_tecnologia_cs", 
        "vendedor", "origem_cliente", "valor_instalacao", "motivo_cancelamento", "data_cancelamento", 
        "numero_servico_cliente", 'tipo_transacao', "tipo_produto", "forma_cobranca", "empresa_cs", 
        "data_carga"
    ]]
    fato.columns = ["id_cliente_nk", "id_endereco_nk", "id_produto_nk", "id_tempo_sk", "id_venda_sk", "id_transacao",
        "valor_venda", "status", "data_venda", "data_habilitacao", "descricao_tecnologia", 
        "vendedor", "origem", "valor_instalacao", "motivo_cancelamento", "data_cancelamento", 
        "numero_servico_cliente", 'tipo_transacao', "tipo_produto", "forma_cobranca", "empresa", 
        "data_carga_venda"]
    fato = fato.sort_values(by='id_cliente_nk')
    fato.to_csv(f"/home/{user}/dados_hubsoft/fato.csv", sep=";", index=False) 


    # Gravar no log
    fim = time.time()
    logger.info("SUCESSO - Dados Transformados e prontos para carga!")
    logger.info(f"SUCESSO - Tempo de execução do script: {(fim - inicio)}")

except BaseException as err:
    fim = time.time()
    logger.info(f"ERRO - {err}")
    logger.info(f"ERRO - Tempo de execução do script: {(fim - inicio)}")

