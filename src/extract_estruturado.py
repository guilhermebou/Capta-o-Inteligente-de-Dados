import pandas as pd
from datetime import datetime, timedelta


def gerar_mensagem(solicitante, cpf, cd_tuss, ds_receita, data):
    """
    Gera mensagem com parte do CPF formatado e dados sobre o exame.
    Ajuste conforme necessidade de exibição do CPF.
    """
    if pd.notnull(cpf):
        cpf_str = str(int(cpf))  # int() remove casas decimais caso venha como float
        cpf_str = cpf_str[-5:]
        cpf_formatado = cpf_str[:3] + '-' + cpf_str[3:]
        cpf_exibicao = f"xxx.xxx.{cpf_formatado}"
    else:
        cpf_exibicao = "CPF não informado"

    mensagem = (
        f"Olá {solicitante}!\n"
        f"Portador do CPF {cpf_exibicao}\n"
        f"Somos do Hospital X, estamos entrando em contato para lhe informar sobre o seu exame {cd_tuss} "
        f"(receita: {ds_receita}) realizado na data {data}."
        #implementação de um chatbot para dar dicas sobre cuidados e etc
        #(com uma base de dados legitima para treinamento da IA)
    )
    return mensagem

def verificar_exames_no_mesmo_dia(df):
    """
    Verifica para cada linha (exame) se o dia do exame (DATA) é o dia atual.
    Caso seja o mesmo dia, gera e imprime a mensagem.
    """
    data_hoje = datetime.today().date()  # Apenas a parte de data (sem horário)

    for _, row in df.iterrows():
        data_exame = datetime.strptime(row['DATA'], '%Y-%m-%d').date()

        # Se o dia do exame for igual ao dia de hoje, já envia a mensagem
        if data_exame == data_hoje:
            mensagem = gerar_mensagem(
                row['SOLICITANTE'],
                row['CPF'] if 'CPF' in row else None,
                row['CD_TUSS'],
                row['DS_RECEITA'],
                row['DATA']
            )
            print(mensagem)
            print("\n" + "-"*50 + "\n")


def checar_recorrencia_paciente(df):
    """
    Verifica se a mesma pessoa (CPF) fez o mesmo exame (CD_TUSS) mais de uma vez.
    Também mantém o nome (SOLICITANTE) no resultado.
    Retorna um DataFrame com as recorrências (contagem > 1).
    """
    agrupado = df.groupby(['CPF', 'SOLICITANTE', 'CD_TUSS', 'DS_RECEITA']).size().reset_index(name='QUANTIDADE')
    recorrentes = agrupado[agrupado['QUANTIDADE'] > 1]
    return recorrentes

def detectar_sazonalidade_bimestral(df):
    """
    Detecta sazonalidade dos exames, dividindo o ano em bimestres (1 a 6).
    Retorna um DataFrame com o exame mais solicitado em cada bimestre.
    """
    df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d', errors='coerce')
    df['BIMESTRE'] = ((df['DATA'].dt.month - 1) // 2) + 1

    agrupado = df.groupby(['BIMESTRE', 'CD_TUSS']).size().reset_index(name='CONTAGEM')
    exames_mais_solicitados = (
        agrupado
        .sort_values(['BIMESTRE', 'CONTAGEM'], ascending=[True, False])
        .groupby('BIMESTRE')
        .head(1)
        .reset_index(drop=True)
    )
    return exames_mais_solicitados

def main():

    csv_file = 'data/sample_estruturados.csv'
    df = pd.read_csv(csv_file)

    csv_tuss_imagem = 'docs/TABELA_ANS_TUSS.csv'
    df_tuss_imagem = pd.read_csv(csv_tuss_imagem)

    # cruzamento de codigos TUSS
    df = df[df['CD_TUSS'].isin(df_tuss_imagem['TUSS'])]


    print("=== Mensagem ===")
    verificar_exames_no_mesmo_dia(df)


    print("=== Recorrências por (CPF, SOLICITANTE, CD_TUSS) ===")
    recorrentes = checar_recorrencia_paciente(df)
    if recorrentes.empty:
        print("Nenhuma recorrência encontrada.")
    else:
        print(recorrentes)

    # levantamento bimestral de exames de imagem
    print("\n=== Exame mais solicitado em cada bimestre ===")
    sazonalidade = detectar_sazonalidade_bimestral(df)
    print(sazonalidade)

if __name__ == "__main__":
    main()
