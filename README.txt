Projeto BI Telecom

Resumo

	Neste projeto realizei o BI de uma empresa real de telecom a qual não explanarei por questões de proteção de dados.
	Neste projeto foi realizada a criação de um Data Warehouse do setor comercial da empresa.
	O projeto segue o seguinte fluxo: 
		1- Extração dos dados do banco de dados através de uma interface disponibilizada pelo proprietário do sistema.
		2- Limpeza e transformação dos dados, transformando valores nulos em valores padrões.
		3- Aplicação de transformações para adequar as regras de negócio.
		4- Carga no banco de dados dimensional em Star Schema, com SGBD PostgreSql
		5- Criação de Dashboards com informações pertinentes a empresa.

Tecnologias Utilizadas
	
	1- Linguagem de programação Python, com as seguintes bibliotecas:
		a) Pandas
		b) Selenium
		c) Loggin
		d) Psycopg2
	2- Banco de dados PostgreSql com modelagem dimensional
	3- Power BI
	4- Servidor CentOS

Solicitações da Empresa

	1- Total de vendas
		a) Por ano, semestre, trimestre, mês e dia
		b) Por cidade(bairro), vendedor, empresa, tipo de pessoa, origem do cliente.
	2- Total de Mudanças de planos (Upgrades e Downgrades)
		a) Por ano, semestre, trimestre, mês e dia
		b) Por cidade(bairro), vendedor, empresa, tipo de pessoa, origem do cliente.
	3- Total de Cancelamentos
		a) Por ano, semestre, trimestre, mês e dia
		b) Por cidade(bairro), vendedor, empresa, tipo de pessoa, origem do cliente.

Descrição do Projeto

	1- Modelagem Relacional

	Para realizar o projeto foi necessário primeiro realizar a modelagem relacional por engenharia reversa das tabelas necessárias para obter as informações solicitadas pela empresa. Esta modelagem pode ser verificada no arquivo modelagem_relacional.png ou modelagem_relacional.mdj.

	2- Extração dos Dados

	Após a modelagem dos dados foi desenvolvido um script Python com Selenium para extração dos dados direto na interface web que permitia acesso aos dados.
	Essa extração foi realizada através de uma automação que buscava os dados, inserindo na aplicação web um código SQL que retorna as linhas solicitadas ao SGBD.
	Para obter estes dados foi necessário exportá-los via CSV e salvar no servidor a qual a aplicação está hospedada.
	O código que realiza a extração está no arquivo 1_extrair.py

	3- Limpeza dos Dados

	A primeira limpeza dos dados está em substituir os dados missing por dados padrões para que os indicadores sejam mais precisos.
	A limpeza é realizada com a biblioteca Pandas do Python, que trabalha de forma colunar realizando o processo de limpeza de milhares de linhas em segundos.
	Neste ponto também foi realizada a conversão de apóstrofos em nomes, pois eles geram erros ao manipular em banco de dados.
	Foi realizada também a conversão de tipos de alguns dados e a transformação de datas para um padrão mais fácil de manipular.
	O código da limpeza pode ser verificado no arquivo 2_transformar_cliente.py

	4- Transformação dos Dados
	
	Essa etapa do processo foi a principal na aplicação das regras de negócio.
	Para se obter os dados com mais precisão, foi realizado o levantamento do historico dos dados e não apenas dos valores salvos atualmente no banco de dados.
	Com isso foi necessário desmembrar informações que estavam salvas em formato de texto nas tabelas de historico do cliente, permitindo a visualização dos dados na hora da venda e algumas alterações.
	Como algumas linhas tiveram duplicação por causa do select, após o desmembramento do historico em dados específicos, foi possível comparar e reduzir a quantidade de linhas da tabela exportada.
	Neste ponto se aplica as regras de negócio, dividindo e classificando o que é venda, o que é upgrade, downgrade e uma troca de titularidade.
	Neste ponto também aplicamos regras para verificação de valores, obtendo assim os valores reais no momento da venda, de uma mudança de plano ou na troca de titularidade.
	Devido a empresa utilizar pacotes, que agregam valores ao plano, é necessário, neste momento, verificar quais foram adicionados durante a venda e quais foram depois. Pois isso impacta no valor do plano na hora da venda. A verificação também impacta posteriormente nos valores durante a mundança ou troca de titularidade.
	Pode ser verificada esse processo no arquivo 3_transformar_preparar_carga.py
	
	5- Modelagem Dimensional
	
	Foi gerada uma modelagem dimensional Star Schema, onde a venda é a tabela fato venda (eventos durante o tempo) e como dimensões existem as tabelas: Cliente, Produto, Endereço e Tempo. Cada uma das tabelas dimensão possui características que definem a tabela fato.
	A modelagem pode ser verificada nos arquivos modelagem_dimensional.png e modelangem_dimensional.mdj

	6- Preparação para carga
	
	Após a limpeza, transformação e aplicação de regras de negócio, os dados foram separados em tabelas que representam cada dimensão e a tabela fato do Data Warehouse. Esses dados foram exportados em tabelas .csv prontas para serem carregadas no Data Warehouse.

	7- Tabela Dimensão Tempo

	Foi gerada também a tabela de tempo, que é responsável pelo controle dos dados de datas. Esta tabela foi gerada no Python com as bibliotecas Pandas, Datetime e Time e foi exportada via .csv.
	Pode ser visualizado seu código no arquivo 4_gerar_tempo.py

	8- Carga dos Dados

	Para realizar a carga dos dados foi utilizada a biblioteca Psycopg2 do Python, que faz conexão com banco de dados PostgreSql. 
	Foi criada uma função que carrega os dados no Banco de Dados. Esta função consegue carregar uma tabela inteira no SGBD em questão de segundos, pois não carrega linha por linha, Fazendo a carga de milhares de linhas em segundos.
	Sua codificação está no arquivo 5_carregar_dimensoes_fato.py

	9- Dashboards

	Após o SGBD Analítico alimentado, o PowerBI é conectado a ele, e pode ser gerada as visualizações.
	Neste projeto as visualizações foram divididas em 3 Dashboards: 
		- um que aborda vendas, mudanças de plano e trocas de titularidade diárias para acompanhamento de data até data; 
		- outro que aborda vendas, mudanças de plano e trocas de titularidade acumuladas por mes, trimestre, semestre e ano; 
		- e outro que aborda cancelamentos
	Todos os dashboards possuem filtros interativos, que mostram os dados conforme solicitado pela empresa.
	Os visuais podem ser verificados nas imagens: Visual1.edited.png, Visual2.edited.png, Visual3.edited.png
	Não foi colocado o arquivo do PowerBI devido a impossibilidade de acesso e por questões de proteção de dados. Logo foi inserida imagens de exemplificação dos Dashboads.

	10- Demais Considerações

	Durante o projeto foi usada a biblioteca Logging, que gera logs para acompanhamento do fluxo do sistema.
	Foi realizada também o desenvolvimento de um Shell Script que executa os scripts Python em ordem específica. Este arquivo é executado pelo agendador de tarefas do linux "Crontab".
	O sistema é executado todos os dias as 00:30 atualizando o Banco de Dados Analítico, e desta forma, os visuais também são atualizados diáriamente.
	Os comandos SLQ utilizados estão nos arquivos DDL_STAR_REMODELADO.sql e busca_dados_e_historico_cliente.sql
	
Conclusão

	O projeto levou cerca de 3 meses para ficar pronto com um desenvolvedor.
	Todos os passos do projeto foram realizados com apoio de pesquisas em sites como StackOverflow e outros forums. Também foi consultada a documentação das bibliotecas e ferramentas utilizadas.
	Este projeto permitiu que o desenvolvedor adquirisse conhecimento sobre o funcionamento de um projeto real em uma empresa em funcionamento e com mudanças de regras de negócio em um curto espaço de tempo, sobre a execução de um projeto do levantamento de requisitos até o deploy em produção, a qual foi necessário atentar-se a questões de segurança, criação e manutenção de acessos de usuários, configuração de servidor, configuração de acesso remoto via VNC, entre outros tópicos.
	
Agradecimentos

	Agradeço a empresa que permitiu o desenvolvimento do projeto e a todos que estiveram ao meu lado durante o desenvolvimento do projeto de modo ativo ou passivo. 
	



