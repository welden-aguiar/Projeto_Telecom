############################################################################
# Projeto Novácia                                                          #
# Autor: Welden Souza de Aguiar                                            #
# Iniciado em: 26/01/2022                                                  #
# Terminado em:                                                            #
############################################################################
# Descrição do Script: Este script é utilizando para acessar a página do   #
# hubsoft e realizar um select buscando informações do cliente, histórico  #
# do cliente e historico dos pacotes                                       #
############################################################################


# Bibliotecas
import subprocess
import os
import glob
from time import sleep
from selenium import webdriver
import requests
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
import getpass
import time


# Contabilizar tempo de execução
inicio = time.time()
path='/home/dwadmin/telecom/comercial'


# Configurando o Logger
user = getpass.getuser()
log_format='%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=f"{path}/syslog.log",
                    filemode='a',
                    level = logging.INFO,
                    format=log_format)
logger = logging.getLogger(user)


# Testando conexão
urlstatus = requests.get('url').status_code
if urlstatus != 200:
    logger.info(f"Status Conexão: ERRO - {urlstatus}")
else:
    logger.info(f"Status Conexão: SUCESSO - {urlstatus}")

try:

    logger.info("INFO - Início da extração dos dados do cliente!")

    # Buscar informações sobre os clientes e os serviços
    # Adicionar o caminho do geckodriver ao PATH
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get('url)
    WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.NAME, "username"))

    # Logar no sistema
    driver.find_element(By.NAME, "username").send_keys("login" + Keys.TAB + "senha" + Keys.ENTER)
    sleep(5)

    sql1 = "select ch.id_cliente_historico as id_cliente_historico, ch.id_cliente as id_cliente, ch.historico as historico, ch.data_cadastro as data_cadastro, u.name as vendedor_historico, cli.codigo_cliente as codigo_cliente, cli.data_cadastro as data_cadastro_cliente, cli.nome_razaosocial as nome_cliente, cli.nome_fantasia as nome_fantasia_cliente, cli.tipo_pessoa as tipo_pessoa_cliente, oc.descricao as origem_cliente, cli.data_nascimento as data_nascimento_cliente, s.id_servico as id_servico, s.data_cadastro as data_cadastro_servico, s.valor as valor_servico, s.descricao as nome_servico, sn.download_contrato as download_servico, sn.upload_contrato as upload_servico, "
    sql2 = "cs.id_cliente_servico as id_cliente_servico, cs.id_cliente_servico_associado as id_cliente_servico_associado, cs.numero_plano as numero_plano, cs.data_habilitacao as data_habilitacao_cs, st.descricao as descricao_tecnologia_cs, cs.origem as origem_cs, cs.id_cliente_servico_antigo as id_servico_antigo, cs.data_cancelamento as data_cancelamento_cs, (select descricao from motivo_cancelamento where cs.id_motivo_cancelamento = id_motivo_cancelamento) as motivo_cancelamento_cs, fc.descricao as forma_cobranca_cs, (select nome_razaosocial from empresa where fc.id_empresa = id_empresa) as empresa_cs, (select descricao from servico_status where cs.id_servico_status = id_servico_status) as status_cs, "
    sql3 = "en.id_endereco_numero as id_endereco_nk, cse.id_cliente_servico_endereco as id_cse, en.cep as cep_localidade, en.bairro as bairro_localidade, en.complemento as complemento_localidade, en.numero as numero_localidade, en.endereco as endereco_localidade, (select nome from cidade where en.id_cidade = id_cidade) as cidade_localidade, (select estado.nome from cidade, estado where cidade.id_cidade = en.id_cidade and cidade.id_estado = estado.id_estado) as estado_localidade, (select estado.sigla from cidade, estado where cidade.id_cidade = en.id_cidade and cidade.id_estado = estado.id_estado) as estado_sigla "
    sql4 = "from cliente_historico ch left join users u on ch.id_usuario = u.id left join cliente cli on cli.id_cliente = ch.id_cliente left join origem_cliente oc on cli.id_origem_cliente = oc.id_origem_cliente left join cliente_servico cs on cs.id_cliente = ch.id_cliente left join servico_tecnologia st on cs.id_servico_tecnologia = st.id_servico_tecnologia left join forma_cobranca fc on cs.id_forma_cobranca = fc.id_forma_cobranca left join servico s on cs.id_servico = s.id_servico left join servico_navegacao sn on cs.id_servico = sn.id_servico left join cliente_servico_endereco cse on cs.id_cliente_servico = cse.id_cliente_servico and cse.tipo like 'instalacao' left join endereco_numero en on cse.id_endereco_numero = en.id_endereco_numero "
    sql5 = "where ch.historico like '%Dados do Serviço%' or ch.historico like '%Pacote%adicionado ao serviço%' or ch.historico like '%Pacote%adicionado no serviço%' or ch.historico like '%Pacote%removido do serviço%' or ch.historico like '%Serviço%do cliente%migrou para o serviço%' or ch.historico like '%Novo serviço de número%serviço adicionado%' or ch.historico like '%O servico%migrou para o servico%' or ch.historico like '%O serviço%foi cancelado%' order by id_cliente, data_cadastro;"

    # Buscar dados
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[3]/div[3]").click()
    driver.find_element(By.CLASS_NAME, "ace_text-input").clear()
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(sql1)
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(Keys.ENTER)
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(sql2)
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(Keys.ENTER)
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(sql3)
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(Keys.ENTER)
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(sql4)
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(Keys.ENTER)
    driver.find_element(By.CLASS_NAME, "ace_text-input").send_keys(sql5)
    sleep(5)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]/button").click()
    WebDriverWait(driver, timeout=180).until(lambda d: d.find_element(By.CLASS_NAME, "TableInteractive-cellWrapper"))
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/a").click()
    WebDriverWait(driver, timeout=180).until(lambda d: d.find_element(By.CLASS_NAME, "text-white-hover"))
    driver.find_element(By.CLASS_NAME , "text-white-hover").click()
    sleep(600)

    # Gravar no log
    logger.info("SUCESSO - Extração dos dados do cliente finalizada com sucesso!")

except BaseException as err:
    fim = time.time()
    logger.info(f"ERRO - {err}")
    logger.info(f"ERRO - Tempo de execução do script: {(fim - inicio)}")

finally:
    driver.quit()


# Manipular o arquivo baixado de informações do cliente
try: 

    logger.info("INFO - Início da manipulação do arquivo!")

    cwd = os.getcwd()
    if os.path.exists(f"/home/{user}/dados_hubsoft") == False:
        os.makedirs(f"/home/{user}/dados_hubsoft")
    # passa o caminho onde está o arquivo query_result*
    arquivo = f"{path}/"+r"/query*.csv"
    # o glob.glob encontra o arquivo requerido pelo caminho
    subprocess.run(["mv", glob.glob(arquivo)[0], f"{path}/dados_totais.csv"])
    subprocess.run(["mv", f"{path}/dados_totais.csv", f"/home/{user}/dados_hubsoft/"])
    
    # Gravar no log
    logger.info("SUCESSO - Arquivo manipulado!")

except BaseException as err:
    fim = time.time()
    logger.info(f"ERRO - {err}")
    logger.info(f"ERRO - Tempo de execução do script: {(fim - inicio)}")
