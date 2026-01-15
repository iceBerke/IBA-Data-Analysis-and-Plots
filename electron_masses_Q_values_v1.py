# Check if electron masses cancel out in a nuclear reaction

# Developed with the help of Claude.AI and ChatGPT v5.2
# Last updated: 07/01/2026

import re

# Minimal periodic table mapping needed for Z lookup

Z_TABLE = {
    "H": 1,  "He": 2, "Li": 3, "Be": 4, "B": 5,  "C": 6,  "N": 7,  "O": 8,  "F": 9,  "Ne": 10,
    "Na": 11,"Mg": 12,"Al": 13,"Si": 14,"P": 15, "S": 16, "Cl": 17,"Ar": 18,
    "K": 19, "Ca": 20, "Sc": 21,"Ti": 22,"V": 23, "Cr": 24,"Mn": 25,"Fe": 26,"Co": 27,"Ni": 28,
    "Cu": 29,"Zn": 30,"Ga": 31,"Ge": 32,"As": 33,"Se": 34,"Br": 35,"Kr": 36
}

# Common particles often written as p, d, t, a (alpha)
ALIASES = {
    "p":  ("H", 1),    # treat as 1H atom for electron counting
    "d":  ("H", 2),    # 2H atom
    "a":  ("He", 4)   # 4He atom
}

def parse_species(token: str):
    t = token.strip()
    
    # Step 1: Remove channel labels (p0→p, p1→p, a0→a)
    t = re.sub(r'([a-zA-Zαγ])\d+$', r'\1', t)
    # "p1" becomes "p", "a0" becomes "a"
    
    # Step 2: Remove excited state markers
    t = t.replace("*", "")
    # "17O*" becomes "17O"
    
    # Step 3: Check if it's an alias (p, d, a)
    if t in ALIASES:
        sym, A = ALIASES[t]  # e.g., "p" → ("H", 1)
        Z = Z_TABLE.get(sym)  # Z for H is 1
        if Z is None:
            raise ValueError(f"Element symbol '{sym}' not in Z_TABLE.")
        return Z
    
    # Step 4: Parse nuclide notation like "16O"
    m = re.fullmatch(r'(\d+)([A-Z][a-z]?)', t)
    # This regex captures: (number)(Element)
    # "16O" → groups: ("16", "O")
    if not m:  # ← ADD THIS CHECK
        raise ValueError(f"Can't parse species token: '{token}'")
    
    A = int(m.group(1))      # Mass number: 16
    sym = m.group(2)         # Element symbol: "O"
    Z = Z_TABLE.get(sym)     # Atomic number: 8
    
    if Z is None:  # ← ADD THIS CHECK
        raise ValueError(f"Element symbol '{sym}' not in Z_TABLE (token '{token}').")
    return Z

def electrons_cancel(reactants, products):

    Z_left = sum(parse_species(x) for x in reactants)
    Z_right = sum(parse_species(x) for x in products)
    return {"Z_left": Z_left, "Z_right": Z_right, "Electron masses cancel": (Z_left == Z_right)}

# ---- Examples ----
print(electrons_cancel(["16O", "d"], ["a0", "14N"]))   
print(electrons_cancel(["16O", "d"], ["p0", "17O"]))   
print(electrons_cancel(["16O", "d"], ["p1", "17O*"]))

