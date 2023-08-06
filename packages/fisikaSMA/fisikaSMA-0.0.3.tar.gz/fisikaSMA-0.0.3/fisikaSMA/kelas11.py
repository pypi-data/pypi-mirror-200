def doppler_effect(frequency, observer_velocity, source_velocity, speed_of_sound=343.2):
    """
    Fungsi ini menghitung pergeseran frekuensi yang disebabkan oleh efek Doppler.
    
    Arguments:
        frequency (float): frekuensi asli dari gelombang suara, dalam Hz
        observer_velocity (float): kecepatan sumber, dalam m/s
        speed_of_sound (float): kecepatan suara, dalam m/s
        
    Returns:
        float: frekuensi yang bergeser, dalam Hz
    """
    vo = float(observer_velocity)
    vs = float(source_velocity)
    c = float(speed_of_sound)
    f = float(frequency)
    
    shifted_frequency = f * ((c + vo) / (c - vs))
    
    return shifted_frequency

def pascals_law(f1, a1, a2):
    """
    Menghitung gaya (f2) pada piston kedua menurut Hukum Pascal.
    f1: Gaya diterapkan ke piston pertama
    a1: Luas piston pertama
    a2: Luas piston kedua
    """
    f2 = (f1 * a2) / a1
    return f2


def inersia_bola(m, r, pejal=False):
    """
    Fungsi ini menghitung momen inersia dari bola jika berputar terhadap pusat massanya. Mengukur kelembaman, atau seberapa susah benda tersebut berputar. 
    
    Arguments:
    m -- massa bola (kg) 
    r -- jari-jari bola (meter) 
    pejal -- apakah bola tersebut pejal? (True, False) 
    
    Returns:
    mi -- momen inersia (kg.m^2)
    """ 
    k = 2/3
    if pejal:
	    k = 2/5
    mi = k*m*r**2
    return mi
