import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from scipy.spatial.distance import euclidean

# ----------------------------------------------------
# 1. PARTE 1: GERAÇÃO DE DADOS E AGRUPAMENTO (K-MEANS)
# ----------------------------------------------------

# Definindo Parâmetros
N_PEDIDOS = 25
K_ENTREGADORES = 4
SEDE_LAT, SEDE_LON = -23.5505, -46.6333  # Coordenadas da Sede (Ex: São Paulo)

print("--- ETAPA 1: AGRUPAMENTO (K-MEANS) ---")

# A. Geração de Dados Simulado
np.random.seed(42) # Para reprodutibilidade
data = {
    'ID_Pedido': range(1, N_PEDIDOS + 1),
    'Lat': np.random.normal(SEDE_LAT, 0.08, N_PEDIDOS),
    'Lon': np.random.normal(SEDE_LON, 0.1, N_PEDIDOS)
}
df = pd.DataFrame(data)

# B. Aplicação do Algoritmo K-Means
coords = df[['Lat', 'Lon']].values
# Definimos random_state=0 para que os resultados sejam sempre os mesmos
kmeans = KMeans(n_clusters=K_ENTREGADORES, random_state=0, n_init='auto')
df['Cluster_ID'] = kmeans.fit_predict(coords)

print(f"Dados Gerados: {N_PEDIDOS} Pedidos.")
print(f"K-Means aplicado, gerando {K_ENTREGADORES} rotas/clusters.")

# Geração dos Pontos Centrais do Cluster (opcional, mas útil)
centroides = kmeans.cluster_centers_

# C. Visualização do Agrupamento K-Means
plt.figure(figsize=(10, 8))
plt.scatter(df['Lon'], df['Lat'], c=df['Cluster_ID'], cmap='viridis', s=100, alpha=0.8, edgecolors='w')
plt.scatter(SEDE_LON, SEDE_LAT, marker='s', color='red', s=300, label='Sede (Ponto Inicial)', edgecolors='black')
# plt.scatter(centroides[:, 1], centroides[:, 0], marker='x', color='blue', s=200, label='Centroides') # Opcional
plt.title('Agrupamento de Entregas (K-Means)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.grid(True)
plt.savefig('grafico_kmeans.png') # Salva o gráfico
plt.show()

# ----------------------------------------------------
# 2. PARTE 2: OTIMIZAÇÃO DE ROTAS (HEURÍSTICA TSP)
# ----------------------------------------------------

print("\n--- ETAPA 2: OTIMIZAÇÃO DE ROTAS (HEURÍSTICA TSP) ---")

def calcular_distancia(p1, p2):
    """Calcula a distância euclidiana entre dois pontos (Lat, Lon)"""
    return euclidean(p1, p2)

def rota_otimizada_heuristica(pontos_cluster, sede_coord):
    """
    Heurística Simples (Nearest Neighbor) para resolver a sequência TSP.
    """
    pontos_visitar = [tuple(p) for p in pontos_cluster.tolist()] # Lista de tuplas (Lat, Lon)
    
    # Adicionar a Sede no início
    rota = [sede_coord]
    distancia_total = 0

    # Construir a rota: ir sempre para o vizinho mais próximo
    while pontos_visitar:
        ponto_atual = rota[-1]
        
        # Encontra o ponto não visitado mais próximo
        distancias = [calcular_distancia(ponto_atual, p) for p in pontos_visitar]
        indice_proximo = np.argmin(distancias)
        
        ponto_proximo = pontos_visitar.pop(indice_proximo)
        
        # Atualiza a rota e a distância
        distancia_total += calcular_distancia(ponto_atual, ponto_proximo)
        rota.append(ponto_proximo)
    
    # Retornar à sede para completar o circuito
    distancia_total += calcular_distancia(rota[-1], sede_coord)
    rota.append(sede_coord)

    rota_df = pd.DataFrame(rota, columns=['Lat', 'Lon'])
    
    return rota_df, distancia_total

# Itera sobre cada cluster (entregador)
todas_rotas = []
total_geral_dist = 0
resultados_tabela = {}

print("Distância das Rotas Otimizadas (Distância Euclidiana):")
for cluster_id in range(K_ENTREGADORES):
    # Seleciona os pontos (coordenadas) do cluster atual
    cluster_points = df[df['Cluster_ID'] == cluster_id][['Lat', 'Lon']].values
    
    # Otimização da Rota
    rota_df, dist_total = rota_otimizada_heuristica(cluster_points, (SEDE_LAT, SEDE_LON))
    
    rota_df['Cluster_ID'] = cluster_id
    todas_rotas.append(rota_df)
    total_geral_dist += dist_total
    
    resultados_tabela[cluster_id] = {
        'Pedidos': len(cluster_points),
        'Distancia': f"{dist_total:.4f}"
    }
    
    print(f"  Entregador {cluster_id}: {len(cluster_points)} paradas. Distância Total: {dist_total:.4f}")

# Exibe o total
print(f"\n--- DISTÂNCIA TOTAL GERAL: {total_geral_dist:.4f} ---")

# D. Visualização das Rotas Otimizadas
rotas_finais_df = pd.concat(todas_rotas, ignore_index=True)

plt.figure(figsize=(10, 8))
cores = plt.cm.get_cmap('viridis', K_ENTREGADORES)

for cluster_id in range(K_ENTREGADORES):
    rota_cluster = rotas_finais_df[rotas_finais_df['Cluster_ID'] == cluster_id]
    
    # Desenha a rota (linha)
    plt.plot(rota_cluster['Lon'], rota_cluster['Lat'], marker='o', 
             linestyle='-', color=cores(cluster_id), linewidth=2, 
             label=f'Rota Entregador {cluster_id}')
    
    # Marca os pontos de entrega
    pedidos_cluster = df[df['Cluster_ID'] == cluster_id]
    plt.scatter(pedidos_cluster['Lon'], pedidos_cluster['Lat'], 
                color=cores(cluster_id), s=150, edgecolors='black', alpha=0.7)

# Marca a Sede por cima
plt.scatter(SEDE_LON, SEDE_LAT, marker='s', color='red', s=400, label='Sede', edgecolors='black', zorder=5)

plt.title('Rotas Otimizadas por Entregador (Heurística Nearest Neighbor)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.legend(loc='upper left')
plt.savefig('grafico_rotas_otimizadas.png') # Salva o gráfico
plt.show()

# Exporta os resultados para preencher o README
print("\n--- Dados para o README.md ---")
for cluster_id, res in resultados_tabela.items():
    print(f"Entregador {cluster_id}: Pedidos={res['Pedidos']}, Distancia={res['Distancia']}")
print(f"Distância Total Geral: {total_geral_dist:.4f}")