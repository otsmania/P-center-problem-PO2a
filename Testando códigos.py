import os
import math

def le_dados_inst(arq_instancia):

    # Inicialização de variáveis

    num_pontos = None
    p_centros = None
    min_pontos_centro = None
    max_pontos_centro = None
    coordenadas = []
    distancia = []
    custo_total = None

    # Abrindo arquivo para leitura

    with open(arq_instancia, 'r', encoding='utf8') as f:
        linhas = f.readlines()

        # Lendo e convertendo os parâmetros

        num_pontos = int(linhas[1].strip().split(';')[0])
        p_centros = int(linhas[1].strip().split(';')[1])
        min_pontos_centro = int(linhas[1].strip().split(';')[2])
        max_pontos_centro = int(linhas[1].strip().split(';')[3])

        del linhas[:3]

        # Lendo as coordenadas

        for i in range(num_pontos):
            coordenadas.append(tuple(map(int, linhas[i].strip().split(';')[1:])))


    return num_pontos, p_centros, min_pontos_centro, max_pontos_centro, coordenadas

def calcular_distancias(coordenadas):

    #Calcula a matriz das distâncias entre os pontos

    n = len(coordenadas)
    distancias = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dist = math.sqrt((coordenadas[i][0] - coordenadas[j][0]) ** 2 +
                             (coordenadas[i][1] - coordenadas[j][1]) ** 2)
            distancias[i][j] = distancias[j][i] = dist
    return distancias

#Calcula distancia euclidiana entre dois pontos

def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

#Escolhendo p-centros

def inicializar_centros(coordenadas, p_centros):
    centros = [0] #Se inicia com o primeiro ponto
    while len(centros) < p_centros: #Executa enquanto o número de centros for menor que o desejado
        max_distancia = -1 #Variável para controlar a maior distância entre um ponto e os centros já escolhidos
        proximo_centro = None
        for i in range(len(coordenadas)):
            if i not in centros:
                menor_distancia = float('inf')  # Valor inicial grande
                for c in centros:
                    dist = calcular_distancia(coordenadas[i], coordenadas[c])
                    if dist < menor_distancia:
                        menor_distancia = dist
                if menor_distancia > max_distancia:
                    max_distancia = menor_distancia
                    proximo_centro = i
        centros.append(proximo_centro)
    return centros

#Atribuindo cada ponto ao centro mais próximo

def atribuir_pontos_a_centros(coordenadas, centros):
    atribuicao = {centro: [] for centro in centros}
    for i, ponto in enumerate(coordenadas):
        # Encontra o centro mais próximo manualmente
        centro_mais_proximo = centros[0]
        menor_distancia = calcular_distancia(ponto, coordenadas[centro_mais_proximo])
        for centro in centros[1:]:
            dist = calcular_distancia(ponto, coordenadas[centro])
            if dist < menor_distancia:
                centro_mais_proximo = centro
                menor_distancia = dist
        atribuicao[centro_mais_proximo].append(i)
    return atribuicao

#Calculando o custo total como a soma das distâncias de cada ponto até o centro mais próximo associado

def calcular_custo_total(coordenadas, centros, atribuicao):
    custo_total = 0
    for centro, pontos in atribuicao.items():
        for ponto in pontos:
            custo_total += int(calcular_distancia(coordenadas[ponto], coordenadas[centro]))
    return custo_total

#Resolvendo o problema dos p-centros utilizando o método de agrupamento

def resolve_instancia(coordenadas, p_centros, max_iteracoes=100):
    centros = inicializar_centros(coordenadas, p_centros)
    for _ in range(max_iteracoes):
        atribuicao = atribuir_pontos_a_centros(coordenadas, centros)
        novos_centros = []
        for centro, grupo in atribuicao.items():
            if grupo:  # Ajusta o centro com base no grupo
                x_medio = sum(coordenadas[i][0] for i in grupo) / len(grupo)
                y_medio = sum(coordenadas[i][1] for i in grupo) / len(grupo)
                # Encontra o ponto mais próximo do centro recalculado
                novo_centro = grupo[0]
                menor_distancia = calcular_distancia((x_medio, y_medio), coordenadas[novo_centro])
                for i in grupo[1:]:
                    dist = calcular_distancia((x_medio, y_medio), coordenadas[i])
                    if dist < menor_distancia:
                        novo_centro = i
                        menor_distancia = dist

                novos_centros.append(novo_centro)
            else:  # Mantém o centro original se o grupo estiver vazio
                novos_centros.append(centro)
        if sorted(novos_centros) == sorted(centros):  # Convergência
            break
        centros = novos_centros

        custo_total = calcular_custo_total(coordenadas, centros, atribuicao)
    return centros, atribuicao, custo_total

# Caminho para a pasta com os arquivos CSV
pasta = "arq_instancia"  # Atualizado para o novo nome da pasta

# Lista para armazenar os resultados
resultados = []

# Processando cada arquivo na pasta
for arquivo in os.listdir(pasta):
    caminho_arquivo = os.path.join(pasta, arquivo)  # Caminho completo
    num_pontos, p_centros, min_pontos_centro, max_pontos_centro, coordenadas = le_dados_inst(caminho_arquivo)  # Lê os dados
    centros, atribuicao, custo_total = resolve_instancia(coordenadas, p_centros)  # Executa o algoritmo
    resultados.append((arquivo, num_pontos, p_centros, min_pontos_centro, max_pontos_centro, custo_total, atribuicao))  # Armazena os resultados


# Função para salvar as soluções em um arquivo CSV sem o uso do módulo csv
def salva_solucao(resultados, pasta_saida):
    # Processando cada solução para salvar de acordo com o formato desejado
    for nome_arquivo, num_pontos, p_centros, min_pontos_centro, max_pontos_centro, custo_total, atribuicao in resultados:
        # Criando o caminho do arquivo de saída com base no nome do arquivo de entrada
        caminho_arquivo_saida = os.path.join(pasta_saida, f"solucao_{nome_arquivo}")

        with open(caminho_arquivo_saida, mode='w', encoding='utf-8') as file:
            # Escrevendo o valor objetivo (custo total) como primeira linha
            file.write(f"{custo_total}\n")

            # Escrevendo as alocações dos centros
            for centro, pontos in atribuicao.items():
                pontos_sem_centro = [ponto for ponto in pontos if ponto != centro]  # Remove o centro da lista
                linha = f"{centro};" + ";".join(map(str, pontos_sem_centro)) + "\n"
                file.write(linha)


# Função principal para processar os arquivos e salvar as soluções
def main():
    # Caminho para a pasta com os arquivos CSV
    pasta_entrada = "arq_instancia"  # Atualizar o caminho
    pasta_saida = "arq_solucao"  # Salva as soluções

    # Lista para armazenar os resultados
    resultados = []

    # Processando cada arquivo na pasta
    for arquivo in os.listdir(pasta_entrada):
        caminho_arquivo = os.path.join(pasta_entrada, arquivo)  # Caminho completo do arquivo
        num_pontos, p_centros, min_pontos_centro, max_pontos_centro, coordenadas = le_dados_inst(
            caminho_arquivo)  # Lê os dados
        centros, atribuicao, custo_total = resolve_instancia(coordenadas, p_centros)  # Executa o algoritmo
        resultados.append((arquivo, num_pontos, p_centros, min_pontos_centro, max_pontos_centro, custo_total,
                           atribuicao))  # Armazena os resultado

    # Chama a função para salvar as soluções no arquivo CSV
    salva_solucao(resultados, pasta_saida)


if __name__ == "__main__":
    main()
