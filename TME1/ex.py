import constraint

# Dimension du problème
n = 8
# Cr eation du problème
pb = constraint.Problem()
# Cŕeation d’une variable python de dimension n
cols = range(n)
# Cŕeation d’une variable cols dont le domaine est {1, ..., n}
pb.addVariables(cols, range(n))
# Ajout de la contrainte AllDiff
pb.addConstraint(constraint.AllDifferentConstraint())
# Ŕecuṕeration de l’ensemble des solutions possibles
s = pb.getSolution()

print(s)


n = 3
p = constraint.Problem()
x = range(1, n**2 + 1)
p.addVariables(x, x)
p.addConstraint(constraint.AllDifferentConstraint())
# Variable contenant la somme de chaque ligne/colonne/diagonale
s = n**2 * (n**2 + 1) / 6
# Ajout des contraintes du carŕe magique
for k in range(n):
    # ligne k
    p.addConstraint(constraint.ExactSumConstraint(s), [x[k*n+i] for i in range(n)])
    # colonne k
    p.addConstraint(constraint.ExactSumConstraint(s), [x[k+n*i] for i in range(n)])
    # première diagonale
    p.addConstraint(constraint.ExactSumConstraint(s), [x[n*i+i] for i in range(n)])
    # deuxième diagonale
    p.addConstraint(constraint.ExactSumConstraint(s), [x[(n-1)*i] for i in range(1, n+1)])
s = p.getSolution()
print(s)