---
captured: 2026-08-21T18:10:15+00:00
session: a5946b21-5223-4113-ae7e-b97d07860b91
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3629
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are a ruthless, evidence-bound analyst. Rule ONLY from the passage
provided. No prior knowledge. If the passage does not address the claim, verdict
is "unverifiable". NEVER "supported" without a passage that directly supports it.
Cite the source_ids you relied on. Confident wrongness is the worst outcome.

VERDICT AXIOM:
  "supported"    = the passage AFFIRMS the claim.
  "refuted"      = the passage NEGATES the claim.
  "unverifiable" = the passage does not address the claim.

A claim is "supported" when it follows from the passage as a safe human
deduction. Do not demand that the passage restate the claim word for word.
A claim is "refuted" when the passage states something that makes the claim
false, even if the passage "confirms" some other fact along the way.

Return ONLY valid JSON. No prose, no code fences.

Claim: The main difference between sigma bonds and pi bonds is that sigma bonds are stronger and more directional, while pi bonds are weaker and less directional.

Passages:
[s0054] [1] Pi bonds are formed by the sidewise positive (same phase) overlap of atomic orbitals along a direction perpendicular to the internuclear axis. During the formation of π bonds, the axes of the atomic orbitals are parallel to each other whereas the overlapping is perpendicular to the internuclear axis. This type of covalent bonding is illustrated below.[Image: Pi Bonds]Pi Bonds are generally weaker than sigma bonds, owing to the significantly lower degree of overlapping. Generally, double bonds consist of one sigma and one pi bond, whereas a typical triple bond is made up of two π bonds and one σ bond. It is important to note that a combination of sigma and pi bonds is always stronger than a single sigma bond.

[2] In chemistry, sigma bonds (σ bonds) are the strongest type of covalent chemical bond.[1] They are formed by head-on overlapping between atomic orbitals. Sigma bonding is most simply defined for diatomic molecules using the language and tools of symmetry groups. In this formal approach, a σ-bond is symmetrical with respect to rotation about the bond axis. By this definition, common forms of sigma bonds are s+s, p_z+p_z, s+p_z and d z^2+d z^2 (where z is defined as the axis of the bond or the internuclear axis).[2] Quantum theory also indicates that molecular orbitals (MO) of identical symmetry actually mix or hybridize. As a practical consequence of this mixing of diatomic molecules, the wavefunctions s+s and p_z+p_z molecular orbitals become blended. The extent of this mixing (or hybridization or blending) depends on the relative energies of the MOs of like symmetry.

[3] A sigma bond is stronger than a pi bond. The reason is that the overlapping of atomic orbitals can take place to a greater extent during the formation of a sigma bond, whereas overlapping of orbitals occurs to a smaller extent during the formation of a pi bond.
A pi bond between two atoms is formed only in addition to a sigma bond. The reason is that the atoms constituting a single bond prefer to form a strong sigma bond rather than a weak pi bond.
Thus, a pi bond is always present in molecules with multiple bonds, i.e., double or triple bonds. In other words, a single bond cannot be a pi bond.
There can be free rotation of atoms around the sigma bonds. Free rotation of atoms around pi bonds is not possible because it involves breaking the pi bonds.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
