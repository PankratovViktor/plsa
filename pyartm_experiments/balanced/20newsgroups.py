from multiprocessing import Pool

from pyartm_datasets import main_cases
from pyartm import regularizers
from pyartm.optimizations import balanced
from pyartm.optimizations import default

import manager


ITERS_COUNT = 100
SAMPLES = 100


if __name__ == '__main__':
    train_n_dw_matrix, test_n_dw_matrix = main_cases.get_20newsgroups([
        'rec.autos',
        'rec.motorcycles',
        'rec.sport.baseball',
        'rec.sport.hockey',
        'sci.crypt',
        'sci.electronics',
        'sci.med',
        'sci.space'
    ], train_proportion=0.8)[:2]

    args_list = list()
    for T in [10, 25]:
        for phi_alpha in [-0.1, 0., 0.1]:
            for theta_alpha in [-0.1, 0., 0.1]:
                regularization_list = [
                    regularizers.Additive(phi_alpha, theta_alpha)] * ITERS_COUNT
                args_list.append((
                    train_n_dw_matrix, test_n_dw_matrix,
                    default.Optimizer(regularization_list), T, SAMPLES,
                    '20news_experiment/20news_{}t_base_{}_{}.pkl'.format(
                        T, phi_alpha, theta_alpha
                    )
                ))
                for beta in [0.9, 1.0, 1.1]:
                    args_list.append((
                        train_n_dw_matrix, test_n_dw_matrix,
                        balanced.Optimizer(regularization_list, beta=beta), T, SAMPLES,
                        '20news_experiment/20news_{}t_artm_{}_{}_{}.pkl'.format(
                            T, phi_alpha, theta_alpha, beta
                        )
                    ))

    Pool(processes=5).map(manager.perform_experiment, args_list)
