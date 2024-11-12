import csv
#Problema de P-centros | que Deus tenha piedade de nós.

#pare de gritar eu também estou com medo...




def ler_dados_instancia(arq_instancia):
    with open(arq_instancia, 'r', newline='', encoding='utf8') as inst_file:
        read = csv.reader(inst_file, delimiter=';')
        
    
        # le os parametros
        next(read)  # pula header
        params = next(read)  # le a segunda linha

     # extrair parametros individuais
        #temp_linha = inst_file.readline()
        #num_pontos = int(temp_linha[2].strip().split(',')[1])
        num_pontos = int(params[0])    # numero de pontos
        num_centros = int(params[1])   # numero de centros
        min_conect = int(params[2])  # conec. minima
        max_conect = int(params[3])  # conec. maxima
        xy_pos = []  # invoca lista para popular com posições //                    não me julgue, eu vim do C# :(
        matriz_dist = []  # invoca lista para popular a matriz de distancias
        print("numero de pontos:", num_pontos)
        print("numero de centros:", num_centros)
        print("conexões minimas:", min_conect)
        print("conexões maximas:", max_conect) # teste de sanidade, sim está no lugar errado mas estava ficando maluco.
        # ler as linhas de cordenadas
        ### que saudade dos Dictionaries, até dos Delegate(), estou ficando velho
        next(read)  #pular o header
        for r in range(num_pontos):
            row = next(read)
            point_id, x, y = int(row[0]), int(row[1]), int(row[2])
            xy_pos.append((x, y))
    
        #  pula o header de distancia //                                         eu sei que é uma maneira burra, mas foi a unica que eu consegui
        next(read)
        #  ler as linhas da matriz de distancia
        
        for i in range(num_pontos):
            row = next(read)
            
            
            linha_dist = [int(s) for s in row[1:]]
            matriz_dist.append(linha_dist)
            
        print("posição X,Y do primeiro ponto pra ver se eu não estou ficando louco:", xy_pos[0])
        print("distancia do ponto 0 ao ponto 1, também para ver se eu não estou maluco:", matriz_dist[2] [3])
                        #não consigo fazer o dist[1][2] ser a distancia do ponto 1 pra o ponto 2, tenho q dar offset de 1 no primeiro termo, não sei resolver





def main():
    ler_dados_instancia("pcentros_trabalho/Instancias_nao_resolvidas/inst_01_n25_k3.csv")
    





if __name__ == "__main__":
    main()