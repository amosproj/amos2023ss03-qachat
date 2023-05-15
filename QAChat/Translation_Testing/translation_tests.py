from datetime import datetime

from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from rapidfuzz.distance import Levenshtein
from QAChat.Data_Processing.deepL_translator import DeepLTranslator, load_data_from_csv
import numpy as np


def test_translation():
    translator = DeepLTranslator()
    similarity_score = []
    diff_arr = []
    # load all data from a csv file
    data = load_data_from_csv("../../DummyData/qa_german.csv")
    total_start = datetime.now()
    comp_arr = []
    bleu_score_arr = []
    for i in data:
        start_text = i
        comp_arr.append(start_text)
        start = datetime.now()
        translation = translator.translate_german_english(i)
        comp_arr.append(translation)
        result = translator.translate_english_german(translation)
        comp_arr.append(result)
        end = datetime.now()
        diff = end - start
        diff_arr.append(diff)
        original = word_tokenize(i.lower())
        translated = word_tokenize(result.lower())
        bleu_score = sentence_bleu([original], translated)
        bleu_score_arr.append(bleu_score)
        # print(diff.seconds)
        # compare two strings and give score of how similar they are
        distance = Levenshtein.distance(i, result)
        max_length = max(len(i), len(result))
        similarity_score.append(1 - (distance / max_length))

    total_end = datetime.now()
    diff_total = (total_end - total_start)
    print(diff_total)
    avg_diff = diff_total / (len(data) * 2)
    print(avg_diff)
    sim_score = sum(similarity_score) / len(similarity_score)
    print(sim_score)
    # save array to file
    with open('similiarity_score.txt', 'w') as outfile:
        outfile.write('\n'.join(str(i) for i in similarity_score))
    with open('time_diff.txt', 'w') as outfile:
        outfile.write('\n'.join(str(i) for i in diff_arr))
    with open('compare.txt', 'w') as outfile:
        outfile.write('\n'.join(str(i) for i in comp_arr))
    with open('bleu_score.txt', 'w') as outfile:
        outfile.write('\n'.join(str(i) for i in bleu_score_arr))


def compute_metrics_bleu():
    # Open the file and read the lines
    with open('bleu_score.txt', 'r') as f:
        lines = f.readlines()

    # Convert each line to a float and store in a list
    blue_scores = [float(line.strip()) for line in lines]

    max_value = np.max(blue_scores)
    min_value = np.min(blue_scores)
    average = np.mean(blue_scores)
    median = np.median(blue_scores)
    variance = np.var(blue_scores)

    print(f"Maximum: {max_value}")
    print(f"Minimum: {min_value}")
    print(f"Average: {average}")
    print(f"Median: {median}")
    print(f"Variance: {variance}")


def compute_metrics_time():
    # Open the file and read the lines
    with open('time_diff.txt', 'r') as f:
        lines = f.readlines()

    # Convert each line to a float and store in a list
    blue_scores = [float(line.strip()) for line in lines]

    max_value = np.max(blue_scores)
    min_value = np.min(blue_scores)
    average = np.mean(blue_scores)
    median = np.median(blue_scores)
    variance = np.var(blue_scores)

    print(f"Maximum: {max_value}")
    print(f"Minimum: {min_value}")
    print(f"Average: {average}")
    print(f"Median: {median}")
    print(f"Variance: {variance}")


if __name__ == '__main__':
    test_translation()
