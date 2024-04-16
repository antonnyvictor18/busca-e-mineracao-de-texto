import xml.etree.ElementTree as ET
from collections import Counter
import csv
import ast
import math

INDEX_path  = 'busca-e-mineracao-de-texto\SRM\SRC\Indexador\INDEX.cfg'
with open(INDEX_path , 'r') as f:
    for line in f:
        if line.startswith('LEIA='):
            leia = line.split('=')[1].strip()
        elif line.startswith('ESCREVA='):
            escreva = line.split('=')[1].strip()
        elif line.startswith('FREQUENCIA='):
            freq = line.split('=')[1].strip()

num_words_list = []
vocab = 0

with open(leia, newline='\n') as csv_file:
    reader = csv.reader(csv_file, delimiter=";")
    next(reader)
    for line in reader:
        li = ast.literal_eval(line[1])
        vocab += 1
        
        for elem in li:
            while elem > len(num_words_list):
                num_words_list.append(0)
            num_words_list[elem - 1] += 1


num_docs = len(num_words_list)

with open(leia, newline='\n') as read_file, \
    open(escreva, "w", newline='') as write_file:
    reader = csv.reader(read_file, delimiter=";")
    next(reader)
    
    writer = csv.writer(write_file, delimiter=";")
    writer.writerow(["Word", "DocNumber", "Weight"])

    lines_read = 0
    lines_written = 0
    for line in reader:
        lines_read += 1
        li = ast.literal_eval(line[1])
        c = Counter(li)
        
        for doc in c:
            if freq == "absoluta":
                weight = c[doc] * math.log(num_docs/len(set(li)) + 1)
            elif freq == "relativa":
                weight = (c[doc]/num_words_list[doc - 1]) * math.log(num_docs/len(set(li)) + 1)
            
            lines_written += 1
            writer.writerow([line[0], doc, weight])
        
            