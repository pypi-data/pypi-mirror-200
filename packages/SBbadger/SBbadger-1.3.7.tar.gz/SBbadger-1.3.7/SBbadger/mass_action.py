
from SBbadger import generate
from SBbadger import generate_serial

if __name__ == "__main__":

    generate_serial.models(

        group_name='mass_action',
        n_models=1,
        n_species=10,
        # rxn_prob=[.35, .30, .30, .05],
        rxn_prob=[1, .0, .0, .0],
        kinetics=['mass_action', ['loguniform', 'loguniform', 'loguniform'],
                                 ['kf', 'kr', 'kc'],
                                 [[0.01, 100], [0.01, 100], [0.01, 100]]],
        allo_reg=[[0.5, 0.5, 0, 0], 0.5, ['uniform', 'uniform', 'uniform'],
                                         ['ro', 'kma', 'ma'],
                                         [[0, 1], [0, 1], [0, 1]]],
        # allo_reg=True,
        add_enzyme=True,
        overwrite=True,
        source=[1, 'loguniform', 0.01, 1, 0.5],
        sink=[2, 'loguniform', 0.01, 1],
        constants=False,
        # constants=True,
        rev_prob=1,
        ic_params=['uniform', 0, 10],
        # dist_plots=True,
        net_plots=True

    )
