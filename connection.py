import csv


def read_data_from_file(filename="sample_data/question.csv"):
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
