import csv
def ler_dados_instancia(arq_instancia):
    # Armazena as coordenadas e as distâncias
    coords = list()
    dists = list()
    # Abre o arquivo e lê todas as linhas
    with open(arq_instancia, 'r', encoding='utf8') as f:
        linhas = f.readlines()
        # Lê os parametros
        qtd_pontos = int(linhas[1].strip().split(';')[0])
        qtd_centros = int(linhas[1].strip().split(';')[1])
        lig_min = int(linhas[1].strip().split(';')[2])
        lig_max = int(linhas[1].strip().split(';')[3]) 
        
        
        print( qtd_centros)
        print(qtd_pontos)
        print(lig_min)
        print(lig_max)
        del linhas[:3]
     # Lê as coordenadas dos pontos
        for i in range(qtd_pontos):
            linha = linhas[i]
            v_linha = linha.strip().split(';')
            x = int(v_linha[1])
            y = int(v_linha[2])
            coords.append([x, y])
        print(coords)
        # Lê a matriz de distâncias
        del linhas[:qtd_pontos + 2]
        for i in range(qtd_pontos):
            v_linha = linhas[i].strip().split(';')
            linha_dist = list()
            for s in v_linha[1:]:
                linha_dist.append(int(s))
            dists.append(linha_dist)
            print(dists)
    return  qtd_pontos, qtd_centros, lig_min, lig_max, coords, dists  
   
def teste_de_sanidade(qtd_pontos, qtd_centros, lig_min, lig_max, coords, dists, arquivo_saida):
    with open(arquivo_saida, 'w+', newline='', encoding='utf8') as f:
        f.write("Parâmetros\n")
        f.write(f"qtd_pontos;{qtd_pontos}\n")
        f.write(f"qtd_centros;{qtd_centros}\n")
        f.write(f"lig_min;{lig_min}\n")
        f.write(f"lig_max;{lig_max}\n\n")

        # Escrever as coordenadas
        f.write("Coordenadas\n")
        f.write("X;Y\n")
        for x, y in coords:
            f.write(f"{x};{y}\n")
        f.write("\n")  # Linha vazia para separação

        # Escrever a matriz de distâncias
        f.write("Matriz de Distâncias\n")
        for linha in dists:
            f.write(";".join(map(str, linha)) + "\n")
       
    
     
def main():
 qtd_pontos, qtd_centros, lig_min, lig_max, coords, dists = ler_dados_instancia("Instancias_nao_resolvidas/inst_01_n25_k3.csv")
 teste_de_sanidade(qtd_pontos, qtd_centros, lig_min, lig_max, coords, dists, "sanidade.csv")





if __name__ == "__main__":
    main()