import dash
from dash import dash_table, html
import pandas as pd

#dados exportados
df_recorrencia = pd.read_csv('data/output/recorrencia_paciente.csv')
df_sazonalidade = pd.read_csv('data/output/sazonalidade_bimestral.csv')
df_exames = pd.read_csv('data/output/contagem_trimestral.csv')

app = dash.Dash(__name__)
app.title = "Dashboard de Exames"

app.layout = html.Div([
    html.H1("Dashboard de Exames", style={'textAlign': 'center'}),

    html.H2("Recorrência de Pacientes"),
    dash_table.DataTable(
        id='table-recorrencia',
        columns=[{"name": col, "id": col} for col in df_recorrencia.columns],
        data=df_recorrencia.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'}
    ),

    html.H2("Sazonalidade Bimestral dos Exames"),
    dash_table.DataTable(
        id='table-sazonalidade',
        columns=[{"name": col, "id": col} for col in df_sazonalidade.columns],
        data=df_sazonalidade.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'}
    ),

    html.H2("Quantidade de Exames Trimestral"),
    dash_table.DataTable(
        id='table-exames',
        columns=[{"name": col, "id": col} for col in df_exames.columns],
        data=df_exames.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'}
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
