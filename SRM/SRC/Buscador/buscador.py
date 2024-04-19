import xml.etree.ElementTree as ET
from collections import Counter
import csv
import logging
import time

def read_configuration(config_path):
    model_path = ""
    queries_path = ""
    results_path = ""
    
    with open(config_path, 'r') as f:
        for line in f:   
            if line.startswith('MODELO='):
                model_path = line.split('=')[1].strip()
            elif line.startswith('CONSULTAS='):
                queries_path = line.split('=')[1].strip()
            elif line.startswith('RESULTADOS='):
                results_path = line.split('=')[1].strip()
    
    return model_path, queries_path, results_path

def process_queries(model_path, queries_path, results_path, min_length=2):
    start_time = time.time()

    logging.info("Starting query processing")

    matrix_dict = {}
    with open(model_path) as model_file:
        model_reader = csv.reader(model_file, delimiter=";")
        next(model_reader)
        
        for line in model_reader:
            if line[0] not in matrix_dict.keys():
                matrix_dict[line[0]] = {int(line[1]): float(line[2])}
            else:
                matrix_dict[line[0]][int(line[1])] = float(line[2])

    with open(results_path, "w", newline='') as result_file:
        writer = csv.writer(result_file, delimiter=";")
        writer.writerow(["QueryNumber", "[DocRanking, DocNumber, Similarity]"])

    result_lines = 0
    with open(queries_path) as query_file:
        query_reader = csv.reader(query_file, delimiter=";")
        next(query_reader)
        query_num = 0
        
        for query in query_reader:
            query_dict = {}
            
            words = query[1].split()
            words = [word for word in words if len(word) >= min_length]
            query_vec = Counter(words)
            
            for word in query_vec:
                word = word.upper()
                if word in matrix_dict.keys():
                    current_dict = matrix_dict[word]
                    for key in current_dict:
                        if key not in query_dict:
                            query_dict[key] = current_dict[key] * query_vec[word]
                        else:
                            query_dict[key] += current_dict[key] * query_vec[word]
            
            query_num += 1
            sorted_values = sorted(query_dict.items(), key=lambda item: item[1], reverse=True)
            
            with open(results_path, "a", newline='') as result_file:
                result_writer = csv.writer(result_file, delimiter=";")
                for i, elem in enumerate(sorted_values):
                    li = [i, elem[0], elem[1]]
                    result_writer.writerow([query[0], li])
                    result_lines += 1

    end_time = time.time()
    total_time = end_time - start_time
    logging.info("Finished query processing")
    logging.info(f"Total number of result lines written: {result_lines}")
    logging.info(f"Total processing time: {total_time:.2f} seconds")
    logging.info(f"Average processing time per query: {total_time / query_num:.4f} seconds")

    return result_lines


def main():

    logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Starting {__file__}")

    model_path, queries_path, results_path = read_configuration('SRM/SRC/Buscador/BUSCA.cfg')

    process_queries(model_path, queries_path, results_path)
    logging.info(f"End of {__file__}")

if __name__ == "__main__":
    main()
