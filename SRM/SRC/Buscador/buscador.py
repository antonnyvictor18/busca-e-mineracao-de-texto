import xml.etree.ElementTree as ET
from collections import Counter
import csv

min_length = 2
BUSCA_path  = 'SRM\SRC\Buscador\BUSCA.cfg'
with open(BUSCA_path , 'r') as f:
    for line in f:
        if line.startswith("STEMMER"):
            stem = True
            continue
        elif line.startswith("NOSTEMMER"):
            stem = False
            continue
                
        if line.startswith('MODELO='):
            modelo = line.split('=')[1].strip()
        elif line.startswith('CONSULTAS='):
            consultas = line.split('=')[1].strip()
        elif line.startswith('RESULTADOS='):
            Path_resultado = line.split('=')[1].strip()
            oldname, extension = Path_resultado.split('.')
            if stem:
                resultado = oldname + "-stemmer." + extension
            else:
                resultado = oldname + "-nostemmer." + extension

matrix_dict = {}
with open(modelo) as model_file:
    model_reader = csv.reader(model_file, delimiter=";")
    next(model_reader)
    
    for line in model_reader:
        if line[0] not in matrix_dict.keys():
            matrix_dict[line[0]] = {int(line[1]): float(line[2])}
        else:
            matrix_dict[line[0]][int(line[1])] = float(line[2])


with open(resultado, "w", newline='') as result_file:
    writer = csv.writer(result_file, delimiter=";")
    writer.writerow(["QueryNumber", "[DocRanking, DocNumber, Similarity]"])

with open(consultas) as query_file:
    query_reader = csv.reader(query_file, delimiter=";")
    next(query_reader)
    query_num = 0
    result_lines = 0
    
    for query in query_reader:
        query_dict = {}
        
        words = query[1].split()
        words = [word for word in words if len(word) >= min_length]
        query_vec = Counter(words)
        
        for word in query_vec:
            if word in matrix_dict.keys():
                current_dict = matrix_dict[word]
                weight_list = []
                for key in current_dict:
                    weight_list.append(current_dict[key])
                    if key not in query_dict:
                        query_dict[key] = current_dict[key] * query_vec[word]
                    else:
                        query_dict[key] += current_dict[key] * query_vec[word]
        
        query_num += 1
        sorted_values = sorted(query_dict.items(), key=lambda item: item[1], reverse=True)#[:100]
        
        with open(resultado, "a", newline='') as result_file:
            result_writer = csv.writer(result_file, delimiter=";")
            for i, elem in enumerate(sorted_values):
                li = [i, elem[0], elem[1]]
                result_writer.writerow([query[0], li])
                result_lines += 1