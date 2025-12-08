from decision_tree import DecisionTree


class SignatureSchemeSelector:
    def __init__(self, csv_path):
        self.tree = DecisionTree(csv_path)

    def ask_yes_no(self, question):
        while True:
            response = input(f"\n{question}\n[y]es / [n]o / [?]don't know: ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            elif response in ['?', 'dk']:
                return None
            else:
                print("Please enter y, n, or ?")

    def ask_multiple_choice(self, question, options):
        print(f"\n{question}")
        for i, opt in enumerate(options, 1):
            print(f"  [{i}] {opt}")
        print(f"  [?] Don't know")

        while True:
            response = input("Your choice (number or ?): ").strip()
            if response == '?':
                return None
            try:
                idx = int(response) - 1
                if 0 <= idx < len(options):
                    return options[idx]
                print(f"Enter 1-{len(options)} or ?")
            except ValueError:
                print(f"Enter 1-{len(options)} or ?")

    def run_interview(self):
        """Run interactive interview"""
        print("\n" + "=" * 60)
        print("DIGITAL SIGNATURE SCHEME SELECTOR")
        print("=" * 60)
        print("\nAnswer questions about your needs...")

        self.tree.reset()

        # Q1: Signature Size
        sig_size = self.ask_yes_no("Do you need SHORT signatures?")
        if sig_size == True:
            self.tree.filter_by_signature_size("short")
            print("→ Filtering for short signatures...")
        elif sig_size == False:
            print("→ No restriction on signature size.")

        # Q2: Standardization
        standardized = self.ask_yes_no("Do you prefer STANDARDIZED schemes?")
        if standardized == True:
            self.tree.filter_by_standardization(True)
            print("→ Filtering for standardized schemes...")
        elif standardized == False:
            self.tree.filter_by_standardization(False)
            print("→ Looking for non-standard schemes...")

        # Q3: Construction Type (if multiple candidates remain)
        candidates = self.tree.get_remaining_candidates()
        if len(candidates) > 1:
            construction = self.ask_multiple_choice(
                "What construction type do you prefer?",
                ["Hash-and-Sign", "Fiat-Shamir Transform", "Number-Theoretic",
                 "Elliptic Curve", "Hash-Based Tree"]
            )
            if construction:
                self.tree.filter_by_construction_type(construction)
                print(f"→ Filtering for {construction}...")

        # Q4: Efficiency
        candidates = self.tree.get_remaining_candidates()
        if len(candidates) > 1:
            efficiency = self.ask_yes_no("Do you prioritize computational efficiency?")
            if efficiency == True:
                self.tree.filter_by_efficiency("fast")
                print("→ Filtering for efficient schemes...")

        # Get recommendation
        rec = self.tree.get_recommendation()
        candidates = self.tree.get_remaining_candidates()

        print("\n" + "=" * 60)
        if rec:
            print(f"✅ RECOMMENDATION: {rec}")
            print(f"Alternatives: {', '.join(candidates)}")

            # Show details
            details = self.get_scheme_details(rec)
            if details:
                print(f"\nDetails about {rec}:")
                print(f"  • Security: {details['Security Assumption']}")
                print(f"  • Sig Size: {details['Signature Size (bits)']} bits")
                print(f"  • Standardized: {details['Standardized']}")
                print(f"  • Construction: {details['Construction Type']}")
                print(f"  • Complexity: {details['Complexity Category']}")
        else:
            print("❌ No matching schemes found.")
        print("=" * 60)

        return rec

    def get_scheme_details(self, scheme_name):
        """Get full scheme details"""
        for scheme in self.tree.schemes:
            if scheme['Scheme Name'] == scheme_name:
                return scheme
        return None

    def run_loop(self):
        """Run in loop for multiple tries"""
        while True:
            self.run_interview()
            again = input("\n\nTry another selection? [y]es / [n]o: ").lower().strip()
            if again != 'y':
                print("\n👋 Thank you!\n")
                break


if __name__ == "__main__":
    CSV_PATH = "../data/signature_schemes.csv"
    selector = SignatureSchemeSelector(CSV_PATH)
    selector.run_loop()
