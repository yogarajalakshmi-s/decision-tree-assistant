import csv

class DecisionTree:
    # Loads signature schemes and stores them.

    def __init__(self, csv_filepath: str):
        self.schemes = []
        self.current_candidates = []
        self._load_schemes(csv_filepath)

    def _load_schemes(self, csv_filepath: str):
        with open(csv_filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.schemes.append(row)

        self.current_candidates = self.schemes.copy()
        print(f"Loaded {len(self.schemes)} schemes.")

    def reset(self):
        self.current_candidates = self.schemes.copy()
