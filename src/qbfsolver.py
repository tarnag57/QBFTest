from pyeda.inter import *
from pyeda.boolalg import *

with open('aim-100-1_6-no-1.cnf', 'r') as cnf_file:
    kernel = expr.ast2expr(parse_cnf(cnf_file.read()))
print(kernel)
print(list(kernel.satisfy_all()))
sats = kernel.satisfy_one()
print(sats)
