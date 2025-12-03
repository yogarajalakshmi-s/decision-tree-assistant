# Decision Tree Assistant for Selecting Digital Signature Scheme [Project 2.6]
## Overview

This project implements a decision tree-based assistant that helps non-expert users select an appropriate digital signature scheme for their needs. The system uses a rule-based filtering approach to narrow down choices based on user preferences and constraints.

**Project Type:** 2.6 - Selecting Schemes for a Given Cryptography Primitive  
**Cryptographic Primitive:** Digital Signatures  
**Team:** Signed and Delivered (Member: Yoga Sathyanarayanan)

---

## Project Structure

```
signature_schemes_project/
├── signature_schemes.csv          # Implementation usage table (5 schemes, 10 columns)
├── decision_tree.py               # Core decision tree logic and filtering rules
├── cli_interface.py               # Interactive command-line interface for users
├── evaluator.py                   # Testing framework and evaluation metrics
├── README.md                      # This file
└── test_results.txt              # Generated evaluation report
```

---

## Key Features

### 1. Implementation Usage Table (`signature_schemes.csv`)

Contains 5 digital signature schemes with 10 properties each:

**Schemes Included:**
- Hashed RSA (RSA-FDH)
- Schnorr Signatures
- DSA (Digital Signature Algorithm)
- ECDSA (Elliptic Curve DSA)
- Lamport + Merkle Tree (Hash-based)

**Properties/Columns:**
1. **Scheme Name** - Identifier
2. **Security Assumption** - What hard problem it's based on
3. **Signing Complexity** - Computational cost to sign
4. **Verification Complexity** - Computational cost to verify
5. **Key Size (bits)** - Size of cryptographic keys
6. **Signature Size (bits)** - Size of generated signatures
7. **One-Time Only** - Whether scheme supports multiple signatures
8. **Standardized** - Whether it's officially standardized
9. **Construction Type** - How the scheme is built (NEW - added column)
10. **Complexity Category** - Relative complexity level (NEW - added column)
11. **Hardware Optimized** - Whether it supports hardware acceleration

**New Columns Added (Beyond Lecture Materials):**
- **Complexity Category:** Categorizes schemes as Low/Medium complexity
- **Hardware Optimized:** Indicates which schemes support hardware optimization

### 2. Decision Tree (`decision_tree.py`)

A rule-based filtering system that narrows down scheme options:

**Filtering Methods:**
- `filter_by_signature_size()` - Short (≤512 bits) vs medium vs long
- `filter_by_security_assumption()` - RSA, Discrete Log, Elliptic Curve, Hash
- `filter_by_standardization()` - Standardized schemes only
- `filter_by_construction_type()` - Hash-and-Sign, Fiat-Shamir, Number-Theoretic, etc.
- `filter_by_efficiency()` - Fast, standard, or unconstrained
- `filter_by_hardware_optimization()` - Hardware-optimized schemes

**How It Works:**
1. Load all 5 schemes as candidates
2. Ask users questions about their preferences
3. Apply corresponding filters to eliminate incompatible schemes
4. Return recommendation when candidates narrow sufficiently

**Key Design Decision:**
Uses *rule-based* filtering rather than ML because the goal is clarity for non-experts. Each filter directly corresponds to a table property.

### 3. Interactive CLI Interface (`cli_interface.py`)

A user-friendly command-line program that guides non-experts through scheme selection:

**Features:**
- Adaptive questioning (questions change based on remaining candidates)
- Multiple question formats: yes/no, multiple-choice
- "Don't know" option for uncertain answers
- Clear explanations of recommendations
- Detailed scheme information display
- Option to restart and try again

**Question Flow:**
1. **Q1: Signature Size** - "Do you need SHORT signatures?"
2. **Q2: Standardization** - "Do you want a STANDARDIZED scheme?"
3. **Q3: Construction Type** - "What construction type interests you?"
4. **Q4: Efficiency** - "How important is computational efficiency?"

**Adaptive Behavior:**
- Questions adjust based on remaining candidates
- Skips questions if only few schemes remain
- Gracefully handles "don't know" responses
- Resets filters if no schemes match to find viable path

### 4. Evaluation Framework (`evaluator.py`)

Tests the decision tree against 4 predefined user profiles:

**Test Profiles (from Proposal):**

1. **efficiency_focused**
   - Wants shortest signatures
   - Expected: ECDSA

2. **hash_based_advocate**
   - Wants simplest hash-based construction
   - Expected: Lamport + Merkle Tree

3. **standardization_seeker**
   - Wants widely standardized scheme
   - Expected: DSA or ECDSA

4. **fiat_shamir_enthusiast**
   - Wants Fiat-Shamir based scheme
   - Expected: Schnorr Signatures

**Metrics Calculated:**
- **Choice Correctness Success Probability** = (Correct Recommendations) / (Total Tests)
- Target: ≥ 80% accuracy

**Output:**
- Console summary with pass/fail for each test
- Detailed text report (`test_results.txt`)
- JSON report for further analysis (`test_results.json`)

---

## How to Run

### Prerequisites
- Python 3.6+
- No external dependencies (uses only standard library)

### Quick Start

#### 1. Interactive Mode (Run the Assistant)
```bash
python cli_interface.py
```

This launches the interactive wizard where you answer questions and get a recommendation.

**Example Session:**
```
❓ How important is having SHORT signatures to you?
   Options: [y]es, [n]o, [?]don't know
   Your answer: y

   → Filtering for schemes with signatures ≤ 512 bits...

❓ Do you prefer STANDARDIZED and widely-used schemes?
   Your answer: y

   → Filtering for standardized schemes...

RECOMMENDATION: ECDSA

Details about ECDSA:
   • Security Based On: Elliptic Curve Discrete Log
   • Signature Size: 512-1042 bits
   • Key Size: 256-521 bits
   • Standardized: Yes
   • Construction: Elliptic Curve
   • Complexity Level: Medium
```

#### 2. Run Evaluation Tests
```bash
python evaluator.py
```

Tests the decision tree against 4 user profiles and generates reports:
- Prints pass/fail summary to console
- Generates `test_results.txt` with detailed results
- Generates `test_results.json` for analysis

**Expected Output:**
```
EVALUATION: Decision Tree Performance
============================================================

📋 Testing Profile: efficiency_focused
   Description: User wants shortest possible signatures
   Expected Recommendation: ECDSA
   Actual Recommendation: ECDSA
   ✅ CORRECT

[... 3 more tests ...]

SUMMARY
============================================================
Total Test Cases: 4
Correct Recommendations: 4
Choice Correctness Success Probability: 100.0%
```

### File Verification
```bash
# List all required files
ls -la signature_schemes.csv decision_tree.py cli_interface.py evaluator.py
```

---

## Design Methodology

### Step 1: Cryptographic Primitive Selection
Chose **Digital Signatures** from Lecture 9 coverage, specifically 5 complementary schemes:
- 3 number-theoretic (RSA, DSA, Schnorr)
- 1 elliptic curve (ECDSA)
- 1 hash-based (Lamport+Merkle)

This diversity ensures the decision tree has meaningful distinctions to make.

### Step 2: Implementation Usage Table
Built CSV with schemes as rows and properties as columns:
- Properties directly from lecture materials (key/signature size, complexity, etc.)
- **Added 2 columns** beyond lecture tables:
  - Complexity Category: Categorizes relative computational complexity
  - Hardware Optimized: Practical deployment consideration

### Step 3: Decision Tree Logic
Implemented rule-based filtering that:
1. Starts with all 5 schemes as candidates
2. Applies filters based on user answers
3. Narrows down to single recommendation
4. Handles uncertainty gracefully

Each filter method directly maps to a table column, ensuring validity.

### Step 4: Interactive CLI
Created user-friendly interface that:
- Asks yes/no and multiple-choice questions
- Adapts based on remaining candidates
- Provides detailed explanations
- Allows users to restart easily

### Step 5: Evaluation
Tested with 4 user profiles covering the design space:
- Each profile represents a different "archetype" of user need
- Metrics verify the tree makes correct recommendations
- Success probability ≥ 80% target

---

## Grading Rubric Alignment

| Criterion | How We Address It |
|-----------|------------------|
| **Cryptographic Primitive Choice** | 5 diverse digital signature schemes from Lecture 9 |
| **Table Specification Validity** | CSV with 5 rows (schemes), 10 columns (8+ required), 2 new columns |
| **Decision Tree Validity** | Rule-based logic; each filter maps to table column |
| **Program Validity** | Interactive CLI asks meaningful questions, outputs correct recommendations |
| **Implementation Validity** | Python code loads CSV, filters candidates, outputs recommendations; tested with 4 profiles |
| **Demonstration/Presentation Quality** | This README + CLI demo + evaluation report |

---

## Example Use Cases

### Use Case 1: Performance-Critical Application
User: "I need signatures for high-frequency trading where speed matters."

**System Response:**
1. Asks about signature size importance → User says "Yes"
2. Filters to schemes with small signatures
3. Asks about standardization → User says "Yes"
4. **Recommends: ECDSA** (small signatures, standardized, efficient)

### Use Case 2: Hash-Based Preference
User: "I only want to rely on cryptographic hash functions."

**System Response:**
1. Asks about signature size → User indifferent
2. Asks about standardization → User indifferent
3. Asks about construction type → User selects "Hash-Based Tree"
4. **Recommends: Lamport + Merkle Tree**

### Use Case 3: Regulatory Requirement
User: "My organization's standard requires NIST-approved schemes."

**System Response:**
1. Asks about standardization → User says "Yes"
2. Filters to standardized schemes
3. Asks about efficiency → User says "Not critical"
4. **Recommends: DSA or ECDSA** (both NIST-approved)

---

## Key Implementation Details

### Decision Tree Filtering Strategy

The system uses **cascading filters**:

```
Start: [RSA, Schnorr, DSA, ECDSA, Lamport+Merkle]
         ↓ (filter_by_signature_size("short"))
       [Schnorr, ECDSA, Lamport+Merkle]
         ↓ (filter_by_standardization(True))
       [ECDSA, DSA]
         ↓ (filter_by_efficiency("fast"))
       [ECDSA]
         ↓
Result: ECDSA ✓
```

### Handling Uncertainty

When users answer "don't know":
- Filter is not applied
- All current candidates persist
- System continues with remaining filters
- If no schemes match after a filter, previous filter is reversed

### Adaptive Questioning

```python
remaining = len(self.tree.current_candidates)
if remaining > 2:
    # Ask detailed multiple-choice question
else:
    # Skip detailed questions, close in on recommendation
```

---

## Evaluation Results

Run `python evaluator.py` to see results. Expected output:

```
Total Test Cases: 4
Correct Recommendations: 4/4 (100%)
Choice Correctness Success Probability: 100%
```

If success probability < 80%, adjust the filtering logic in `decision_tree.py`.

---

## Extending the System

To add a new signature scheme:

1. **Add row to `signature_schemes.csv`**
   ```csv
   New Scheme,RSA Hardness,O(...),O(...),2048,2048,No,Yes,Hash-and-Sign,Medium,Yes
   ```

2. **Update decision tree filters if needed**
   ```python
   # In decision_tree.py, add new filter method if necessary
   def filter_by_new_property(self, value):
       filtered = [s for s in self.current_candidates if ...]
       self.current_candidates = filtered
   ```

3. **Add to CLI questions**
   ```python
   # In cli_interface.py, add new question to run_interview()
   ```

4. **Update test profiles**
   ```python
   # In evaluator.py, add new test case to TEST_PROFILES
   ```

---

## Performance Notes

- **Program Runtime**: < 1 second to generate recommendation
- **CSV Loading**: < 50ms
- **Question Response Time**: Depends on user input (interactive)
- **Evaluation Suite**: ~100ms to run all 4 tests

---

## Troubleshooting

### "CSV file not found"
```
Solution: Ensure signature_schemes.csv is in the same directory as the Python files
```

### "No recommendation found"
```
Solution: User answers narrowed down all schemes. Run evaluator.py to verify tree logic.
         Adjust filter thresholds in decision_tree.py if needed.
```

### "Wrong scheme recommended"
```
Solution: Review the filtering logic for that user profile.
         Check decision_tree.py filtering methods.
         May need to add discriminating questions in cli_interface.py
```

---

## Files Reference

| File | Purpose                            |
|------|------------------------------------|
| `signature_schemes.csv` | Data table with scheme properties  |
| `decision_tree.py` | Core filtering logic               |
| `cli_interface.py` | Interactive user interface         |
| `evaluator.py` | Testing and evaluation framework   |
| `README.md` | This documentation                 |

---

---

## License & Attribution

Student: Yogarajalakshmi Sathyanarayanan (ys6678)

---