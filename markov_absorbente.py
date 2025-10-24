import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io, base64

def procesar_markov(P):
    P = np.array(P)
    n = len(P)
    absorbentes = [i for i in range(n) if P[i, i] == 1]
    no_absorbentes = [i for i in range(n) if P[i, i] != 1]

    Q = P[np.ix_(no_absorbentes, no_absorbentes)]
    R = P[np.ix_(no_absorbentes, absorbentes)]

    I = np.eye(len(Q))
    N = np.linalg.inv(I - Q)
    B = np.dot(N, R)

    return Q, R, N, B, absorbentes, no_absorbentes

def graficar_matriz(P):
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        P,
        annot=True,           
        fmt=".2f",            
        cmap="YlGnBu",        
        cbar=True,
        square=True,
        linewidths=0.5,
        linecolor='white',
        ax=ax
    )
    ax.set_title("Matriz de Transición", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Estado j", fontsize=12)
    ax.set_ylabel("Estado i", fontsize=12)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight", dpi=200)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()