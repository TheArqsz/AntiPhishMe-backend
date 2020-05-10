from collections import Counter
import numpy as np
# Remember mixed standard python functions and numpy functions are very slow 
def get_entropy(x):
    p, lens = Counter(x), np.float(len(x))
    return -sum( count/lens * np.log2(count/lens) for count in p.values())
