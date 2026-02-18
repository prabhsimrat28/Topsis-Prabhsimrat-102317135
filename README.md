# TOPSIS – Technique for Order Preference by Similarity to Ideal Solution

TOPSIS is a Multi-Criteria Decision Making (MCDM) method developed in the 1980s.  
It selects the best alternative based on:

- Shortest Euclidean distance from the Ideal Solution
- Farthest distance from the Negative-Ideal Solution

---

## Installation

Install directly from PyPI:

## Usage

After installation, open your terminal and run:
topsis <InputDataFile> <Weights> <Impacts> <OutputFile>


### Example:

topsis test.csv "1,1,2,3,1" "+,-,+,-,-" output.csv

## Output

The output file will contain:

- Original data
- Topsis Score
- Rank (1 = Best Alternative)

---