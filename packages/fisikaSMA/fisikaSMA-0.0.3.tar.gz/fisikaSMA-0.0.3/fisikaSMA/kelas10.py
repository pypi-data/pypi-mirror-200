def GLB(V, t):
    """
    Fungsi ini digunakan untuk menghitung jarak pada Gerak Lurus Beraturan.
    
    Arguments:
    V -- kecepatan dalam m/s (velocity) 
    t -- waktu dalam s (time) 

    Returns:
    s -- jarak dalam m (space)
    """ 

    s = V*t
    return s

def GLBB(V0,a,s):
    """
    Fungsi ini digunakan untuk menghitung kecepatan akhir pada Gerak Lurus Berubah Beraturan.
    
    Arguments:
    V0 -- kecepatan awal dalam m/s (velocity) 
    s -- jarak dalam m (space)
    a -- percepatan dalam m/s^2 (acceleration)

    Returns:
    Vt -- kecepatan akhir dalam m/s (velocity) 
    """ 

    Vt = (V0**2 + 2*a*s)**0.5
    return Vt


def Impuls(F, dt):
    """
    Fungsi ini digunakan untuk menghitung besaran impuls suatu benda.
    
    Arguments:
    F -- gaya impulsif (N)
    dt -- perubahan waktu (s) 
    
    Returns:
    Im – Impuls (Ns) 
    """ 

    Im = F*dt
    return Im
