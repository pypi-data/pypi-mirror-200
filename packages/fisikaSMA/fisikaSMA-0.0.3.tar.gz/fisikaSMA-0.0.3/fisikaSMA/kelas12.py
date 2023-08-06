def lorentz(i1, i2, p, j):
    """
    Fungsi ini menghitung Gaya Lorentz antara dua kawat sejajar akibat arus listrik.
    
    Arguments:
    i1 -- kuat arus di kawat 1 (ampere) 
    i2 -- kuat arus di kawat 2 (ampere) 
    p -- panjang kawat (meter) 
    j -- jarak antara kedua kawat (meter) 

    Returns:
    f -- gaya lorentz (N)
    """ 
    f = 2*10**-7*i1*i2*p/j
    return f

def ohm(V, I):
    """
    Fungsi ini menghitung arus listrik dengan menggunakan Hukum Ohm.
    
    Arguments:
    V -- tegangan listrik (volt)
    I -- arus listrik (ampere)  


    Returns:
    R -- hambatan listrik (ohm)
    """ 
    R = V/I
    return R

def relativitas_kec(v1,v2):
    """
    Fungsi ini menghitung relativitas kecepatan benda 1 terhadap benda 2.
    
    Arguments:
    v1 -- kecepatan benda 1 (m/s) 
    v2 -- kecepatan benda 2 (m/s)
    c -- kecepatan cahaya (3x10^8 m/s)


    Returns:
    v -- kecepatan relatif benda 1 terhadap benda 2 (m/s)
    """ 
    c = 300000000
    v = ((v1+v2)/(1+((v1*v2)/(c^2))))
    return v