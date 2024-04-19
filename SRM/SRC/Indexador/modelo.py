from collections import Counter
import csv
import ast
import math
import logging
import time

logging.basicConfig(filename='SRM/processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
INDEX_FILE_PATH = 'SRM\SRC\Indexador\INDEX.cfg'
logging.info(f"Starting {__file__}")

def calculate_average_time(total_time, total_items):
    if total_items > 0:
        return total_time / total_items
    else:
        return 0
    
logging.info("Starting the indexing process")
start_time = time.time()

logging.info("Reading configuration file")
with open(INDEX_FILE_PATH, 'r') as index_file:
    for line in index_file:
        if line.startswith('LEIA='):
            data_file_path = line.split('=')[1].strip()
        elif line.startswith('ESCREVA='):
            output_file_path = line.split('=')[1].strip()
        elif line.startswith('FREQUENCIA='):
            frequency_type = line.split('=')[1].strip()

word_count_per_doc = []
total_unique_words = 0

logging.info("Reading data file")
with open(data_file_path, newline='\n') as csv_file:
    reader = csv.reader(csv_file, delimiter=";")
    next(reader)
    for line in reader:
        word_list = ast.literal_eval(line[1])
        total_unique_words += 1

        for word in word_list:
            while word > len(word_count_per_doc):
                word_count_per_doc.append(0)
            word_count_per_doc[word - 1] += 1

total_documents = len(word_count_per_doc)

lines_read = 0
lines_written = 0

with open(data_file_path, newline='\n') as read_file, open(output_file_path, "w", newline='') as write_file:
    reader = csv.reader(read_file, delimiter=";")
    next(reader)

    writer = csv.writer(write_file, delimiter=";")
    writer.writerow(["Word", "DocNumber", "Weight"])

    logging.info("Starting data processing")
    for line in reader:
        lines_read += 1
        word_list = ast.literal_eval(line[1])
        word_counter = Counter(word_list)

        for doc_number in word_counter:
            if frequency_type == "absoluta":
                weight = word_counter[doc_number] * math.log(total_documents / len(set(word_list)) + 1)
            elif frequency_type == "relativa":
                weight = (word_counter[doc_number] / word_count_per_doc[doc_number - 1]) * math.log(total_documents / len(set(word_list)) + 1)

            lines_written += 1
            writer.writerow([line[0], doc_number, weight])

    logging.info("Data processing completed")

end_time = time.time()
total_processing_time = end_time - start_time

logging.info(f"Total number of documents read: {lines_read}")
logging.info(f"Total number of lines written: {lines_written}")
logging.info(f"Total processing time: {total_processing_time:.2f} seconds")
logging.info(f"Average time per document: {calculate_average_time(total_processing_time, lines_read):.4f} seconds")
logging.info(f"Average time per word: {calculate_average_time(total_processing_time, total_unique_words):.4f} seconds")
logging.info(f"Average time per written line: {calculate_average_time(total_processing_time, lines_written):.4f} seconds")
logging.info("End of process")
logging.info(f"End of {__file__}")
