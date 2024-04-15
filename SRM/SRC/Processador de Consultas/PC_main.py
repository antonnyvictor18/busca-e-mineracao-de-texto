import xml.etree.ElementTree as ET
import csv

# Lê o arquivo de configuração
PC_path  = 'busca-e-mineracao-de-texto\SRM\SRC\Processador de Consultas\PC.cfg'
with open(PC_path , 'r') as f:
    for line in f:
        if line.startswith("STEMMER"):
            from nltk.stem import PorterStemmer
            ps = PorterStemmer()
            stem = True
            continue
        elif line.startswith("STEMMER"):
            stem = False
            continue 
        elif line.startswith('LEIA='):
            xml_filename = line.split('=')[1].strip()
        elif line.startswith('CONSULTAS='):
            consultas_filename = line.split('=')[1].strip()
        elif line.startswith('ESPERADOS='):
            resultados_filename = line.split('=')[1].strip()
            
# Faz a leitura do arquivo XML
tree = ET.parse(xml_filename)
root = tree.getroot()

# Inicializa as listas de consultas e resultados esperados
consultas = []
resultados_esperados = []

# Processa cada consulta presente no arquivo XML
for query in root.iter('QUERY'):
    query_number = query.find('QueryNumber').text
    query_text = query.find('QueryText').text.upper().replace(';', '')
    if stem: 
        query_text = ' '.join(ps.stem(word) for word in query_text.split())
    consultas.append([query_number, query_text])

    for item in query.findall('Records/Item'):
        doc_number = item.text
        score = item.get('score')
        doc_votes = len(score.replace('0', ''))
        
    resultados_esperados.append([query_number, doc_number, doc_votes])

# Escreve as consultas no arquivo CSV
with open(consultas_filename, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['QueryNumber', 'QueryText'])
    for consulta in consultas:
        writer.writerow(consulta)

# Escreve os resultados esperados no arquivo CSV
with open(resultados_filename, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['QueryNumber', 'DocNumber', 'DocVotes'])
    for resultado in resultados_esperados:
        writer.writerow(resultado)