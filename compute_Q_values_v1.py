# Python script for the calculation of Q-values of nuclear reactions common in
# NRA analysis
# The formula applied assumes electron homogeneity in the nuclear reaction 
# (between reactants and products)
# Use electron_masses_Q_values_v1 to check for electron homogeneity

# Developed with the help of Claude.AI and ChatGPT v5.2
# Last updated: 07/01/2026

# Values from Atomic Mass Table (https://www-nds.iaea.org/masses/mass.mas03)
# Other source (same as the excited energy values): https://www-nds.iaea.org/relnsd/vcharthtml/VChartHTML.html 

# Boron 11 mass in u or Daltons
m_B11 = 11.009305167
unc_B11= 13e-9

# Carbon 12 mass in u or Daltons
m_C12 = 12.0000000
unc_C12 = 0

# Carbon 13 mass in u or Daltons
m_C13 = 13.00335483534
unc_C13 = 25e-11

# Nitrogen 14 mass in u or Daltons
m_N14 = 14.00307400425 
unc_N14 = 24e-11

# Nitrogen 15 mass in u or Daltons
m_N15 = 15.0001088983
unc_N15 = 6e-10

# Oxygen 16 mass in u or Daltons
#m_O16 = 15.99491461956
m_O16 = 15.9949146193 
unc_O16 = 3e-10

# Oxygen 17 mass in u or Daltons
#m_O17 = 16.999131703 
m_O17 = 16.9991317560
unc_O17 = 7e-10

# Deuterium mass in u or Daltons
#m_deuterium = 2.01410177785  
m_deuterium = 2.01410177784 
unc_deuterium = 2e-11

# Proton mass in u or Daltons
#m_proton  = 1.00782503207   
m_proton = 1.00782503190 
unc_proton = 1e-11

# 4He (~ alpha-particle) mass in u or Daltons
m_alpha = 4.00260325413 
unc_alpha = 16e-11

# Conversion factors
# Dalton to kilograms
DALTON_TO_KG = 1.66053906660e-27 # kg
# Electron volt to joules
EV_TO_J = 1.602176634e-19 # J

u_to_MeV = 931.49410242  # MeV/u

# Convert Dalton to Kg
m_A_O16 = m_O16 * DALTON_TO_KG
m_a_deuterium = m_deuterium * DALTON_TO_KG
m_b_proton = m_proton * DALTON_TO_KG
m_B_O17 = m_O17 * DALTON_TO_KG
m_b_alpha = m_alpha * DALTON_TO_KG
m_B_N14 = m_N14 * DALTON_TO_KG

c = 299792458

# Obtain Q0 value
Q0_O16_deuterium_proton_O17 = (m_A_O16 + m_a_deuterium - m_b_proton - m_B_O17) * (c**2) / EV_TO_J
Q0_O16_deuterium_proton_O17_kev = Q0_O16_deuterium_proton_O17 / 1000

Q0_O16_deuterium_alpha_N14 = (m_A_O16 + m_a_deuterium - m_b_alpha - m_B_N14) * (c**2) / EV_TO_J
Q0_O16_deuterium_alpha_N14_kev = Q0_O16_deuterium_alpha_N14 / 1000
#print(f"Q0(016_d_p1_O17) = {Q0_O16_deuterium_proton_O17_kev:.3f} keV")

# Excited state (E_x in keV)
# Source: https://www-nds.iaea.org/relnsd/vcharthtml/VChartHTML.html 
E_O17_p1 = 870.756	
E_O17_p0 = 0.0
E_N14_a0 = 0.0

E_N15_p1 = 5270.155
E_N15_p2 = 5298.822 
E_N15_p3 = 6323.78
E_N15_p4 = 7155.05
E_N15_p5 = 7300.83
E_N15_p6 = 7567.1
E_N15_p7 = 8312.62

E_C12_a1 = 4439.82 

E_B11_a1 = 2124.693 

# Corrected Q-value 
Q1_O16_d_p1_O17 = Q0_O16_deuterium_proton_O17_kev - E_O17_p1
Q1_O16_d_p0_O17 = Q0_O16_deuterium_proton_O17_kev - E_O17_p0
Q1_O16_d_a0_N14 = Q0_O16_deuterium_alpha_N14_kev - E_N14_a0
print(f"Q1(O16_d_p1_O17) = {Q1_O16_d_p1_O17:.3f} keV")
print(f"Q1(O16_d_p0_O17) = {Q1_O16_d_p0_O17:.3f} keV")
print(f"Q1(O16_d_a0_N14) = {Q1_O16_d_a0_N14:.3f} keV")
