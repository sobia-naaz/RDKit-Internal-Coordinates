from rdkit import Chem
from rdkit.Chem import AllChem, rdMolTransforms

# Create molecule (Ethanol example)
smiles = "C[C@@H](C(=O)O)NC(=O)[C@H](CC(C)C)N"
mol = Chem.MolFromSmiles(smiles)

if mol is None:
    print("Error creating molecule")
    exit()

# Add hydrogens
mol = Chem.AddHs(mol)

# Generate 3D coordinates
AllChem.EmbedMolecule(mol)

# Optimize geometry
AllChem.UFFOptimizeMolecule(mol)

# Get conformer
conf = mol.GetConformer()

# ================================
# CARTESIAN COORDINATES
# ================================
print("\n=== CARTESIAN COORDINATES ===")
for atom in mol.GetAtoms():
    pos = conf.GetAtomPosition(atom.GetIdx())
    print(f"{atom.GetSymbol()} {atom.GetIdx()}: {pos.x:.3f}, {pos.y:.3f}, {pos.z:.3f}")

# ================================
# BOND LENGTHS
# ================================
print("\n=== BOND LENGTHS ===")
for bond in mol.GetBonds():
    i = bond.GetBeginAtomIdx()
    j = bond.GetEndAtomIdx()
    dist = rdMolTransforms.GetBondLength(conf, i, j)
    print(f"{i}-{j}: {dist:.3f} Å")

# ================================
# BOND ANGLES
# ================================
print("\n=== BOND ANGLES ===")
for atom in mol.GetAtoms():
    neighbors = [n.GetIdx() for n in atom.GetNeighbors()]
    if len(neighbors) >= 2:
        for i in range(len(neighbors)):
            for j in range(i+1, len(neighbors)):
                angle = rdMolTransforms.GetAngleDeg(conf, neighbors[i], atom.GetIdx(), neighbors[j])
                print(f"{neighbors[i]}-{atom.GetIdx()}-{neighbors[j]}: {angle:.2f}°")

# ================================
# DIHEDRAL ANGLES
# ================================
print("\n=== DIHEDRAL ANGLES ===")
for bond in mol.GetBonds():
    i = bond.GetBeginAtomIdx()
    j = bond.GetEndAtomIdx()

    neighbors_i = [n.GetIdx() for n in mol.GetAtomWithIdx(i).GetNeighbors() if n.GetIdx() != j]
    neighbors_j = [n.GetIdx() for n in mol.GetAtomWithIdx(j).GetNeighbors() if n.GetIdx() != i]

    for a in neighbors_i:
        for b in neighbors_j:
            dihedral = rdMolTransforms.GetDihedralDeg(conf, a, i, j, b)
            print(f"{a}-{i}-{j}-{b}: {dihedral:.2f}°")

# ================================
# Z-MATRIX
# ================================
print("\n=== Z-MATRIX ===")

atoms = mol.GetAtoms()

for i, atom in enumerate(atoms):
    symbol = atom.GetSymbol()

    if i == 0:
        print(symbol)

    elif i == 1:
        dist = rdMolTransforms.GetBondLength(conf, 0, 1)
        print(f"{symbol} 1 {dist:.3f}")

    elif i == 2:
        dist = rdMolTransforms.GetBondLength(conf, 1, 2)
        angle = rdMolTransforms.GetAngleDeg(conf, 0, 1, 2)
        print(f"{symbol} 2 {dist:.3f} 1 {angle:.2f}")

    else:
        dist = rdMolTransforms.GetBondLength(conf, i-1, i)
        angle = rdMolTransforms.GetAngleDeg(conf, i-2, i-1, i)
        dihedral = rdMolTransforms.GetDihedralDeg(conf, i-3, i-2, i-1, i)
        print(f"{symbol} {i} {dist:.3f} {i-1} {angle:.2f} {i-2} {dihedral:.2f}")

