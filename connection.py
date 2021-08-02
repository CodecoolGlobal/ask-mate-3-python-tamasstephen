import csv


def read_data_from_file():
    with open("sample_data/question.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
