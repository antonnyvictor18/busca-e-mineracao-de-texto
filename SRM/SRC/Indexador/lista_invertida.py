import xml.etree.ElementTree as ET
import string
import csv
import logging
import time


def parse_xml_file(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    docs = []
    for record in root.findall("./RECORD"):
        doc_id = record.find("./RECORDNUM").text
        abstract = record.find("./ABSTRACT")
        if abstract is None:
            abstract = record.find("./EXTRACT")
        if abstract is not None:
            doc_text = abstract.text.strip()
            doc_text = doc_text.translate(str.maketrans("", "", string.punctuation)).upper()
            docs.append((doc_id, doc_text))
    
    return docs

def create_inverted_index(documents):
    inverted_index = {}
    for doc_id, doc_text in documents:
        for word in doc_text.split():
            if word not in inverted_index:
                inverted_index[word] = [int(doc_id)]
            else:
                inverted_index[word].append(int(doc_id))

    return inverted_index

def write_inverted_index_to_file(inverted_index, output_file):
    with open(output_file, "w", newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Word", "Documents"])
        for word, docs in inverted_index.items():
            writer.writerow([word, docs])

def calcular_tempo_medio(total_time, total_items):
    if total_items > 0:
        return total_time / total_items
    else:
        return 0

def main():
    logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Starting {__file__}")
    logging.info("Starting the inverted index creation process")
    start_time = time.time()

    GLI_path  = 'SRM/SRC/Indexador/GLI.cfg'
    input_files = []
    output_file = None

    logging.info("Reading the configuration file")
    with open(GLI_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("LEIA="):
                input_files.append(line[len("LEIA="):])
            elif line.startswith("ESCREVA="):
                output_file = line[len("ESCREVA="):]          

    logging.info("Reading XML files")
    documents = []
    for input_file in input_files:
        try:
            documents += parse_xml_file(input_file)
        except Exception as e:
            logging.error(f"Error while reading the file {input_file}: {e}")

    logging.info("Creating the inverted index")
    inverted_index = create_inverted_index(documents)

    logging.info("Writing the inverted index to the output file")
    write_inverted_index_to_file(inverted_index, output_file)

    end_time = time.time()
    total_time = end_time - start_time

    logging.info(f"Total number of documents read: {len(documents)}")
    logging.info(f"Total processing time: {total_time:.2f} seconds")
    logging.info(f"Average time per document: {calcular_tempo_medio(total_time, len(documents)):.4f} seconds")

    logging.info("Process completed")
    logging.info(f"End of {__file__}")

main()
