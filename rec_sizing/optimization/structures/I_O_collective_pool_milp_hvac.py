INPUTS_POOL_HVAC = {
	'nr_days': 1/8,
	'l_grid': [0.01, 0.01, 0.01],
	'delta_t': 1.0,
	'storage_ratio': 1.0,
	'strict_pos_coeffs': True,
	'total_share_coeffs': True,
	'meters': {
		'Meter#1': {
			'l_buy': [2.0, 2.0, 2.0],
			'l_sell': [0.0, 0.0, 0.9],
			'l_cont': 0.1,
			'l_gic': 0.1,
			'l_bic': 0.1,
			'e_c': [0.0, 0.5, 0.0],
			'p_meter_max': 10,
			'p_gn_init': 1.0,
			'e_g_factor': [0.5, 0.0, 0.0],
			'p_gn_min': 0.0,
			'p_gn_max': 0.0,
			'e_bn_init': 0.0,
			'e_bn_min': 0.0,
			'e_bn_max': 1.0,
			'soc_min': 0.0,
			'eff_bc': 1.0,
			'eff_bd': 1.0,
			'soc_max': 100.0,
			'deg_cost': 0.0,
            'hvac': {
                'HVAC#1': {
                    'type': 'inverter',
                    'mu': 0.1,
                    'psi': 3,
                    'temp_min': 18.0,
                    'temp_max': 23.0,
                    'init_temp': 17,
                    'hvac_capacity': 2,
                    't_out': [22.0000, 22.0000, 30.0000],
                    'thermal_resist': 4,
                    'thermal_cap': 0.3
                },
                'HVAC#2': {
                  'type': 'state',
                   'mu': 0.1,
                   'psi': 4,
                   'temp_min': 18.0,
                   'temp_max': 24.0,
                  'init_temp': 22,
                   'hvac_capacity': 2,
                   't_out': [22.0000, 22.0000, 22.0000],
                   'thermal_resist': 5,
                   'thermal_cap': 0.2
                }
            }
		},
		'Meter#2': {
			'l_buy': [2.0, 2.0, 2.0],
			'l_sell': [0.0, 0.0, 0.0],
			'l_cont': 0.1,
			'l_gic': 0.0,
			'l_bic': 0.1,
			'e_c': [0.1, 0.1, 0.1],
			'p_meter_max': 10,
			'p_gn_init': 0.0,
			'e_g_factor': [0.1, 0.1, 0.1],
			'p_gn_min': 0.0,
			'p_gn_max': 1.0,
			'e_bn_init': 0.0,
			'e_bn_min': 0.0,
			'e_bn_max': 0.0,
			'soc_min': 0.0,
			'eff_bc': 1.0,
			'eff_bd': 1.0,
			'soc_max': 100.0,
			'deg_cost': 0.0,
            'hvac': {
                'HVAC#1': {
                    'type': 'inverter',
                    'mu': 0.1,
                    'psi': 3,
                    'temp_min': 18.0,
                    'temp_max': 23.0,
                    'init_temp': 17,
                    'hvac_capacity': 2,
                    't_out': [22.0000, 22.0000, 30.0000],
                    'thermal_resist': 4,
                    'thermal_cap': 0.3
                },
                'HVAC#2': {
                  'type': 'state',
                   'mu': 0.1,
                   'psi': 4,
                   'temp_min': 18.0,
                   'temp_max': 24.0,
                  'init_temp': 22,
                   'hvac_capacity': 2,
                   't_out': [22.0000, 22.0000, 22.0000],
                   'thermal_resist': 5,
                   'thermal_cap': 0.2
                }
            }
		}
	}
}

OUTPUTS_POOL_HVAC = {'obj_value': 1.616, 'milp_status': 'Optimal', 'nr_dates': 0.125, 'w_clustering': [1, 1, 1], 'p_cont': {'Meter#1': 0.2, 'Meter#2': 0.4}, 'p_gn_new': {'Meter#1': 0.0, 'Meter#2': 1.0}, 'p_gn_total': {'Meter#1': 1.0, 'Meter#2': 1.0}, 'e_bn_new': {'Meter#1': 0.7, 'Meter#2': 0.0}, 'e_bn_total': {'Meter#1': 0.7, 'Meter#2': 0.0}, 'e_cmet': {'Meter#1': [0.2, 0.2, 0.0], 'Meter#2': [0.0, 0.4, 0.0]}, 'e_g': {'Meter#1': [0.5, 0.0, 0.0], 'Meter#2': [0.1, 0.1, 0.1]}, 'e_bc': {'Meter#1': [0.7, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_bd': {'Meter#1': [0.0, 0.7, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_sup': {'Meter#1': [0.2, 0.2, 0.0], 'Meter#2': [0.0, 0.4, 0.0]}, 'e_sur': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_pur_pool': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_sale_pool': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_slc_pool': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_bat': {'Meter#1': [0.7, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'delta_sup': {'Meter#1': [1.0, 1.0, 0.0], 'Meter#2': [0.0, 1.0, 0.0]}, 'e_consumed': {'Meter#1': [0.2, 0.2, 0.0], 'Meter#2': [0.0, 0.4, 0.0]}, 'e_alc': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'delta_slc': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'delta_coeff': {'Meter#1': [1.0, 1.0, 0.0], 'Meter#2': [0.0, 1.0, 0.0]}, 'delta_rec_balance': [0.0, 0.0, 0.0], 'delta_meter_balance': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'hvac_power': {'Meter#1': {'HVAC#1': [0.0, 0.4, 0.0], 'HVAC#2': [0.0, 0.0, 0.0]}, 'Meter#2': {'HVAC#1': [0.0, 0.4, 0.0], 'HVAC#2': [0.0, 0.0, 0.0]}}, 'hvac_temp': {'Meter#1': {'HVAC#1': [17.0, 18.7, 19.83], 'HVAC#2': [22.0, 22.0, 22.0]}, 'Meter#2': {'HVAC#1': [17.0, 18.7, 19.83], 'HVAC#2': [22.0, 22.0, 22.0]}}, 'hvac_cost_comfort': {'Meter#1': {'HVAC#1': [1.0, 0.0, 0.0], 'HVAC#2': [0.0, 0.0, 0.0]}, 'Meter#2': {'HVAC#1': [1.0, 0.0, 0.0], 'HVAC#2': [0.0, 0.0, 0.0]}}, 'c_ind2pool': {'Meter#1': 0.811, 'Meter#2': 0.805}, 'dual_prices': [2.0, 2.0, 0.9]}