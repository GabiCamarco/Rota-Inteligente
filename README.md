# 📦 Rota Inteligente: Otimização de Entregas com K-Means e Heurística TSP

## 📝 Descrição do Projeto

Este projeto implementa uma solução de **Inteligência Artificial** e otimização para resolver o problema logístico da empresa "Sabor Express". Nosso objetivo é transformar rotas manuais e ineficientes em caminhos otimizados, reduzindo custos de combustível e tempo de entrega.

A solução é desenvolvida em Python e baseada em um modelo de duas etapas essenciais para a otimização de rotas:

1.  **Agrupamento Geográfico (Clustering):** Usando **K-Means**.
2.  **Otimização da Sequência de Visitas (TSP Heurístico):** Usando o **Vizinho Mais Próximo**.

---

## 🎯 Abordagem Técnica e Algoritmos

A área de entrega (cidade) é modelada como um **Grafo**, onde os pontos de entrega e a sede são os **nós**, e as conexões entre eles são as arestas.

### 1. Etapa de Agrupamento: K-Means

* **Finalidade:** Dividir os **25 pedidos** simulados em **4 grupos (clusters)**, um para cada entregador ($K=4$).
* **Algoritmo:** **K-Means** (Aprendizado Não Supervisionado).
* **Benefício:** Garante que cada entregador receba apenas pedidos geograficamente próximos, o que é o primeiro passo para a redução drástica da distância percorrida.

### 2. Etapa de Otimização: Heurística do Vizinho Mais Próximo

* **Finalidade:** Encontrar a **melhor sequência de paradas** dentro de cada cluster, minimizando a distância total. Este é um sub-problema do **Caixeiro Viajante (TSP)**.
* **Estratégia:** O entregador sai da Sede e, em cada ponto, escolhe o pedido **não visitado** que está **mais próximo** (guloso), retornando à Sede no final.

### 💡 Conexão com o Algoritmo A-Estrela ($A^{*}$)

Em um sistema de roteirização real, o algoritmo **$A$-Estrela ($A^{*}$)** seria o responsável por encontrar o **caminho mais curto real** (por ruas) entre uma parada e a próxima, navegando no grafo da cidade. O uso da distância Euclidiana em nosso código simula a função de custo que o $A^{*}$ utilizaria.

---

## 📊 Resultados e Análise

O código rodou uma simulação com 25 pedidos (coordenadas geográficas simuladas) e 4 entregadores, partindo de uma Sede centralizada.

### Tabela de Distâncias Otimizadas

A tabela abaixo mostra a eficiência da otimização para cada rota (Entregador), medida pela distância Euclidiana total:

| Entregador (Cluster ID) | Pedidos Atribuídos | Distância Total Percorrida (Simulada - Unidades) |
| :--- | :--- | :--- |
| **0** | **2** | **0.4315** |
| **1** | **8** | **0.5525** |
| **2** | **8** | **0.6931** |
| **3** | **7** | **0.4883** |
| **TOTAL GERAL** | **25** | **2.1654** |

> **Análise de Eficiência:** A **Distância Total Otimizada** de **2.1654** unidades demonstra a eficácia da abordagem combinada (K-Means + Heurística). Esta otimização se traduz em redução de custos operacionais e maior capacidade de entrega por hora.

### Visualizações (Geradas pelo Script)

| Etapa | Imagem Gerada | Descrição |
| :--- | :--- | :--- |
| **Agrupamento** | `grafico_kmeans.png` | Mapa dos 25 pedidos coloridos em 4 clusters distintos e a Sede (quadrado vermelho). |
| **Otimização** | `grafico_rotas_otimizadas.png` | Visualização das 4 rotas (linhas coloridas) geradas pela heurística, partindo da Sede, visitando os pedidos do cluster e retornando à Sede. |

---

## 🔍 Pesquisa: Otimização em Escala (UPS ORION)

A solução da "Sabor Express" utiliza princípios semelhantes aos encontrados em grandes sistemas logísticos.

O sistema **UPS ORION** (*On-Road Integrated Optimization Navigator*) é um exemplo mundial. Ele utiliza milhões de dados em tempo real e algoritmos complexos (como a Programação Linear Inteira Mista) para otimizar as rotas de dezenas de milhares de motoristas.

O sucesso do ORION reforça a abordagem deste projeto: **a IA é fundamental para segmentar e otimizar rotas, garantindo a máxima eficiência e economia de recursos.** O uso do **K-Means** no nosso projeto imita o princípio de **dividir o problema** geograficamente antes de aplicar a otimização de sequência.

---

## ⚙️ Como Executar o Projeto

1.  **Clone o Repositório:** Obtenha o arquivo `rota_inteligente.py`.
2.  **Instale as Dependências:**
    ```bash
    pip install numpy pandas scikit-learn matplotlib scipy
    ```
3.  **Execute o Script:**
    ```bash
    python main.py
    ```

**🎥 Vídeo Pitch:** Assista à explicação detalhada e a demonstração dos resultados aqui: **[INSERIR LINK DO SEU VÍDEO NO YOUTUBE AQUI]**
