import xml.etree.ElementTree as ET
from nltk.stem import PorterStemmer
import csv
import logging
import time


def parse_configuration_file(config_filename):
    xml_filename = ""
    consultas_filename = ""
    resultados_filename = ""
    with open(config_filename, 'r') as f:
        for line in f:
            if line.startswith('LEIA='):
                xml_filename = line.split('=')[1].strip()
            elif line.startswith('CONSULTAS='):
                consultas_filename = line.split('=')[1].strip()
            elif line.startswith('ESPERADOS='):
                resultados_filename = line.split('=')[1].strip()
    return xml_filename, consultas_filename, resultados_filename

def process_queries(root):
    ps = PorterStemmer()
    consultas = []
    resultados_esperados = []

    for query in root.iter('QUERY'):
        query_number = query.find('QueryNumber').text
        query_text = query.find('QueryText').text.upper().replace(';', '')
        query_text = ' '.join(ps.stem(word) for word in query_text.split())
        consultas.append([query_number, query_text])

        for item in query.findall('Records/Item'):
            doc_number = item.text
            score = item.get('score')
            doc_votes = len(score.replace('0', ''))
            resultados_esperados.append([query_number, doc_number, doc_votes])

    return consultas, resultados_esperados

def write_to_csv(data, filename, header):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def main():
    logging.basicConfig(filename='SRM/processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logging.info(f"Starting {__file__}")
    logging.info("Starting the query processing")

    logging.info("Reading the configuration file")
    start_time = time.time()

    xml_filename, consultas_filename, resultados_filename = parse_configuration_file('SRM/SRC/Processador de Consultas/PC.cfg')
    
    logging.info("Finished reading the configuration file")

    logging.info("Reading the XML file")
    tree = ET.parse(xml_filename)
    root = tree.getroot()

    logging.info("Finished reading the XML file")

    logging.info("Processing queries")
    consultas, resultados_esperados = process_queries(root)

    logging.info("Finished processing queries")

    logging.info("Writing queries to CSV")
    write_to_csv(consultas, consultas_filename, ['QueryNumber', 'QueryText'])

    logging.info("Writing expected results to CSV")
    write_to_csv(resultados_esperados, resultados_filename, ['QueryNumber', 'DocNumber', 'DocVotes'])

    end_time = time.time()
    total_time = end_time - start_time

    logging.info(f"Total number of queries processed: {len(consultas)}")
    logging.info(f"Total processing time: {total_time:.2f} seconds")
    logging.info(f"Average processing time per query: {total_time / len(consultas):.4f} seconds")

    logging.info("Process completed")
    logging.info(f"End of {__file__}")

if __name__ == "__main__":
    main()
