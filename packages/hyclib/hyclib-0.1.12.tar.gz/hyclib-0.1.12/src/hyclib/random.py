import random
import contextlib

import numpy as np
import torch

@contextlib.contextmanager
def set_seed(seed):
    python_state = random.getstate()
    np_state = np.random.get_state()
    torch_state = torch.random.get_rng_state()
    random.seed(seed)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    try:
        yield
    finally:
        random.setstate(python_state)
        np.random.set_state(np_state)
        torch.random.set_rng_state(torch_state)