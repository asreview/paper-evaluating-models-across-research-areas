Input:
    - read, all publications that have been labeled.
    - a, alpha and b.


Output: Train, a balanced training dataset, supersampling inclusions depending on the number of exclusions and total number of publications that have been labeled.

Parameters:
a - Governs the weight of the 1's. Higher values mean linearly more 1's
    in your training sample.
alpha - Governs the scaling the weight of the 1's, as a function of the
    ratio of ones to zeros. A positive value means that the lower the
    ratio of zeros to ones, the higher the weight of the ones.
b - Governs how strongly we want to sample depending on the total
    number of samples. A value of 1 means no dependence on the total
    number of samples, while lower values mean increasingly stronger
    dependence on the number of samples.
beta - Governs the scaling of the weight of the zeros depending on the
    number of samples. Higher values means that larger samples are more
    strongly penalizing zeros. By default 1.

------------

resample(read, a, alpha, b, beta)
    # characteristics of the already labeled publications
    n_read = len(read)
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
    # at least one inclusion, but always leave two spots for exclusions
    n_one_train = max(1, min(n_train - 2, n_one_train))
    # the spots that are left are for exclusions
    n_zero_train = n_train - n_one_train

    # sample inclusions and exclusions
    one_train_idx = sample(n_one_train, one_idx)
    zero_train_idx = sample(n_zero_train, zero_idx)

    train = append(one_train_idx, zero_train_idx)
    return(shuffle(train))


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
