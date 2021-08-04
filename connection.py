import csv
# from tempfile import NamedTemporaryFile


def read_data_from_file(filename="sample_data/test_questions.csv"):
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def write_data_to_file(data, headers, filename="sample_data/test_questions.csv"):
    with open(filename, "w") as csvfile:
        fieldnames = headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for fields in data:
            writer.writerow(fields)
         
         
# def delete_questions(question_id, filename):
#     print("reach this function")
#     tempfile = NamedTemporaryFile('w+t')
#     with open(filename, 'r') as csvfile, tempfile:
#         reader = csv.DictReader(csvfile)
#         writer = csv.DictWriter(tempfile, fieldnames=HEADERS)
#         writer.writeheader()
#         for row in reader:
#             if question_id != row["id"]:
#                 writer.writerow(row)
#             # else:
#             #     pass
#     shutil.move(tempfile.name, filename)
