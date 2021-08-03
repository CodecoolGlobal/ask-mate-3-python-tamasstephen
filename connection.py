import csv


def read_data_from_file(filename="sample_data/test_questions.csv"):
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def write_data_to_file(data, headers, filename="sample_data/test_questions.csv"):
    with open(filename, "w") as csvfile:
        print(headers)
        print(data[0])
        fieldnames = headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for fields in data:
            writer.writerow(fields)
         
