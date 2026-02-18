import sys
import os
import numpy as np
import pandas as pd

def validate_arguments():
    if len(sys.argv)!=5:
        print("Usage: python <program.py> <InputFile> <Weights> <Impacts> <OutputFile>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]


def load_dataset(file_path):
    try:
        df =pd.read_csv(file_path)
    except FileNotFoundError:
        print("Error: Input file not found")
        sys.exit(1)

    if df.shape[1]<3:
        print("Error: Input file must contain at least 3 columns")
        sys.exit(1)

    return df


def process_weights(weights_str,expected_len):
    weights=weights_str.strip().split(',')

    if len(weights)!=expected_len:
        print("Error: Number of weights must match number of numeric columns")
        sys.exit(1)

    try:
        weights=np.array([float(w) for w in weights])
    except ValueError:
        print("Error: Weights must be numeric")
        sys.exit(1)

    return weights


def process_impacts(impacts_str,expected_len):
    impacts=impacts_str.strip().split(',')

    if len(impacts)!=expected_len:
        print("Error: Number of impacts must match number of numeric columns")
        sys.exit(1)

    for symbol in impacts:
        if symbol not in ['+', '-']:
            print("Error: Impacts must be '+' or '-'")
            sys.exit(1)

    return impacts


def validate_numeric_columns(df):
    numeric_df=df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

    if numeric_df.isnull().values.any():
        print("Error: From 2nd to last columns must contain numeric values only")
        sys.exit(1)

    return numeric_df


def normalize_and_weight(matrix,weights):
    denominator=np.sqrt((matrix ** 2).sum(axis=0))
    normalized=matrix/denominator
    return normalized*weights


def calculate_ideal_solutions(weighted_matrix, impacts):
    ideal_best=[]
    ideal_worst=[]

    for i in range(len(impacts)):
        column=weighted_matrix[:, i]
        if impacts[i] =='+':
            ideal_best.append(column.max())
            ideal_worst.append(column.min())
        else:
            ideal_best.append(column.min())
            ideal_worst.append(column.max())

    return np.array(ideal_best), np.array(ideal_worst)


def calculate_scores(weighted_matrix,ideal_best,ideal_worst):
    distance_best=np.sqrt(((weighted_matrix -ideal_best) **2).sum(axis=1))
    distance_worst=np.sqrt(((weighted_matrix -ideal_worst) **2).sum(axis=1))
    return distance_worst / (distance_best + distance_worst)



def main():

    input_file,weights_str,impacts_str,output_file=validate_arguments()

    data = load_dataset(input_file)

    numeric_data=validate_numeric_columns(data)

    weights=process_weights(weights_str, numeric_data.shape[1])
    impacts=process_impacts(impacts_str, numeric_data.shape[1])

    weighted_matrix=normalize_and_weight(numeric_data.values, weights)

    ideal_best,ideal_worst=calculate_ideal_solutions(weighted_matrix, impacts)

    scores=calculate_scores(weighted_matrix, ideal_best, ideal_worst)

    result_df = data.copy()
    result_df["Topsis Score"]=scores
    result_df["Rank"]=result_df["Topsis Score"].rank(method='max', ascending=False).astype(int)

    if not output_file.endswith(".csv"):
        print("Error: Output file must have .csv extension")
        sys.exit(1)

    try:
        if os.path.exists(output_file):
            os.remove(output_file)
        result_df.to_csv(output_file, index=False)
        print("TOPSIS calculation completed successfully.")
    except:
        print("Error: Unable to write output file")
        sys.exit(1)


if __name__ == "__main__":
    main()
