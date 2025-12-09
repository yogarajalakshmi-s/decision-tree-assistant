# Decision Tree Assistant for Selecting Digital Signature Schemes

## Project Overview

This project implements an interactive decision tree system to help non-expert users select the most appropriate digital signature scheme for their specific needs. The system guides users through simple questions and recommends the best scheme based on their preferences.

## Problem Statement

Choosing the right digital signature scheme is challenging for users without cryptography expertise. Different schemes have different tradeoffs in terms of signature size, computational efficiency, standardization, and security assumptions. This project simplifies that selection process.

## Solution

An interactive CLI-based decision tree that:
- Asks 4 adaptive questions about user preferences
- Filters schemes based on answers
- Recommends the best matching scheme
- Displays full scheme details and alternatives
- Handles uncertainty ("don't know" responses)

## Project Details

**Project Type:** 2.6 - Selecting Schemes for a Given Cryptography Primitive  
**Cryptographic Primitive:** Digital Signatures  
**Course:** CS-GY 6903 Applied Cryptography, Fall 2025

## Digital Signature Schemes Included

1. **Hashed RSA (RSA-FDH)** - 2048-4096 bit signatures, RSA-based, standardized
2. **Schnorr Signatures** - 320-512 bit signatures, discrete log-based, Fiat-Shamir
3. **DSA** - 320-512 bit signatures, discrete log-based, FIPS standardized
4. **ECDSA** - 512-1042 bit signatures, elliptic curve-based, NIST standardized
5. **Lamport + Merkle Tree** - 256-512 bit signatures, hash-based, post-quantum safe

## Implementation Usage Table

The system uses a CSV table with 5 schemes and 10 properties:

| Property | Description |
|----------|-------------|
| Scheme Name | Identifier |
| Security Assumption | Mathematical hardness assumption |
| Key Size | Cryptographic key length |
| Signature Size | Generated signature length |
| Standardized | Official approval (NIST, FIPS, etc.) |
| Construction Type | Mathematical construction method |
| Complexity Category | Computational cost (Low/Medium/High) |
| Hardware Optimized | Hardware acceleration support |
| Signing Complexity | Cost to create signature |
| Verification Complexity | Cost to verify signature |

## System Architecture

### 4 Main Components

**1. signature_schemes.csv**
- Data layer containing all 5 schemes and their 10 properties
- Loaded and used by decision_tree.py

**2. decision_tree.py**
- Core filtering logic (~300 lines)
- Filtering methods:
  - `filter_by_signature_size(preference)`
  - `filter_by_security_assumption(assumption)`
  - `filter_by_standardization(wants_std)`
  - `filter_by_construction_type(ctype)`
  - `filter_by_efficiency(level)`
- Returns best recommendation based on priority:
  1. Lowest complexity category
  2. Standardized (if tied)
  3. Smallest signature size (if tied)

**3. cli_interface.py**
- Interactive user interface (~200 lines)
- Asks 4 questions:
  1. Do you need short signatures?
  2. Do you prefer standardized schemes?
  3. What construction type interests you?
  4. Do you prioritize computational efficiency?
- Supports yes/no/don't-know responses
- Displays recommendation with full scheme details

**4. evaluator.py**
- Testing framework (~350 lines)
- Tests 4 user profiles:
  1. Efficiency-focused (wants short signatures)
  2. Hash-based advocate (wants hash-based security)
  3. Standardization seeker (wants standardized schemes)
  4. Fiat-Shamir enthusiast (wants Fiat-Shamir construction)
- Calculates success probability
- Generates text and JSON reports

## How to Use

### Running the Interactive CLI
```bash
python3 cli_interface.py
```

Answer the 4 questions interactively. Example:
```
Do you need SHORT signatures?
[y]es / [n]o / [?]don't know: y
→ Filtering for short signatures...

Do you prefer STANDARDIZED schemes?
[y]es / [n]o / [?]don't know: y
→ Filtering for standardized schemes...

RECOMMENDATION: DSA
Details:
  • Security: Discrete Log Problem
  • Signature Size: 320-512 bits
  • Standardized: Yes
  • Construction: Number-Theoretic
  • Complexity: Medium
```

### Running the Evaluator
```bash
python3 evaluator.py
```

Output shows:
- Results for all 4 test profiles
- Success probability (target: ≥80%)
- Generates `report.txt` and `report.json`

## Decision Tree Logic

### Example: User wants short signatures + standardized
```
Start: [RSA, Schnorr, DSA, ECDSA, Lamport]
  ↓ Filter: Signature Size ≤ 512 bits
Intermediate: [Schnorr, DSA, Lamport]
  ↓ Filter: Standardized = Yes
Final: [DSA]
  ↓ Recommendation: DSA
```

## Requirements Met

- Cryptographic Primitive: Digital Signatures (5 schemes)
- Implementation Usage Table: 5 rows × 10 columns (8+ required)
- 2 New Columns: Complexity Category, Hardware Optimized
- Decision Tree Code: Rule-based filtering with 5 methods
- Non-Expert Interface: Interactive CLI with simple questions
- Input from Table: All filters read CSV properties
- Questions at Decision Nodes: 4 adaptive questions
- Meaningful Success Metric: 100% (4/4 tests passing)
- Software Implementation: 850+ lines of well-documented code

## File Structure
```
project/
├── data/
   ├── signature_schemes.csv          # Data table (5 schemes × 10 properties)
├── source/
   ├── decision_tree.py               # Core filtering logic
   ├── cli_interface.py               # Interactive user interface
   ├── evaluator.py                   # Testing framework
   ├── report.txt                     # Text evaluation report
   ├── report.json                    # JSON evaluation report
└── README.md                      # This file
```

## Technical Details

- **Language:** Python 3.6+
- **Dependencies:** None (standard library only)
- **CSV Parsing:** csv.DictReader
- **Code Structure:** Object-oriented design with clear separation of concerns
- **Testing:** Scripted user profiles with automated evaluation

## Key Design Decisions

1. **Rule-based filtering (not ML):** Provides transparency - users understand why they got each recommendation

2. **Priority ranking:** Complexity first, then standardization, then signature size - prioritizes computational efficiency

3. **Uncertainty handling:** "Don't know" option skips filters, allowing users to express incomplete preferences

4. **Adaptive questions:** System only asks relevant questions based on remaining candidates

5. **CSV-based scheme storage:** Easy to add new schemes without code changes

## Learning Outcomes

- Structured approach to complex decision problems
- Importance of well-designed property tables
- User experience in cryptography tool design
- Testing and evaluation methodology
- Rule-based system design

## License

Educational project for NYU CS-GY 6903 Applied Cryptography course.

---

**Author:** Yogarajalakshmi Sathyanarayanan (ys6678)   
**Date:** Fall 2025