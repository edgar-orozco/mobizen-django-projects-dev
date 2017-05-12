# -*- coding: utf-8 -*- 
import re
from verifica import models

def tipo_de_placa(placa):
    placa = placa.replace(' ','').replace('-','')
    # valida placas: A-00-AAA, 000-AAA, AAA-0000, AAA-000-A
    if re.compile(r'^((\d{3}|[A-Z]\d{2})[A-Z]{3}|[A-Z]{3}(\d{4}|\d{3}[A-Z]))$').match(placa):
        return 'Particular'
    #Valida 000-AA, 00-A-00, 00-AAA
    if re.compile(r'^(\d{3}[A-Z]{2}|\d{2}[A-Z](\d{2}|[A-Z]{2}))$').match(placa):
        return 'Discapacitado'
    #Valida 00000, A-000-A, AAA-00, A00AA, 0A0AA, A0AA0
    if re.compile(r'^(\d{5}|[A-Z]\d{3}[A-Z]|[A-Z]{3}\d{2}|[A-Z]\d{2}\[A-Z]{2}|[A-Z]\d[A-Z]{2}\d|\d[A-Z]\d[A-Z]{2})$').match(placa):
        return 'Motocicleta'
# Esta placa no es particular pero hay gente que escribe AAA111 en lugar de 111AAA
    if re.compile(r'^[A-Z]{3}\d{3}$').match(placa):
        return 'Particular'
    # Valida: AA-00, AA-000, 0AA-00, AA-0-A
    if re.compile(r'^([A-Z]{2}\d{2,3}|\d[A-Z]{2}\d{2}|[A-Z]{2}\d[A-Z])$').match(placa):
        return 'Auto Antiguo'
    # Valida: 00-00-AA, A-000-AA
    if re.compile(r'^(\d{4}|[A-Z]\d{3})[A-Z]{2}$').match(placa):
        return 'Camión Privado CDMX'
    # Valida: AA-00000, AA-0000-A
    if re.compile(r'^([A-Z]{2}\d{5}|[A-Z]{2}\d{4}[A-Z])$').match(placa):
        return 'Camión Privado'
    # Valida: 0-AAA, 00-AA-1
    if re.compile(r'^(\d[A-Z]{3}|\d{2}[A-Z]{2}\d)$').match(placa):
        return 'Autobús CDMX'
    # Valida: 0-AAA-00, 00-AAA-00
    if re.compile(r'^\d{1,2}[A-Z]{3}\d{2}$').match(placa):
        return 'Autobús'
    # Valida: A-0000, A-0A-00
    if re.compile(r'^([A-Z](\d{4}|\d[A-Z]\d{2}))$').match(placa):
        return 'Remolque CDMX'
    # Valida: 0-AA-0000, 0AA-000-A
    if re.compile(r'^(\d[A-Z]{2}(\d{4}|\d{3}[A-Z]))$').match(placa):
        return 'Remolque'
    # Valida: A-00-000, 00-00-AAA, A-0000-A
    if re.compile(r'^([A-Z]\d{5}|\d{4}[A-Z]{3}|[A-Z]\d{4}[A-Z])$').match(placa):
        return 'Taxi'
    # Valida: 000-000, 000 0000, A-000-000, 0-AAA-000, 000-000-A, 000-A-000, A-000-AAA
    if re.compile(r'^([A-Z]{0,1}\d{3}([A-Z]{3}|\d{3,4})[A-Z]{0,1}|\d{1}[A-Z]{3}\d{3}|\d{3}[A-Z]\d{3})$').match(placa):
        return 'Transporte Público'
    
    # Valida: AA-00, 0-AA-00
    if re.compile(r'^([A-Z]{2}\d{2}|\d{1}[A-Z]{3}\d{2})$').match(placa):
        return 'Demostración'
    
    raise Exception

def estado_motocicleta(placa):
    if re.compile(r'^(\d{5}|G\d{2}[A-Z]{2}|Z0[4-9]A[T-Z]|Z[1-4]\d[A-Z]{2}|Z50[A-Z]{2}|Z51[A-L][A-Z]|Z51M[A-W]|1A\d[A-Z]{2}|[2-4][A-Z]\d[A-Z]{2}|5[A-M][0-3][A-Z]{2}|5M4([A-L][A-Z]|M[[A-M])|F\dT[W-Z]\d|F\d[U-Z][A-Z]\d|G\d[A-M][A-Z]\d)$').match(placa):
        return u'DIF'
    
    if re.compile(r'^(H\d{3}[T-Z]|J\d{3}[A-V]|(H[L-Z]|J[A-K])[A-Z]\d{2}|J\d{2}[A-Z]{2}|G\d[N-Z][A-Z]\d|H\d([A-E][A-Z]|F[A-L])\d)$').match(placa):
        return u'MEX'
    
    if re.compile(r'^(A\d{3}[A-H]|A[A-K][A-Z]\d{2}|N\d{2}[A-K][A-Z]|N5[01]|N5([01][A-Z]|2L)[A-Z]|A\d([A-S][A-Z]|T[A-L])\d)$').match(placa):
        return u'AGU'
    
    if re.compile(r'^(A\d{3}[J-X]|A[L-Z][A-Z]\d{2}|N(53L[A-Z]|\d{2}[M-X][A-Z]|0[0-5]Y[A-Z])|A\d(T[M-Z]|[U-Z][A-Z])\d|B\d([A-H][A-Z]|K[A-Y])\d)$').match(placa):
        return u'BCN'
    
    if re.compile(r'^(A\d{3}[Y-Z]|B\d{3}[A-B]|B[A-K][A-Z]\d{2}|N(06YZ|0[7-9]Y[A-Z]|[1-9]\dZ[A-Z])|P([0-4]\d[A-Z]{2}|5[0-6][A-Z]{2}|P57([A-H]|K[A-Y])))$').match(placa):
        return u'BCS'
    
    if re.compile(r'^(B\d{3}[C-T]|B[L-Z][A-Z]\d{2}|A\d{2}[A-Z]{2}|C\d(D[L-Z]|[E-V][A-Z]|W[A-X])\d)$').match(placa):
        return u'CAM'
    
    if re.compile(r'^(B\d{3}[U-Z]|C\d{3}[A-B]|C[A-K][A-Z]\d{2}|P(58K[Y-Z]|59[A-Z]{2}|[6-9]\d[L-W][A-Z]|0\dX[A-Z]|10X[A-Y])|C\d(W[Y-Z]|[X-Z][A-Z])\d|D\d([A-N][A-Z]|P[A-J])\d)$').match(placa):
        return u'CHP'
    
    if re.compile(r'^(C\d{3}[C-Z]|D\d{3}[A-C]|(C[L-Z]|D[A-D])[A-Z]\d{2}|P\d{2}(X[Y-Z]|[Y-Z][A-Z])|R([0-5]\d[A-Z]{2}|6([0-2][A-H][A-Z]|2J[A-Y]))|D\d(P[K-Z]|[R-Z][A-Z])\d|E\d([A-F][A-Z]|G[A-W])\d)$').match(placa):
        return u'CHH'
    
    if re.compile(r'^(D\d{3}[D-X]|D[E-T][A-Z]\d{2}|R(63J[Y-Z]|\d{2}[K-V][A-Z]|(0\d|1[0-4])W[A-Z]|15W[A-Y])|E\d(G[X-Z]|[F-Z][A-Z])\d|F\dA[A-H]\D)$').match(placa):
        return u'COA'
    
    if re.compile(r'^(D\d{3}[Y-Z]|E\d{3}[A-U]|(D[U-Z]|E[A-G])[A-Z]\d{2}|K\d{2}\[A-Z]{2}|F\d(A[J-Z]|[B-S][A-Z]|T[A-V])\d)$').match(placa):
        return u'COL'
    
    if re.compile(r'^(E\d{3}[V-Z]|F\d{3}A|E[H-T][A-Z]\d{2}|R((1[6-9]|[2-9]\d)W[Y-Z]|\d{2}[X-Z][A-Z])|S(\d{2}([A-G][A-Z]|H[A-W])|([0-5]\d|6[0-7])HX)|H\d(F[M-Z]|[G-X][A-Z]|Y[A-Y])\d)$').match(placa):
        return u'DUR'
    
    if re.compile(r'^(F\d{3}[B-S]|(E[U-Z]|F[A-M])[A-Z]\d{2}|S((6[8-9]|[7-9]\d)H[X-Z]|\d{2}[J-U][A-Z]|([0-1]\d|20)V[A-X])|H\d(YZ|Z[A-Z])\d|J(\d([A-W][A-Z]|)\d|[0-7]X[A-J]\d|8XK[0-4]))$').match(placa):
        return u'GUA'
    
    if re.compile(r'^(F\d{3}[T-Z]|F[N-Z][A-Z]\d{2}|S(2[1-9]V[X-Z]|[3-9]\d[W-Z][A-Z])|T(\d{2}([A-F][A-Z]|G[A-X])|([0-6]\d|7[0-2])GY)|J(8X(K[5-9]|[L-Z]\d)|9[A-Z]{2}\d)|K\d([A-G][A-Z]|J[A-X])\d)$').match(placa):
        return u'GRO'
    
    if re.compile(r'^(G\d{3}[A-G]|G[A-K][A-Z]\d{2}|T(7[3-9]G[Y-Z]|[8-9]\dG[A-Z]|\d{2}[H-T][A-Z]|[0-1]\dU[A-X]|2[0-5]UY)|K\d(J[Y-Z]|[K-Z][A-Z])\d|L\d([A-B][A-Z]|C[A-J])\d)$').match(placa):
        return u'HID'
    
    if re.compile(r'^(G\d{3}[H-Z]|H\d{3}[A-S]|(G[L-Z]|H[A-K])[A-Z]\d{2}|M\d{2}[A-Z]{2}|L\d(C[K-Z]|[D-U][A-Z]|V[A-W])\d)$').match(placa):
        return u'JAL'
    
    if re.compile(r'^(J\d{3}[W-Z]|K\d{3}[A-P]|(J[L-Z]|K[A-B])[A-Z]\d{2}|D\d{2}[A-Z]{2}|L\d(V[X-Z]|[W-Z][A-Z])\d|M\d([A-M][A-Z]|N[A-H])\d)$').match(placa):
        return u'MIC'
    
    if re.compile(r'^(K\d{3}[R-Z]|L\d{3}[A-J]|K[C-T][A-Z]\d{2}|T((2[6-9]|[3-9]\d)U[Y-Z]|\d{2}[V-Z][A-Z])|U(\d{2}([A-E][A-Z]|F[A-W])|([0-6]\d|7[0-7])FX)|M\d(N[J-Z]|[P-Z][A-Z])\d|N\d([A-E][A-Z]|F[A-V])\d)$').match(placa):
        return u'MOR'
    
    if re.compile(r'^(L\d{3}[K-S]|(K[U-Z]|L[A-D])[A-Z]\d{2}|U((7[8-9]|[8-9]\d)FX|\d{2}(F[Y-Z]|[G-S][A-Z]|T[A-W])|([0-2]\d|30)TX)|N\d(F[W-Z]|[G-Y][A-Z]|Z[A-G])\d)$').match(placa):
        return u'NAY'
    
    if re.compile(r'^(L\d{3}[T-Z]|M\d{3}[A-T]|L[E-Z][A-Z]\d{2}|U((3[1-9]|[4-9]\d)TX|\d{2}(T[[Y-Z]|[U-Z][A-Z]))|V(\d{2}([A-D][A-Z]|E[A-V])|([0-7]\d|8[0-2])EW)|N\dZ[H-Z]\d|P\d([A-R][A-Z]|S[A-U])\d)$').match(placa):
        return u'NLE'
    
    if re.compile(r'^(M\d{3}[U-Z]|N\d{3}[A-C]|M[A-K][A-Z]\d{2}|E\d{2}[A-Z]{2}|P\d(S[V-Z]|[T-Z][A-Z])\d|R\d([A-J][A-Z]|K[A-F])\d)$').match(placa):
        return u'OAX'
    
    if re.compile(r'^(N\d{3}[D-Z]|M[L-Z][A-Z]\d{2}|F\d{2}[A-Z]{2}|R\d(K[G-Z]|[L-Z][A-Z])\d|S\d([A-B][A-Z]|C[A-T])\d)$').match(placa):
        return u'PUE'
    
    if re.compile(r'^(P\d{3}[A-E]|N[A-K][A-Z]\d{2}|V((8[3-9]|9\d)EW|\d{2}(E[X-Z]|[F-R][A-Z]|S[A-V])|([0-2]\d|3[0-5])SW)|S\d(C[U-Z]|[D-V][A-Z]|W[A-E])\d)$').match(placa):
        return u'QUE'
    
    if re.compile(r'^(P\d{3}[F-N]|(N[L-Z]|P[A-K])[A-Z]\d{2}|[B-C]\d{2}[A-Z]{2}|S\d(W[F-Z]|[X-Z][A-Z])\d|T\d([A-M][A-Z]|N[A-S])\d)$').match(placa):
        return u'ROO'
    
    if re.compile(r'^(P\d{3}[P-Z]|R\d{3}[A-B]|P[L-Z][A-Z]\d{2}|V((3[6-9]|[4-9]\d)SW|\d{2}(S[X-Z]|[R-Z][A-Z]))|W(\d{2}([A-C][A-Z]|D[A-U])|([0-7]\d|8[0-7])DV)|T\d(N[T-Z]|[P-Z][A-Z])\d|U\d([A-F][A-Z]|G[A-D])\d)$').match(placa):
        return u'SLP'
    
    if re.compile(r'^(R\d{3}[C-V]|R[A-N][A-Z]\d{2}|H\d{2}[A-Z]{2}|U\d(G[E-Z]|[H-Y][A-Z]|Z[A-R])\d)$').match(placa):
        return u'SIN'
    
    if re.compile(r'^(R\d{3}[W-Z]|S\d{3}[A-M]|(R[P-Z]|S[A-C])[A-Z]\d{2}|W((8[8-9]|9\d)DV|\d{2}([E-P][A-Z]|R[A-U])|([0-3]\d|40)RV)|U\dZ[S-Z]\d|V\d([A-S][A-Z]|T[A-C])\d)$').match(placa):
        return u'SON'
    
    if re.compile(r'^(S\d{3}[N-V]|S[D-N][A-Z]\d{2}|W((4[1-9]|[5-9]\d)RV|\d{2}(R[W-Z]|[S-Z][A-Z]))|X(\d{2}([A-B][A-Z]|C[A-T])|([0-8]\d|9[0-2])CU)|V\d(T[D-Z]|[U-Z][A-Z])\d|W\d([A-J][A-Z]|K[A-P])\d)$').match(placa):
        return u'TAB'
    
    if re.compile(r'^(S\d{3}[W-Z]|T\d{3}[A-S]|(S[P-Z]|T[A-C])[A-Z]\d{2}|X((9[3-9])CU|\d{2}(C[V-Z]|[D-N][A-Z]|P[A-T])|([0-3]\d|4[0-5])PU)|W\d(K[R-Z]|[L-Z][A-Z])\d|X\d([A-C][A-Z]|D[A-B])\d)$').match(placa):
        return u'TAM'
    
    if re.compile(r'^(T\d{3}[T-V]|T[D-N][A-Z]\d{2}|X((4[6-9]|[5-9]\d)PU|\d{2}(P[V-Z]|[R-Z][A-Z]))|Y(\d{2}(A[A-Z]|B[A-S])|([0-8]\d|9[0-7])BT)|X\d(D[C-Z]|[E-V][A-Z]|W[A-N])\d)$').match(placa):
        return u'TLA'
    
    if re.compile(r'^(T\d{3}[W-Z]|U\d{3}[A-V]|(T[P-Z]|U[A-K])[A-Z]\d{2}|Y((9[8-9])BT|\{d}(B[U-Z]|[C-M][A-Z]|N[A-S])|([0-4]\d|50)NT)|X\d(W[P-Z]|[X-Z][A-Z])\d|Y\d([A-N][A-Z]|PA)\d)$').match(placa):
        return u'VER'
    
    if re.compile(r'^(U\d{3}[W-Z]|W\d{3}[A-R]|(U[L-Z]|V[A-K])[A-Z]\d{2}|Y((5[1-9]|[6-9]\d)NT|\d{2}(N[U-Z]|[P-Z][A-Z]))|Z(\d{2}A[A-S]|(0[0-3])AT)|Y\d(P[B-Z]|[R-Z][A-Z])\d|Z\d([A-F][A-Z]|G[A-M])\d)$').match(placa):
        return u'YUC'
    
    if re.compile(r'^(W\d{3}[S-Z]|V[L-Z][A-Z]\d{2}|L\d{2}[A-Z]{2}|Z\d(G[N-Z]|[H-Z][A-Z])\d)$').match(placa):
        return u'ZAC'

def estado_particular(placa):
    if re.compile(r'^(\d{3}[A-Z]{3}|[A-Z]\d{2}[A-Z]{3})$').match(placa):
        return u'DIF'
    
    if re.compile(r'^(L[G-Z]|[M-N][A-Z]|P[A-E])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'MEX'
    
    if re.compile(r'^A[A-F][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'AGU'
    
    if re.compile(r'^(A[G-Z]|B[A-Z]{1}|C[A-Y])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'BCN'
    
    if re.compile(r'^(CZ|D[A-E])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'BCS'
    
    if re.compile(r'^D[F-K][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'CAM'
    
    if re.compile(r'^D[L-S][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'CHP'
    
    if re.compile(r'^(D[T-Z]|E[A-T])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'CHH'
    
    if re.compile(r'^(E[U-Z]|F[A-P])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'COA'
    
    if re.compile(r'^F[R-W][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'COL'
    
    if re.compile(r'^(F[X-Z]|G[A-F])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'DUR'
    
    if re.compile(r'^G[G-Y][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'GUA'
    
    if re.compile(r'^(GZ|H[A-F])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'GRO'
    
    if re.compile(r'^H[G-R][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'HID'
    
    if re.compile(r'^(H[S-Z]|[J-K][A-Z]|L[A-F])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'JAL'
    
    if re.compile(r'^P[F-U][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'MIC'
    
    if re.compile(r'^(P[V-Z]|R[A-D])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'MOR'
    
    if re.compile(r'^R[E-J][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'NAY'
    
    if re.compile(r'^(R[K-Z]|S[A-Z]|T[A-G])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'NLE'
    
    if re.compile(r'^T[H-M][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'OAX'
    
    if re.compile(r'^(T[N-Z]|U[A-J])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'PUE'
    
    if re.compile(r'^U[K-P][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'QUE'
    
    if re.compile(r'^U[R-V][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'ROO'
    
    if re.compile(r'^(U[W-Z]|V[A-E])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'SLP'
    
    if re.compile(r'^V[F-S][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'SIN'
    
    if re.compile(r'^(V[T-Z]|W[A-K])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'SON'
    
    if re.compile(r'^W[L-W][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'TAB'
    
    if re.compile(r'^(W[X-Z]|X[A-S])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'TAM'
    
    if re.compile(r'^X[T-X][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'TLA'
    
    if re.compile(r'^(X[Y-Z]|Y[A-V])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'VER'
    
    if re.compile(r'^(Y[W-Z]|Z[A-C])[A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'YUC'
    
    if re.compile(r'^Z[D-H][A-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'ZAC'

def estado_discapacitado(placa):
    if re.compile(r'^(\d{3}(S[W-Z]|[T-Z][A-Z])|\d{2}[A-Z]\d{2})$').match(placa):
        return u'DIF'
    
    if re.compile(r'^(\d{3}E[L-V]|\d{2}F(DZ|[E-T][A-Z]|U[A-D]))$').match(placa):
        return u'MEX'
    
    if re.compile(r'^(\d{3}A[A-J]|\d{2}A([A-N][A-Z]|P[A-E]))$').match(placa):
        return u'AGU'
    
    if re.compile(r'^(\d{3}A[K-U]|\d{2}(A(P[F-Z]|[R-Z][A-Z])|B([A-C][A-Z]|D[A-K])))$').match(placa):
        return u'BCN'
    
    if re.compile(r'^(\d{3}(A[V-Z]|B[A-D])\d{2}B(D[L-Z]|[E-S][A-Z]|T[A-R]))$').match(placa):
        return u'BCS'
    
    if re.compile(r'^(\d{3}B[E-N]|\d{2}(B(T[S-Z]|[U-Z][A-Z])|C([A-F][A-Z]|G[A-W])))$').match(placa):
        return u'CAM'
    
    if re.compile(r'(^\d{3}B[P-Y]|\d{2}C(G[X-Z]|[H-W][A-Z]|X[A-B]))$').match(placa):
        return u'CHP'
    
    if re.compile(r'^(\d{3}(BZ|C[A-H])|\d{2}(C(X[C-Z]|[Y-Z][A-Z])|D([A-K][A-Z]|L[A-G])))$').match(placa):
        return u'CHH'
    
    if re.compile(r'^(\d{3}(C[J-Z]|D[A-R])|\d{2}(D(L[H-Z]|[M-Z][A-Z])|EA[A-M]))$').match(placa):
        return u'COA'
    
    if re.compile(r'^(\d{3}(D[S-Z]|EA)|\d{2}E(A[N-Z]|[B-N][A-Z]|P[A-T]))$').match(placa):
        return u'COL'
    
    if re.compile(r'^(\d{3}E[B-K]|\d{2}(E(P[U-Z]|[R-Z][A-Z])|F([A-C][A-Z]|D[A-Y])))$').match(placa):
        return u'DUR'
    
    if re.compile(r'^(\d{3}(E[W-Z]|F[A-E])|\d{2}(F(U[E-Z]|[V-Z][A-Z])|G([A-G][A-Z]|H[A-J])))$').match(placa):
        return u'GUA'
    
    if re.compile(r'^(\d{3}F[F-P]|\d{2}G(H[K-Z]|[J-W][A-Z]|X[A-P]))$').match(placa):
        return u'GRO'
    
    if re.compile(r'^(\d{3}(F[R-Z]|G[A-X])|\d{2}(G(X[R-Z]|[Y-Z][A-Z])|H([A-K][A-Z]|L[A-V])))$').match(placa):
        return u'HID'
    
    if re.compile(r'^(\d{3}(G[Y-Z]|J[A-E])|\d{2}(H(L[W-Z]|[M-Z][A-Z])|J(A[A-Z]|BA)))$').match(placa):
        return u'JAL'
    
    if re.compile(r'^(\d{3}J[F-P]|\d{2}J(B[B-Z]|[C-P][A-Z]|R[A-F]))$').match(placa):
        return u'MIC'
    
    if re.compile(r'^(\d{3}J[R-Z]|\d{2}(J(R[G-Z]|[S-Z][A-Z])|K([A-D][A-Z]|E[A-L])))$').match(placa):
        return u'MOR'
    
    if re.compile(r'^(\d{3}K[A-J]|\d{2}K(E[M-Z]|[F-T][A-Z]|U[A-S]))$').match(placa):
        return u'NAY'
    
    if re.compile(r'^(\d{3}(K[L-Z]|L[A-T])|\d{2}(K(U[T-Z]|[V-Z][A-Z])|L([A-G][A-Z]|H[A-X])))$').match(placa):
        return u'NLE'
    
    if re.compile(r'^(\d{3}(L[U-Z]|M[A-C])|\d{2}L(H[Y-Z]|[J-X][A-Z]|Y[A-C]))$').match(placa):
        return u'OAX'
    
    if re.compile(r'^(\d{3}M[D-M]|\d{2}(L(Y[D-Z]|Z[A-Z])|M([A-L][A-Z]|M[A-H])))$').match(placa):
        return u'PUE'
    
    if re.compile(r'^(\d{3}M[N-X]|\d{2}(M(M[J-Z]|[N-Z][A-Z])|N(A[A-Z]|B[A-N])))$').match(placa):
        return u'QUE'
    
    if re.compile(r'^(\d{3}(M[Y-Z]|N[A-G])|\d{2}N(B[P-Z]|[C-P][A-Z]|R[A-U))$').match(placa):
        return u'ROO'
    
    if re.compile(r'^(\d{3}N[H-S]|\d{2}(N(R[V-Z]|[S-Z][A-Z])|P([A-D][A-Z]|E[A-Z])))$').match(placa):
        return u'SLP'
    
    if re.compile(r'^(\d{3}(N[T-Z]|P[A-B])|\d{2}P(F[A-Z]|[G-U][A-Z]|V[A-E]))$').match(placa):
        return u'SIN'
    
    if re.compile(r'^(\d{3}P[C-L]|\d{2}(P(V[F-Z]|[W-Z][A-Z])|R([A-H][A-Z]|J[A-K])))$').match(placa):
        return u'SON'
    
    if re.compile(r'^(\d{3}P[M-W]|\d{2}R(J[L-Z]|[K-X][A-Z]|Y[A-R]))$').match(placa):
        return u'TAB'
    
    if re.compile(r'^(\d{3}(P[X-Z]|R[A-F])|\d{2}(R(Y[S-Z]|Z[A-Z])|S([A-L][A-Z]|M[A-W])))$').match(placa):
        return u'TAM'
    
    if re.compile(r'^(\d{3}R[G-R]|\d{2}(S(M[X-Z]|[T-Z][A-Z])|T([A-B][A-Z]|C[A-B])))$').match(placa):
        return u'TLA'
    
    if re.compile(r'^(\d{3}(R[S-Z]|SA)|\d{2}T(C[C-Z]|[D-R][A-Z]|S[A-G]))$').match(placa):
        return u'VER'
    
    if re.compile(r'^(\d{3}S[B-K]|\d{2}(T(S[H-Z)|[U-Z][A-Z]|U([A-E][A-Z]|F[A-M])))$').match(placa):
        return u'YUC'
    
    if re.compile(r'^(\d{3}S[L-V]|\d{2}U(F[N-Z]|[G-U][A-Z]|V[A-T]))$').match(placa):
        return u'ZAC'

# def estado_taxi(placa):
#     if validar_placa_particular(placa) == False:
#         raise Exception
# 
#     if re.compile(r'').match(placa):
#         return u'DIF'
#     
#     if re.compile(r'').match(placa):
#         return u'MEX'
#     
#     if re.compile(r'').match(placa):
#         return u'AGU'
#     
#     if re.compile(r'').match(placa):
#         return u'BCN'
# 
#     if re.compile(r'').match(placa):
#         return u'BCS'
# 
#     if re.compile(r'').match(placa):
#         return u'CAM'
# 
#     if re.compile(r'').match(placa):
#         return u'CHP'
# 
#     if re.compile(r'').match(placa):
#         return u'CHH'
# 
#     if re.compile(r'').match(placa):
#         return u'COA'
# 
#     if re.compile(r'').match(placa):
#         return u'COL'
# 
#     if re.compile(r'').match(placa):
#         return u'DUR'
# 
#     if re.compile(r'').match(placa):
#         return u'GUA'
# 
#     if re.compile(r'').match(placa):
#         return u'GRO'
# 
#     if re.compile(r'').match(placa):
#         return u'HID'
# 
#     if re.compile(r'').match(placa):
#         return u'JAL'
# 
#     if re.compile(r'').match(placa):
#         return u'MIC'
# 
#     if re.compile(r'').match(placa):
#         return u'MOR'
# 
#     if re.compile(r'').match(placa):
#         return u'NAY'
# 
#     if re.compile(r'').match(placa):
#         return u'NLE'
# 
#     if re.compile(r'').match(placa):
#         return u'OAX'
# 
#     if re.compile(r'').match(placa):
#         return u'PUE'
# 
#     if re.compile(r'').match(placa):
#         return u'QUE'
# 
#     if re.compile(r'').match(placa):
#         return u'ROO'
# 
#     if re.compile(r'').match(placa):
#         return u'SLP'
# 
#     if re.compile(r'').match(placa):
#         return u'SIN'
# 
#     if re.compile(r'').match(placa):
#         return u'SON'
# 
#     if re.compile(r'').match(placa):
#         return u'TAB'
# 
#     if re.compile(r'').match(placa):
#         return u'TAM'
# 
#     if re.compile(r'').match(placa):
#         return u'TLA'
# 
#     if re.compile(r'').match(placa):
#         return u'VER'
# 
#     if re.compile(r'').match(placa):
#         return u'YUC'
# 
#     if re.compile(r'').match(placa):
#         return u'ZAC'

def estado_camion_privado(placa):
    if re.compile(r'^(\d{4}|[A-Z]\d{3})[A-Z]{2}$').match(placa):
        return u'DIF'
    
    if re.compile(r'^(K[L-Z]|L[A-Z]|M[A-S])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'MEX'
    
    if re.compile(r'^A[A-F](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'AGU'
    
    if re.compile(r'^(A[G-Z]|B[A-Z]|C[A-D])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'BCN'
    
    if re.compile(r'^C[E-L](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'BCS'
    
    if re.compile(r'^C[M-U](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'CAM'
    
    if re.compile(r'^(C[V-Z]|D[A-C])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'CHP'
    
    if re.compile(r'^(D[D-Z]|E[A-G])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'CHH'
    
    if re.compile(r'^(E[H-Z]|F[A-B])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'COA'
    
    if re.compile(r'^F[C-J](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'COL'
    
    if re.compile(r'^F[K-X](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'DUR'
    
    if re.compile(r'^(F[Y-Z]|G[A-W])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'GUA'
    
    if re.compile(r'^(G[X-Z]|H[A-G])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'GRO'
    
    if re.compile(r'^H[H-T](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'HID'
    
    if re.compile(r'^(H[U-Z]|J[A-Z]|K[A-K](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'JAL'
    
    if re.compile(r'^(M[T-Z]|N[A-Z])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'MIC'
    
    if re.compile(r'^N[U-Z](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'MOR'
    
    if re.compile(r'^P[A-G](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'NAY'
    
    if re.compile(r'^(P[H-Z]|R[A-P])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'NLE'
    
    if re.compile(r'^R[R-Y](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'OAX'
    
    if re.compile(r'^(RZ|S[A-R])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'PUE'
    
    if re.compile(r'^S[S-Y](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'QUE'
    
    if re.compile(r'^(SZ|T[A-B])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'ROO'
    
    if re.compile(r'^T[C-P](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'SLP'
    
    if re.compile(r'^(T[R-Z]|U[A-L])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'SIN'
    
    if re.compile(r'^(U[M-Z]|V[A-K])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'SON'
    
    if re.compile(r'^V[L-T](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'TAB'
    
    if re.compile(r'^(V[U-Z]|W[A-X])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'TAM'
    
    if re.compile(r'^(W[Y-Z]|X[A-E])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'TLA'
    
    if re.compile(r'^(X[F-Z]|Y[A-M])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'VER'
    
    if re.compile(r'^Y[N-U](\d{5}|\d{4}[A-Z])$').match(placa):
        return u'YUC'
    
    if re.compile(r'^(Y[V-Z]|Z[A-J])(\d{5}|\d{4}[A-Z])$').match(placa):
        return u'ZAC'


def estado_autobus_privado(placa):
    if re.compile(r'^(\d[A-Z]{3}|\d{2}[A-Z]\d)$').match(placa):
        return u'DIF'
    
    if re.compile(r'^\d{1,2}(H[R-Z][A-Z]|J[A-Z]{2}|K[A-H][A-Z]|KJ[A-G])\d{2}$').match(placa):
        return u'MEX'
    
    if re.compile(r'^\d{1,2}A(A[A-Z]|B[A-R])\d{2}$').match(placa):
        return u'AGU'
    
    if re.compile(r'^\d{1,2}A(B[S-Z]|[C-M][A-Z]|N[A-W])\d{2}$').match(placa):
        return u'BCN'
    
    if re.compile(r'^\d{1,2}A(N[X-Z]|P[A-Z])\d{2}$').match(placa):
        return u'BCS'
    
    if re.compile(r'^\d{1,2}A(R[A-Z]|S[A-L])\d{2}$').match(placa):
        return u'CAM'
    
    if re.compile(r'^\d{1,2}A(S[M-Z]|[T-Y][A-Z])\d{2}$').match(placa):
        return u'CHP'
    
    if re.compile(r'^\d{1,2}(AZ[A-Z]|[B-C][A-Z]{2}|D[A-C][A-Z])\d{2}$').match(placa):
        return u'CHH'
    
    if re.compile(r'^\d{1,2}D[D-S][A-Z]\d{2}$').match(placa):
        return u'COA'
    
    if re.compile(r'^\d{1,2}D[T-U][A-Z]\d{2}$').match(placa):
        return u'COL'
    
    if re.compile(r'^\d{1,2}(D[V-Z][A-Z]|E[A-R][A-Z]|ES[A-R])\d{2}$').match(placa):
        return u'DUR'
    
    if re.compile(r'^\d{1,2}(E[S-Z][A-Z]|F[A-R][A-Z])\d{2}$').match(placa):
        return u'GUA'
    
    if re.compile(r'^\d{1,2}(F[S-Z][A-Z]|GA[A-Z])\d{2}$').match(placa):
        return u'GRO'
    
    if re.compile(r'^\d{1,2}G[B-M][A-Z]\d{2}$').match(placa):
        return u'HID'
    
    if re.compile(r'^\d{1,2}(G[N-Z][A-Z]|H[A-P][A-Z])\d{2}$').match(placa):
        return u'JAL'
    
    if re.compile(r'^\d{1,2}K(J[H-Z]|[K-X][A-Z])\d{2}$').match(placa):
        return u'MIC'
    
    if re.compile(r'^\d{1,2}K(Y[A-Z]|Z[A-M])\d{2}$').match(placa):
        return u'MOR'
    
    if re.compile(r'^\d{1,2}(KZ[N-Z]|LA[A-Z])\d{2}$').match(placa):
        return u'NAY'
    
    if re.compile(r'^\d{1,2}(L[B-Z][A-Z]|M[A-M][A-Z])\d{2}$').match(placa):
        return u'NLE'
    
    if re.compile(r'^\d{1,2}M[N-T][A-Z]\d{2}$').match(placa):
        return u'OAX'
    
    if re.compile(r'^\d{1,2}(M[U-Z][A-Z]|N[A-C][A-Z])\d{2}$').match(placa):
        return u'PUE'
    
    if re.compile(r'^\d{1,2}N[D-K][A-Z]\d{2}$').match(placa):
        return u'QUE'
    
    if re.compile(r'^\d{1,2}N[L-S][A-Z]\d{2}$').match(placa):
        return u'ROO'
    
    if re.compile(r'^\d{1,2}(N[T-Z][A-Z]|P[A-Z]{2}|R[A-F][A-Z])\d{2}$').match(placa):
        return u'SLP'
    
    if re.compile(r'^\d{1,2}(R[G-Z][A-Z]|[S-T][A-Z]{2})\d{2}$').match(placa):
        return u'SIN'
    
    if re.compile(r'^\d{1,2}U[A-M][A-Z]\d{2}$').match(placa):
        return u'SON'
    
    if re.compile(r'^\d{1,2}(U[N-Z][A-Z]|V[A-N][A-Z])\d{2}$').match(placa):
        return u'TAB'
    
    if re.compile(r'^\d{1,2}(V[P-Z][A-Z]|W[A-X][A-Z])\d{2}$').match(placa):
        return u'TAM'
    
    if re.compile(r'^\d{1,2}(W[Y-Z][A-Z]|X[A-E][A-Z])\d{2}$').match(placa):
        return u'TLA'
    
    if re.compile(r'^\d{1,2}(X[F-Z][A-Z]|Y[A-Z]{2}|ZA[A-Z])\d{2}$').match(placa):
        return u'VER'
    
    if re.compile(r'^\d{1,2}Z[B-K][A-Z]\d{2}$').match(placa):
        return u'YUC'
    
    if re.compile(r'^\d{1,2}Z[L-N][A-Z]\d{2}$').match(placa):
        return u'ZAC'

def estado_remolque_privado(placa):
    if re.compile(r'^([A-Z]\d{4}|[A-Z]\d[A-Z]\d{2})$').match(placa):
        return u'DIF'
    
    if re.compile(r'^\d(H[U-Z]|[J-L][A-Z]|M[A-J])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'MEX'
    
    if re.compile(r'^\dA[A-E](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'AGU'
    
    if re.compile(r'^\d(A[F-Z]|B[A-D])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'BCN'
    
    if re.compile(r'^\dB[E-J](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'BCS'
    
    if re.compile(r'^\dB[K-P](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'CAM'
    
    if re.compile(r'^\dB[R-Y](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'CHP'
    
    if re.compile(r'^\d(BZ|C[A-X])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'CHH'
    
    if re.compile(r'^\d(A[F-Z]|B[A-D])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'COA'
    
    if re.compile(r'^\d(C[Y-Z]|D[A-Z]|E[A-V])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'COL'
    
    if re.compile(r'^\dF[B-Y](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'DUR'
    
    if re.compile(r'^\d(FZ|G[A-E])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'GUA'
    
    if re.compile(r'^\dG[F-S](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'GRO'
    
    if re.compile(r'^\d(G[T-Z]|H[A-F])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'HID'
    
    if re.compile(r'^\dH[G-T](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'JAL'
    
    if re.compile(r'^\dM[K-X](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'MIC'
    
    if re.compile(r'^\d(M[Y-Z]|N[A-C])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'MOR'
    
    if re.compile(r'^\dN[D-L](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'NAY'
    
    if re.compile(r'^\d(N[M-Z]|P[A-F])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'NLE'
    
    if re.compile(r'^\dP[G-L](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'OAX'
    
    if re.compile(r'^\dP[M-Z](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'PUE'
    
    if re.compile(r'^\dR[A-H](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'QUE'
    
    if re.compile(r'^\dR[J-N](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'ROO'
    
    if re.compile(r'^\dR[P-U](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'SLP'
    
    if re.compile(r'^\d(R[V-Z]|S[A-T])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'SIN'
    
    if re.compile(r'^\d(S[U-Z]|[T-V][A-Z]|W[A-B])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'SON'
    
    if re.compile(r'^\dW[C-G](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'TAB'
    
    if re.compile(r'^\d(W[H-Z]|XA)(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'TAM'
    
    if re.compile(r'^\dX[B-W](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'TLA'
    
    if re.compile(r'^\d(X[X-Z]|Y[A-N])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'VER'
    
    if re.compile(r'^\dY[P-U](\d{4}|\d{3}[A-Z])$').match(placa):
        return u'YUC'
    
    if re.compile(r'^\d(Y[V-Z]|Z[A-K])(\d{4}|\d{3}[A-Z])$').match(placa):
        return u'ZAC'

def estado_taxi(placa):
    if re.compile(r'^([A-Z](\d{5}|\d{4}[A-Z])|\d{7}|\d{3}[A-Z]\d{3})$').match(placa):
        return u'DIF'
    
    if re.compile(r'^(\d{4}|[A-Z]\d{3})(J[E-Z]|K[A-Z]|LA)[A-Z]$').match(placa):
        return u'MEX'
    
    if re.compile(r'^(\d{4}|[A-Z]\d{3})A[A-C][A-Z]$').match(placa):
        return u'AGU'
    
    if re.compile(r'^(\d{4}|[A-Z]\d{3})A[D-U][A-Z]$').match(placa):
        return u'BCN'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(A[V-Z]|B[A-D])[A-Z]$').match(placa):
        return u'BCS'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})B[E-G][A-Z]$').match(placa):
        return u'CAM'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})B[H-V][A-Z]$').match(placa):
        return u'CHP'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(B[W-Z]|C[A-S])[A-Z]$').match(placa):
        return u'CHH'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(C[T-Z]|D[A-U])[A-Z]$').match(placa):
        return u'COA'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})D[V-X][A-Z]$').match(placa):
        return u'COL'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(D[Y-Z]|E[A-F])[A-Z]$').match(placa):
        return u'DUR'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(E[G-Z]|F[A-E])[A-Z]$').match(placa):
        return u'GUA'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})F[F-T][A-Z]$').match(placa):
        return u'GRO'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(F[U-Z]|G[A-L])[A-Z]$').match(placa):
        return u'HID'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(G[M-Z]|H[A-Z]|J[A-D])[A-Z]$').match(placa):
        return u'JAL'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})L[B-S][A-Z]$').match(placa):
        return u'MIC'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(L[T-Z]|M[A-C])[A-Z]$').match(placa):
        return u'MOR'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})M[D-J][A-Z]$').match(placa):
        return u'NAY'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(M[K-Z]|[N-R][A-Z]|S[A-H])[A-Z]$').match(placa):
        return u'NLE'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})S[J-R][A-Z]$').match(placa):
        return u'OAX'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(S[S-Z]|T[A-F])[A-Z]$').match(placa):
        return u'PUE'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})T[G-L][A-Z]$').match(placa):
        return u'QUE'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})T[M-R][A-Z]$').match(placa):
        return u'ROO'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})T[S-U][A-Z]$').match(placa):
        return u'SLP'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(T[V-Z]|U[A-N])[A-Z]$').match(placa):
        return u'SIN'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(U[P-Z]|V[A-L])[A-Z]$').match(placa):
        return u'SON'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})V[M-R][A-Z]$').match(placa):
        return u'TAB'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(V[S-Z]|W[A-V])[A-Z]$').match(placa):
        return u'TAM'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(W[W-Z]|X[A-B])[A-Z]$').match(placa):
        return u'TLA'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(X[C-Z]|Y[A-R])[A-Z]$').match(placa):
        return u'VER'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})(Y[S-Z]|Z[A-E])[A-Z]$').match(placa):
        return u'YUC'

    if re.compile(r'^(\d{4}|[A-Z]\d{3})Z[F-K][A-Z]$').match(placa):
        return u'ZAC'

def estado_camion_publico(placa):
    if re.compile(r'^\d{6,7}$').match(placa):
        return u'DIF'
    
    if re.compile(r'^\d(K[U-Z]|[L-M][A-Z]|N[A-J])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'MEX'
    
    if re.compile(r'^\dA[A-G][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'AGU'
    
    if re.compile(r'^\d(A[H-Z]|B[A-U])(\d{3}|\d{2}[A-Z])$').match(placa):
        return u'BCN'

    if re.compile(r'^\d(B[V-Z]|C[A-F])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'BCS'

    if re.compile(r'^\dC[G-L][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'CAM'

    if re.compile(r'^\d(C[M-Z]|D[A-Z])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'CHP'

    if re.compile(r'^\d(E[A-Z]|FA)[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'CHH'

    if re.compile(r'^\dF[B-X][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'COA'

    if re.compile(r'^\d(F[Y-Z]|G[A-D])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'COL'

    if re.compile(r'^\d(G[E-Z]|H[A-C])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'DUR'

    if re.compile(r'^\dH[D-Y][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'GUA'

    if re.compile(r'^\d(HZ|J[A-J])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'GRO'

    if re.compile(r'^\dJ[K-T][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'HID'

    if re.compile(r'^\d(J[K-Z]|K[A-T])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'JAL'

    if re.compile(r'^\dN[K-X][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'MIC'

    if re.compile(r'^\d(N[Y-Z]|P[A-E])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'MOR'

    if re.compile(r'^\d(P[F-Z]|RA)[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'NAY'

    if re.compile(r'^\dR[B-S][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'NLE'

    if re.compile(r'^\d(R[T-Z]|S[A-B])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'OAX'

    if re.compile(r'^\dS[C-L][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'PUE'

    if re.compile(r'^\dS[M-V][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'QUE'

    if re.compile(r'^\dS[W-Y][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'ROO'

    if re.compile(r'^\d(SZ|T[A-M])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'SLP'

    if re.compile(r'^\d(T[N-Z]|U[A-M])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'SIN'

    if re.compile(r'^\d(U[N-Z]|V[A-Z]|W[A-G])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'SON'

    if re.compile(r'^\dW[H-N][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'TAB'

    if re.compile(r'^\dW[P-X][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'TAM'

    if re.compile(r'^\d(W[Y-Z]|X[A-C])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'TLA'

    if re.compile(r'^\d(X[D-Z]|Y[A-J])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'VER'

    if re.compile(r'^\d(Y[K-Z]|Z[A-E])[A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'YUC'

    if re.compile(r'^\dZ[F-J][A-Z](\d{3}|\d{2}[A-Z])$').match(placa):
        return u'ZAC'


def estado_antiguos(placa):
    if re.compile(r'^(C[M-Z]\d{3}|\d[A-Z]{2}\d{2})$').match(placa):
        return u'DIF'
    
    if re.compile(r'^(G[J-Z]\d{2}|(L[X-Z]|M[A-Z]|N[A-J])\d[A-Z])$').match(placa):
        return u'MEX'
    
    if re.compile(r'^(B[V-Z]\d{2}|F[A-P]\d[A-Z])$').match(placa):
        return u'AGU'
    
    if re.compile(r'^(C[A-J]\d{2}|(F[R-Z]|G[A-L])\d[A-Z])$').match(placa):
        return u'BCN'

    if re.compile(r'^(C[K-R]\d{2}|G[M-Z]\d[A-Z])$').match(placa):
        return u'BCS'

    if re.compile(r'^(C[S-W]\d{2}|H[A-K]\d[A-Z])$').match(placa):
        return u'CAM'

    if re.compile(r'^((C[X-Z]|D[A-B])\d{2}|H[L-X]\d[A-Z])$').match(placa):
        return u'CHP'

    if re.compile(r'^(D[C-R]\d{2}|(H[Y-Z]|J[A-M])\d[A-Z])$').match(placa):
        return u'CHH'

    if re.compile(r'^((D[S-Z]|E[A-B])\d{2}|(J[N-Z]|K[A-N])\d[A-Z])$').match(placa):
        return u'COA'

    if re.compile(r'^(E[C-F]\d{2}|K[P-Z]\d[A-Z])$').match(placa):
        return u'COL'

    if re.compile(r'^(E[G-R]\d{2}|L[A-W]\d[A-Z])$').match(placa):
        return u'DUR'

    if re.compile(r'^(E[S-Z]\d{2}|N[K-X]\d[A-Z])$').match(placa):
        return u'GUA'

    if re.compile(r'^(F[A-E]\d{2}|(N[Y-Z]|P[A-H])\d[A-Z])$').match(placa):
        return u'GRO'

    if re.compile(r'^(F[F-P]\d{2}|(P[J-Z]|R[A-F])\d[A-Z])$').match(placa):
        return u'HID'

    if re.compile(r'^((F[R-Z]|G[A-H])\d{2}|R[G-Z]\d[A-Z])$').match(placa):
        return u'JAL'

    if re.compile(r'^(H[A-G]\d{2}|S[A-J]\d[A-Z])$').match(placa):
        return u'MIC'

    if re.compile(r'^(H[H-S]\d{2}|S[K-S]\d[A-Z])$').match(placa):
        return u'MOR'

    if re.compile(r'^(H[T-W]\d{2}|S[T-X]\d[A-Z])$').match(placa):
        return u'NAY'

    if re.compile(r'^((H[X-Z]|J[A-M])\d{2}|(S[Y-Z]|T[A-N])\d[A-Z])$').match(placa):
        return u'NLE'

    if re.compile(r'^(J[N-U]\d{2}|T[P-V]\d[A-Z])$').match(placa):
        return u'OAX'

    if re.compile(r'^((J[V-Z]|K[A-D])\d{2}|(T[W-Z]|U[A-F])\d[A-Z])$').match(placa):
        return u'PUE'

    if re.compile(r'^(K[E-R]\d{2}|U[G-T]\d[A-Z])$').match(placa):
        return u'QUE'

    if re.compile(r'^(K[S-W]\d{2}|U[U-Y]\d[A-Z])$').match(placa):
        return u'ROO'

    if re.compile(r'^((K[X-Z]|L[A-L])\d{2}|(UZ|V[A-N])\d[A-Z])$').match(placa):
        return u'SLP'

    if re.compile(r'(^L[M-Z]\d{2}|(V[P-Z]|W[A-B])\d[A-Z])$').match(placa):
        return u'SIN'

    if re.compile(r'^(M[A-U]\d{2}|W[C-V]\d[A-Z])$').match(placa):
        return u'SON'

    if re.compile(r'^(M[V-Z]\d{2}|(W[W-Z]|XA)\d[A-Z])$').match(placa):
        return u'TAB'

    if re.compile(r'^(N[A-S]\d{2}|X[B-U]\d[A-Z])$').match(placa):
        return u'TAM'

    if re.compile(r'^(N[T-Z]\d{2}|(X[V-Z]|Y[A-B])\d[A-Z])$').match(placa):
        return u'TLA'

    if re.compile(r'^(P[A-N]\d{2}|Y[C-R]\d[A-Z])$').match(placa):
        return u'VER'

    if re.compile(r'^(P[P-Z]\d{2}|(Y[S-Z]|Z[A-B])\d[A-Z])$').match(placa):
        return u'YUC'

    if re.compile(r'^(R[A-Z]\d{2}|Z[C-Z]\d[A-Z])$').match(placa):
        return u'ZAC'

def parse_placa(placa):
    clean_placa = placa.upper()
    if 'I' in placa:
        raise Exception
    if 'O' in placa:
        raise Exception
#     if 'Q' in placa:
#         raise Exception
    try:
        tipo = tipo_de_placa(clean_placa)
    except:
        tipo_placa, created = models.TipoPlaca.objects.get_or_create(tipo='particular', estado='DIF')
        return tipo_placa
    if 'CDMX' in tipo:
        estado = u'DIF'
    elif tipo == 'Particular':
        estado = estado_particular(clean_placa)
    elif tipo == 'Motocicleta':
        estado = estado_motocicleta(clean_placa)
    elif tipo == 'Discapacitado':
        estado = estado_discapacitado(clean_placa)
    elif tipo == 'Auto Antiguo':
        estado = estado_antiguos(clean_placa)
    elif tipo == 'Taxi':
        estado = estado_taxi(clean_placa)
    elif tipo == 'Autobús':
        estado = estado_autobus_privado(clean_placa)
    elif tipo == 'Camión Privado':
        estado = estado_camion_privado(clean_placa)
    elif tipo == 'Transporte Público':
        estado = estado_camion_publico(clean_placa)
    elif tipo == 'Remolque':
        estado = estado_remolque_privado(clean_placa)
    try:
        tipo_placa, created = models.TipoPlaca.objects.get_or_create(tipo=tipo, estado=estado)
        return tipo_placa
    except:
        tipo_placa, created = models.TipoPlaca.objects.get_or_create(tipo='Particular', estado='DIF')
        return tipo_placa