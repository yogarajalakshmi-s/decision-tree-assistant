from decision_tree import DecisionTree

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
            expected="ECDSA"
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
            prefs={"construction": "Fiat-Shamir"},
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
