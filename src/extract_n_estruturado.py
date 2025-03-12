import pandas as pd
import re
import time

start_time = time.time()

keywords = {
    "rx": r"(?i)\b(?:rx|raio[\s-]*x)\b",
    "hemograma": r"(?i)\b(?:hemograma|hemog(?:rama)?|hmg)\b",
    "ressonancia": r"(?i)\b(?:resson[âa]ncia(?:\s+magn[ée]tica)?|rm)\b",
    "tomografia": r"(?i)\b(?:tomografia[\s-]+computadorizada|tc)\b",
    "ultrasonografia": r"(?i)\b(?:ultra-?s{1,2}onografia|usg)\b",
    "doppler": r"(?i)\b(?:doppler|doppl[ée]r)\b"
}

def extract_keyword(text):
    if not isinstance(text, str):
        return ""
    for key, pattern in keywords.items():
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return ""

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)


    #df = df[df['CD_RECEITA'].isin(df_tuss_imagem['DESCRICAO'].apply(extract_keyword))]
    #apos a normalização cruzar com codigo tuss

    df["Solicitação"] = df["DS_RECEITA"].apply(extract_keyword)
    df = df[df["Solicitação"] != ""]

    return df

end_time = time.time()
elapsed_seconds = end_time - start_time
elapsed_minutes = elapsed_seconds / 60.0

print(f"Tempo total de execução: {elapsed_minutes:.2f} minutos.")
