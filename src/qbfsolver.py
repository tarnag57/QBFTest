from pyeda.inter import *

a, b, c, d = map(exprvar, 'abcd')
kernel = (~a | ~b) & (b | c | d) & (a | d) & (c | d) & (~c | ~d) & (~a | b | c | ~d)
kernel = kernel.to_cnf()
print(kernel)
print(list(kernel.satisfy_all()))
with ~a, ~b:
    sats = kernel.satisfy_one()
    print(sats)
