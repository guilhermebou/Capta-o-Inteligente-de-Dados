import time  # Para medir o tempo
import google.generativeai as genai
import pandas as pd
import json
import re


API_KEY = ""


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-8b')


df = pd.read_csv('resultado_parcial2.csv', encoding='utf-8')


df['medicamento'] = None
df['dosagem'] = None
df['periodo'] = None

#teste 50linhas
df_test = df.head(20).copy()


start_time = time.time()


def extract_info(texto_receita: str) -> dict:

    prompt = f"""
Você é um extrator de dados altamente preciso e detalhista.
Sua tarefa é analisar o texto da receita e extrair,
sem omitir ou truncar nenhum detalhe,
as informações completas sobre o medicamento,
sua dosagem e o período da dosagem.
Responda estritamente em JSON, sem nenhum texto adicional.

Receita: "{texto_receita}"

Retorne um objeto JSON no formato:
{{
  "medicamento": "string ou null",
  "dosagem": "string ou null",
  "periodo": "string ou null"
}}

Se alguma informação não estiver presente, retorne null para esse campo. """
    response = model.generate_content(prompt)
    resposta_texto = response.text.strip()

    # Impressão para diagnóstico (opcional)
    # print(f"Resposta do modelo:\n{resposta_texto}\n{'-'*50}")

    # isolar JSON com regex
    match = re.search(r'(\{.*\})', resposta_texto, flags=re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            dados_extraidos = json.loads(json_str)
        except json.JSONDecodeError:
            dados_extraidos = {
                "medicamento": None,
                "dosagem": None,
                "periodo": None
            }
    else:

        dados_extraidos = {
            "medicamento": None,
            "dosagem": None,
            "periodo": None
        }

    return dados_extraidos


for index, row in df_test.iterrows():
    texto_receita = row['DS_RECEITA']
    print(f"Processando linha {index}...")

    try:
        # ANALISE 1
        dados_extraidos_1 = extract_info(texto_receita)

        medicamento = dados_extraidos_1.get('medicamento')
        dosagem = dados_extraidos_1.get('dosagem')
        periodo = dados_extraidos_1.get('periodo')

        # extracao foi nula
        if not medicamento and not dosagem and not periodo:
            print("Campos nulos na primeira análise. Tentando segunda análise...")
            # ANALISE2
            dados_extraidos_2 = extract_info(texto_receita)
            medicamento = dados_extraidos_2.get('medicamento')
            dosagem = dados_extraidos_2.get('dosagem')
            periodo = dados_extraidos_2.get('periodo')

        # att colunas do DF
        df_test.at[index, 'medicamento'] = medicamento
        df_test.at[index, 'dosagem'] = dosagem
        df_test.at[index, 'periodo'] = periodo

    except Exception as e:
        print(f"Erro na chamada ou processamento da linha {index}: {e}")


end_time = time.time()
elapsed_seconds = end_time - start_time
elapsed_minutes = elapsed_seconds / 60.0


print("\n--- DF Teste (primeiras 50 linhas) ---")
print(df_test)


df_test.to_csv('data/output/resultado_parcial_gemini.csv', index=False, encoding='utf-8')
print("\nProcessamento finalizado.")


print(f"Tempo total de execução: {elapsed_minutes:.2f} minutos.")
