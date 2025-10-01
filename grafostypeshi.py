# networkx → para crear grafos (nodos y conexiones)
# matplotlib → para dibujar el grafo
import networkx as nx
import matplotlib.pyplot as plt

# Cada concepto será un nodo en el grafo
# Cada nodo tiene atributos: tipo, unidad, campo de estudio y si es vectorial o no
# vectorial=True significa que tiene dirección (ej. fuerza, velocidad)
# vectorial=False significa que solo tiene magnitud (ej. energía)
categorias = {
    "Fuerza": {"tipo": "magnitud", "unidad": "Newton", "campo": "mecánica", "vectorial": True},
    "Energía cinética": {"tipo": "energía", "unidad": "Joule", "campo": "mecánica", "vectorial": False},
    "Energía potencial": {"tipo": "energía", "unidad": "Joule", "campo": "mecánica", "vectorial": False},
    "Carga eléctrica": {"tipo": "propiedad", "unidad": "Coulomb", "campo": "electromagnetismo", "vectorial": False},
    "Campo eléctrico": {"tipo": "campo", "unidad": "N/C", "campo": "electromagnetismo", "vectorial": True},
    "Velocidad": {"tipo": "magnitud", "unidad": "m/s", "campo": "mecánica", "vectorial": True},
    "Aceleración": {"tipo": "magnitud", "unidad": "m/s²", "campo": "mecánica", "vectorial": True}
}

# Aquí decimos cómo se "parecen" dos nodos del grafo.
# Les damos puntos según lo que tengan en común:
#   +2 si están en el mismo campo de estudio 
#   +2 si tienen la misma unidad 
#   +1 si son del mismo tipo 
#   +1 si los dos son vectoriales o los dos son escalares
def similitud(cat1, cat2):
    score = 0
    
    if cat1["campo"] == cat2["campo"]:
        score += 2
    if cat1["unidad"] == cat2["unidad"]:
        score += 2
    if cat1["tipo"] == cat2["tipo"]:
        score += 1
    if cat1["vectorial"] == cat2["vectorial"]:
        score += 1
    
    return score

# Aquí creamos el grafo y le añadimos los nodos y las aristas
G = nx.Graph()

# Añadimos todos los nodos al grafo
for categoria, atributos in categorias.items():
    G.add_node(categoria, **atributos)  # **atributos mete todo el diccionario dentro del nodo

# Ahora comparamos cada nodo con los demás para ver cuán similares son
# Si tienen alguna similitud, añadimos una arista entre ellos
for c1, a1 in categorias.items():
    for c2, a2 in categorias.items():
        if c1 != c2:  # evitamos comparar un nodo consigo mismo
            peso = similitud(a1, a2)  # calculamos el score de similitud
            if peso > 0:  # solo conectamos si hay algo en común
                G.add_edge(c1, c2, weight=peso)  # añadimos arista con peso = similitud

# Ahora vamos a representar visualmente los conceptos y sus conexiones
pos = nx.spring_layout(G, seed=42)  # posiciones de los nodos en el dibujo (automático)
plt.figure(figsize=(10,7))  # tamaño de la imagen

# Dibujamos los nodos (conceptos físicos)
nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1800)

# Dibujamos las etiquetas (los nombres: Fuerza, Velocidad, etc.)
nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

# Dibujamos las conexiones (aristas) entre nodos
edges = G.edges(data=True)
nx.draw_networkx_edges(G, pos, edgelist=edges)

# Mostramos el peso de cada arista (qué tan similares son los conceptos)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v): d["weight"] for u,v,d in edges})

plt.title("Grafo de conceptos de física", fontsize=14)
plt.axis("off")  # quitamos ejes porque no hacen falta
plt.show()

# Dado un concepto (ej. "Velocidad"), buscamos los más parecidos en el grafo
# Ordenamos por el peso de las conexiones y devolvemos los mejores
def conceptos_similares(nombre_categoria, top=3):
    if nombre_categoria not in G:  # si el concepto no existe, devolvemos vacío
        return []
    vecinos = G[nombre_categoria]  # buscamos los nodos conectados
    similares = sorted(vecinos.items(), key=lambda x: x[1]["weight"], reverse=True)  # los ordenamos por peso
    return [(n, d["weight"]) for n, d in similares[:top]]  # devolvemos los top mejores

for concepto in categorias.keys():  # recorremos cada nodo del grafo
    print(f"\nConceptos similares a '{concepto}':")
    similares = conceptos_similares(concepto, top=3)  # buscamos los 3 más parecidos
    if similares:
        for nombre, peso in similares:
            print(f"  - {nombre} (similitud = {peso})")
    else:
        print("  No tiene conceptos similares.")
