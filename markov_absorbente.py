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
    plt.imshow(P, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(label='Probabilidad')
    plt.title("Matriz de Transición")
    plt.xlabel("Estado j")
    plt.ylabel("Estado i")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()