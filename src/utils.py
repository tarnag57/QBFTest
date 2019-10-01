"""
Utility functions such as file reading and parsing
"""
import pyeda as pyeda
from quantifier import *
import typing as typing


def read_qdimacs_file(filename: str):
    """
    :param filename: The file containing the quantified expression in QDIMACS format
    :return: QBFormula parsed from the file
    """
    with open(filename, 'r') as file:
        line = file.readline()

        # Skip comments
        while line.startswith('c'):
            line = file.readline()

        # Parse QBF line
        param_line = line
        tokens = param_line.split(' ')
        if len(tokens) != 4:
            raise_qdimacs_exception('parameter line has wrong number of tokens (found: {})'.format(len(tokens)))

        if tokens[0] != 'p':
            raise Exception('parameter line should start with a \'p\'')

        if tokens[1] != 'cnf':
            raise Exception('parameter line should have \'cnf\' as its second token')

        # Quantified expressions
        var_num = int(tokens[2])

        quants, line_pos = parse_quant_exprs(file, var_num)
        file.seek(line_pos)

        # Parse kernel
        content = file.read()
        kernel_str = '{}{}'.format(param_line, content)
        kernel = pyeda.boolalg.expr.ast2expr(parse_cnf(kernel_str))

        return QBFFormula(quants, kernel)


def parse_quant_exprs(
        file: typing.TextIO,
        var_num: int,
    ) -> (typing.List[QuantExpr], int):
    """
    :param file: File handler with cursor at the first quantifier line
    :param var_num: Number of variables
    :return: The parsed quant expressions and the line position of the SAT part
    """

    quants = []
    used_vars = [0 for _ in range(var_num)]       # Enforce invariants

    while True:
        line_pos = file.tell()
        line = file.readline()
        tokens = line.split(' ')

        if tokens[0] != 'a' and tokens[0] != 'e':
            for i in range(var_num):
                if used_vars[i] == 0:
                    raise_qdimacs_exception('variable {} is unbound'.format(i+1))

            break

        quantifier = Quantifier.Exists if tokens[0] == 'a' else Quantifier.Forall
        int_tokens = list(map(lambda x: int(x), tokens[1:]))

        # Truncate the the last '0' token
        int_tokens = int_tokens[:-1]

        # Bookkeeping
        for token in int_tokens:
            if used_vars[token-1] != 0:
                raise Exception("variable {} has been bound multiple times".format(token))
            used_vars[token-1] = 1

        quants.append(QuantExpr(quantifier, int_tokens))

    return quants, line_pos


def raise_qdimacs_exception(s: str):
    raise Exception('Invalid QDIMACS file format, {}'.format(s))
