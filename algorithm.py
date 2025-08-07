import argparse
import json
import pathlib
import sys
from datetime import datetime
from typing import Dict, Any

import pandas as pd
from ollama import Client  # pip install ollama

PROMPT_TEMPLATE = """
You are a cybersecurity expert specialized in detecting and analyzing phishing emails.
Analyze the provided email (subject, body, sender, links) and decide if it is phishing or legitimate.
Return ONLY a JSON object with the following fields and their values for this email:

{
  "Is_Phishing": true or false,
  "Risk": "High", "Medium", or "Low",
  "Social_Engineering_Elements": [list of strings],
  "Actions": [list of recommended actions],
  "Reason": "A brief reason why this email is phishing or not."
}

Do NOT include type information, descriptions, or any extra text. Only output the result JSON object.
"""

def build_prompt(email_text: str) -> str:
    return f"{PROMPT_TEMPLATE}\n\nEMAIL:\n{email_text.strip()}"

def query_ollama(client: Client, model: str, prompt: str, max_retries: int = 3) -> Dict[str, Any]:
    response = client.generate(
        model=model,
        prompt=prompt,
        format="json",
        stream=False,
    )
    raw = response.get("response", "")
    return json.loads(raw)

def main() -> None:
    parser = argparse.ArgumentParser(description="Run emails through Ollama LLM and save output.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV.")
    parser.add_argument("--output", required=False, default=None, help="Path for output CSV.")
    parser.add_argument("--batch", type=int, default=5, help="Number of emails to process (0 for all).")
    parser.add_argument("--model", default="llama3.2", help="Model name for Ollama.")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)
    df = pd.read_csv(input_path)

    if args.batch > 0:
        df = df.head(args.batch)

    client = Client(host="http://localhost:11434")

    new_cols = ["Is_Phishing", "Risk", "Social_Engineering_Elements", "Actions", "Reason"]
    for col in new_cols:
        df[col] = None

    print(f"Processing {len(df)} emails with model '{args.model}' ...")
    for idx, row in df.iterrows():
        email_text = str(row["Email"])
        prompt = build_prompt(email_text)
        parsed_json = query_ollama(client, args.model, prompt)
        for key in new_cols:
            df.at[idx, key] = parsed_json.get(key)
        print(f"Email {idx + 1}/{len(df)} processed")

    output_path = (
        pathlib.Path(args.output)
        if args.output
        else input_path.with_name(f"{input_path.stem}_LLM_{datetime.now():%Y%m%d_%H%M%S}.csv")
    )

    df.to_csv(output_path, index=False)
    print(f"Done, Output saved to: {output_path.resolve()}")

# Example usage:
#read from the cleaned dataset, output the the specified file. only process the first 5 emails. use the designated model.
# python algorithm.py --input cleaned_phishing_dataset.csv --output llm_phishing_output.csv --batch 5 --model llama3.2
#same as above, but process all emails + use default naming and model(Ollama 3.2)
# python algorithm.py --input cleaned_phishing_dataset.csv --batch 0

if __name__ == "__main__":
    main()
