| População | Mutação | Melhor Fitness | Geração de Convergência | Violações |
|----------|--------|---------------|------------------------|----------|
| 50       | 0.05   | 326200        | 160                    | 11        |
| 50       | 0.20   | 328500        | 160                    | 0        |
| 100      | 0.05   | 335200        | 160                    | 4        |
| 100      | 0.20   | 327000        | 20                    | 0        |


```mermaid
xychart-beta
    title "Evolução do Fitness — pop=50, mut=0.05"
    x-axis "Geração" [0, 30, 60, 90, 120, 150, 180]
    y-axis "Fitness" 280000 --> 350000
    line [283300, 314200, 320800, 320800, 322200, 322200, 326200]
```

```mermaid
xychart-beta
    title "Evolução do Fitness — pop=50, mut=0.20"
    x-axis "Geração" [0, 30, 60, 90, 120, 150, 180]
    y-axis "Fitness" 280000 --> 350000
    line [278800, 299800, 314000, 314000, 316500, 321500, 328500]
```

```mermaid
xychart-beta
    title "Evolução do Fitness — pop=100, mut=0.05"
    x-axis "Geração" [0, 30, 60, 90, 120, 150, 180]
    y-axis "Fitness" 280000 --> 350000
    line [286800, 326500, 326500, 329500, 331500, 331500, 335200]
```

```mermaid
xychart-beta
    title "Evolução do Fitness — pop=100, mut=0.20"
    x-axis "Geração" [0, 30, 60, 90, 120, 150, 180]
    y-axis "Fitness" 280000 --> 340000
    line [300300, 327000, 327000, 327000, 327000, 327000, 327000]
```

**Conclusões**
- Por conta da nossa reparação, taxas de mutação baixas (0.05) produziram soluções com muitos erros.
- Mutação alta (0.20) diminuiu o fitness final em troca de 0 violações.
- População maior (100) convergiu mais rápido e com maior estabilidade.
- O algoritmo depende de uma taxa de mutação maior, mas consegue resolver o problema com estabilidade com os parâmetros corretos.
