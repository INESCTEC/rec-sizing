INPUTS_NO_INSTALL_POOL = {
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
			'e_g_factor': [0.9, 0.0, 0.0],
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
			'l_buy': [2.0, 2.0, 2.0],
			'l_sell': [0.0, 0.0, 0.0],
			'l_cont': 0.1,
			'l_gic': 0.1,
			'l_bic': 0.1,
			'e_c': [0.1, 0.1, 0.1],
			'p_meter_max': 10,
			'p_gn_init': 0.0,
			'e_g_factor': [0.0, 0.0, 0.0],
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

OUTPUTS_NO_INSTALL_POOL = {
	'obj_value': -0.083,
	'milp_status': 'Optimal',
	'p_cont': {
		'Meter#1': 0.2,
		'Meter#2': 0.1
	},
	'p_gn_new': {
		'Meter#1': 0.0,
		'Meter#2': 0.0
	},
	'p_gn_total': {
		'Meter#1': 1.0,
		'Meter#2': 0.0
	},
	'e_bn_new': {
		'Meter#1': 0.0,
		'Meter#2': 0.0
	},
	'e_bn_total': {
		'Meter#1': 1.0,
		'Meter#2': 0.0
	},
	'e_cmet': {
		'Meter#1': [-0.1, -0.1, -0.2],
		'Meter#2': [0.1, 0.1, 0.1]
	},
	'e_g': {
		'Meter#1': [0.9, 0.0, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'e_bc': {
		'Meter#1': [0.8, 0.0, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'e_bd': {
		'Meter#1': [0.0, 0.6, 0.2],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'e_sup': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'e_sur': {
		'Meter#1': [0.0, 0.0, 0.1],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'e_pur_pool': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.1, 0.1, 0.1]
	},
	'e_sale_pool': {
		'Meter#1': [0.1, 0.1, 0.1],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'e_slc_pool': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.1, 0.1, 0.1]
	},
	'e_bat': {
		'Meter#1': [0.8, 0.2, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'delta_sup': {
		'Meter#1': [0.0, 1.0, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'e_consumed': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.1, 0.1, 0.1]
	},
	'e_alc': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.1, 0.1, 0.1]
	},
	'delta_slc': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'delta_cmet': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'delta_alc': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'delta_coeff': {
		'Meter#1': [0.0, 0.0, 0.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'delta_rec_balance': [0.0, 0.0, 1.0],
	'delta_meter_balance': {
		'Meter#1': [1.0, 1.0, 1.0],
		'Meter#2': [0.0, 0.0, 0.0]
	},
	'c_ind2pool': {
		'Meter#1': -0.088,
		'Meter#2': 0.004
	},
	'dual_prices': [0.8875, 0.8875, 0.9]
}

INPUTS_INSTALL_POOL = {
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
			'soc_max': 100.0
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
			'soc_max': 100.0
		}
	}
}

OUTPUTS_INSTALL_POOL = {
    'obj_value': 0.006,
    'milp_status': 'Optimal',
    'p_cont': {
        'Meter#1': 0.0,
        'Meter#2': 0.0
    },
    'p_gn_new': {
        'Meter#1': 0.0,
        'Meter#2': 1.0
    },
    'p_gn_total': {
        'Meter#1': 1.0,
        'Meter#2': 1.0
    },
    'e_bn_new': {
        'Meter#1': 0.5,
        'Meter#2': 0.0
    },
    'e_bn_total': {
        'Meter#1': 0.5,
        'Meter#2': 0.0
    },
    'e_cmet': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_g': {
        'Meter#1': [
            0.5,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.1,
            0.1,
            0.1
        ]
    },
    'e_bc': {
        'Meter#1': [
            0.5,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_bd': {
        'Meter#1': [
            0.0,
            0.5,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_sup': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_sur': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_pur_pool': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_sale_pool': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_slc_pool': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_bat': {
        'Meter#1': [
            0.5,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'delta_sup': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_consumed': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'e_alc': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'delta_slc': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'delta_cmet': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'delta_alc': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'delta_coeff': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'delta_rec_balance': [
        0.0,
        0.0,
        0.0
    ],
    'delta_meter_balance': {
        'Meter#1': [
            0.0,
            0.0,
            0.0
        ],
        'Meter#2': [
            0.0,
            0.0,
            0.0
        ]
    },
    'c_ind2pool': {
        'Meter#1': 0.006,
        'Meter#2': 0.0
    },
    'dual_prices': [
        0.0,
        0.0125,
        0.9
    ]
}

INPUTS_CLUSTER_POOL = {
	'nr_days': 2,
	'l_grid': [0.01, 0.02, 0.03, 0.04, 0.01, 0.02, 0.03, 0.04, 0.01, 0.02, 0.03, 0.04,
			   0.01, 0.02, 0.03, 0.04, 0.01, 0.02, 0.03, 0.04, 0.01, 0.02, 0.03, 0.04,
			   0.01, 0.02, 0.03, 0.04, 0.01, 0.02, 0.03, 0.04, 0.01, 0.02, 0.03, 0.04,
			   0.01, 0.02, 0.03, 0.04, 0.01, 0.02, 0.03, 0.04, 0.01, 0.02, 0.03, 0.04],
	'delta_t': 1,
	'nr_clusters': 1,
	'storage_ratio': 1.0,
	'strict_pos_coeffs': True,
	'total_share_coeffs': True,
	'meters': {
		'CPE#1': {
			'l_buy': [0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.064, 0.063, 0.062, 0.061, 0.060,
					  0.045, 0.044, 0.043, 0.042, 0.041, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077,
					  0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.064, 0.063, 0.062, 0.061, 0.060,
					  0.045, 0.044, 0.043, 0.042, 0.041, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077],
			'l_sell': [0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.064, 0.063, 0.062, 0.061, 0.060,
					   0.045, 0.044, 0.043, 0.042, 0.041, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077,
					   0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.064, 0.063, 0.062, 0.061, 0.060,
					   0.045, 0.044, 0.043, 0.042, 0.041, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077],
			'l_cont': 0.1,
			'l_gic': 0.1,
			'l_bic': 0.1,
			'e_c': [1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2,
					1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2,
					1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2,
					1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2],
			'p_meter_max': 10,
			'p_gn_init': 1.0,
			'e_g_factor': [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
						   0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0,
						   0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
						   0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0],
			'p_gn_min': 0.0,
			'p_gn_max': 0.0,
			'e_bn_init': 1.0,
			'e_bn_min': 0.0,
			'e_bn_max': 0.0,
			'soc_min': 0.0,
			'eff_bc': 0.99,
			'eff_bd': 0.99,
			'soc_max': 100.0
		},
		'CPE#2': {
			'l_buy': [0.045, 0.044, 0.043, 0.042, 0.041, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077,
					  0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.064, 0.063, 0.062, 0.061, 0.060,
					  0.045, 0.044, 0.043, 0.042, 0.041, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077,
					  0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.064, 0.063, 0.062, 0.061, 0.060],
			'l_sell': [0.045, 0.044, 0.043, 0.042, 0.041, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077,
					  0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.064, 0.063, 0.062, 0.061, 0.060,
					  0.045, 0.044, 0.043, 0.042, 0.041, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077,
					  0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.064, 0.063, 0.062, 0.061, 0.060],
			'l_cont': 0.1,
			'l_gic': 0.1,
			'l_bic': 0.1,
			'e_c': [0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2,
					0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2,
					0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2,
					0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2],
			'p_meter_max': 10,
			'p_gn_init': 0.0,
			'e_g_factor': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
						   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
						   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
						   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			'p_gn_min': 0.0,
			'p_gn_max': 0.0,
			'e_bn_init': 0.0,
			'e_bn_min': 0.0,
			'e_bn_max': 0.0,
			'soc_min': 0.0,
			'eff_bc': 0.99,
			'eff_bd': 0.99,
			'soc_max': 100.0
		}
	}
}

OUTPUTS_CLUSTER_POOL = {
	'obj_value': 7.274,
	'milp_status': 'Optimal',
	'p_cont': {
		'CPE#1': 3.01,
		'CPE#2': 0.4
	},
	'p_gn_new': {
		'CPE#1': 0.0,
		'CPE#2': 0.0
	},
	'p_gn_total': {
		'CPE#1': 1.0,
		'CPE#2': 0.0
	},
	'e_bn_new': {
		'CPE#1': 0.0,
		'CPE#2': 0.0
	},
	'e_bn_total': {
		'CPE#1': 1.0,
		'CPE#2': 0.0
	},
	'e_cmet': {
		'CPE#1': [2.0, 2.010101, 3.0, 3.01, 3.01, 2.9, -0.1, 1.7, 3.0082226, 3.01, 2.4, 1.3,
				  0.2, 1.3, 2.899949, 3.01, 2.610101, 2.7, 0.8, 1.9, 3.0, 3.01, 3.0, 2.0],
		'CPE#2': [0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2,
				  0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2]
	},
	'e_g': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
				  0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'e_bc': {
		'CPE#1': [1.0, 0.01010101, 0.0, 0.0, 0.01, 1.0, 0.0, 0.0, 0.40822263, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.49994898, 0.0, 0.01010101, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'e_bd': {
		'CPE#1': [0.0, 0.0, 0.0, 0.99, 0.0, 0.0, 0.9, 0.0, 0.0, 0.49, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.49, 0.0, 0.0, 0.0, 0.0, 0.0, 0.99, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'e_sup': {
		'CPE#1': [2.0001, 2.010201, 3.0, 3.0101, 3.0101, 2.9, 0.0, 1.7, 3.0082226, 3.01, 2.4, 1.3,
				  0.2, 1.3, 2.899949, 3.01, 2.610101, 2.7, 0.8001, 1.9001, 3.0001, 3.0101, 3.0001, 2.0001],
		'CPE#2': [0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1001, 0.2001, 0.3, 0.4001, 0.3001, 0.2001,
				  0.1001, 0.2001, 0.3001, 0.4, 0.3001, 0.2001, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2]
	},
	'e_sur': {
		'CPE#1': [0.0001, 0.0001, 0.0, 0.0001, 0.0001, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0001, 0.0001, 0.0, 0.0001, 0.0001, 0.0001,
				  0.0001, 0.0001, 0.0001, 0.0, 0.0001, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'e_pur_pool': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'e_sale_pool': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'e_slc_pool': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'e_bat': {
		'CPE#1': [0.99, 1.0, 1.0, 0.0, 0.0099, 0.9999, 0.090809091, 0.090809091, 0.49494949, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.49494949, 0.0, 0.01, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'delta_sup': {
		'CPE#1': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
				  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'CPE#2': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
				  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
	},
	'e_consumed': {
		'CPE#1': [2.0, 2.010101, 3.0, 3.01, 3.01, 2.9, 0.0, 1.7, 3.0082226, 3.01, 2.4, 1.3,
				  0.2, 1.3, 2.899949, 3.01, 2.610101, 2.7, 0.8, 1.9, 3.0, 3.01, 3.0, 2.0],
		'CPE#2': [0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2,
				  0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2]
	},
	'e_alc': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'delta_slc': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'delta_cmet': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'delta_alc': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'delta_coeff': {
		'CPE#1': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
				  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'CPE#2': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
				  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
	},
	'delta_rec_balance': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
						  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
	'delta_meter_balance': {
		'CPE#1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		'CPE#2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
				  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	},
	'c_ind2pool': {
		'CPE#1': 6.535,
		'CPE#2': 0.739
	},
	'dual_prices': [0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.065, 0.073, 0.074, 0.075, 0.076, 0.077,
					0.051, 0.052, 0.043, 0.054, 0.055, 0.04, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077]
}
