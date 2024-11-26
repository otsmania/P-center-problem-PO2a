import csv #se pa q vou tirar isso aq dps, mas n sei ainda pq exportar dado é mt triste

#Problema de P-centros | que Deus tenha piedade de nós.

#pare de gritar eu também estou com medo...

#EU ODEIO INDENTAÇÃO, NÃO TINHA NADA DE ERRADO COM ' { } ' , ABSOLUTAMENTE NINGUEM RECLAMOU NUNCA.  

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
        #finalmente funcionou
        del linhas[:qtd_pontos + 2]
        for i in range(qtd_pontos):
            v_linha = linhas[i].strip().split(';')
            linha_dist = list()
            for s in v_linha[1:]:
                linha_dist.append(int(s))
            dists.append(linha_dist)
            print(dists)
    return  qtd_pontos, qtd_centros, lig_min, lig_max, coords, dists  #nao mude isso por tudo que é mais sagrado nesse mundo
   
   #tem muito número na minha tela, eu quero minha mãe
   
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



#                                                                           #HEURISTICA#                                                             #
#atenção, apartir dessa linha para baixo, não há mais esperanças, apenas tristeza e confusão te aguarda, cada linha que se passa Deus se afasta mais dos homens. 
def heuristica_distancia_maxima(dists, qtd_centros, lig_min, lig_max):
   
   
    centros = [0]  #pegar o primeiro ponto pq tem q ser deterministica random n pode 
    while len(centros) < qtd_centros:
        max_dist = -1
        novo_centro = -1
        for i in range(len(dists)):
            if i in centros:
                continue
            
            dist_min = min(dists[i][c] for c in centros) #pega a menor distancia do ponto atual (i) até o proximo 
            # Encontrar o ponto mais distante
            if dist_min > max_dist:
                max_dist = dist_min
                novo_centro = i
        centros.append(novo_centro)

    # juntar os ponto nos respectivo centro
    atribuicoes = {c: [] for c in centros}  #pelo menos python tem dict, só falta tirar identação e função delegate pra ficar bom.
    for i in range(len(dists)):
        if i in centros:
            continue
        # coloca o ponto atual no centro q ta mais perto
        distancias = [(c, dists[i][c]) for c in centros]
        distancias.sort(key=lambda x: x[1])  # até agora não sei como  função lambda existe, como q uma função anonima cai na memória?, Mas eu gosto da letra então eu vou deixar passar
        for c, _ in distancias:                          #taquei na net e isso aq ordena tupla com base no primeiro valor, pra eu ordenar os valores do menor pro maior
            if len(atribuicoes[c]) < lig_max:
                atribuicoes[c].append(i)
                break

    # distribuir os ponto pelo min-max
    for c in atribuicoes:
        while len(atribuicoes[c]) < lig_min:  #assaltando os ponto dos vizinho se o minimo nao chegou, perdeu playboy
            
            mais_proximo = None
            menor_dist = float("inf")
            for i in range(len(dists)):
                if i in atribuicoes[c] or i in centros:
                    continue
                dist = dists[i][c]
                if dist < menor_dist and any(
                    len(atribuicoes[cn]) > lig_min for cn in centros if cn != c
                ):
                    menor_dist = dist
                    mais_proximo = i
            if mais_proximo is not None:
                atribuicoes[c].append(mais_proximo)
                for cn in centros:
                    if mais_proximo in atribuicoes[cn]:
                        atribuicoes[cn].remove(mais_proximo)
                        break

    #soma tudo pra dar um custo total, essa aq q eu to com medo  ->>>> perguntar pro professor pq eu n faço ideia do q eu estou fazendo.
    custo_total = 0
    for c in atribuicoes:
        for p in atribuicoes[c]:
            custo_total += dists[p][c]

    #print criminoso só pra eu ver qq ta acontecendo por que eu não fiz o output ainda.
    resultado = [str(custo_total)]
    for c in atribuicoes:
        linha = [str(c)] + [str(p) for p in atribuicoes[c]]
        resultado.append(";".join(linha))
    
    return resultado, custo_total, atribuicoes

def resolve_instancia(arq_instancia, arq_solucao):
    
    qtd_pontos, qtd_centros, lig_min, lig_max, coords, dists = ler_dados_instancia(arq_instancia)
    
    
    resultado, custo_total, atribuicoes = heuristica_distancia_maxima(dists, qtd_centros, lig_min, lig_max)
    
    
    with open(arq_solucao, "w", encoding="utf8") as f:
        for linha in resultado:
            f.write(linha + "\n")
    
    print(f"Solução salva em {arq_solucao}")




#sim, está feio, não, não funciona bem, mas funciona o *suficiente*     
def main():
 qtd_pontos, qtd_centros, lig_min, lig_max, coords, dists = ler_dados_instancia("Instancias_nao_resolvidas/inst_24_n100_k5.csv")
 teste_de_sanidade(qtd_pontos, qtd_centros, lig_min, lig_max, coords, dists, "sanidade_pra_carlho.csv")
 resultado = heuristica_distancia_maxima(dists, qtd_centros, lig_min, lig_max)
 print("------------")
 for linha in resultado:
     print(linha)
 
 
       


#que saudade de escrever C#
if __name__ == "__main__":
    main()