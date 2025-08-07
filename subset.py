import pandas as pd
import random
import argparse
import pathlib

class Subset_Maker():
    """
    Object that encapsulates subset creation of a given csv
    """
    def __init__(self, csv):
        """
        Initializes a new Subset_Maker instance.

        Args:
            csv (str): Path to CSV file to make a subset of.
        """
        self.base_df = pd.read_csv(csv)
        self.base_legit = self.base_df[self.base_df['Class'] == 'Legit']
        self.base_phishing = self.base_df[self.base_df['Class'] == 'Phishing']
        self.subset = pd.DataFrame()

    def Generate_Subset(self, size):
        """
        Generates a new random subset of a specified size from the stored CSV file.

        Args:
            size (int): Number of rows in the new subset.
        """
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

# Example usage:
# read from cleaned_phishing_dataset.csv and derive a subset of size 300
# python subset.py --input cleaned_phishing_dataset.csv --size 300

if __name__ == "__main__":
    main()