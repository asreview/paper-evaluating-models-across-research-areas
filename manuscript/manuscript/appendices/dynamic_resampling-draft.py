Input:


Output:


from math import log, floor

import numpy as np

from asreview.balance_strategies.base import BaseBalance
from asreview.balance_strategies.simple import SimpleBalance
from asreview.utils import get_random_state


class DoubleBalance(BaseBalance):
    """Class for the double balance strategy.

    Class to get the two way rebalancing function and arguments.
    It super samples ones depending on the number of 0's and total number
    of samples in the training data.

    Arguments
    ---------
    a: float
        Governs the weight of the 1's. Higher values mean linearly more 1's
        in your training sample.
    alpha: float
        Governs the scaling the weight of the 1's, as a function of the
        ratio of ones to zeros. A positive value means that the lower the
        ratio of zeros to ones, the higher the weight of the ones.
    b: float
        Governs how strongly we want to sample depending on the total
        number of samples. A value of 1 means no dependence on the total
        number of samples, while lower values mean increasingly stronger
        dependence on the number of samples.
    beta: float
        Governs the scaling of the weight of the zeros depending on the
        number of samples. Higher values means that larger samples are more
        strongly penalizing zeros.
    """

    name = "double"


read
n_read = len(read)
# characteristics of the already labeled publications
one_idx = where(read == 1)
zero_idx = where(read == 0)
n_one = len(one_idx)
n_zero: len(zero_idx)
n_train = n_one + n_zero

# Compute the weights.
one_weight =  a * (n_one / n_zero)**(-alpha)
zero_weight = weight = 1 - (1 - b) * (1 + log(n_read))**(-beta)
tot_zo_weight =  one_weight * n_one + zero_weight * n_zero

# number of inclusions to sample
n_one_train = one_weight * n_one * n_train / tot_zo_weight
# minimaal 1 inclusie, en altijd 2plekken over voor exclusie
n_one_train = max(1, min(n_train - 2, n_one_train))
# what is left is for the exclusions
n_zero_train = n_train - n_one_train

# sample inclusions and exclusions
one_train_idx = sample(n_one_train, one_idx)
zero_train_idx = sample(n_zero_train, zero_idx)

# Copy/sample until there are n_train indices sampled
sample(n_x_train, idx):
    # n x train = desired size of training sample, nxread = how much you've read
    # number of copies needed, rounded down.
    n_copy = n_x_train / len(idx)
    # for the remainder, sample
    n_sample = n_x_train % len(idx)
    # paste idx n_copy times
    x_train = tile(idx, n_copy)
    # add sample
    x_train = append(x_train, random_sample(idx, n_sample))
    return(n_x_train)






    n_copy = np.int(n_train / len(src_idx))

    n_sample = n_train - n_copy * len(src_idx)
    # tile = kopieren van inclusies tot remainder, remainder random samplen.
    dest_idx = np.tile(src_idx, n_copy).reshape(-1)

    # Add samples to finish up.
    dest_idx = np.append(dest_idx,
                         random_state.choice(src_idx, n_sample, replace=False))
    return dest_idx



# put together and shuffle
    def __init__(self, a=2.155, alpha=0.94, b=0.789, beta=1.0,
                 random_state=None):


        # Get random ones and zeros.
        one_train_idx = fill_training(one_idx, n_one_train, self._random_state)
        zero_train_idx = fill_training(zero_idx, n_zero_train,
                                       self._random_state)

        # put together ones and zeroes
        all_idx = np.concatenate([one_train_idx, zero_train_idx])
        # shuffle
        self._random_state.shuffle(all_idx)
        # training en result matrix
        return X[all_idx], y[all_idx]

    def full_hyper_space(self):
        from hyperopt import hp
        parameter_space = {
            "bal_a": hp.lognormal("bal_a", 0, 1),
            "bal_alpha": hp.uniform("bal_alpha", 0, 2),
            "bal_b": hp.uniform("bal_b", 0, 1),
            # "bal_beta": hp.uniform("bal_beta", 0, 2), = 1
        }
        return parameter_space, {}


def _one_weight(n_one, n_zero, a, alpha):
    """Get the weight of the ones."""
    weight = a * (n_one / n_zero)**(-alpha)
    return weight


def _zero_weight(n_read, b, beta):
    """Get the weight of the zeros."""
    weight = 1 - (1 - b) * (1 + log(n_read))**(-beta)
    return weight


def random_round(value, random_state):
    """Round up or down, depending on how far the value is.

    For example: 8.1 would be rounded to 8, 90% of the time, and rounded
    to 9, 10% of the time.
    """
    base = int(floor(value))
    if random_state.rand() < value - base:
        base += 1
    return base


def fill_training(src_idx, n_train, random_state):
    """Copy/sample until there are n_train indices sampled.
    """
    # Copy as many as we need, rounded down.
    n_copy = np.int(n_train / len(src_idx))

    n_sample = n_train - n_copy * len(src_idx)
    # tile = kopieren van inclusies tot remainder, remainder random samplen.
    dest_idx = np.tile(src_idx, n_copy).reshape(-1)

    # Add samples to finish up.
    dest_idx = np.append(dest_idx,
                         random_state.choice(src_idx, n_sample, replace=False))
    return dest_idx
