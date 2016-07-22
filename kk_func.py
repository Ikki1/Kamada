
# coding: utf-8

# In[50]:

from functools import reduce
import sympy as sp
from sympy import oo
import numpy as np
sp.init_printing()
from nbsupport import md
from itertools import chain
from sympy.simplify.cse_main import cse
from itertools import product, chain

###
def display_substitution(substitution):
    md('$', *chain.from_iterable([[v, r'\mapsto ', e, r'\quad '] for v, e in substitution]), '$')
    
# The dimension of the visualization: choose 2 or 3 for 2D/3D visualization, respectively.
dimension = 2

# k: Strength of the spring (Hook's Law)
# l: Natural length of the spring
k_ij, l_ij = [sp.Symbol(s, real=True, positive=True)
        for s in r'\bar{k_{ij}} \bar{\ell_{ij}}'.split()]

# p, q: i'th and j'th points connected by the spring (k_ij, l_ij)
p, q = [sp.Matrix([sp.Symbol(v + '_' + str(i), real=True) for i in range(dimension)])
        for v in 'p q'.split()]


##md(r'Locations of the vertices $\boldsymbol{p}$ and $\boldsymbol{q}$: $', p, ', ', q, '$')

# The actual length of the spring is the distance between points p and q
length = (p - q).norm()
##md('**The actual length of the spring**: $', length, '$')

# The potential energy as given by Hook's Law and its derivatives
potential = k_ij * (length - l_ij) ** 2 / 2

potentials = [
    sp.Matrix([potential]),
    sp.Matrix([potential]).jacobian(p).T,
    sp.hessian(potential, p)]

# ###
# def display_potentials(potentials):
#     for i, p in zip(range(len(potentials)), potentials):
#         md('$$\mathbf {Potential}', "'" * i, ': ', p, '$$')
#         md('-----')

# ##display_potentials(potentials)

# cse_result = cse_substitution, eliminated = cse(potentials)

# ##display_potentials(eliminated)

# def expand_cse_substitution(cse_substitution):
#     substitution = []
#     for v, e in cse_substitution:
#         substitution.append((v, e.subs(substitution)))
#     return substitution

# ##display_substitution(expand_cse_substitution(cse_substitution))

# def pick_cse(proposed_substitution, *args):
#     proposed_substitution = expand_cse_substitution(proposed_substitution)
#     cse_substitution, lambda_substitution = [], []
#     for i, v1, v2 in args:
#         _, e = proposed_substitution[i]
#         cse_substitution.append((e, sp.Symbol(v1)))
#         if v2:
#             lambda_substitution.append((sp.Symbol(v1), sp.Symbol(v2)))
#     return cse_substitution, lambda_substitution

# cse_substitution, lambda_substitution = pick_cse(
#     expand_cse_substitution(cse_substitution),
#     (6, r'\Delta\ell{}', 'l'), (5, 'r', None), (2, 'r1', None), (0, 'r0', None))

# ##display_substitution(cse_substitution)

# potentials = [p.subs(cse_substitution) for p in potentials]

# ##
# display_potentials(potentials)


# In[51]:

symbols = (k_ij, l_ij, p, q)
f_potentials = [[sp.lambdify(symbols, s) for s in potential] for potential in potentials]


# In[ ]:



