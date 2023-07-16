# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

import csv
from datetime import datetime

from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from rapidfuzz.distance import Levenshtein
from QAChat.Common.deepL_translator import DeepLTranslator
import numpy as np
import datetime


def load_data_from_csv(file_path):
    data = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for dataset in row:
                data.append(dataset)
    return data


def test_translation():
    translator = DeepLTranslator()
    similarity_score = []
    diff_arr = []
    # load all data from a csv file
    data = load_data_from_csv("../../DummyData/qa_german.csv")
    total_start = datetime.now()
    comp_arr = []
    bleu_score_arr = []
    for phrase in data:
        start_text = phrase
        comp_arr.append(start_text)
        start = datetime.now()
        translation = translator.translate_to(phrase, "EN-US").text
        comp_arr.append(translation)
        result = translator.translate_to(translation, "DE").text
        comp_arr.append(result)
        end = datetime.now()
        diff = end - start
        diff_arr.append(diff)
        original = word_tokenize(phrase.lower())
        translated = word_tokenize(result.lower())
        bleu_score = sentence_bleu([original], translated)
        bleu_score_arr.append(bleu_score)
        # print(diff.seconds)
        # compare two strings and give score of how similar they are
        distance = Levenshtein.distance(phrase, result)
        max_length = max(len(phrase), len(result))
        similarity_score.append(1 - (distance / max_length))

    total_end = datetime.now()
    diff_total = total_end - total_start
    print(diff_total)
    avg_diff = diff_total / (len(data) * 2)
    print(avg_diff)
    sim_score = sum(similarity_score) / len(similarity_score)
    print(sim_score)
    # save array to file
    with open("similiarity_score.txt", "w") as outfile:
        outfile.write("\n".join(str(i) for i in similarity_score))
    with open("time_diff.txt", "w") as outfile:
        outfile.write("\n".join(str(i) for i in diff_arr))
    with open("compare.txt", "w") as outfile:
        outfile.write("\n".join(str(i) for i in comp_arr))
    with open("bleu_score.txt", "w") as outfile:
        outfile.write("\n".join(str(i) for i in bleu_score_arr))


def compute_metrics_bleu():
    # Open the file and read the lines
    with open("bleu_score.txt", "r") as f:
        lines = f.readlines()

    # Convert each line to a float and store in a list
    blue_scores = [float(line.strip()) for line in lines]

    max_value = np.max(blue_scores)
    min_value = np.min(blue_scores)
    average = np.mean(blue_scores)
    median = np.median(blue_scores)
    variance = np.var(blue_scores)

    print("BLEU:")
    print(f"Maximum: {max_value}")
    print(f"Minimum: {min_value}")
    print(f"Average: {average}")
    print(f"Median: {median}")
    print(f"Variance: {variance}")


def compute_metrics_levenshtein():
    # Open the file and read the lines
    with open("similiarity_score.txt", "r") as f:
        lines = f.readlines()

    # Convert each line to a float and store in a list
    sim_scores = [float(line.strip()) for line in lines]

    max_value = np.max(sim_scores)
    min_value = np.min(sim_scores)
    average = np.mean(sim_scores)
    median = np.median(sim_scores)
    variance = np.var(sim_scores)

    print("Levenshtein:")
    print(f"Maximum: {max_value}")
    print(f"Minimum: {min_value}")
    print(f"Average: {average}")
    print(f"Median: {median}")
    print(f"Variance: {variance}")


def compute_metrics_time():
    # Open the file and read the lines
    with open("time_diff.txt", "r") as f:
        lines = f.readlines()

    time_scores = []

    for line in lines:
        line = line.strip()
        hours, minutes, seconds = map(float, line.split(":"))
        time_scores.append(
            datetime.timedelta(
                hours=hours, minutes=minutes, seconds=seconds
            ).total_seconds()
        )

    max_value = np.max(time_scores)
    min_value = np.min(time_scores)
    average = np.mean(time_scores)
    median = np.median(time_scores)
    print("Time:")
    print(f"Maximum: {max_value}")
    print(f"Minimum: {min_value}")
    print(f"Average: {average}")
    print(f"Median: {median}")


if __name__ == "__main__":
    # test_translation()
    compute_metrics_bleu()
    compute_metrics_levenshtein()
    compute_metrics_time()
