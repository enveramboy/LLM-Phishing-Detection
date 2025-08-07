import pandas as pd
import random
import argparse
import pathlib

class Subset_Maker():
    """
    Object that encapsulates subset creation of a given csv
    """
    def __init__(self, csv):
        self.base_df = pd.read_csv(csv)
        self.base_legit = self.base_df[self.base_df['Class'] == 'Legit']
        self.base_phishing = self.base_df[self.base_df['Class'] == 'Phishing']
        self.subset = pd.DataFrame()
    # def Generate_Subset(self, size):
    #     legit_pool = self.base_legit.copy()
    #     phishing_pool = self.base_phishing.copy()
    #     for i in range(int(int(size)/2)):
    #         sample_idx = random.randint(0, len(legit_pool)-1)
    #         print(f"Sample Index: {sample_idx}")
    #         self.subset._append(legit_pool.iloc[sample_idx], ignore_index=True)
    #         legit_pool = legit_pool.drop(sample_idx, axis='index')
            
    #         sample_idx = random.randint(0, len(phishing_pool)-1)
    #         self.subset._append(phishing_pool.iloc[sample_idx], ignore_index=True)
    #         phishing_pool = phishing_pool.drop(sample_idx, axis='index')
    #     self.subset.to_csv(f"cleaned_phishing_subset_{size}.csv", index=False)   
    def Generate_Subset(self, size):
        data = []
        data.append(self.base_legit.sample(n=int(int(size)/2), random_state=1))
        data.append(self.base_phishing.sample(n=int(int(size)/2), random_state=1))
        self.subset = pd.concat(data, ignore_index=True)
        self.subset.to_csv(f"cleaned_phishing_subset_{size}.csv", index=False) 

def main() -> None:
    parser = argparse.ArgumentParser(description="Derive subset of a provided CSV.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV.")
    parser.add_argument("--size", required=True, help="Subset size")
    args = parser.parse_args()

    subset_maker = Subset_Maker(pathlib.Path(args.input))
    subset_maker.Generate_Subset(args.size)

if __name__ == "__main__":
    main()