import sys
import gurobipy as gp
from gurobipy import GRB
from functools import partial

# =========================================  Explications ========================================= #
#               Le projet consiste à organiser des vidéos dans des serveurs de cache                #
#                 pour que les utilisateurs puissent les regarder plus rapidement.                  #
#                     Au lieu d’aller chercher chaque vidéo dans un data center,                    #
#   on essaie de placer les vidéos les plus demandées dans des serveurs proches des utilisateurs.   #
#           L’objectif est donc de réduire le temps d’attente en choisissant intelligemment         #
#        quelles vidéos mettre dans quels caches pour satisfaire au mieux les demandes prévues.     #
# ================================================================================================= #

# ====================================================================== Parametres ======================================================================= #
# TODO : Traduire en francais ?                                                                                                                             #
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
# TODO : Integrer une limite temporelle pour ne pas s'arrêter qu'aux 0.5% ?                                                                                 #
epsilon_to_compare_gap = 5e-3   # Ecart minimal avant l'arrêt de la fonction optimise.                                                                      #
# ========================================================================================================================================================= #

# ======================================================================= Fonctions ======================================================================= #
def get_data(path : str) :

    with open(path, "r") as f:
        firstline  = list(map(int, f.readline().split()))   # La première ligne permet de connaitre le nombre de vidéos, caches, ... 
        secondline = list(map(int, f.readline().split()))   # La deuxième ligne nous donne la taille de chaques vidéos.

        V    = firstline[0]
        E    = firstline[1]
        R    = firstline[2]
        C    = firstline[3]
        X    = firstline[4]
        S    = [x for x in secondline]

        # Ensuite, on récupère les données selon le format suivant : 
        # - La Latence pour récuperer une vidéo du datacenter depuis cet endpoint
        # - Le nombre de cache servers y étant connecté -> pour autant de prochaines lignes que cette valeur :
        #   - l'ID du cache server
        #   - le délais pour récuperer une vidéo de ce cache server depuis cet endpoint
        for _ in range (E):
            line = list(map(int, f.readline().split()))
            Ld.append(line[0])
            K.append(line[1])
            temp_c_id = []
            temp_Lc   = []
            for _ in range (K[-1]) :
                line = list(map(int, f.readline().split()))
                temp_c_id.append(line[0])
                temp_Lc.append(line[1])
            C_id.append(temp_c_id)
            Lc.append(temp_Lc)

        # Pour le nombre de requêtes :
        #  - l'ID de la vidéo demmandé
        #  - l'ID de l'endpoint effectuant les requêtes
        #  - Le nombre de requêtes prédites
        for _ in range (R):
            line = list(map(int, f.readline().split()))
            Rv.append(line[0])
            Re.append(line[1])
            Rn.append(line[2])

    return V, E, R, C, X, S, Ld, K, C_id, Lc, Rv, Re, Rn

class CallbackData:
    def __init__(self):
        self.last_gap_change_time = -GRB.INFINITY
        self.last_gap = GRB.INFINITY

# TODO : Vérifier la fonctionnalité du callback.
def callback(model, where, *, cbdata):
    """
    Dès que l'écart est inférieure à 0.5%, on peut s'arrêter.
    """

    if where != GRB.Callback.MIP:
            return

    if model.cbGet(GRB.Callback.MIP_SOLCNT) == 0:
        return

    best  = model.cbGet(GRB.Callback.MIP_OBJBST)
    bound = model.cbGet(GRB.Callback.MIP_OBJBND)

    if best == 0 or best >= GRB.INFINITY or bound >= GRB.INFINITY:
        return

    # TODO : Utiliser MIPGap ? -> https://docs.gurobi.com/projects/optimizer/en/13.0/reference/parameters.html#mipgap
    gap = (bound - best) / abs(best)
    if gap < cbdata.last_gap - epsilon_to_compare_gap:
        time = model.cbGet(GRB.Callback.RUNTIME)
        print(f"gap = {gap:.4%}, time = {time:.2f}s")
        cbdata.last_gap = gap
        cbdata.last_gap_change_time = time
        
def write_solution(m : gp.Model, C, V, Y,path : str = "video.out") :
        # TODO Revoir ici, le faire moi meme

        if m.status in (GRB.OPTIMAL, GRB.SUBOPTIMAL):
            print(f"Valeur trouvée : {m.objVal}")
            print(f"gap final      : {m.MIPGap:.4%}")

            cache_to_videos = {c: [] for c in range(C)}
            for v in range(V):
                for c in range(C):
                    if Y[v, c].x > 0.5:
                        cache_to_videos[c].append(v)

            non_empty = {c: vids for c, vids in cache_to_videos.items() if vids}

            with open(path, "w") as f:
                f.write(str(len(non_empty)) + "\n")
                for c, vids in non_empty.items():
                    f.write(str(c) + " " + " ".join(map(str, vids)) + "\n")
# ========================================================================================================================================================= #

# ===================================================================== Build model ======================================================================= #
def main(path : str = "videos/datasets/example.in") : 
    with gp.Env() as env, gp.Model(env=env) as m:

        # TODO : Accélerer la création des contraintes -> Passer sous forme matricielle ?
        # TODO : Essayer de trouver une autre modélisation

        # ==================== Données ==================== #
        m.Params.OutputFlag = 1          
        m.Params.MIPGap     = epsilon_to_compare_gap
        V, E, R, C, X, S, Ld, K, C_id, Lc, Rv, Re, Rn = get_data(path)
        
        # ==================== addVars ==================== #
        Y  = m.addVars(V, C, vtype = GRB.BINARY, name="Yij") # 1 si vidéo v est mise dans le DataCenter C, 0 sinon
        U  = m.addVars(R,    vtype = GRB.BINARY, name="Ur" ) # 1 si la requête R est desservie par le data center, 0 sinon
        P  = m.addVars(R                       , name="Pr" ) # Gain de latence pour chaque requete
        Z  = m.addVars(R, C, vtype = GRB.BINARY, name="Zrc") # 1 si la requête R est desservie par le cache C, 0 sinon
        # TODO : Enlever cette variable et utiliser le dict à la place 
        # Z = {} 
        # for r in range(R):
        #     e = Re[r]
        #     for c in C_id[e]:
        #         Z[r, c] = m.addVar(vtype=GRB.BINARY, name=f"Z_{r}_{c}")

        # ==================== setObjective ==================== #
        m.setObjective(
            gp.quicksum(P[r] * Rn[r] for r in range(R)),
            GRB.MAXIMIZE
        )

        m.addConstrs(
            (gp.quicksum(Y[i, j] * S[i] for i in range(V)) <= X for j in range(C)), 
            name="Capacity"
        )

        m.addConstrs(
            (gp.quicksum(Z[r, c] for c in C_id[Re[r]]) + U[r] == 1 for r in range(R)),
            name="ServeRequest"
        )

        m.addConstrs(
            (Z[r, c] <= Y[Rv[r], c] for r in range(R) for c in C_id[Re[r]]),
            name="VideoMustBeInCache"
        )

        m.addConstrs(
            (P[r] == Ld[Re[r]]- (Ld[Re[r]] * U[r] + gp.quicksum(Lc[Re[r]][C_id[Re[r]].index(c)] * Z[r, c]for c in C_id[Re[r]]))for r in range(R)),
            name="Pr"
        )

        # TODO : Besoin de alpha et beta ? Trouver une autre méthode.
        alpha = {}
        for e in range(E):
            alpha[e] = {}
            for c in range(C):
                alpha[e][c] = 1 if c in C_id[e] else 0

        beta = {}
        for e in range(E):
            beta[e] = {v: 0 for v in range(V)}

        for r in range(R):
            video = Rv[r]
            endpoint = Re[r]
            beta[endpoint][video] = 1  

        valid_video_cache = {}
        for v in range(V):
            for c in range(C):
                valid_video_cache[(v, c)] = sum(alpha[e][c] * beta[e][v] for e in range(E))

        m.addConstrs(
            (Y[v, c] <= valid_video_cache[(v, c)] for v in range(V) for c in range(C)),
            name="ValidVideoCache"
        )

        # ==================== Lancement du moteur VROUMVROUM ==================== #
        m.write("videos.mps")
        callback_data = CallbackData()
        callback_func = partial(callback, cbdata=callback_data)
        m.optimize(callback_func)
                                                                                                                                                            #
        write_solution(m, C, V, Y, "video.out")                                                                                                             #
# ========================================================================================================================================================= #

# ======================================================================== main =========================================================================== #
if __name__ == "__main__":                                                                                                                                  #
    # "videos/datasets/trending_4000_10k.in"                                                                                                                #
    # "videos/datasets/example.in"                                                                                                                          #
    args = sys.argv[1]                                                                                                                                      #
    main(args)                                                                                                                                              #
# ========================================================================================================================================================= #

# Fait main, avec l'aide occationnel du chatbot de Gurobi pour certaines contraintes, ainsi que pour le passage sous forme matricielle;