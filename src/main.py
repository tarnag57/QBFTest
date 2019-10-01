import utils as utils
import os

filename = '{}\\..\\problems\\SmallProblems\\test.qdimacs'.format(os.getcwd())
stuff = utils.read_qdimacs_file(filename)
print(stuff)
