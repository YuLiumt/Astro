# =======================================
# 一些基本方程
# =======================================
def baryonic_mass(gravitational_mass):
	"""
	由 gravitational mass 计算 baryonic mass
	"""
	return gravitational_mass + 0.075 * gravitational_mass ** 2

def gravitational_mass_2(chirp_mass, mass_ratio):
	"""
	由 chirp_mass, mass_ratio 计算 gravitational_mass_2
	"""	
	return chirp_mass * ((1 + mass_ratio) / (mass_ratio ** 3)) ** (1/5)

def gravitational_mass_1(gravitational_mass_2, mass_ratio):
	"""
	由 gravitational_mass_2, mass_ratio 计算 gravitational_mass_1
	"""	
	return gravitational_mass_2 * mass_ratio

def Compactness(gravitational_mass, EOS):
	"""
	For a given NS EoS, Compactness are determined by M
	"""
	EOSList = ['ALF2', 'BB2', 'H3', 'MS2', 'SLy4', 'ALF4', 'DD2', 'H4', 'NL3', 'TM1', 'APR', 'ENG', 'MPA1', 'SFHo', 'TMA', 'APR3', 'GS2', 'MS1', 'SFHx', 'APR4', 'GlendNH3', 'MS1b', 'SLy'] 

	assert EOS in EOSList, 'The equation of state is not in the folder of EOS_gravitationalMass_Compactness!'

	filename = 'EOS_gravitationalMass_Compactness/' + EOS + '.txt'
	with open(filename) as f :
	
	return 1

def M_ej(chirp_mass, mass_ratio, EOS):
	"""
	The dynamical ejecta mass are determined by the gravitational mass of the two NSs and NS EOSs
	"""	

	# the fitting coefficients from numerical relativity simulations.
	a = - 1.357
	b = 6.113
	c = - 49.434
	d = 16.114
	n = 2.548
	
	m_2 = gravitational_mass_2(chirp_mass, mass_ratio)
	m_1 = gravitational_mass_1(m_2, mass_ratio)
	c_1 = Compactness(m_1, EOS)
	c_2 = Compactness(m_2, EOS)
	b_1 = baryonic_mass(m_1)
	b_2 = baryonic_mass(m_2)
	
	return (a * (m_2 / m_1) ** (1/3) * ((1 - 2 * c_1)/c_1) + b * (m_2 / m_1) ** n) * b_1 + \
	(a * (m_1 / m_2) ** (1/3) * ((1 - 2 * c_2)/c_2) + b * (m_1 / m_2) ** n) * b_2 + \
	c * ((b_1 + b_2) - (m_1 + m_2)) + d

if __name__ == '__main__':
	print(M_ej(1.12, 1., 'ALF2'))