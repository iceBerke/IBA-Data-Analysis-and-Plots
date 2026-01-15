# Python script for the calculation of Q-values of nuclear reactions common in
# NRA analysis
# The formula applied assumes electron homogeneity in the nuclear reaction 
# (between reactants and products)
# Use electron_masses_Q_values_v1 to check for electron homogeneity

# GUI Calculator

# Add a reset button and a copy Q button too

# Developed with the help of Claude.AI and ChatGPT v5.2
# Last updated: 07/01/2026

import tkinter as tk
from tkinter import ttk, messagebox

class QValueCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Nuclear Reaction Q-Value Calculator")
        self.root.geometry("500x500")
        
        # Conversion factors
        # Dalton to kilograms
        self.DALTON_TO_KG = 1.66053906660e-27 # kg
        # Electron volt to joules
        self.EV_TO_J = 1.602176634e-19 # J
        #self.u_to_MeV = 931.49410242  # MeV/u
        
        # Speed of light
        self.c = 299792458

        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="Nuclear Reaction: A(a,b(0, 1, etc.))B", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input fields for masses
        row = 1
        
        # Target A
        ttk.Label(main_frame, text="Atomic mass of A (target nucleus) [u/Da]:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.mass_A = ttk.Entry(main_frame, width=20)
        self.mass_A.grid(row=row, column=1, pady=5)
        
        # Projectile a
        row += 1
        ttk.Label(main_frame, text="Atomic mass of a (incident particle) [u/Da]:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.mass_a = ttk.Entry(main_frame, width=20)
        self.mass_a.grid(row=row, column=1, pady=5)
        
        # Ejectile b
        row += 1
        ttk.Label(main_frame, text="Atomic mass of b (ejected particle) [u/Da]:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.mass_b = ttk.Entry(main_frame, width=20)
        self.mass_b.grid(row=row, column=1, pady=5)
        
        # Residual B
        row += 1
        ttk.Label(main_frame, text="Atomic mass of B (residual nucleus) [u/Da]:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.mass_B = ttk.Entry(main_frame, width=20)
        self.mass_B.grid(row=row, column=1, pady=5)
        
        # Excited state energy
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, 
                                                            sticky=(tk.W, tk.E), pady=15)
        
        row += 1
        ttk.Label(main_frame, text="Excitation energy E_x [keV]:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.E_excited = ttk.Entry(main_frame, width=20)
        self.E_excited.insert(0, "0.0")  # Default to ground state
        self.E_excited.grid(row=row, column=1, pady=5)
        
        # Calculate button
        row += 1
        calc_button = ttk.Button(main_frame, text="Calculate Q-Value", command=self.calculate)
        calc_button.grid(row=row, column=0, columnspan=2, pady=20)
        
        # Results frame
        row += 1
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.result_Q0 = tk.StringVar(value="Q₀ = --- keV")
        self.result_Q = tk.StringVar(value="Q = --- keV")
        
        ttk.Label(results_frame, textvariable=self.result_Q0, font=('Arial', 11)).pack(anchor=tk.W, pady=5)
        ttk.Label(results_frame, textvariable=self.result_Q, font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=5)
        
    def calculate(self):

        try:
            # Get masses
            m_A = float(self.mass_A.get())
            m_a = float(self.mass_a.get())
            m_b = float(self.mass_b.get())
            m_B = float(self.mass_B.get())
            E_x = float(self.E_excited.get())

            mA = m_A * self.DALTON_TO_KG
            ma = m_a * self.DALTON_TO_KG
            mb = m_b * self.DALTON_TO_KG
            mB = m_B * self.DALTON_TO_KG
            
            # Calculate Q0 in MeV
            Q0 = (mA + ma - mb - mB) * (self.c**2) / self.EV_TO_J
            Q0_keV = Q0 / 1000
            
            # Calculate corrected Q-value
            Q_keV = Q0_keV - E_x
            
            # Display results
            self.result_Q0.set(f"Q₀ = {Q0_keV:.3f} keV ")
            self.result_Q.set(f"Q = {Q_keV:.3f} keV ")
            
            # Warning for endothermic reactions
            if Q_keV < 0:
                messagebox.showinfo("Endothermic Reaction", 
                                   f"This reaction is endothermic (Q < 0).\n"
                                   f"A threshold energy is required.")
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numerical values for all masses.")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QValueCalculator(root)
    root.mainloop()
