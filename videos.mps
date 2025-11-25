* Signature: 0x114cc7e0fb07ca66
NAME 
OBJSENSE MAX
ROWS
 N  OBJ
 L  Capacity[0]
 L  Capacity[1]
 L  Capacity[2]
 E  ServeRequest[0]
 E  ServeRequest[1]
 E  ServeRequest[2]
 E  ServeRequest[3]
 L  VideoMustBeInCache[0,0]
 L  VideoMustBeInCache[0,2]
 L  VideoMustBeInCache[0,1]
 L  VideoMustBeInCache[2,0]
 L  VideoMustBeInCache[2,2]
 L  VideoMustBeInCache[2,1]
 L  VideoMustBeInCache[3,0]
 L  VideoMustBeInCache[3,2]
 L  VideoMustBeInCache[3,1]
 E  Pr[0]   
 E  Pr[1]   
 E  Pr[2]   
 E  Pr[3]   
 L  ValidVideoCache[0,0]
 L  ValidVideoCache[0,1]
 L  ValidVideoCache[0,2]
 L  ValidVideoCache[1,0]
 L  ValidVideoCache[1,1]
 L  ValidVideoCache[1,2]
 L  ValidVideoCache[2,0]
 L  ValidVideoCache[2,1]
 L  ValidVideoCache[2,2]
 L  ValidVideoCache[3,0]
 L  ValidVideoCache[3,1]
 L  ValidVideoCache[3,2]
 L  ValidVideoCache[4,0]
 L  ValidVideoCache[4,1]
 L  ValidVideoCache[4,2]
COLUMNS
    MARKER    'MARKER'                 'INTORG'
    Yij[0,0]  Capacity[0]  50
    Yij[0,0]  ValidVideoCache[0,0]  1
    Yij[0,1]  Capacity[1]  50
    Yij[0,1]  ValidVideoCache[0,1]  1
    Yij[0,2]  Capacity[2]  50
    Yij[0,2]  ValidVideoCache[0,2]  1
    Yij[1,0]  Capacity[0]  50
    Yij[1,0]  VideoMustBeInCache[3,0]  -1
    Yij[1,0]  ValidVideoCache[1,0]  1
    Yij[1,1]  Capacity[1]  50
    Yij[1,1]  VideoMustBeInCache[3,1]  -1
    Yij[1,1]  ValidVideoCache[1,1]  1
    Yij[1,2]  Capacity[2]  50
    Yij[1,2]  VideoMustBeInCache[3,2]  -1
    Yij[1,2]  ValidVideoCache[1,2]  1
    Yij[2,0]  Capacity[0]  80
    Yij[2,0]  ValidVideoCache[2,0]  1
    Yij[2,1]  Capacity[1]  80
    Yij[2,1]  ValidVideoCache[2,1]  1
    Yij[2,2]  Capacity[2]  80
    Yij[2,2]  ValidVideoCache[2,2]  1
    Yij[3,0]  Capacity[0]  30
    Yij[3,0]  VideoMustBeInCache[0,0]  -1
    Yij[3,0]  ValidVideoCache[3,0]  1
    Yij[3,1]  Capacity[1]  30
    Yij[3,1]  VideoMustBeInCache[0,1]  -1
    Yij[3,1]  ValidVideoCache[3,1]  1
    Yij[3,2]  Capacity[2]  30
    Yij[3,2]  VideoMustBeInCache[0,2]  -1
    Yij[3,2]  ValidVideoCache[3,2]  1
    Yij[4,0]  Capacity[0]  110
    Yij[4,0]  VideoMustBeInCache[2,0]  -1
    Yij[4,0]  ValidVideoCache[4,0]  1
    Yij[4,1]  Capacity[1]  110
    Yij[4,1]  VideoMustBeInCache[2,1]  -1
    Yij[4,1]  ValidVideoCache[4,1]  1
    Yij[4,2]  Capacity[2]  110
    Yij[4,2]  VideoMustBeInCache[2,2]  -1
    Yij[4,2]  ValidVideoCache[4,2]  1
    Ur[0]     ServeRequest[0]  1
    Ur[0]     Pr[0]     1000
    Ur[1]     ServeRequest[1]  1
    Ur[1]     Pr[1]     500
    Ur[2]     ServeRequest[2]  1
    Ur[2]     Pr[2]     1000
    Ur[3]     ServeRequest[3]  1
    Ur[3]     Pr[3]     1000
    MARKER    'MARKER'                 'INTEND'
    Pr[0]     OBJ       1500
    Pr[0]     Pr[0]     1
    Pr[1]     OBJ       1000
    Pr[1]     Pr[1]     1
    Pr[2]     OBJ       500
    Pr[2]     Pr[2]     1
    Pr[3]     OBJ       1000
    Pr[3]     Pr[3]     1
    MARKER    'MARKER'                 'INTORG'
    Zrc[0,0]  ServeRequest[0]  1
    Zrc[0,0]  VideoMustBeInCache[0,0]  1
    Zrc[0,0]  Pr[0]     100
    Zrc[0,1]  ServeRequest[0]  1
    Zrc[0,1]  VideoMustBeInCache[0,1]  1
    Zrc[0,1]  Pr[0]     300
    Zrc[0,2]  ServeRequest[0]  1
    Zrc[0,2]  VideoMustBeInCache[0,2]  1
    Zrc[0,2]  Pr[0]     200
    Zrc[1,0]  OBJ       0
    Zrc[1,1]  OBJ       0
    Zrc[1,2]  OBJ       0
    Zrc[2,0]  ServeRequest[2]  1
    Zrc[2,0]  VideoMustBeInCache[2,0]  1
    Zrc[2,0]  Pr[2]     100
    Zrc[2,1]  ServeRequest[2]  1
    Zrc[2,1]  VideoMustBeInCache[2,1]  1
    Zrc[2,1]  Pr[2]     300
    Zrc[2,2]  ServeRequest[2]  1
    Zrc[2,2]  VideoMustBeInCache[2,2]  1
    Zrc[2,2]  Pr[2]     200
    Zrc[3,0]  ServeRequest[3]  1
    Zrc[3,0]  VideoMustBeInCache[3,0]  1
    Zrc[3,0]  Pr[3]     100
    Zrc[3,1]  ServeRequest[3]  1
    Zrc[3,1]  VideoMustBeInCache[3,1]  1
    Zrc[3,1]  Pr[3]     300
    Zrc[3,2]  ServeRequest[3]  1
    Zrc[3,2]  VideoMustBeInCache[3,2]  1
    Zrc[3,2]  Pr[3]     200
    MARKER    'MARKER'                 'INTEND'
RHS
    RHS1      Capacity[0]  100
    RHS1      Capacity[1]  100
    RHS1      Capacity[2]  100
    RHS1      ServeRequest[0]  1
    RHS1      ServeRequest[1]  1
    RHS1      ServeRequest[2]  1
    RHS1      ServeRequest[3]  1
    RHS1      Pr[0]     1000
    RHS1      Pr[1]     500
    RHS1      Pr[2]     1000
    RHS1      Pr[3]     1000
    RHS1      ValidVideoCache[1,0]  1
    RHS1      ValidVideoCache[1,1]  1
    RHS1      ValidVideoCache[1,2]  1
    RHS1      ValidVideoCache[3,0]  1
    RHS1      ValidVideoCache[3,1]  1
    RHS1      ValidVideoCache[3,2]  1
    RHS1      ValidVideoCache[4,0]  1
    RHS1      ValidVideoCache[4,1]  1
    RHS1      ValidVideoCache[4,2]  1
BOUNDS
 BV BND1      Yij[0,0]
 BV BND1      Yij[0,1]
 BV BND1      Yij[0,2]
 BV BND1      Yij[1,0]
 BV BND1      Yij[1,1]
 BV BND1      Yij[1,2]
 BV BND1      Yij[2,0]
 BV BND1      Yij[2,1]
 BV BND1      Yij[2,2]
 BV BND1      Yij[3,0]
 BV BND1      Yij[3,1]
 BV BND1      Yij[3,2]
 BV BND1      Yij[4,0]
 BV BND1      Yij[4,1]
 BV BND1      Yij[4,2]
 BV BND1      Ur[0]   
 BV BND1      Ur[1]   
 BV BND1      Ur[2]   
 BV BND1      Ur[3]   
 BV BND1      Zrc[0,0]
 BV BND1      Zrc[0,1]
 BV BND1      Zrc[0,2]
 BV BND1      Zrc[1,0]
 BV BND1      Zrc[1,1]
 BV BND1      Zrc[1,2]
 BV BND1      Zrc[2,0]
 BV BND1      Zrc[2,1]
 BV BND1      Zrc[2,2]
 BV BND1      Zrc[3,0]
 BV BND1      Zrc[3,1]
 BV BND1      Zrc[3,2]
ENDATA
