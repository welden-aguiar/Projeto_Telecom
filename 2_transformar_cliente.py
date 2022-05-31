############################################################################
# Projeto Novácia                                                          #
# Autor: Welden Souza de Aguiar                                            #
# Iniciado em: 26/01/2022                                                  #
# Terminado em:                                                            #
############################################################################
# Descrição do Script: Este script é utilizando para realizar limpeza e    #
# uma transformação nos dados dos clientes                                 #
############################################################################


# Bibliotecas
import pandas as pd
import getpass
import logging
from datetime import date, datetime
import time


# Contabilizar tempo de execução
inicio = time.time()
path='/home/dwadmin/telecom/comercial'


# Declarar variáveis globais
user = getpass.getuser()
int_nan = int(999999999)
data_nan = "2199-01-01"
data_ini = "1970-01-01"


# Configurando o Logger
user = getpass.getuser()
log_format='%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=f"{path}/syslog.log",
                    filemode='a',
                    level = logging.INFO,
                    format=log_format)
logger = logging.getLogger(user)


# Limpar e transformar dados dos clientes
try:

    logger.info("INFO - Início da limpeza dos dados!")

    comercial = pd.read_csv(f"/home/{user}/dados_hubsoft/dados_totais.csv", dtype=object)

    #### CLIENTE ####

    # coluna id_cliente
    comercial['id_cliente'].fillna(int_nan, inplace=True)
    
    # coluna codigo_cliente
    comercial['codigo_cliente'].fillna(int_nan, inplace=True)
    comercial['codigo_cliente'] = comercial['codigo_cliente'].astype(int)

    # coluna data_cadastro_cliente
    comercial.loc[comercial['data_cadastro_cliente'] < data_ini, 'data_cadastro_cliente'] = data_nan
    comercial['data_cadastro_cliente'] = pd.to_datetime(comercial['data_cadastro_cliente']).dt.strftime('%Y-%m-%d')
    comercial['data_cadastro_cliente'].fillna(data_nan, inplace=True)
    
    # coluna nome_cliente
    comercial['nome_cliente'].fillna("NÃO INFORMADO", inplace=True)
    comercial['nome_cliente'] = comercial['nome_cliente'].replace({'\'' : ''}, regex=True)
    comercial.nome_cliente = comercial.nome_cliente.str.upper()

    # coluna nome_fantasia_cliente
    comercial['nome_fantasia_cliente'].fillna("NÃO ATRIBUIDO", inplace=True)
    comercial['nome_fantasia_cliente'] = comercial['nome_fantasia_cliente'].replace({'\'' : ''}, regex=True)
    comercial.nome_fantasia_cliente = comercial.nome_fantasia_cliente.str.upper()

    # coluna tipo_pessoa_cliente
    comercial['tipo_pessoa_cliente'].fillna("NÃO ATRIBUIDO", inplace=True)
    comercial.tipo_pessoa_cliente = comercial.tipo_pessoa_cliente.str.upper()

    # coluna origem_cliente
    comercial['origem_cliente'].fillna("NÃO INFORMADO", inplace=True)
    comercial.origem_cliente = comercial.origem_cliente.str.upper()

    # coluna data_nascimento_cliente
    comercial.loc[comercial['data_nascimento_cliente'] < data_ini, 'data_nascimento_cliente'] = data_nan
    comercial['data_nascimento_cliente'] = pd.to_datetime(comercial['data_nascimento_cliente']).dt.strftime('%Y-%m-%d')
    comercial['data_nascimento_cliente'].fillna(data_nan, inplace=True)

    #### SERVICO ####

    # coluna id_servico_
    comercial['id_servico'].fillna(int_nan, inplace=True)

    # coluna data_cadastro_servico
    comercial.loc[comercial['data_cadastro_servico'] < data_ini, 'data_cadastro_servico'] = data_nan
    comercial['data_cadastro_servico'] = pd.to_datetime(comercial['data_cadastro_servico']).dt.strftime('%Y-%m-%d')
    comercial['data_cadastro_servico'].fillna(data_nan, inplace=True)

    # coluna valor_servico
    comercial['valor_servico'].fillna(0.0, inplace=True)
    
    # coluna nome_servico
    comercial['nome_servico'].fillna("NÃO ATRIBUIDO", inplace=True)
    comercial['nome_servico'] = comercial['nome_servico'].replace({'\'' : '', '\'':''}, regex=True)

    comercial.nome_servico = comercial.nome_servico.str.upper()

    # coluna download_servico
    comercial['download_servico'].fillna(0.0, inplace=True)

    # coluna upload_servico
    comercial['upload_servico'].fillna(0.0, inplace=True)

    #### CLIENTE SERVICO ####

    # coluna id_cliente_servico
    comercial['id_cliente_servico'].fillna(int_nan, inplace=True)

    # coluna id_cliente_servico_associado
    comercial['id_cliente_servico_associado'].fillna(int_nan, inplace=True)
    comercial['id_cliente_servico_associado'] = comercial['id_cliente_servico_associado'].astype(int)

    # coluna numero_plano
    comercial['numero_plano'] = comercial['numero_plano'].astype(int)
    comercial['numero_plano'].fillna(int_nan, inplace=True)

    # coluna data_habilitacao_cs 
    comercial['data_habilitacao_cs'] = pd.to_datetime(comercial['data_habilitacao_cs']).dt.strftime('%Y-%m-%d')
    comercial['data_habilitacao_cs'].fillna(data_nan, inplace=True)

    # coluna descricao_tecnologia_cs
    comercial['descricao_tecnologia_cs'].fillna("NÃO ATRIBUIDO", inplace=True)
    comercial['descricao_tecnologia_cs'] = comercial['descricao_tecnologia_cs'].replace({'\'' : ''}, regex=True)
    comercial.descricao_tecnologia_cs = comercial.descricao_tecnologia_cs.str.upper()

    # coluna origem_cs
    comercial['origem_cs'].fillna("NÃO ATRIBUIDO", inplace=True)
    comercial.origem_cs = comercial.origem_cs.str.upper()

    # coluna id_servico_antigo
    comercial['id_servico_antigo'].fillna(int_nan, inplace=True)
    comercial['id_servico_antigo'] = comercial['id_servico_antigo'].astype(int)

    # coluna data_cancelamento_cs
    comercial.loc[comercial['data_cancelamento_cs'] < data_ini, 'data_cancelamento_cs'] = data_nan
    comercial['data_cancelamento_cs'] = pd.to_datetime(comercial['data_cancelamento_cs']).dt.strftime('%Y-%m-%d')
    comercial['data_cancelamento_cs'].fillna(data_nan, inplace=True)

    # coluna motivo_cancelamento_cs
    comercial['motivo_cancelamento_cs'].fillna("NÃO CANCELADO", inplace=True)
    comercial.motivo_cancelamento_cs = comercial.motivo_cancelamento_cs.str.upper()

    # coluna forma_cobranca_cs
    comercial['forma_cobranca_cs'].fillna("NÃO INFORMADO", inplace=True)
    comercial.forma_cobranca_cs = comercial.forma_cobranca_cs.str.upper()

    # coluna empresa_cs
    comercial['empresa_cs'].fillna("NÃO INFORMADO", inplace=True)
    comercial.empresa_cs = comercial.empresa_cs.str.upper()

    #### ENDERECO ####

    # coluna id_endereco_nk
    comercial['id_endereco_nk'].fillna(int_nan, inplace=True)

    # coluna id_cse
    comercial['id_cse'].fillna(int_nan, inplace=True)

    # coluna cep_localidade
    comercial['cep_localidade'].fillna(99999999, inplace=True)

    # coluna bairro_localidade
    comercial['bairro_localidade'].fillna("NÃO INFORMADO", inplace=True)
    comercial['bairro_localidade'] = comercial['bairro_localidade'].replace({'\'' : ''}, regex=True)
    comercial.bairro_localidade = comercial.bairro_localidade.str.upper()

    # coluna complemento_localidade
    comercial['complemento_localidade'].fillna("NÃO INFORMADO", inplace=True)
    comercial['complemento_localidade'] = comercial['complemento_localidade'].replace({'\'' : ''}, regex=True)
    comercial.complemento_localidade = comercial.complemento_localidade.str.upper()

    # coluna numero_localidade
    comercial['numero_localidade'].fillna("NÃO INFORMADO", inplace=True)
    comercial.numero_localidade = comercial.numero_localidade.str.upper()

    # coluna endereco_localidade
    comercial['endereco_localidade'].fillna("NÃO INFORMADO", inplace=True)
    comercial['endereco_localidade'] = comercial['endereco_localidade'].replace({'\'' : ''}, regex=True)
    comercial.endereco_localidade = comercial.endereco_localidade.str.upper()

    # coluna cidade_localidade
    comercial['cidade_localidade'].fillna("NÃO INFORMADO", inplace=True)
    comercial['cidade_localidade'] = comercial['cidade_localidade'].replace({'\'' : ''}, regex=True)
    comercial.cidade_localidade = comercial.cidade_localidade.str.upper()

    # coluna estado_localidade
    comercial['estado_localidade'].fillna("NÃO INFORMADO", inplace=True)
    comercial['estado_localidade'] = comercial['estado_localidade'].replace({'\'' : ''}, regex=True)
    comercial.estado_localidade = comercial.estado_localidade.str.upper()

    # coluna estado_sigla
    comercial['estado_sigla'].fillna("NÃO INFORMADO", inplace=True)
    comercial.estado_sigla = comercial.estado_sigla.str.upper()


    #### EXPORTAR PARA CSV ####
    
    comercial.to_csv(f"/home/{user}/dados_hubsoft/dados_transformados.csv", sep=';', index=False)

    # Gravar no log
    fim = time.time()
    logger.info("SUCESSO - Dados dos clientes limpos e transformados com sucesso!")
    logger.info(f"SUCESSO - Tempo de execução do script: {(fim - inicio)}")

except BaseException as err:
    fim = time.time()
    logger.info(f"ERRO - {err}")
    logger.info(f"ERRO - Tempo de execução do script: {(fim - inicio)}")
