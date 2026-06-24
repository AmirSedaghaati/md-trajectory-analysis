"""
RMSD and RMSF analysis of a short GROMACS MD trajectory.
Demo/portfolio project — simulation system follows the standard
Lemkul "Lysozyme in Water" GROMACS tutorial (PDB 1AKI).
This is not connected to any published research.
"""
import MDAnalysis as mda
from MDAnalysis.analysis import rms, align
import matplotlib.pyplot as plt
import numpy as np
import os

TOPOLOGY = "md_0_1.tpr"
TRAJECTORY = "md_0_1.xtc"
OUTPUT_DIR = "results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

u = mda.Universe(TOPOLOGY, TRAJECTORY)
print(f"Loaded {len(u.atoms)} atoms across {len(u.trajectory)} frames")

# --- RMSD over time, aligned to the first frame ---
align.AlignTraj(u, u, select="protein and backbone", in_memory=True).run()
rmsd_calc = rms.RMSD(u, u, select="protein and backbone", ref_frame=0).run()
time_ns = rmsd_calc.results.rmsd[:, 1] / 1000  # ps -> ns
rmsd_values = rmsd_calc.results.rmsd[:, 2]      # Angstrom

plt.figure(figsize=(7, 4))
plt.plot(time_ns, rmsd_values)
plt.xlabel("Time (ns)")
plt.ylabel("RMSD (Å)")
plt.title("Backbone RMSD vs. time")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/rmsd.png", dpi=150)
print(f"RMSD plot saved. Mean RMSD: {rmsd_values.mean():.2f} Å")

# --- RMSF per residue (CA atoms) ---
ca_atoms = u.select_atoms("protein and name CA")
rmsf_calc = rms.RMSF(ca_atoms).run()

plt.figure(figsize=(8, 4))
plt.plot(ca_atoms.resids, rmsf_calc.results.rmsf)
plt.xlabel("Residue number")
plt.ylabel("RMSF (Å)")
plt.title("Per-residue flexibility (RMSF)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/rmsf.png", dpi=150)
print(f"RMSF plot saved. Most flexible residue: {ca_atoms.resids[np.argmax(rmsf_calc.results.rmsf)]}")

print("\nDone. Check the results/ folder for rmsd.png and rmsf.png.")