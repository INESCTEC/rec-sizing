INPUTS_POOL_EWH = {
	'nr_days': 1,
	'l_grid': [0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
			   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
	'delta_t': 1.0,
	'storage_ratio': 1.0,
	'strict_pos_coeffs': True,
	'total_share_coeffs': True,
	'meters': {
		'Meter#1': {
			'ewh': {
				'EWH#1': {
					'params_input': {
						"user": "sample_user",
						"datetime_start": "2022-12-07T00:00:00.000Z",
						"datetime_end": "2022-12-13T23:59:00.000Z",
						"load_diagram_exists": 0,
						"ewh_specs": {
							"ewh_capacity": 100,
							"ewh_power": 1800,
							"ewh_max_temp": 80,
							"user_comf_temp": 40,
							"tariff": 1,
							"price_simple": 0.119585,
							"price_dual_day": 0.149118,
							"price_dual_night": 0.070511,
							"tariff_simple": 0.3604,
							"tariff_dual": 0.4285
						},
					},
					'dataset': {
						"start": ["07/12/2022 08:00",
								  "07/12/2022 08:15",
								  "07/12/2022 12:00",
								  "07/12/2022 20:00"],
						"duration": [10, 10, 5, 5]
					}
				},
			},
			'l_buy': [2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'l_sell': [0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'l_cont': 0.1,
			'l_gic': 0.1,
			'l_bic': 0.1,
			'e_c': [0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'p_meter_max': 10,
			'p_gn_init': 1.0,
			'e_g_factor': [0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
						   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'p_gn_min': 0.0,
			'p_gn_max': 0.0,
			'e_bn_init': 1.0,
			'e_bn_min': 0.0,
			'e_bn_max': 0.0,
			'soc_min': 0.0,
			'eff_bc': 1.0,
			'eff_bd': 1.0,
			'soc_max': 100.0
		},
		'Meter#2': {
			'ewh': None,
			'l_buy': [2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'l_sell': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'l_cont': 0.1,
			'l_gic': 0.1,
			'l_bic': 0.1,
			'e_c': [0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'p_meter_max': 10,
			'p_gn_init': 0.0,
			'e_g_factor': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
						   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'p_gn_min': 0.0,
			'p_gn_max': 0.0,
			'e_bn_init': 0.0,
			'e_bn_min': 0.0,
			'e_bn_max': 0.0,
			'soc_min': 0.0,
			'eff_bc': 1.0,
			'eff_bd': 1.0,
			'soc_max': 100.0
		}
	}
}

OUTPUTS_POOL_EWH = {
	"obj_value": -0.057,
	"milp_status": "Optimal",
	"p_cont": {
		"Meter#1": 0.2,
		"Meter#2": 0.1
	},
	"p_gn_new": {
		"Meter#1": 0.0,
		"Meter#2": 0.0
	},
	"p_gn_total": {
		"Meter#1": 1.0,
		"Meter#2": 0.0
	},
	"e_bn_new": {
		"Meter#1": 0.0,
		"Meter#2": 0.0
	},
	"e_bn_total": {
		"Meter#1": 1.0,
		"Meter#2": 0.0
	},
	"e_cmet": {
		"Meter#1": [-0.1, -0.1, -0.2, 0.0, 0.2, 0.0, 0.0001, 0.094903285, 0.0, 0.0, -0.2, -0.2,
					0.0, 0.0, -0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_g": {
		"Meter#1": [0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_bc": {
		"Meter#1": [0.8, 0.0, 0.0, 0.0, 0.0, 0.0539, 0.0001, 0.0, 0.0, 0.417, 0.583, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.378, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_bd": {
		"Meter#1": [0.0, 0.6, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.054, 0.0, 0.0, 0.2,
					0.513, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.465, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_sup": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0001, 0.094903285, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_sur": {
		"Meter#1": [0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2,
					0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_pur_pool": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_sale_pool": {
		"Meter#1": [0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_slc_pool": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_bat": {
		"Meter#1": [0.8, 0.2, 0.0, 0.0, 0.0, 0.0539, 0.054, 0.054, 0.0, 0.417, 1.0, 0.8,
					0.287, 0.287, 0.087, 0.087, 0.087, 0.087, 0.465, 0.465, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"delta_sup": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0,
					1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_consumed": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0001, 0.094903285, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"e_alc": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"delta_slc": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"delta_cmet": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"delta_alc": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"delta_coeff": {
		"Meter#1": [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0,
					1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		"Meter#2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"delta_rec_balance": [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
						  0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
	"delta_meter_balance": {
		"Meter#1": [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
					0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"Meter#2": [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	"ewh_temp": {
		"Meter#1": {
			"EWH#1": [60.0, 59.431964, 58.871995, 58.319979, 57.775801, 58.95937,
					  61.193403, 60.60842, 60.847922, 40.2, 50.259057, 49.829351,
					  49.405748, 54.420315, 53.931516, 53.449658, 52.974644, 52.506374,
					  52.044755, 51.589691, 51.141089, 55.950411, 55.439883, 54.936605]
		},
		"Meter#2": {}
	},
	"ewh_delta_in": {
		"Meter#1": {
			"EWH#1": [0.0, 0.0, 0.0, 0.0, 0.12345679, 0.20006173, 0.0, 0.058582275, 1.0, 0.74259259, 0.0, 0.0,
					  1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.98703704, 0.0, 0.0, 0.0]
		},
		"Meter#2": {}
	},
	"ewh_optimized_load": {
		"Meter#1": {
			"EWH#1": [0.0, 0.0, 0.0, 0.0, 0.1999999998, 0.3241000026,
					  0.0, 0.09490328550000002, 1.62, 1.2029999958000002, 0.0, 0.0,
					  1.62, 0.0, 0.0, 0.0, 0.0, 0.0,
					  0.0, 0.0, 1.5990000048000002, 0.0, 0.0, 0.0]
		},
		"Meter#2": {}
	},
	"ewh_original_load": {
		"Meter#1": {
			"EWH#1": [0.0, 0.0, 0.0, 0.0, 0.0, 0.378, 0.0, 0.0, 1.566, 1.62, 0.783, 0.0,
					  1.107, 0.0, 0.0, 0.0, 0.0, 0.0, 0.378, 0.0, 1.134, 0.0, 0.0, 0.0]
		},
		"Meter#2": {}
	},
	"ewh_delta_use": {
		"Meter#1": {
			"EWH#1": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0, 0.0,
					  0.08333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08333333333333333, 0.0, 0.0, 0.0]
		},
		"Meter#2": {}
	},
	"c_ind2pool": {
		"Meter#1": -0.07,
		"Meter#2": 0.013
	},
	"dual_prices": [0.8, 0.8, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}
