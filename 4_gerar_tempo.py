############################################################################
# Projeto Novácia                                                          #
# Autor: Welden Souza de Aguiar                                            #
# Iniciado em: 26/01/2022                                                  #
# Terminado em:                                                            #
############################################################################
# Descrição do Script: Este script é utilizando para gerar os dados para a #
# dimensão tempo e carregá-la no DataWarehouse                             #
############################################################################


# Bibliotecas
import pandas as pd
import getpass
import logging
import time
from datetime import datetime, date


# Contabilizar tempo de execução
inicio = time.time()
path='/home/dwadmin/telecom/comercial'


# Declarar variáveis globais
user = getpass.getuser()
data_nan = "2199-01-01"


# Configurar o Logger
log_format='%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=f"{path}/syslog.log",
                    filemode='a',
                    level = logging.DEBUG,
                    format=log_format)
logger = logging.getLogger(user)


# Gerar dados da dimensão Tempo
try:

    logger.info("INFO - Inicio da criação da dimensão tempo!")
    start = date(year=1995, month=1, day=1)
    end = date(year=2030, month=12, day=31)
    datelist = pd.date_range(start, end)
    tempo = pd.DataFrame({"id_tempo_sk":datelist})

    tempo['dia'] = tempo['id_tempo_sk'].dt.day
    tempo['mes'] = tempo['id_tempo_sk'].dt.month
    tempo['mes_nome'] = tempo['id_tempo_sk'].dt.month_name()
    tempo.loc[tempo['mes_nome'] == 'January', 'mes_nome'] = 'Janeiro'
    tempo.loc[tempo['mes_nome'] == 'February', 'mes_nome'] = 'Fevereiro'
    tempo.loc[tempo['mes_nome'] == 'March', 'mes_nome'] = 'Março'
    tempo.loc[tempo['mes_nome'] == 'April', 'mes_nome'] = 'Abril'
    tempo.loc[tempo['mes_nome'] == 'May', 'mes_nome'] = 'Maio'
    tempo.loc[tempo['mes_nome'] == 'June', 'mes_nome'] = 'Junho'
    tempo.loc[tempo['mes_nome'] == 'July', 'mes_nome'] = 'Julho'
    tempo.loc[tempo['mes_nome'] == 'August', 'mes_nome'] = 'Agosto'
    tempo.loc[tempo['mes_nome'] == 'September', 'mes_nome'] = 'Setembro'
    tempo.loc[tempo['mes_nome'] == 'October', 'mes_nome'] = 'Outubro'
    tempo.loc[tempo['mes_nome'] == 'November', 'mes_nome'] = 'Novembro'
    tempo.loc[tempo['mes_nome'] == 'December', 'mes_nome'] = 'Dezembro'
    tempo['ano'] = tempo['id_tempo_sk'].dt.year
    tempo['dia_da_semana'] = tempo['id_tempo_sk'].dt.day_name()
    tempo.loc[tempo['dia_da_semana'] == 'Sunday', 'dia_da_semana'] = 'Domingo'
    tempo.loc[tempo['dia_da_semana'] == 'Monday', 'dia_da_semana'] = 'Segunda'
    tempo.loc[tempo['dia_da_semana'] == 'Tuesday', 'dia_da_semana'] = 'Terça'
    tempo.loc[tempo['dia_da_semana'] == 'Wednesday', 'dia_da_semana'] = 'Quarta'
    tempo.loc[tempo['dia_da_semana'] == 'Thursday', 'dia_da_semana'] = 'Quinta'
    tempo.loc[tempo['dia_da_semana'] == 'Friday', 'dia_da_semana'] = 'Sexta'
    tempo.loc[tempo['dia_da_semana'] == 'Saturday', 'dia_da_semana'] = 'Sábado'
    tempo['trimestre_do_ano'] = tempo['id_tempo_sk'].dt.quarter
    tempo.loc[tempo['trimestre_do_ano'] <= 2, 'semestre_do_ano'] = 1
    tempo.loc[tempo['trimestre_do_ano'] > 2, 'semestre_do_ano'] = 2
    tempo['semestre_do_ano'] = tempo['semestre_do_ano'].astype(int)

    tempo['id_tempo_sk'] = pd.to_datetime(tempo['id_tempo_sk']).dt.strftime('%Y-%m-%d')

    tempo.loc[len(tempo)] = [data_nan, "01", "01", "INEXISTENTE", "2199", "INEXISTENTE", "0", "0"]

    tempo.to_csv(f"/home/{user}/dados_hubsoft/dimensao_tempo.csv", sep=";", index=False) 

    logger.info("SUCESSO - Dimensão Tempo criada com sucesso!")


except BaseException as err:
    fim = time.time()
    logger.info(f"ERRO - {err}")
    logger.info(f"ERRO - Tempo de execução do script: {(fim - inicio)}")
