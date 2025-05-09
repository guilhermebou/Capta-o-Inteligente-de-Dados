import os
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    filename='logs/mensagens.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def registrar_log(cpf, mensagem, data_envio):
    logging.info(f"CPF: {cpf} - Mensagem: {mensagem.strip()} - Data de envio: {data_envio}")

def gerar_mensagem(solicitante, cpf, cd_tuss, ds_receita, data):
    if pd.notnull(cpf):
        cpf_str = str(int(cpf))
        cpf_str = cpf_str[-5:]
        cpf_formatado = cpf_str[:3] + '-' + cpf_str[3:]
        cpf_exibicao = f"xxx.xxx.{cpf_formatado}"
    else:
        cpf_exibicao = "CPF não informado"

    mensagem = (
        f"Olá {solicitante}!\n"
        f"Portador do CPF {cpf_exibicao}\n"
        f"Somos do Hospital X, estamos entrando em contato para o registro do seu exame TUSS {cd_tuss} - "
        f"{ds_receita}) realizado na data {data}."
        # implementação de um chatbot para dar dicas sobre cuidados e etc
        # (com uma base de dados legítima para treinamento da IA)
    )
    return mensagem

def enviar_mensagem(df):
    for _, row in df.iterrows():
        mensagem = gerar_mensagem(
            row['SOLICITANTE'],
            row['CPF'] if 'CPF' in row else None,
            row['CD_TUSS'],
            row['DS_RECEITA'],
            row['DATA']
        )
        print(mensagem)
        print("\n" + "-" * 50 + "\n")

        cpf_key = row['CPF'] if 'CPF' in row and pd.notnull(row['CPF']) else "CPF não informado"
        data_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registrar_log(cpf_key, mensagem, data_envio)

def checar_recorrencia_paciente(df):
    agrupado = df.groupby(['CPF', 'SOLICITANTE', 'TEL', 'CD_TUSS', 'DS_RECEITA']).size().reset_index(name='QUANTIDADE')
    recorrentes = agrupado[agrupado['QUANTIDADE'] > 1]
    return recorrentes

def detectar_sazonalidade_bimestral(df):
    df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d', errors='coerce')
    df['BIMESTRE'] = ((df['DATA'].dt.month - 1) // 2) + 1

    agrupado = df.groupby(['BIMESTRE', 'CD_TUSS', 'DS_RECEITA']).size().reset_index(name='CONTAGEM')
    exames_mais_solicitados = (
        agrupado
        .sort_values(['BIMESTRE', 'CONTAGEM'], ascending=[True, False])
        .groupby('BIMESTRE')
        .head(1)
        .reset_index(drop=True)
    )
    return exames_mais_solicitados

def exames_por_trimestre(df):
    df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d', errors='coerce')

    #calcula o trimestre pela data
    df['TRIMESTRE'] = df['DATA'].dt.quarter
    contagem_trimestre = df.groupby('TRIMESTRE').size().reset_index(name='CONTAGEM')
    return contagem_trimestre
