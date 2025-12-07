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

    def filter_by_standardization(self, wants_std: bool):
        filtered = []
        for s in self.current_candidates:
            is_std = s["Standardized"].strip().lower() == "yes"
            if wants_std == is_std:
                filtered.append(s)
        self.current_candidates = filtered


    def filter_by_construction_type(self, ctype: str):
        filtered = []
        for s in self.current_candidates:
            if ctype.lower() in s["Construction Type"].lower():
                filtered.append(s)
        self.current_candidates = filtered


    def filter_by_efficiency(self, level: str):
        # level is fast, normal or any
        filtered = []
        for s in self.current_candidates:
            complexity = s["Complexity Category"]

            if level == "fast" and complexity in ["Low"]:
                filtered.append(s)
            elif level == "normal" and complexity in ["Low", "Medium"]:
                filtered.append(s)
            elif level == "any":
                filtered.append(s)

        self.current_candidates = filtered

    def get_recommendation(self):
        if not self.current_candidates:
            return None
        if len(self.current_candidates) == 1:
            return self.current_candidates[0]["Scheme Name"]

        # Priority: pick by Complexity Category (Low > Medium > High)
        # Then by Standardized (Yes > No)
        # Then by smallest signature size

        def score(scheme):
            complexity_score = ["Low", "Medium", "High"].index(scheme["Complexity Category"])
            standardized_score = 0 if scheme["Standardized"].lower() == "yes" else 1
            sig_size = int(scheme["Signature Size (bits)"].split("-")[1])  # max size
            return (complexity_score, standardized_score, sig_size)

        return sorted(self.current_candidates, key=score)[0]["Scheme Name"]

    def get_remaining_candidates(self):
        return [s["Scheme Name"] for s in self.current_candidates]

