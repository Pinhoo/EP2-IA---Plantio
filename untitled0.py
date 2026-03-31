import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--pop", type=int, default=100)
parser.add_argument("--gen", type=int, default=500)
parser.add_argument("--mut", type=float, default=0.25)
parser.add_argument("--cross", type=float, default=1.0)
args = parser.parse_args()

NUM_TALHOES = 16
NUM_ESTACOES = 4
TAM = NUM_TALHOES * NUM_ESTACOES

estacoes = [
    ["Verão", 5000, 80],
    ["Outono", 3500, 60],
    ["Inverno", 2500, 40],
    ["Primavera", 4000, 70]
]

tp_solo = ["Argiloso", "Arenoso", "Misto"]
mapa_terrenos = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 2, 2, 2, 2, 2, 2]

plantios = [
  ["Soja", 8000, [0, 2], [0, 1], 400, "Alto", 6],
  ["Milho", 7000, [0, 2], [0, 3], 350, "Alto", 5],
  ["Trigo", 5000, [1, 2], [2, 1], 200, "Médio", 4],
  ["Café", 12000, [0], [0, 1, 2, 3], 500, "Baixo", 8],
  ["Cana", 9000, [2], [0, 1], 600, "Baixo", 7],
  ["Algodão", 6500, [0], [0, 3], 300, "Alto", 5],
  ["Feijão", 4500, [0, 1, 2], [1, 2], 150, "Médio", 3],
  ["Pousio", 0, [0, 1, 2], [0, 1, 2, 3], 0, "Nenhum", 0]
]

def get_gene(ind, t, e):
    return ind[t * NUM_ESTACOES + e]

def set_gene(ind, t, e, val):
    ind[t * NUM_ESTACOES + e] = val

def vizinhos(t):
    v = []
    if t > 0: v.append(t-1)
    if t < NUM_TALHOES-1: v.append(t+1)
    return v

def reparar(ind):
    for t in range(NUM_TALHOES):
        for e in range(NUM_ESTACOES):
            c = get_gene(ind, t, e)
            solo = mapa_terrenos[t]
            if (solo not in plantios[c][2]) or (e not in plantios[c][3]):
                opcoes = [i for i,p in enumerate(plantios) if solo in p[2] and e in p[3]]
                set_gene(ind, t, e, random.choice(opcoes) if opcoes else 7)

    for t in range(NUM_TALHOES):
        for e in range(NUM_ESTACOES):
            c1 = get_gene(ind, t, e)
            c2 = get_gene(ind, t, (e+1)%4)
            if c1 == c2 and plantios[c1][0] != "Pousio":
                set_gene(ind, t, (e+1)%4, 7)

    for t in range(NUM_TALHOES):
        tem_cafe = any(plantios[get_gene(ind, t, e)][0] == "Café" for e in range(4))
        if tem_cafe:
            for e in range(4):
                set_gene(ind, t, e, 3)

    for t in range(NUM_TALHOES):
        nomes = [plantios[get_gene(ind, t, e)][0] for e in range(4)]
        if "Café" not in nomes and "Pousio" not in nomes:
            set_gene(ind, t, random.randint(0,3), 7)

    for e in range(NUM_ESTACOES):
        for _ in range(10):
            consumo = sum(plantios[get_gene(ind, t, e)][4] for t in range(NUM_TALHOES))
            mao = sum(plantios[get_gene(ind, t, e)][6] for t in range(NUM_TALHOES))
            if consumo <= estacoes[e][1] and mao <= estacoes[e][2]:
                break
            t = random.randint(0, NUM_TALHOES-1)
            set_gene(ind, t, e, 7)

    for e in range(NUM_ESTACOES):
        for t in range(NUM_TALHOES):
            c1 = get_gene(ind, t, e)
            risco1 = plantios[c1][5]
            for v in vizinhos(t):
                c2 = get_gene(ind, v, e)
                risco2 = plantios[c2][5]
                if (risco1 == "Alto" and risco2 == "Alto") or (risco1 == "Médio" and risco2 == "Médio"):
                    set_gene(ind, v, e, 7)
    return ind

def fitness(ind):
    R_total = 0
    viol = {"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0,"R7":0,"R8":0}

    for t in range(NUM_TALHOES):
        for e in range(NUM_ESTACOES):
            c = get_gene(ind, t, e)
            cultura = plantios[c]
            R_total += cultura[1]
            if mapa_terrenos[t] not in cultura[2]: viol["R1"] += 1
            if e not in cultura[3]: viol["R2"] += 1

    for e in range(NUM_ESTACOES):
        consumo = sum(plantios[get_gene(ind, t, e)][4] for t in range(NUM_TALHOES))
        if consumo > estacoes[e][1]: viol["R3"] += consumo - estacoes[e][1]

    for e in range(NUM_ESTACOES):
        mao = sum(plantios[get_gene(ind, t, e)][6] for t in range(NUM_TALHOES))
        if mao > estacoes[e][2]: viol["R4"] += mao - estacoes[e][2]

    for t in range(NUM_TALHOES):
        for e in range(NUM_ESTACOES):
            c1 = get_gene(ind, t, e)
            c2 = get_gene(ind, t, (e+1)%4)
            if c1 == c2 and plantios[c1][0] not in ["Pousio","Café"]:
                viol["R5"] += 1

    for e in range(NUM_ESTACOES):
        for t in range(NUM_TALHOES):
            c1 = get_gene(ind, t, e)
            risco1 = plantios[c1][5]
            for v in vizinhos(t):
                c2 = get_gene(ind, v, e)
                risco2 = plantios[c2][5]
                if risco1 == risco2 and risco1 in ["Alto","Médio"]:
                    viol["R6"] += 1

    for t in range(NUM_TALHOES):
        tem_cafe = any(plantios[get_gene(ind, t, e)][0] == "Café" for e in range(4))
        if tem_cafe:
            for e in range(4):
                if plantios[get_gene(ind, t, e)][0] != "Café":
                    viol["R7"] += 1

    for t in range(NUM_TALHOES):
        count = sum(1 for e in range(4) if plantios[get_gene(ind, t, e)][0] == "Pousio")
        if count == 0: viol["R8"] += 1

    pesos = {"R1":1000,"R2":1000,"R3":5000,"R4":500,"R5":5000,"R6":400,"R7":20000,"R8":800}
    penalidade = sum(pesos[r]*viol[r] for r in viol)

    return R_total - penalidade

def gerar_individuo():
    ind = []
    for t in range(NUM_TALHOES):
        for e in range(NUM_ESTACOES):
            solo = mapa_terrenos[t]
            opcoes = [i for i,p in enumerate(plantios) if solo in p[2] and e in p[3]]
            ind.append(random.choice(opcoes) if opcoes else 7)
    return ind

def crossover(p1, p2):
    corte = random.randint(0, TAM-1)
    return p1[:corte] + p2[corte:]

def mutacao(ind):
    for i in range(TAM):
        if random.random() < args.mut:
            ind[i] = random.randint(0, len(plantios)-1)
    return ind

def selecao(pop):
    return max(random.sample(pop, 3), key=fitness)

def GA():
    pop = [reparar(gerar_individuo()) for _ in range(args.pop)]
    for g in range(args.gen):
        nova = sorted(pop, key=fitness, reverse=True)[:int(0.05*args.pop)]
        while len(nova) < args.pop:
            p1 = selecao(pop)
            p2 = selecao(pop)
            filho = crossover(p1, p2) if random.random() < args.cross else p1[:]
            filho = mutacao(filho)
            if random.random() < 0.1:
                filho = reparar(filho)
            nova.append(filho)
        pop = nova
        if g % 10 == 0:
            print(f"Geração {g} | Fitness: {fitness(max(pop, key=fitness))}")
    return max(pop, key=fitness)

def analisar_individuo(ind):
    violacoes = []
    total = 0

    for t in range(NUM_TALHOES):
        for e in range(NUM_ESTACOES):
            c = get_gene(ind, t, e)
            cultura = plantios[c]

            if mapa_terrenos[t] not in cultura[2]:
                violacoes.append((t, "R1", cultura[0]))
                total += 1

            if e not in cultura[3]:
                violacoes.append((t, "R2", cultura[0]))
                total += 1

    for e in range(NUM_ESTACOES):
        consumo = sum(plantios[get_gene(ind, t, e)][4] for t in range(NUM_TALHOES))
        if consumo > estacoes[e][1]:
            violacoes.append(("GLOBAL", "R3", estacoes[e][0]))
            total += 1

    for e in range(NUM_ESTACOES):
        mao = sum(plantios[get_gene(ind, t, e)][6] for t in range(NUM_TALHOES))
        if mao > estacoes[e][2]:
            violacoes.append(("GLOBAL", "R4", estacoes[e][0]))
            total += 1

    for t in range(NUM_TALHOES):
        for e in range(NUM_ESTACOES):
            c1 = get_gene(ind, t, e)
            c2 = get_gene(ind, t, (e+1)%4)
            if c1 == c2 and plantios[c1][0] not in ["Pousio","Café"]:
                violacoes.append((t, "R5", plantios[c1][0]))
                total += 1

    for e in range(NUM_ESTACOES):
        for t in range(NUM_TALHOES):
            c1 = get_gene(ind, t, e)
            risco1 = plantios[c1][5]
            for v in vizinhos(t):
                c2 = get_gene(ind, v, e)
                risco2 = plantios[c2][5]
                if risco1 == risco2 and risco1 in ["Alto","Médio"]:
                    violacoes.append((t, "R6", f"{plantios[c1][0]}-{plantios[c2][0]}"))
                    total += 1

    for t in range(NUM_TALHOES):
        tem_cafe = any(plantios[get_gene(ind, t, e)][0] == "Café" for e in range(4))
        if tem_cafe:
            for e in range(NUM_ESTACOES):
                if plantios[get_gene(ind, t, e)][0] != "Café":
                    violacoes.append((t, "R7", "Café inconsistente"))
                    total += 1

    for t in range(NUM_TALHOES):
        count = sum(1 for e in range(NUM_ESTACOES) if plantios[get_gene(ind, t, e)][0] in ["Pousio", "Café"])
        if count == 0:
            violacoes.append((t, "R8", "Sem pousio"))
            total += 1

    return violacoes, total

def imprimir_resultado(ind):
    print("\nPlano Anual de Plantio:\n")
    print("Talhão | Verão    | Outono   | Inverno  | Primavera | Receita")
    print("-------|----------|----------|----------|-----------|--------")

    receita_total = 0
    violacoes, total_violacoes = analisar_individuo(ind)

    for t in range(NUM_TALHOES):
        linha = []
        receita_t = 0
        erros_t = []

        for e in range(NUM_ESTACOES):
            c = get_gene(ind, t, e)
            nome = plantios[c][0]
            linha.append(nome.ljust(8))
            receita_t += plantios[c][1]

        # verificar violações nesse talhão
        for v in violacoes:
            if v[0] == t:
                erros_t.append(v)

        receita_total += receita_t

        linha_str = " | ".join(linha)

        if erros_t:
            msg = f" ← INVÁLIDO: {erros_t[0][1]} ({erros_t[0][2]})!"
        else:
            msg = ""

        print(f"T{str(t+1).zfill(2)}    | {linha_str} | R$ {receita_t:,.0f}{msg}")
    print("\nConsumo hídrico por estação:")


    for e in range(NUM_ESTACOES):
        consumo = sum(plantios[get_gene(ind, t, e)][4] for t in range(NUM_TALHOES))
        limite = estacoes[e][1]

        status = "✓" if consumo <= limite else "✗"

        print(f"  {estacoes[e][0]:10}: {consumo:,.0f} / {limite:,.0f} m³ {status}")
        
    print("\nMão de obra por estação:")
    for e in range(NUM_ESTACOES):
        consumo = sum(plantios[get_gene(ind, t, e)][6] for t in range(NUM_TALHOES))
        limite = estacoes[e][2]

        status = "✓" if consumo <= limite else "✗"
        print(f"  {estacoes[e][0]:10}: {consumo:,.0f} / {limite:,.0f} m³ {status}")
        

    print(f"\nReceita Total: R$ {receita_total:,.0f}")
    print(f"Violações: {total_violacoes}")

melhor = GA()
imprimir_resultado(melhor)
print("Fitness:", fitness(melhor))