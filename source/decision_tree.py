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

    def filter_by_signature_size(self, pref: str):
        filtered = []
        for s in self.current_candidates:
            raw = s["Signature Size (bits)"]
            parts = [int(x) for x in raw.replace("-", ",").split(",")]
            avg = (min(parts) + max(parts)) // 2

            if pref == "short" and avg <= 512:
                filtered.append(s)
            elif pref == "medium" and 512 < avg <= 2048:
                filtered.append(s)
            elif pref == "long" and avg > 2048:
                filtered.append(s)

        self.current_candidates = filtered


    def filter_by_security_assumption(self, assumption: str):
        filtered = []
        for s in self.current_candidates:
            if assumption.lower() in s["Security Assumption"].lower():
                filtered.append(s)

        self.current_candidates = filtered
