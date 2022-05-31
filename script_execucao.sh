#!/bin/bash

cd /home/welden/Documentos/NVC_Projeto/comercial.prod

python3 1_extrair.py
python3 2_transformar_cliente.py
python3 3_transformar_preparar_carga.py
python3 4_gerar_tempo.py
python3 5_carregar_dimensoes_fato.py