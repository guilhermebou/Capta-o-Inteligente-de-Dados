import os
import pandas as pd
import logging
from datetime import datetime, timedelta

#config log
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
        print("\n" + "-"*50 + "\n")

        cpf_key = row['CPF'] if 'CPF' in row and pd.notnull(row['CPF']) else "CPF não informado"
        data_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registrar_log(cpf_key, mensagem, data_envio)

def checar_recorrencia_paciente(df):

    agrupado = df.groupby(['CPF', 'SOLICITANTE', 'CD_TUSS', 'DS_RECEITA']).size().reset_index(name='QUANTIDADE')
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



def main():
    csv_file = 'data/sample_estruturados_teste.csv'
    df = pd.read_csv(csv_file)

    csv_tuss_imagem = 'docs/TABELA_ANS_TUSS.csv'
    df_tuss_imagem = pd.read_csv(csv_tuss_imagem)

    # cruzamento TUSS
    df = df[df['CD_TUSS'].isin(df_tuss_imagem['TUSS'])]
    df.to_csv('data/output/output_estruturados.csv')


    print("=== Mensagem ===")
    enviar_mensagem(df)

    print("=== Recorrências por (CPF, SOLICITANTE, CD_TUSS) ===")
    df_recorrencia = checar_recorrencia_paciente(df)
    if df_recorrencia.empty:
        print("Nenhuma recorrência encontrada.")
    else:
        print(df_recorrencia)

    print("\n=== Exame mais solicitado em cada bimestre ===")
    df_sazonalidade = detectar_sazonalidade_bimestral(df)
    print(df_sazonalidade)

    print("\n=== Exames trimestre ===")
    df_exames = exames_por_trimestre(df)
    print(df_exames)

    #dados para uso no dashboard

    df_recorrencia.to_csv('data/output/recorrencia_paciente.csv', index=False)
    df_sazonalidade.to_csv('data/output/sazonalidade_bimestral.csv', index=False)
    df_exames.to_csv('data/output/contagem_trimestral.csv', index=False)

if __name__ == "__main__":
    main()
