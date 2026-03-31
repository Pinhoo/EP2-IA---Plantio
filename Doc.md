
# Modelagem do Problema

## Cromossomo

A ideia deste problema é descorbrir o melhor plano de plantio de uma fazenda no período de um ano. Aqui cada **gene** indica qual a cultura a ser plantada dentro de cada período da estação em um dos 16 talhões disponíveis da fazenda. Ou seja, cada posição dos cromossomos decidem o que vai ser plantado ao longo do ano 

A organização dos genes segue a lógica:

```
índice = talhão × número de estações + estação
```

### Domínio dos valores

Cada gene pode assumir um valor inteiro que representa uma cultura:

- 0 → Soja  
- 1 → Milho  
- 2 → Trigo  
- 3 → Café  
- 4 → Cana  
- 5 → Algodão  
- 6 → Feijão  
- 7 → Pousio  

### Tamanho do cromossomo

O problema considera:

- 16 talhões  
- 4 estações do ano  

Portanto:

```
16 × 4 = 64 genes
```

---

## Função de Aptidão

A função de aptidão (fitness) tem como objetivo **maximizar o lucro total**, levando ao código a descartar soluções que violem as regras do problema.

### Fórmula geral

```
Fitness = Receita Total − Penalidades − Penalidade por excesso de pousio
```

### Receita

A receita é calculada somando o lucro de todas as culturas plantadas:

```
Receita Total = soma dos lucros de todas as culturas
```

---

### Penalidades

Cada restrição gera penalidade quando não é respeitada. Os pesos foram definidos de acordo com a importância de cada regra:

| Restrição | Descrição | Peso |
|----------|----------|------|
| R1 | Solo incompatível | 1000 |
| R2 | Estação inválida | 1000 |
| R3 | Excesso de água | 5000 |
| R4 | Excesso de mão de obra | 500 |
| R5 | Falha na rotação | 5000 |
| R6 | Conflito entre vizinhos | 400 |
| R7 | Regra do café | 5000 |
| R8 | Falta de pousio | 800 |

Além disso, existe uma penalidade de **600** para casos de **pousio em excesso** (pousios>1), evitando desperdício de espaço.

### Justificativa dos pesos
Nesse caso os pesos foram escolhidos de maneira arbitrária a fim de remover as restrições violadas com mais frequência enquanto ainda permite diversidade genética, evitando que o fitness fique travado em todas as gerações

## Operadores

### Seleção

Foi utilizado o método de **torneio (k = 3)**:

- 3 indivíduos são escolhidos aleatoriamente  
- o melhor entre eles é selecionado  

---

### Crossover

O crossover adotado é de **um ponto**:

- um ponto aleatório divide os cromossomos dos pais  
- o filho é formado combinando partes de cada um  

```
filho = p1[:corte] + p2[corte:]
```

Promovendo diversidade
---

### Mutação

A mutação é parametrizavel e quando ocorre, o gene recebe uma nova cultura aleatória  

---

### Tratamento das restrições

Os operadores (crossover e mutação) **não garantem diretamente soluções válidas** e por isso, foi implementada uma **função de reparo**, que corrige automaticamente restrições violadas

---

## Inicialização

A população inicial é gerada de forma **aleatória com restrições básicas**, ou seja:

- apenas culturas compatíveis com o solo e a estação são escolhidas  
- a regra do café já é aplicada durante a criação  
- em seguida, a função de reparo ajusta possíveis inconsistências  

---

## Critério de Parada

Nosso critério é baseado no número de gerações que também é parametrizavel

Não foi utilizado critério de convergência, mas isso poderia ser uma melhoria futura caso tivessemos mais tempo

---

## Considerações Finais

O modelo proposto busca equilibrar:

- **refinamento** (com a função de reparo)  
- **pressão seletiva** (via seleção por torneio)  

Na prática, isso permite encontrar soluções viáveis e com bom retorno econômico, mesmo diante de várias restrições.
A função de reparo, em especial, é uma parte essencial da abordagem, garantindo que o algoritmo não evolua soluções inviáveis.