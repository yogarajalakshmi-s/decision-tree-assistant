from decision_tree import DecisionTree
import json
from datetime import datetime

class UserProfile:
    def __init__(self, name, prefs, expected):
        self.name = name
        self.prefs = prefs
        self.expected = expected


class Evaluator:
    TEST_PROFILES = [
        UserProfile(
            "efficiency_focused",
            prefs={"signature_size": "short"},
            expected="Lamport + Merkle Tree"
        ),
        UserProfile(
            "hash_based",
            prefs={"security": "Hash"},
            expected="Lamport + Merkle Tree"
        ),
        UserProfile(
            "standardization",
            prefs={"standardized": True},
            expected="DSA"
        ),
        UserProfile(
            "fiat_shamir",
            prefs={"construction": "Fiat-Shamir Transform"},
            expected="Schnorr Signatures"
        ),
    ]

    def __init__(self, csv_path):
        self.tree = DecisionTree(csv_path)
        self.results = []

    def simulate(self, profile: UserProfile):
        self.tree.reset()

        prefs = profile.prefs

        # Apply filters
        if "signature_size" in prefs:
            self.tree.filter_by_signature_size(prefs["signature_size"])

        if "security" in prefs:
            self.tree.filter_by_security_assumption(prefs["security"])

        if "standardized" in prefs:
            self.tree.filter_by_standardization(prefs["standardized"])

        if "construction" in prefs:
            self.tree.filter_by_construction_type(prefs["construction"])

        rec = self.tree.get_recommendation()
        return {
            "profile": profile.name,
            "expected": profile.expected,
            "actual": rec,
            "correct": (rec == profile.expected)
        }

    def run(self):
        correct = 0
        out = []

        for p in self.TEST_PROFILES:
            r = self.simulate(p)
            out.append(r)
            if r["correct"]:
                correct += 1

        score = correct / len(self.TEST_PROFILES)
        return out, score

    def write_text_report(self, path="report.txt"):
        lines = []
        lines.append("Digital Signature Decision Tree - Evaluation Report\n")
        lines.append(f"Generated: {datetime.now()}\n")
        lines.append("=" * 60 + "\n")

        results, score = self.run()

        for r in results:
            lines.append(f"Profile: {r['profile']}\n")
            lines.append(f"Expected: {r['expected']}\n")
            lines.append(f"Actual: {r['actual']}\n")
            lines.append(f"Correct: {r['correct']}\n")
            lines.append("\n")

        lines.append(f"Success Probability: {score:.2%}\n")

        with open(path, "w") as f:
            f.writelines(lines)

    def write_json_report(self, path="report.json"):
        results, score = self.run()
        data = {
            "timestamp": datetime.now().isoformat(),
            "success_probability": score,
            "results": results
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    CSV_PATH = "../data/signature_schemes.csv"

    evaluator = Evaluator(CSV_PATH)
    results, score = evaluator.run()

    # Print detailed results to console
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    for r in results:
        print(f"\nProfile: {r['profile']}")
        print(f"Expected: {r['expected']}")
        print(f"Actual: {r['actual']}")
        print(f"Correct: {'YES' if r['correct'] else 'NO'}")

    print("\n" + "=" * 60)
    print(f"Success Probability: {score:.2%}")
    print("=" * 60 + "\n")

    # Also save to files
    evaluator.write_text_report()
    evaluator.write_json_report()
