INPUTS_POOL_HP = {
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
            'hp': {
                'HP#1': {
                    'type': 'inverter',  # or 'inverter'
                    'power_rated': 4.0,  # Rated power of HP [kW]
                    'capacity_tank': 500,  # Water tank capacity [kg]
                    'c_p': 4.18,  # Specific heat capacity of water [kJ/kg°C]

                    # Initial and desired temperatures
                    'temp_inlet': 15.0,  # Inlet water temp [°C]
                    'temp_desired': 55.0,  # Desired water temp [°C]
                    'temp_out_init': 50.0,  # Initial outlet temp [°C]
                    'temp_indoor_init': 18,  # Initial indoor temp [°C]
                    'temp_indoor_final': 22,  # Final indoor temp [°C]

                    # Comfort temperature bounds
                    'temp_indoor_min': 20.0,  # Min indoor temp [°C]
                    'temp_indoor_max': 24.0,  # Max indoor temp [°C]
                    'temp_out_min': 50.0,  # Min outlet temp [°C]
                    'temp_out_max': 70.0,  # Max outlet temp [°C]

                    # Building parameters
                    'u_value': 0.3,  # Building heat loss coefficient [kW/°C]
                    'thermal_resistance': 3,  # Building thermal resistance coefficient
                    'h_rad': 0.05,  # Convective heat transfer coeff of radiator [kW/m2°C]
                    'area_rad': 5.0,  # Radiator surface area [m²]

                    # External time-varying series
                    'mass_hw_demand': [0.0, 1 , 1],
                    'mass_radiator': [50] * 3,
                    't_out': [14, 14, 14],
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
            'hp': {
                'HP#1': {
                    'type': 'inverter',  # or 'inverter'
                    'power_rated': 8.0,  # Rated power of HP [kW]
                    'capacity_tank': 500,  # Water tank capacity [kg]
                    'c_p': 4.18,  # Specific heat capacity of water [kJ/kg°C]

                    # Initial and desired temperatures
                    'temp_inlet': 15.0,  # Inlet water temp [°C]
                    'temp_desired': 55.0,  # Desired water temp [°C]
                    'temp_out_init': 50.0,  # Initial outlet temp [°C]
                    'temp_indoor_init': 20,  # Initial indoor temp [°C]
                    'temp_indoor_final': 22,  # Final indoor temp [°C]

                    # Comfort temperature bounds
                    'temp_indoor_min': 20.0,  # Min indoor temp [°C]
                    'temp_indoor_max': 24.0,  # Max indoor temp [°C]
                    'temp_out_min': 50.0,  # Min outlet temp [°C]
                    'temp_out_max': 70.0,  # Max outlet temp [°C]

                    # Building parameters
                    'u_value': 0.3,  # Building heat loss coefficient [kW/°C]
                    'thermal_resistance': 3,  # Building thermal resistance coefficient
                    'h_rad': 0.05,  # Convective heat transfer coeff of radiator [kW/m2°C]
                    'area_rad': 5.0,  # Radiator surface area [m²]

                    # External time-varying series
                    'mass_hw_demand': [0.0, 1 , 1],
                    'mass_radiator': [50] * 3,
                    't_out': [20, 20, 20],
                    }
                }
		}
	}
}

OUTPUTS_POOL_HP = {'obj_value': 19.097, 'milp_status': 'Optimal', 'nr_dates': 0.125, 'w_clustering': [1, 1, 1], 'p_cont': {'Meter#1': 2.0741074, 'Meter#2': 2.3786039}, 'p_gn_new': {'Meter#1': 0.0, 'Meter#2': 1.0}, 'p_gn_total': {'Meter#1': 1.0, 'Meter#2': 1.0}, 'e_bn_new': {'Meter#1': 0.03692986, 'Meter#2': 0.0}, 'e_bn_total': {'Meter#1': 0.03692986, 'Meter#2': 0.0}, 'e_cmet': {'Meter#1': [2.0741074, 2.0741074, 1.4207489], 'Meter#2': [2.3786039, 0.78645456, 0.78645456]}, 'e_g': {'Meter#1': [0.5, 0.0, 0.0], 'Meter#2': [0.1, 0.1, 0.1]}, 'e_bc': {'Meter#1': [0.03692986, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_bd': {'Meter#1': [0.0, 0.03692986, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_sup': {'Meter#1': [2.0741074, 2.0741074, 1.4207489], 'Meter#2': [2.3786039, 0.78645456, 0.78645456]}, 'e_sur': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_pur_pool': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_sale_pool': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_slc_pool': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'e_bat': {'Meter#1': [0.03692986, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'delta_sup': {'Meter#1': [1.0, 1.0, 1.0], 'Meter#2': [1.0, 1.0, 1.0]}, 'e_consumed': {'Meter#1': [2.0741074, 2.0741074, 1.4207489], 'Meter#2': [2.3786039, 0.78645456, 0.78645456]}, 'e_alc': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'delta_slc': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'delta_coeff': {'Meter#1': [1.0, 1.0, 1.0], 'Meter#2': [1.0, 1.0, 1.0]}, 'delta_rec_balance': [0.0, 0.0, 0.0], 'delta_meter_balance': {'Meter#1': [0.0, 0.0, 0.0], 'Meter#2': [0.0, 0.0, 0.0]}, 'hp_power': {'Meter#1': {'HP#1': [2.5371775, 1.6110373, 1.4207489]}, 'Meter#2': {'HP#1': [2.3786039, 0.78645456, 0.78645456]}}, 'hp_temp_indoor': {'Meter#1': {'HP#1': [18.0, 20.0, 20.0]}, 'Meter#2': {'HP#1': [20.0, 20.0, 20.0]}}, 'hp_power_circulation': {'Meter#1': {'HP#1': [2.5371775, 1.5645928, 1.3743045]}, 'Meter#2': {'HP#1': [2.3786039, 0.74001012, 0.74001012]}}, 'hp_power_heating': {'Meter#1': {'HP#1': [0.0, 0.046444444, 0.046444444]}, 'Meter#2': {'HP#1': [0.0, 0.046444444, 0.046444444]}}, 'hp_power_tank': {'Meter#1': {'HP#1': [0.0, 0.0, 0.0]}, 'Meter#2': {'HP#1': [0.0, 0.0, 0.0]}}, 'hp_outlet_temp': {'Meter#1': {'HP#1': [50.0, 39.733333, 37.333333]}, 'Meter#2': {'HP#1': [50.0, 29.333333, 29.333333]}}, 'hp_cost_comfort': {'Meter#1': {'HP#1': [2.0, 0.0, 0.0]}, 'Meter#2': {'HP#1': [0.0, 0.0, 0.0]}}, 'c_ind2pool': {'Meter#1': 11.164, 'Meter#2': 7.933}, 'dual_prices': [2.0, 2.0, 2.0]}
