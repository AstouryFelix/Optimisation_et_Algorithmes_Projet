import math
import json
import gurobipy as gp
from gurobipy import GRB, nlfunc as nl
import matplotlib.pyplot as plt

# ============================= Explications ============================= #

# Un DataCenter possède toute les vidéos de la plateforme
# Les endpoints prédisent la demande de vidéo
# Les CacheServers ont une latence avec les endpoints auquels ils sont connectés
# 

# ============================= Parameters ============================= #

# ----- Load data from .in -----
V    = 0   # The number of videos                                                                  (1 ≤ V ≤ 10000)
E    = 0   # The number of endpoints                                                               (1 ≤ E ≤ 1000)
R    = 0   # The number of request descriptions                                                    (1 ≤ R ≤ 1000000)
C    = 0   # The number of cache servers                                                           (1 ≤ C ≤ 1000)
X    = 0   # The capacity of each cache server in megabytes                                        (1 ≤ X ≤ 500000)
S    = []  # The size of video i < V in megabytes                                                  (1 ≤ S[V] ≤ 1000)
Ld   = []  # The latency of serving a video request from the data center to this endpoint, in ms   (2 ≤ ld[E] ≤ 4000)
K    = []  # The number of cache servers that this endpoint is connected to.                       (0 ≤ K[C] ≤ C) 
C_id = []  # The ID of the cache server.                                                           (0 ≤ c < C)

Lc   = []  # The latency of serving a video request from this cache server  
           # to this endpoint, in ms. You can assume that latency from the   
           # cache is strictly lower than latency from the data center                             (1 ≤ Lc < ld of endpoint)

Rv   = []  # The ID of the requested video                                                         (0 ≤ Rv < V)
Re   = []  # The ID of the endpoint from which the requests are coming from                        (0 ≤ Re < E)
Rn   = []  # The number of requests                                                                (0 < Rn ≤ 10000)


# with open("videos/datasets/trending_4000_10k.in", "r") as f:
with open("videos/datasets/example.in", "r") as f:
    firstline  = list(map(int, f.readline().split()))
    secondline = list(map(int, f.readline().split()))

    V    = firstline[0]
    E    = firstline[1]
    R    = firstline[2]
    C    = firstline[3]
    X    = firstline[4]
    S    = [x for x in secondline]

    for x in range (E):
        line = list(map(int, f.readline().split()))
        Ld.append(line[0])
        K.append(line[1])
        temp_c_id = []
        temp_Lc   = []
        for y in range (K[-1]) :
            line = list(map(int, f.readline().split()))
            temp_c_id.append(line[0])
            temp_Lc.append(line[1])
        C_id.append(temp_c_id)
        Lc.append(temp_Lc)

    for x in range (R):
        line = list(map(int, f.readline().split()))
        Rv.append(line[0])
        Re.append(line[1])
        Rn.append(line[2])

print(V   )
print(E   )
print(R   )
print(C   )
print(X   )
print(S   )
print(Ld  )
print(K   )
print(C_id)
print(Lc  )
print(Rv  )
print(Re  )
print(Rn  )

# ============================= Fonctions ============================= #
def fonction_1():
    """
    Description de ma foction ici
    """
    return

def callback(model, where, *, cbdata):
    """
    La fonction callback est particulière, on l'overwrite. Regarder exercice callback.py
    """
    return

def show_results():
    sol = None

    if m.Status == GRB.OPTIMAL:
        sol = {
            
        }
        print("Optimal objective:", m.ObjVal)
        print(sol)
    else:
        print("Optimization status:", m.Status)


# ============================= Build model ============================= #
with gp.Env() as env, gp.Model(env=env) as m:

    # Decision variables
    # Lt gain de latence total = (l)
    # 1/R * sum(i=0, V, sum(k=0, E, R[K] * max(j€C, E[])   ))
    X  = m.addVars(vtype = GRB.BINARY, name="Xij")
    Lt = m.addVar (lb=0,               name="Lt" )

    m.setObjective(Lt, GRB.MINIMIZE)


    m.addConstr( Lt   == L1*nl.cos(theta1) + L2*nl.cos(theta1 + theta2),                        name = "position of x"                              )

    m.optimize()
    # show_results()




