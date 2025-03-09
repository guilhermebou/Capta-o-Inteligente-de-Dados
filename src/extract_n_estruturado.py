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

    df["Solicitação"] = df["DS_RECEITA"].apply(extract_keyword)

    df.to_csv(output_file, index=False)
    print(f"Arquivo processado e salvo em {output_file}")

input_csv = "data/sample_nao_estruturados.csv"
output_csv = "data/output/sample_nao_estruturados_solicitacoes.csv"
process_csv(input_csv, output_csv)

end_time = time.time()
elapsed_seconds = end_time - start_time
elapsed_minutes = elapsed_seconds / 60.0

print(f"Tempo total de execução: {elapsed_minutes:.2f} minutos.")
