# IMPLEMENTAÇÃO DE UM SISTEMA DE RECUPERAÇÃO EM MEMÓRIA SEGUNDO O MODELO VETORIAL

Implementação de um sistema de recuperação em memória segundo o modelo vetorial que fora apresentando em aula da 
disciplina Busca e Mineração de Texto (COS738) ministrada pelo professor Geraldo Xexéo.

## Módulos:
1. PC.py - Processador de consultas.
2. lista_invertida.py - Gerador de lista invertida.
3. modelo.py - Cria o modelo vetorial.
4. buscador.py - Buscador, responsável pelos resultados finais.


## Arquivos gerados pelo sistema
1. consultas.csv - Criado pelo PC, lista todas as consultas processadas.
2. esperados.csv - Criado pelo PC, lista número do documento e seu número de votos.
3. gli.csv - Criado pelo lista_invertida, cada linha correponde a uma palavra e à lista dos índices dos documentos em que a palavra aparece. O índice do documento aparece na lista o mesmo número de vezes que a palavra aparece no documento.
4. modelo.csv - Criado pelo modelo, especificado no arquivo modelo.txt.
5. resultados.csv - Criado pelo buscador, para cada consulta listamos o rank e o índice dos seus 5 documentos mais similares e o grau de similaridade para cada documento.

## Como executar
Para que o projeto funcione corretamente, faz-se necessário que os módulos sejam executados na seguinte ordem: 1 -> 2 -> 3 -> 4.
