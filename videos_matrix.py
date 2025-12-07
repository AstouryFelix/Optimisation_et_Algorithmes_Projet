import sys, time
import numpy as np
import gurobipy as gp
from gurobipy import GRB

# =========================================  Explications ========================================= #
#               Le projet consiste à organiser des vidéos dans des serveurs de cache                #
#                 pour que les utilisateurs puissent les regarder plus rapidement.                  #
#                     Au lieu d’aller chercher chaque vidéo dans un data center,                    #
#   on essaie de placer les vidéos les plus demandées dans des serveurs proches des utilisateurs.   #
#           L’objectif est donc de réduire le temps d’attente en choisissant intelligemment         #
#        quelles vidéos mettre dans quels caches pour satisfaire au mieux les demandes prévues.     #
# ================================================================================================= #

# ====================================================================== Parametres ======================================================================= #
V    = 0                        # The number of videos                                                                   (1 ≤ V ≤ 10000)                    #
E    = 0                        # The number of endpoints                                                                (1 ≤ E ≤ 1000)                     #
R    = 0                        # The number of request descriptions                                                     (1 ≤ R ≤ 1000000)                  #
C    = 0                        # The number of cache servers                                                            (1 ≤ C ≤ 1000)                     #
X    = 0                        # The capacity of each cache server in megabytes                                         (1 ≤ X ≤ 500000)                   #
S    = []                       # The size of video i < V in megabytes                                                   (1 ≤ S[V] ≤ 1000)                  #
Ld   = []                       # The latency of serving a video request from the data center to this endpoint, in ms    (2 ≤ ld[E] ≤ 4000)                 #
K    = []                       # The number of cache servers that this endpoint is connected to.                        (0 ≤ K[C] ≤ C)                     #
C_id = []                       # The ID of the cache server.                                                            (0 ≤ c < C)                        #
                                                                                                                                                            #
Lc   = []                       # The latency of serving a video request from this cache server                          (1 ≤ Lc < ld of endpoint)          #
                                # to this endpoint, in ms. You can assume that latency from the                                                             #
                                # cache is strictly lower than latency from the data center                                                                 #
                                                                                                                                                            #
Rv   = []                       # The ID of the requested video                                                          (0 ≤ Rv < V)                       #
Re   = []                       # The ID of the endpoint from which the requests are coming from                         (0 ≤ Re < E)                       #
Rn   = []                       # The number of requests                                                                 (0 < Rn ≤ 10000)                   #
                                                                                                                                                            #
epsilon_to_compare_gap = 5e-3   # Ecart minimal avant l'arrêt de la fonction optimise.                                                                      #
max_time = GRB.INFINITY                                                                                                                                     #
# ========================================================================================================================================================= #

# ======================================================================= Fonctions ======================================================================= #
def get_data(path : str) :                                                                                                                                  #
                                                                                                                                                            #
    with open(path, "r") as f:                                                                                                                              #
        firstline  = list(map(int, f.readline().split()))   # La première ligne permet de connaitre le nombre de vidéos, caches, ...                        #
        secondline = list(map(int, f.readline().split()))   # La deuxième ligne nous donne la taille de chaques vidéos.                                     #
                                                                                                                                                            #
        V    = firstline[0]                                                                                                                                 #
        E    = firstline[1]                                                                                                                                 #
        R    = firstline[2]                                                                                                                                 #
        C    = firstline[3]                                                                                                                                 #
        X    = firstline[4]                                                                                                                                 #
        S    = [x for x in secondline]                                                                                                                      #
                                                                                                                                                            #
        # Ensuite, on récupère les données selon le format suivant :                                                                                        #
        # - La Latence pour récuperer une vidéo du datacenter depuis cet endpoint                                                                           #
        # - Le nombre de cache servers y étant connecté -> pour autant de prochaines lignes que cette valeur :                                              #
        #   - l'ID du cache server                                                                                                                          #
        #   - le délais pour récuperer une vidéo de ce cache server depuis cet endpoint                                                                     #
        for _ in range (E):                                                                                                                                 #
            line = list(map(int, f.readline().split()))                                                                                                     #
            Ld.append(line[0])                                                                                                                              #
            K.append(line[1])                                                                                                                               #
            temp_c_id = []                                                                                                                                  #
            temp_Lc   = []                                                                                                                                  #
            for _ in range (K[-1]) :                                                                                                                        #
                line = list(map(int, f.readline().split()))                                                                                                 #
                temp_c_id.append(line[0])                                                                                                                   #
                temp_Lc.append(line[1])                                                                                                                     #
            C_id.append(temp_c_id)                                                                                                                          #
            Lc.append(temp_Lc)                                                                                                                              #
                                                                                                                                                            #
        # Pour le nombre de requêtes :                                                                                                                      #
        #  - l'ID de la vidéo demmandé                                                                                                                      #
        #  - l'ID de l'endpoint effectuant les requêtes                                                                                                     #
        #  - Le nombre de requêtes prédites                                                                                                                 #
        for _ in range (R):                                                                                                                                 #
            line = list(map(int, f.readline().split()))                                                                                                     #
            Rv.append(line[0])                                                                                                                              #
            Re.append(line[1])                                                                                                                              #
            Rn.append(line[2])                                                                                                                              #
                                                                                                                                                            #
    return (V,                                                                                                                                              #
            E,                                                                                                                                              #
            R,                                                                                                                                              #
            C,                                                                                                                                              #
            X,                                                                                                                                              #
            np.array(S),                                                                                                                                    #
            np.array(Ld),                                                                                                                                   #
            np.array(K),                                                                                                                                    #
            C_id,                                                                                                                                           #
            Lc,                                                                                                                                             #
            np.array(Rv),                                                                                                                                   #
            np.array(Re),                                                                                                                                   #
            np.array(Rn)                                                                                                                                    #
            )                                                                                                                                               #
                                                                                                                                                            #
def write_solution(model : gp.Model, C, V, Y, path : str = "video.out") :                                                                                   #
                                                                                                                                                            #
        # ==================== Etat du model ==================== #                                                                                         #
        if model.status == GRB.OPTIMAL:                                                                                                                     #
            print(f"Solution optimale (à moins de {epsilon_to_compare_gap}% près) trouvée")                                                                 #
            print(f"Valeur objectif: {model.ObjVal}")                                                                                                       #
                                                                                                                                                            #
        elif model.status == GRB.TIME_LIMIT:                                                                                                                #
            print("Limite temporelle atteinte")                                                                                                             #
            if model.SolCount > 0 :                                                                                                                         #
                print(f"Valeur objectif: {model.ObjVal}")                                                                                                   #
            else:                                                                                                                                           #
                print(f"Gap actuel: {model.MIPGap*100}%")                                                                                                   #
                print("Aucunes solution n'a eu le temps d'être exploré")                                                                                    #
                return                                                                                                                                      #
                                                                                                                                                            #
        else :                                                                                                                                              #
            return                                                                                                                                          #
                                                                                                                                                            #
        # ==================== Ecriture des resultats ==================== #                                                                                #
        result =  [[c] for c in range(C)]                                                                                                                   #
        for c in range(C) :                                                                                                                                 #
            for v in range(V):                                                                                                                              #
                if Y[v, c].x == 1:                                                                                                                          #
                    result[c].append(v)                                                                                                                     #
                                                                                                                                                            #
        gen = [x for x in result if len(x) > 1]                                                                                                             #
        with open(path, "w") as f:                                                                                                                          #
            f.write(str(sum(1 for _ in gen)) + "\n")                                                                                                        #
            for c in gen:                                                                                                                                   #
                for v in range(0,len(c)):                                                                                                                   #
                    f.write(f"{c[v]} ")                                                                                                                     #
                f.write("\n")                                                                                                                               #
# ========================================================================================================================================================= #

# ===================================================================== Build model ======================================================================= #
def main(path : str = "videos/datasets/example.in") :                                                                                                       #
    with gp.Env() as env, gp.Model(env=env) as m:                                                                                                           #
                                                                                                                                                            #                                                                                                                                                            #
        # ==================== Données ==================== #                                                                                               #
        m.setParam('MIPGap', epsilon_to_compare_gap) # Permet le remplacement du callback                                                                   #
        m.setParam('OutputFlag', 1)                                                                                                                         #
        m.setParam('TimeLimit', max_time)                                                                                                                   #
                                                                                                                                                            #
        # Conseil Gurobot                                                                                                                                   #
        m.setParam('Presolve', 2)      # Aggressive presolve                                                                                                #
        m.setParam('Cuts', 2)          # Aggressive cuts                                                                                                    #
        m.setParam('Heuristics', 0.2)  # Spend 20% time on heuristics                                                                                       #
        m.setParam('MIPFocus', 1)      # Focus on finding good solutions quickly                                                                            #
        start = time.time()                                                                                                                                 #
        V, E, R, C, X, S, Ld, K, C_id, Lc, Rv, Re, Rn = get_data(path)                                                                                      #
                                                                                                                                                            #
        # ==================== addVars ==================== #                                                                                               #
        Y  = m.addMVar((V, C), vtype = GRB.BINARY, name="Yij") # 1 si vidéo v est mise dans le CacheServeur C, 0 sinon                                      #
        U  = m.addMVar(R,      vtype = GRB.BINARY, name="Ur" ) # 1 si la requête R est desservie par le data center, 0 sinon                                #
        G  = m.addMVar(R,                          name="Gr" ) # Gain de latence pour chaque requete                                                        #
        Z  = m.addMVar((R, C), vtype = GRB.BINARY, name="Zrc") # 1 si la requête R est desservie par le cache C, 0 sinon                                    #
                                                                                                                                                            #
        # ==================== setObjective ==================== #                                                                                          #                                            
        m.setObjective(                                                                                                                                     #
            G @ Rn,                                                                                                                                         #
            GRB.MAXIMIZE                                                                                                                                    #
        )                                                                                                                                                   #
                                                                                                                                                            #
        m.addConstrs(                                                                                                                                       #
            (Y[:, j] * S <= X for j in range(C)),                                                                                                           #
            name="Capacity"                                                                                                                                 #
        )                                                                                                                                                   #
                                                                                                                                                            #
        m.addConstrs(                                                                                                                                       #
            (gp.quicksum(Z[r, c] for c in C_id[Re[r]]) + U[r]                                                                                               #
            == 1 for r in range(R)),                                                                                                                        #
            name="ServeRequest"                                                                                                                             #
        )                                                                                                                                                   #
                                                                                                                                                            #
        m.addConstrs(                                                                                                                                       #
            (Z[r, c] <= Y[Rv[r], c] for r in range(R) for c in C_id[Re[r]]),                                                                                #
            name="VideoMustBeInCache"                                                                                                                       #
        )                                                                                                                                                   #
                                                                                                                                                            #
        m.addConstrs(                                                                                                                                       #
            (G[r] == Ld[Re[r]]- (Ld[Re[r]] * U[r] +                                                                                                         #
            gp.quicksum(Lc[Re[r]][C_id[Re[r]].index(c)] * Z[r, c]                                                                                           #
            for c in C_id[Re[r]]))for r in range(R)),                                                                                                       #
            name="Gr"                                                                                                                                       #
        )                                                                                                                                                   #
                                                                                                                                                            #
        # TODO : Besoin de A et B ? Trouver une autre méthode.                                                                                              #
        A = {}                                                                                                                                              #
        for e in range(E):                                                                                                                                  #
            A[e] = {}                                                                                                                                       #
            for c in range(C):                                                                                                                              #
                A[e][c] = 1 if c in C_id[e] else 0                                                                                                          #
                                                                                                                                                            #
        B = {}                                                                                                                                              #
        for e in range(E):                                                                                                                                  #
            B[e] = {v: 0 for v in range(V)}                                                                                                                 #
                                                                                                                                                            #
        for r in range(R):                                                                                                                                  #
            video = Rv[r]                                                                                                                                   #
            endpoint = Re[r]                                                                                                                                #
            B[endpoint][video] = 1                                                                                                                          #
                                                                                                                                                            #
        valid_video_cache = {}                                                                                                                              #
        for v in range(V):                                                                                                                                  #
            for c in range(C):                                                                                                                              #
                valid_video_cache[(v, c)] = sum(A[e][c] * B[e][v]                                                                                           #
                    for e in range(E))                                                                                                                      #
                                                                                                                                                            #
        m.addConstrs(                                                                                                                                       #
            (Y[v, c] <= valid_video_cache[(v, c)]                                                                                                           #
             for v in range(V) for c in range(C)),                                                                                                          #
            name="ValidVideoCache"                                                                                                                          #
        )                                                                                                                                                   #
                                                                                                                                                            #                                            
        # ==================== Lancement du moteur VROUMVROUM ==================== #                                                                        #                                            
                                                                                                                                                            #
        second = time.time()                                                                                                                                #
        print(f"==================================\n{second - start}\n==================================")                                                  #
                                                                                                                                                            #
        m.optimize()                                                                                                                                        #                                            
        m.write("videos.mps")                                                                                                                               #                                            
        write_solution(m, C, V, Y, "videos.out")                                                                                                            #
        print(f"==================================\n{time.time() - second}\n==================================")                                            #
# ========================================================================================================================================================= #

# ======================================================================== main =========================================================================== #
if __name__ == "__main__":                                                                                                                                  #
    # python .\videos_matrix.py .\datasets\trending_4000_10k.in                                                                                             #
    # python .\videos_matrix.py .\datasets\example.in                                                                                                       #
    args = sys.argv[1]                                                                                                                                      #
    main(args)                                                                                                                                              #
# ========================================================================================================================================================= #

# Fait main, avec l'aide occationnel du chatbot de Gurobi pour certaines contraintes, ainsi que pour le passage sous forme matricielle;