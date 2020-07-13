from astropy import constants as const
from astropy import units as u

def time_in_ms(t, m=1):
    M = m * u.Msun
    T = t * const.G * M / const.c**3
    return T.to(u.ms)

def length_in_km(d, m=1):
    M = m * u.Msun
    D = d * const.G * M / const.c**2
    return D.to(u.km)

if __name__ == "__main__":
    print(time_in_ms(20))
    print(length_in_km(1))
