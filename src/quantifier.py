import enum
from pyeda.inter import *
from typing import *


class Quantifier(enum.Enum):
    """
    Enum for quantifier types
    """
    Exists = 0
    Forall = 1


class QuantExpr:

    def __init__(self, quantifier: Quantifier, variables: List[int]):
        """
        :param quantifier: Quantifier enum, existential or universal
        :param variables: List of ints, variables corresponding to that quantifier
        """
        self.quantifier = quantifier
        self.variables = variables

    def __str__(self):
        quantifier_str = "\u2203" if self.quantifier == Quantifier.Exists else "\u2200"
        tokens_str = map(lambda var: 'x[{}]'.format(var), self.variables)
        return '{} {}\n'.format(quantifier_str, ', '.join(tokens_str))


class QBFFormula:

    def __init__(self, quants: List[QuantExpr], kernel):
        """
        :param quants: list of QuantExprs, quantifiers in front of the kernel
        :param kernel: Pyeda expression, kernel of the formula
        """
        self.quants = quants
        self.kernel = kernel

    def __str__(self):
        quant_str = map(lambda q: str(q), self.quants)
        return '{}\n{}\n'.format(''.join(quant_str), self.kernel)
