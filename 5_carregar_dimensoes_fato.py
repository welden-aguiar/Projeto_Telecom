############################################################################
# Projeto Novácia                                                          #
# Autor: Welden Souza de Aguiar                                            #
# Iniciado em: 26/01/2022                                                  #
# Terminado em:                                                            #
############################################################################
# Descrição do Script: Este script é utilizando para carregar os dados das #
# dimensões e da tabela fato no DataWarehouse                              #
############################################################################


# Bibliotecas
import pandas as pd
import getpass
import psycopg2
import logging
from datetime import datetime
import time


# Contabilizar tempo de execução
inicio = time.time()
path='/home/dwadmin/telecom/comercial'


# Declarar variáveis globais
user = getpass.getuser()


# Configurar o Logger
log_format='%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=f"{path}/syslog.log",
                    filemode='a',
                    level = logging.DEBUG,
                    format=log_format)
logger = logging.getLogger(user)

con = psycopg2.connect(host='192.168.5.132', database='dwadmin', user='dwadmin', password='CG*125CC')
cur = con.cursor()
con.autocommit=True

def csv_to_psql(connection, csv, table):
    sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ';'"
    file = open(csv, "r")
    with connection.cursor() as cur:
        cur.execute("truncate table " + table + " cascade;")
        cur.copy_expert(sql=sql % table, file=file)
        connection.commit()
    return connection.commit()

try:

    logger.info("INFO - Início da carga das Dimensões e da Tabela Fato!")

    csv_to_psql(con, f"/home/{user}/dados_hubsoft/dimensao_cliente.csv", 'public.cliente')
    csv_to_psql(con, f"/home/{user}/dados_hubsoft/dimensao_endereco.csv", 'public.endereco')
    csv_to_psql(con, f"/home/{user}/dados_hubsoft/dimensao_tempo.csv", 'public.tempo')
    csv_to_psql(con, f"/home/{user}/dados_hubsoft/dimensao_produto.csv", 'public.produto')
    csv_to_psql(con, f"/home/{user}/dados_hubsoft/fato.csv", 'public.venda_fato')
    csv_to_psql(con, f"/home/{user}/dados_hubsoft/clientes_ativos.csv", 'public.clientes_ativos')

    fim = time.time()
    logger.info("SUCESSO - Dimensões e Tabela Fato carregadas com sucesso!")
    logger.info(f"SUCESSO - Tempo de execução da carga: {(fim - inicio)}")

except BaseException as err:
    fim = time.time()
    logger.info("ERRO - Erro ao inserir os dados no Banco de Dados.")
    logger.info(f" ERRO - {err}")
