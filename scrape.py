import pandas as pd
import re
from bs4 import BeautifulSoup


paths = {
    "Enron": "phishing_datasets/Enron.csv",
    "Ling": "phishing_datasets/Ling.csv",
    "SpamAssasin": "phishing_datasets/SpamAssasin.csv",
    "CEAS_08": "phishing_datasets/CEAS_08.csv",
    "Nazario": "phishing_datasets/Nazario.csv"
}

#email cleaning function 
def clean_email_text(text):
    if pd.isnull(text):
        return ""
    soup = BeautifulSoup(text, "html.parser")
    for tag in soup.find_all(True):
        if tag.name not in ["a", "img"]:
            tag.unwrap()
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r'[^\w\s<>:/.\-@"]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


processed_dfs = []

# Process Enron and Ling
for name in ["Enron", "Ling"]:
    df = pd.read_csv(paths[name])
    df = df[["subject", "body", "label"]].dropna()
    df["Email"] = "SUBJECT: " + df["subject"] + " EMAIL: " + df["body"]
    df["Class"] = df["label"].apply(lambda x: "Phishing" if x == 1 else "Legit")
    df["Email"] = df["Email"].apply(clean_email_text)
    processed_dfs.append(df[["Email", "Class"]])

# Process SpamAssassin
df = pd.read_csv(paths["SpamAssasin"])
if {"sender", "subject", "body", "label"}.issubset(df.columns):
    df = df[["sender", "subject", "body", "label"]].dropna()
    df["Email"] = "FROM: " + df["sender"] + " SUBJECT: " + df["subject"] + " EMAIL: " + df["body"]
    df["Class"] = df["label"].apply(lambda x: "Phishing" if x == 1 else "Legit")
    df["Email"] = df["Email"].apply(clean_email_text)
    processed_dfs.append(df[["Email", "Class"]])

# process CEAS_08
df = pd.read_csv(paths["CEAS_08"])
if {"subject", "body", "label"}.issubset(df.columns):
    df = df[["subject", "body", "label"]].dropna()
    df["Email"] = "SUBJECT: " + df["subject"] + " EMAIL: " + df["body"]
    df["Class"] = df["label"].apply(lambda x: "Phishing" if x == 1 else "Legit")
    df["Email"] = df["Email"].apply(clean_email_text)
    processed_dfs.append(df[["Email", "Class"]])

# process Nazario ( all are phising emails)
df = pd.read_csv(paths["Nazario"], names=["Email"])
df["Class"] = "Phishing"
df["Email"] = df["Email"].apply(clean_email_text)
df = df[df["Email"].str.len().between(300, 3000)]
processed_dfs.append(df[["Email", "Class"]])

#Combine and save final dataset 
combined_df = pd.concat(processed_dfs, ignore_index=True)
combined_df.drop_duplicates(subset=["Email"], inplace=True)
combined_df = combined_df[combined_df["Email"].str.len().between(300, 3000)]
combined_df.to_csv("cleaned_phishing_dataset.csv", index=False)

print(f" Saved cleaned_phishing_dataset.csv with {len(combined_df)} emails.")



