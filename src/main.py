from flask import Flask, jsonify
import pandas as pd
from database import get_db
from extract_estruturado import enviar_mensagem, checar_recorrencia_paciente, detectar_sazonalidade_bimestral, exames_por_trimestre
import extract_n_estruturado
import extract_gemini

app = Flask(__name__)


@app.route('/')
def index():
    return "RUN API "


@app.route('/sample_estruturado')
def processar():

    db = next(get_db())

    result = db.execute("SELECT * FROM sample_estruturados_teste")
    rows = result.fetchall()
    columns = result.keys()
    df_sample = pd.DataFrame(rows, columns=columns)

    df_tuss_imagem = pd.read_csv('docs/TABELA_ANS_TUSS.csv')

    df = df_sample[df_sample['CD_TUSS'].isin(df_tuss_imagem['TUSS'])]
    df.to_csv('data/output/output_estruturados.csv', index=False)

    enviar_mensagem(df)
    recorrencia = checar_recorrencia_paciente(df)
    sazonalidade = detectar_sazonalidade_bimestral(df)
    exames_trimestre = exames_por_trimestre(df)


    #dados para uso no dashboard
    recorrencia.to_csv('data/output/recorrencia_paciente.csv', index=False)
    sazonalidade.to_csv('data/output/sazonalidade_bimestral.csv', index=False)
    exames_trimestre.to_csv('data/output/contagem_trimestral.csv', index=False)


@app.route('/sample_n_estruturado')
def processar():

    db = next(get_db())

    result = db.execute("SELECT * FROM sample_nao_estruturados")
    rows = result.fetchall()
    columns = result.keys()
    df = pd.DataFrame(rows, columns=columns)

    df = extract_n_estruturado.process_csv(df)
    df.to_csv('data/output/sample_nao_estruturados_solicitacoes.csv', index=False)


if __name__ == '__main__':
    app.run(debug=True)
