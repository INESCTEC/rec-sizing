"""
Class for implementing and running the Stage 2 MILP for an energy community.
The implementation is specific to a pool market structure.
"""
import itertools
import math
import os
import re

import numpy as np
from loguru import logger
from pulp import (
	CPLEX_CMD,
	HiGHS_CMD,
	listSolvers,
	LpBinary,
	LpMinimize,
	LpProblem,
	LpStatus,
	lpSum,
	LpVariable,
	pulp,
	value,
	LpInteger
)

from rec_sizing.configs.configs import (
	MIPGAP,
	SOLVER,
	TIMEOUT
)
from rec_sizing.custom_types.collective_milp_pool_types import (
	BackpackCollectivePoolDict,
	OutputsCollectivePoolDict
)
from rec_sizing.optimization.helpers.milp_helpers import (
	dict_none_lists,
	dict_per_param,
	none_lists,
	time_intervals
)


class CollectiveMILPPool:
	def __init__(self, backpack: BackpackCollectivePoolDict,
				 nr_dates: int,
				 solver=SOLVER,
				 timeout=TIMEOUT,
				 mipgap=MIPGAP):
		"""
		Initialize core MILP class
		:param backpack: necessary data
		:param nr_dates: number of original days considered in the optimization horizon; >= nr_days = nr_clusters
		:param solver: which available solver should be used; currently supports CBC and CPLEX
		:param timeout: time limit (s) for the solver to find a solution, after which the best (not optimal) is returned
		:param mipgap: tolerance for the solver; between 0 and 1
		"""
		# Indices and sets
		self._nr_days = backpack.get('nr_days')  # operation period (days) (= nr_clusters)
		self._nr_dates = nr_dates  # number of original days considered in the optimization horizon (days)
		self._horizon = None  # operation period (hours)
		# Parameters
		self._l_buy = None  # supply energy tariff [€/kWh]
		self._l_sell = None  # feed in energy tariff [€/kWh]
		self._l_grid = backpack.get('l_grid')  # access tariff of the local grid [€/kWh]
		self._w_clustering = backpack.get('w_clustering')  # clustering weights, i.e., nr. of days represented [days]
		self._l_cont = None  # contracted power tariff, adjusted to one day [€/kW.day]
		self._days = None  # number of days in the optimization horizon [days]
		self._l_gic = None  # investment cost for RES installation, adjusted to one day [€/kW.day]
		self._l_bic = None  # investment cost for storage installation, adjusted to one day [€/kWh.day]
		self._e_c = None  # meter load profile [kWh]
		self._p_meter_max = None  # meters' power limit (constrains total contracted power) [kWh]
		self._p_gn_init = None  # initial installed RES capacity [kW]
		self._e_g_factor = None  # generation profile factor of RES for the meter's location (multiplies by kWh)
		self._delta_t = backpack.get('delta_t')  # interval settlement duration [h]
		self._p_gn_min = None  # minimum RES capacity to be installed
		self._p_gn_max = None  # maximum RES capacity to be installed
		self._e_bn_init = None  # initial installed storage capacity [kW]
		self._e_bn_min = None  # minimum storage capacity to be installed
		self._e_bn_max = None  # maximum storage capacity to be installed
		self._storage_ratio = backpack.get('storage_ratio')  # ratio between the reference maximum admissible input and
		# output storage power and the reference storage nominal capacity.
		self._soc_min = None  # minimum state of charge of the storage systems in the meter [%]
		self._eff_bc = None  # charging efficiency of the storage systems in the meter [%]
		self._eff_bd = None  # discharging efficiency of the storage systems in the meter [%]
		self._soc_max = None  # maximum state of charge of the storage systems in the meter [%]
		self._deg_cost = None  # degradation cost for the BESS [€/kWh]
		self._big_m = None  # a very big number [kWh]
		# EVs data
		self.sets_btm_ev = {}
		self._trip_ev = {}  # EV energy consumption, in kWh
		self._min_energy_storage_ev = {}  # Minimum stored energy to be guaranteed for vehicle ev at CPE n, in kWh
		self._battery_capacity_ev = {}  # The battery energy capacity of vehicle ev at CPE n, in kWh
		self._eff_bc_ev = {}  # Charging efficiency of vehicle ev at CPE n, between 0 and 1
		self._eff_bd_ev = {}  # Discharging efficiency of vehicle ev at CPE n, between 0 and 1
		self._init_e_ev = {}  # the initial energy content of the EV, in kWh
		self._pmax_c_ev = {}  # Maximum power charge of vehicle ev at CPE n, in kW
		self._pmax_d_ev = {}  # Maximum power discharge of vehicle ev at CPE n, in kW
		self._bin_ev = {}  # Whether a vehicle ev at CPE n is plugged-in or not (if plugged-in = 1 else = 0)
		self._small_m = None  # a very small number, to avoid infeasibility in big M constraints [kWh]
		# MILP variables
		self.solver = solver  # solver chosen for the MILP
		self.timeout = timeout  # solvers temporal limit to find optimal solution (s)
		self.mipgap = mipgap  # controls the solver's tolerance; intolerant [0 - 1] fully permissive
		self.regulatory_context = "General"  # can be one of "General" or "Portuguese" - for constraint (3)
		self.strict_pos_coeffs = backpack.get('strict_pos_coeffs')  # no negative coefficients if True
		self.total_share_coeffs = backpack.get('total_share_coeffs')  # share all required in the REC if True
		self._meters_data = backpack.get('meters')  # data from Meters
		self.milp = None  # for storing the MILP formulation
		self.status = None  # stores the status of the MILP's solution
		self.obj_value = None  # stores the MILP's numeric solution
		self.time_intervals = None  # for number of time intervals per horizon
		self.time_series = None  # for a range of time intervals
		self.time_24_subseries = None  # for a subrange of time intervals that sinalize the end of each day
		self.set_meters = None  # set with Meters' ID
		# EWH
		self._ewh_paramsInput = {}
		self._ewh_dataset = {}
		self.set_ewh = {}
		self.wh_init = {}
		self.ewh_power = {}
		self.delta_t = {}
		self.ewh_start_temp = {}
		self.ewh_capacity = {}
		self.waterHeatCap = {}
		self.heatTransferCoeff = {}
		self.ewh_area = {}
		self.ambTemp = {}
		self.wh_min = {}
		self.wh_max = {}
		self.ewh_min_temp = {}
		self.ewh_max_temp = {}
		self.delta_use = {}
		self.tempSet = {}
		self.bigNumber = {}
		self.regressor_aboveSet_m_temp = {}
		self.regressor_aboveSet_m_delta = {}
		self.regressor_aboveSet_b = {}
		self.regressor_belowSet_m_temp = {}
		self.regressor_belowSet_m_delta = {}
		self.regressor_belowSet_b = {}
		# HVAC
		self._hvac = {}
		self.mu = {}  # Building insulation factor
		self.psi = {}  # HVAC temperature efficiency factor
		self.hvac_temp_min = {}  # Min room temperature constraint
		self.hvac_temp_max = {}  # Max room temperature constraint
		self.hvac_init_temp = {}  # Initial room temperature
		self.hvac_capacity = {}  # Maximum HVAC power
		self.T_out = {}  # Outside temperature
		self.set_hvac = {}  # Set of active HVAC units
		self.thermal_resist = {}
		self.thermal_cap = {}
		self.type = {}
		# HP
		self._hp = {}
		self.set_hp = {}
		self.hp_type = {}
		self.hp_power_rated = {}
		self.hp_capacity_tank = {}
		self.hp_c_p = {}
		self.hp_temp_inlet = {}
		self.hp_temp_desired = {}
		self.hp_temp_out_init = {}
		self.hp_temp_indoor_init = {}
		self.hp_temp_indoor_final = {}
		self.hp_temp_indoor_min = {}
		self.hp_temp_indoor_max = {}
		self.hp_temp_out_min = {}
		self.hp_temp_out_max = {}
		self.hp_u_value = {}
		self.hp_thermal_resistance = {}
		self.hp_h_rad = {}
		self.hp_area_rad = {}
		self.hp_mass_hw_demand = {}
		self.hp_mass_radiator = {}
		self.hp_t_out = {}


	def __define_milp(self):
		"""
		Method to define the collective MILP problem.
		"""
		logger.debug(f'-- defining the collective (pool) MILP problem...')

		# Define a minimization MILP
		self.milp = LpProblem(f'collective_pool', LpMinimize)

		# Additional temporal variables
		self._horizon = self._nr_days * 24
		self.time_intervals = time_intervals(self._horizon, self._delta_t)
		self.time_series = range(self.time_intervals)

		if self._nr_days >= 1:
			time_intervals_in_one_day = time_intervals(24, self._delta_t)
			self.time_24_subseries = [time_intervals_in_one_day * day - 1 for day in range(1, self._nr_days + 1, 1)]

		# Set of Meters
		self.set_meters = list(self._meters_data.keys())

		# For simplicity, unpack Meters' information into lists, by type of data, where each Meter is solely
		# identified by its relative position on the list
		self._l_buy = dict_per_param(self._meters_data, 'l_buy')
		self._l_sell = dict_per_param(self._meters_data, 'l_sell')
		self._l_cont = dict_per_param(self._meters_data, 'l_cont')
		self._l_gic = dict_per_param(self._meters_data, 'l_gic')
		self._l_bic = dict_per_param(self._meters_data, 'l_bic')
		self._e_c = dict_per_param(self._meters_data, 'e_c')
		self._p_meter_max = dict_per_param(self._meters_data, 'p_meter_max')
		self._big_m = 2 * max(self._p_meter_max.values())
		self._small_m = 0.0001
		self._p_gn_init = dict_per_param(self._meters_data, 'p_gn_init')
		self._e_g_factor = dict_per_param(self._meters_data, 'e_g_factor')
		self._p_gn_min = dict_per_param(self._meters_data, 'p_gn_min')
		self._p_gn_max = dict_per_param(self._meters_data, 'p_gn_max')
		self._e_bn_init = dict_per_param(self._meters_data, 'e_bn_init')
		self._e_bn_min = dict_per_param(self._meters_data, 'e_bn_min')
		self._e_bn_max = dict_per_param(self._meters_data, 'e_bn_max')
		self._soc_min = dict_per_param(self._meters_data, 'soc_min')
		self._eff_bc = dict_per_param(self._meters_data, 'eff_bc')
		self._eff_bd = dict_per_param(self._meters_data, 'eff_bd')
		self._soc_max = dict_per_param(self._meters_data, 'soc_max')
		self._deg_cost = dict_per_param(self._meters_data, 'deg_cost')
		# EVs data
		for n in self.set_meters:
			meter_btm_ev = self._meters_data[n].get('btm_evs')
			if meter_btm_ev is not None:
				self.sets_btm_ev[n] = list(meter_btm_ev.keys())
				self._trip_ev[n] = {ev: meter_btm_ev[ev]['trip_ev'] for ev in self.sets_btm_ev[n]}
				self._min_energy_storage_ev[n] = {ev: meter_btm_ev[ev]['min_energy_storage_ev']
												  for ev in self.sets_btm_ev[n]}
				self._battery_capacity_ev[n] = {ev: meter_btm_ev[ev]['battery_capacity_ev']
												for ev in self.sets_btm_ev[n]}
				self._eff_bc_ev[n] = {ev: meter_btm_ev[ev]['eff_bc_ev'] for ev in self.sets_btm_ev[n]}
				self._eff_bd_ev[n] = {ev: meter_btm_ev[ev]['eff_bd_ev'] for ev in self.sets_btm_ev[n]}
				self._init_e_ev[n] = {ev: meter_btm_ev[ev]['init_e_ev'] for ev in self.sets_btm_ev[n]}
				self._pmax_c_ev[n] = {ev: meter_btm_ev[ev]['pmax_c_ev'] for ev in self.sets_btm_ev[n]}
				self._pmax_d_ev[n] = {ev: meter_btm_ev[ev]['pmax_d_ev'] for ev in self.sets_btm_ev[n]}
				self._bin_ev[n] = {ev: meter_btm_ev[ev]['bin_ev'] for ev in self.sets_btm_ev[n]}
			else:
				self.sets_btm_ev[n] = []
		# EWH
		# unpack variables
		for n in self.set_meters:
			try:
				self._ewh = self._meters_data[n]['ewh']
			except KeyError:
				self._ewh = None
			if self._ewh is not None:
				self.set_ewh[n] = list(self._ewh.keys())
				self._ewh_paramsInput[n] = {e: self._ewh[e]['params_input'] for e in self.set_ewh[n]}
				self._ewh_dataset[n] = {e: self._ewh[e]['dataset'] for e in self.set_ewh[n]}
			else:
				self.set_ewh[n] = []

		if bool(self._ewh_dataset):
			# create EWH varBackpacks
			from rec_sizing.ewh.ewh_flex import ewh_preparation
			global varBackpack

			varBackpack = {}
			for n in self.set_meters:
				self._ewh = self._meters_data[n]['ewh']

				if self._ewh is not None:
					varBackpack[n] = {
						e: ewh_preparation(self._ewh_paramsInput[n][e], self._ewh_dataset[n][e], resample='1h')
						for e in self.set_ewh[n]
					}

					self.wh_init[n] = {e: varBackpack[n][e]['wh_init'] for e in self.set_ewh[n]}
					self.ewh_power[n] = {e: varBackpack[n][e]['ewh_power'] for e in self.set_ewh[n]}
					self.delta_t[n] = {e: varBackpack[n][e]['delta_t'] for e in self.set_ewh[n]}
					self.ewh_start_temp[n] = {e: varBackpack[n][e]['ewh_start_temp'] for e in self.set_ewh[n]}
					self.ewh_capacity[n] = {e: varBackpack[n][e]['ewh_capacity'] for e in self.set_ewh[n]}
					self.waterHeatCap[n] = {e: varBackpack[n][e]['waterHeatCap'] for e in self.set_ewh[n]}
					self.heatTransferCoeff[n] = {e: varBackpack[n][e]['heatTransferCoeff'] for e in self.set_ewh[n]}
					self.ewh_area[n] = {e: varBackpack[n][e]['ewh_area'] for e in self.set_ewh[n]}
					self.ambTemp[n] = {e: varBackpack[n][e]['ambTemp'] for e in self.set_ewh[n]}
					self.wh_min[n] = {e: varBackpack[n][e]['wh_min'] for e in self.set_ewh[n]}
					self.wh_max[n] = {e: varBackpack[n][e]['wh_max'] for e in self.set_ewh[n]}
					self.ewh_min_temp[n] = {e: varBackpack[n][e]['ewh_min_temp'] for e in self.set_ewh[n]}
					self.ewh_max_temp[n] = {e: varBackpack[n][e]['ewh_max_temp'] for e in self.set_ewh[n]}
					self.delta_use[n] = {e: varBackpack[n][e]['delta_use'] for e in self.set_ewh[n]}
					self.tempSet[n] = {e: varBackpack[n][e]['tempSet'] for e in self.set_ewh[n]}
					self.bigNumber[n] = {e: varBackpack[n][e]['bigNumber'] for e in self.set_ewh[n]}
					self.regressor_aboveSet_m_temp[n] = \
						{e: varBackpack[n][e]['regressor_aboveSet_m_temp'] for e in self.set_ewh[n]}
					self.regressor_aboveSet_m_delta[n] = \
						{e: varBackpack[n][e]['regressor_aboveSet_m_delta'] for e in self.set_ewh[n]}
					self.regressor_aboveSet_b[n] = \
						{e: varBackpack[n][e]['regressor_aboveSet_b'] for e in self.set_ewh[n]}
					self.regressor_belowSet_m_temp[n] = \
						{e: varBackpack[n][e]['regressor_belowSet_m_temp'] for e in self.set_ewh[n]}
					self.regressor_belowSet_m_delta[n] = \
						{e: varBackpack[n][e]['regressor_belowSet_m_delta'] for e in self.set_ewh[n]}
					self.regressor_belowSet_b[n] = \
						{e: varBackpack[n][e]['regressor_belowSet_b'] for e in self.set_ewh[n]}
				else:
					varBackpack[n] = []

		# Unpack HVAC information
		for n in self.set_meters:
			if self._meters_data[n].get('hvac') is not None:
				self._hvac = self._meters_data[n].get('hvac')
				self.set_hvac[n] = list(self._hvac.keys())
				self.mu[n] = {h: self._hvac[h]['mu'] for h in self.set_hvac[n]}
				self.psi[n] = {h: self._hvac[h]['psi'] for h in self.set_hvac[n]}
				self.hvac_capacity[n] = {h: self._hvac[h]['hvac_capacity'] for h in self.set_hvac[n]}
				self.hvac_temp_min[n] = {h: self._hvac[h]['temp_min'] for h in self.set_hvac[n]}
				self.hvac_temp_max[n] = {h: self._hvac[h]['temp_max'] for h in self.set_hvac[n]}
				self.hvac_init_temp[n] = {h: self._hvac[h]['init_temp'] for h in self.set_hvac[n]}
				self.T_out[n] = {h: self._hvac[h]['t_out'] for h in self.set_hvac[n]}
				self.thermal_resist[n] = {h: self._hvac[h]['thermal_resist'] for h in self.set_hvac[n]}
				self.thermal_cap[n] = {h: self._hvac[h]['thermal_cap'] for h in self.set_hvac[n]}
				self.type[n] = {h: self._hvac[h]['type'] for h in self.set_hvac[n]}
			else:
				self.set_hvac[n] = []

		#Unpack HP information
		for n in self.set_meters:
			if self._meters_data[n].get('hp') is not None:
				self._hp = self._meters_data[n].get('hp')
				self.set_hp[n] = list(self._hp.keys())
				self.hp_type[n] = {hp: self._hp[hp]['type'] for hp in self.set_hp[n]}
				self.hp_power_rated[n] = {hp: self._hp[hp]['power_rated'] for hp in self.set_hp[n]}
				self.hp_capacity_tank[n] = {hp: self._hp[hp]['capacity_tank'] for hp in self.set_hp[n]}
				self.hp_c_p[n] = {hp: self._hp[hp]['c_p'] for hp in self.set_hp[n]}
				self.hp_temp_inlet[n] = {hp: self._hp[hp]['temp_inlet'] for hp in self.set_hp[n]}
				self.hp_temp_desired[n] = {hp: self._hp[hp]['temp_desired'] for hp in self.set_hp[n]}
				self.hp_temp_out_init[n] = {hp: self._hp[hp]['temp_out_init'] for hp in self.set_hp[n]}
				self.hp_temp_indoor_init[n] = {hp: self._hp[hp]['temp_indoor_init'] for hp in self.set_hp[n]}
				self.hp_temp_indoor_final[n] = {hp: self._hp[hp]['temp_indoor_final'] for hp in self.set_hp[n]}
				self.hp_temp_indoor_min[n] = {hp: self._hp[hp]['temp_indoor_min'] for hp in self.set_hp[n]}
				self.hp_temp_indoor_max[n] = {hp: self._hp[hp]['temp_indoor_max'] for hp in self.set_hp[n]}
				self.hp_temp_out_min[n] = {hp: self._hp[hp]['temp_out_min'] for hp in self.set_hp[n]}
				self.hp_temp_out_max[n] = {hp: self._hp[hp]['temp_out_max'] for hp in self.set_hp[n]}
				self.hp_u_value[n] = {hp: self._hp[hp]['u_value'] for hp in self.set_hp[n]}
				self.hp_thermal_resistance[n] = {hp: self._hp[hp]['thermal_resistance'] for hp in self.set_hp[n]}
				self.hp_h_rad[n] = {hp: self._hp[hp]['h_rad'] for hp in self.set_hp[n]}
				self.hp_area_rad[n] = {hp: self._hp[hp]['area_rad'] for hp in self.set_hp[n]}
				self.hp_mass_hw_demand[n] = {hp: self._hp[hp]['mass_hw_demand'] for hp in self.set_hp[n]}
				self.hp_mass_radiator[n] = {hp: self._hp[hp]['mass_radiator'] for hp in self.set_hp[n]}
				self.hp_t_out[n] = {hp: self._hp[hp]['t_out'] for hp in self.set_hp[n]}
			else:
				self.set_hp[n] = []


		# Initialize the decision variables
		# contracted power tariff by n [kW]
		p_cont = {meter_id: None for meter_id in self.set_meters}
		# new installed RES capacity at n [kW]
		p_gn_new = {meter_id: None for meter_id in self.set_meters}
		# total installed RES capacity at n [kW]
		p_gn_total = {meter_id: None for meter_id in self.set_meters}
		# new installed storage system(s)  capacity at n [kW]
		e_bn_new = {meter_id: None for meter_id in self.set_meters}
		# total installed storage system(s) capacity at n [kW]
		e_bn_total = {meter_id: None for meter_id in self.set_meters}
		# net consumption at meter n [kWh]
		e_cmet = dict_none_lists(self.time_intervals, self.set_meters)
		# behind-the-meter generation at meter n [kWh]
		e_g = dict_none_lists(self.time_intervals, self.set_meters)
		# energy charged by meter n's storage system(s) [kWh]
		e_bc = dict_none_lists(self.time_intervals, self.set_meters)
		# energy charged by meter n's storage system(s) [kWh]
		e_bd = dict_none_lists(self.time_intervals, self.set_meters)
		# energy supplied to n from its retailer [kWh]
		e_sup = dict_none_lists(self.time_intervals, self.set_meters)
		# energy surplus sold by n to its retailer [kWh]
		e_sur = dict_none_lists(self.time_intervals, self.set_meters)
		# energy bought locally by n
		e_pur = dict_none_lists(self.time_intervals, self.set_meters)
		# energy sold locally by n
		e_sale = dict_none_lists(self.time_intervals, self.set_meters)
		# energy self-consumed by n (in theory, g.t.e. that value)
		e_slc = dict_none_lists(self.time_intervals, self.set_meters)
		# energy stored by the storage system(s) in n [kWh]
		e_bat = dict_none_lists(self.time_intervals, self.set_meters)
		# when True allows supply when false allows surplus
		delta_sup = dict_none_lists(self.time_intervals, self.set_meters)
		# consumption at meter n (in theory, g.t.e. that value)
		e_consumed = dict_none_lists(self.time_intervals, self.set_meters)
		# consumed energy bought locally by n (in theory, g.t.e. that value)
		e_alc = dict_none_lists(self.time_intervals, self.set_meters)
		# auxiliary binary variable for defining self-consumed energy by n
		delta_slc = dict_none_lists(self.time_intervals, self.set_meters)
		# EV decision variables
		# energy stored in ev [kWh]
		ev_stored = {n: dict_none_lists(self.time_intervals, self.sets_btm_ev[n]) for n in self.set_meters}
		# power charge of ev [kW]
		p_ev_charge = {n: dict_none_lists(self.time_intervals, self.sets_btm_ev[n]) for n in self.set_meters}
		# power discharge of ev [kW]
		p_ev_discharge = {n: dict_none_lists(self.time_intervals, self.sets_btm_ev[n]) for n in self.set_meters}
		if self.strict_pos_coeffs:
			# auxiliary binary variable for imposing positive allocation coefficients
			delta_coeff = dict_none_lists(self.time_intervals, self.set_meters)
		if self.total_share_coeffs:
			# auxiliary binary variable for signaling if the REC has a surplus or a deficit
			delta_rec_balance = none_lists(self.time_intervals)
			# auxiliary binary variable for signaling if a meter has a surplus or a deficit
			delta_meter_balance = dict_none_lists(self.time_intervals, self.set_meters)

		# EWH - Initialize decision variables
		if bool(self._ewh_dataset):
			temp = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			w_tot = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			w_in = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			w_loss = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			delta_in = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			w_water = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			costComfort = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			binAux = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			energyEWH = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}

		# HVAC - Initialize decision variables
		if self.set_hvac is not None:
			hvac_temp = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}
			hvac_power = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}
			delta_hvac = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}
			hvac_active = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}
			hvac_cost_comfort = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}
			hvac_mode = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}
			hvac_mode_heat = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}
			hvac_mode_off = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}
			hvac_mode_cool = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in self.set_meters}

		# HP - Initialize decision variables
		if self.set_hp is not None:
			self.hp_temp_indoor = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.hp_temp_outlet = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.hp_power = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.hp_active = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.hp_cost_comfort = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.hp_op_mode = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.heating_kwh = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.circulation_kw = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.tank_heating_kwh = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.hp_temp_return = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}
			self.hp_lost_power = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in self.set_meters}

		# Define the decision variables as puLP objets
		if self.total_share_coeffs:
			for t in self.time_series:
				increment = f't{t:07d}'
				delta_rec_balance[t] = LpVariable('delta_rec_balance_' + increment, cat=LpBinary)

		for n in self.set_meters:
			increment = f'{n}'
			p_cont[n] = LpVariable('p_cont_' + increment, lowBound=0)
			p_gn_new[n] = LpVariable('p_gn_new_' + increment, lowBound=0)
			p_gn_total[n] = LpVariable('p_gn_total_' + increment, lowBound=0)
			e_bn_new[n] = LpVariable('e_bn_new_' + increment, lowBound=0)
			e_bn_total[n] = LpVariable('e_bn_total_' + increment, lowBound=0)

		t_n_series = itertools.product(self.set_meters, self.time_series)  # iterates over each Meter and each time step
		for n, t in t_n_series:
			increment = f'{n}_t{t:07d}'
			e_cmet[n][t] = LpVariable('e_cmet_' + increment)
			e_g[n][t] = LpVariable('e_g_' + increment, lowBound=0)
			e_bc[n][t] = LpVariable('e_bc_' + increment, lowBound=0)
			e_bd[n][t] = LpVariable('e_bd_' + increment, lowBound=0)
			e_sup[n][t] = LpVariable('e_sup_' + increment, lowBound=0)
			e_sur[n][t] = LpVariable('e_sur_' + increment, lowBound=0)
			e_pur[n][t] = LpVariable('e_pur_' + increment, lowBound=0)
			e_sale[n][t] = LpVariable('e_sale_' + increment, lowBound=0)
			e_slc[n][t] = LpVariable('e_slc_' + increment, lowBound=0)
			e_bat[n][t] = LpVariable('e_bat_' + increment, lowBound=0)
			delta_sup[n][t] = LpVariable('delta_sup_' + increment, cat=LpBinary)
			e_consumed[n][t] = LpVariable('e_consumed_' + increment, lowBound=0)
			e_alc[n][t] = LpVariable('e_alc_' + increment, lowBound=0)
			delta_slc[n][t] = LpVariable('delta_slc_' + increment, cat=LpBinary)
			if self.strict_pos_coeffs:
				delta_coeff[n][t] = LpVariable('delta_coeff_' + increment, cat=LpBinary)
			if self.total_share_coeffs:
				delta_meter_balance[n][t] = LpVariable('delta_meter_balance_' + increment, cat=LpBinary)
			# EV variables
			for ev in self.sets_btm_ev[n]:
				increment = f'{n}_{ev}_t{t:07d}'
				ev_stored[n][ev][t] = LpVariable('ev_stored_' + increment, lowBound=0)
				p_ev_charge[n][ev][t] = LpVariable('p_ev_charge_' + increment, lowBound=0)
				p_ev_discharge[n][ev][t] = LpVariable('p_ev_discharge_' + increment, lowBound=0)

			# EWH decision variables
			if bool(self._ewh_dataset):
				for e in self.set_ewh[n]:
					increment = f'{n}_{e}_t{t:07d}'
					# Temperature of water at EWH outlet at the beginning of time interval t (°C)
					temp[n][e][t] = LpVariable(f'temp_' + increment, lowBound=0)
					# Total energy balance of prosumer’s EWH at time interval t (kWh)
					w_tot[n][e][t] = LpVariable(f'w_tot_' + increment, lowBound=0)
					# Energy into the prosumer’s EWH at time interval t (kWh)
					w_in[n][e][t] = LpVariable(f'w_in_' + increment, lowBound=0)
					# Thermal energy losses at time interval t (kWh)
					w_loss[n][e][t] = LpVariable(f'w_loss_' + increment)
					# Binary variable for EWH operation status (1 = ON, 0 = OFF)
					delta_in[n][e][t] = LpVariable(f'delta_in_' + increment, lowBound=0, upBound=1)
					# Amount of energy stored in the EWH after usage and mixing with inlet
					w_water[n][e][t] = LpVariable(f'w_water_' + increment, lowBound=0)
					# Extra cost associated with water temperature reaching below comfort
					costComfort[n][e][t] = LpVariable(f'costComfort_' + increment, lowBound=0)
					# Binary Variable for if-else expression 15
					binAux[n][e][t] = LpVariable(f'binAux_' + increment, cat=LpBinary)
					# Pricing of that specific energy usage
					energyEWH[n][e][t] = LpVariable(f'energyEWH_' + increment, lowBound=0)

			if not all(not v for v in self.set_hvac.values()):
				for h in self.set_hvac[n]:
					increment = f'{n}_{h}_t{t:07d}'
					hvac_temp[n][h][t] = LpVariable(f'hvac_temp_' + increment, lowBound=0)
					hvac_power[n][h][t] = LpVariable(f'hvac_power_' + increment, lowBound=0)
					delta_hvac[n][h][t] = LpVariable(f'delta_hvac_' + increment, lowBound=0, upBound=5, cat=LpInteger)
					hvac_active[n][h][t] = LpVariable(f'hvac_active_' + increment, lowBound=0, upBound=1, cat=LpBinary)
					hvac_mode[n][h][t] = LpVariable(f'hvac_mode_' + increment, lowBound=0, upBound=1, cat=LpBinary)
					hvac_mode_heat[n][h][t] = LpVariable(f'hvac_mode_heat_' + increment, lowBound=0, upBound=1, cat=LpBinary)
					hvac_mode_off[n][h][t] = LpVariable(f'hvac_mode_off_' + increment, lowBound=0, upBound=1, cat=LpBinary)
					hvac_mode_cool[n][h][t] = LpVariable(f'hvac_mode_cool_' + increment, lowBound=0, upBound=1, cat=LpBinary)
					hvac_cost_comfort[n][h][t] = LpVariable(f'hvac_cost_comfort_' + increment, lowBound=0)

			if not all(not v for v in self.set_hp.values()):
				for hp in self.set_hp[n]:
					increment = f'{n}_{hp}_t{t:07d}'
					self.hp_temp_indoor[n][hp][t] = LpVariable(f'hp_temp_indoor_' + increment, lowBound=0)
					self.hp_temp_outlet[n][hp][t] = LpVariable(f'hp_temp_outlet_' + increment, lowBound=0)
					self.hp_power[n][hp][t] = LpVariable(f'power_hp_' + increment, lowBound=0)
					self.hp_active[n][hp][t] = LpVariable(f'hp_active_' + increment, lowBound=0, upBound=1, cat=LpBinary)
					self.hp_cost_comfort[n][hp][t] = LpVariable(f'hp_cost_comfort_' + increment, lowBound=0)
					self.heating_kwh[n][hp][t] = LpVariable(f'hp_power_heating_' + increment, lowBound=0)
					self.circulation_kw[n][hp][t] = LpVariable(f'hp_power_circulation_' + increment, lowBound=0)
					self.tank_heating_kwh[n][hp][t] = LpVariable(f'hp_power_tank_' + increment, lowBound=0)
					self.hp_temp_return[n][hp][t] = LpVariable(f'hp_temp_return_' + increment, lowBound=0)
					self.hp_lost_power[n][hp][t] = LpVariable(f'hp_lost_power_' + increment, lowBound=0)

		# Eq. 1: Objective Function
		objective = (
				lpSum(
					lpSum(
						e_sup[n][t] * self._l_buy[n][t]
						- e_sur[n][t] * self._l_sell[n][t]
						+ e_slc[n][t] * self._l_grid[t]
						+ lpSum(
							costComfort[n][e][t] * 100
							for e in self.set_ewh[n]
						)
						+ e_bd[n][t] * self._deg_cost[n]
						for n in self.set_meters
					) * self._w_clustering[t]
					for t in self.time_series
				) +
				lpSum(
					p_cont[n] * self._l_cont[n] * self._nr_dates
					+ p_gn_new[n] * self._l_gic[n] * self._nr_dates
					+ e_bn_new[n] * self._l_bic[n] * self._nr_dates
					for n in self.set_meters
				)
		)
		# HVAC penalty
		if not all(not v for v in self.set_hvac.values()):
			for t in self.time_series:
				for n in self.set_meters:
					if t != 0 :
						objective += (lpSum(hvac_cost_comfort[n][h][t] * 2 for h in self.set_hvac[n]))
		# HP penalty
		if not all(not v for v in self.set_hp.values()):
			for t in self.time_series:
				for n in self.set_meters:
					if t != 0 :
						objective += (lpSum(self.hp_cost_comfort[n][hp][t] * 2 for hp in self.set_hp[n]))

		self.milp += objective, 'Objective Function'

		# Eq. 2-35: Constraints
		for t in self.time_series:
			increment = f'{t:07d}'

			# Eq. 17
			self.milp += \
				lpSum(e_sale[n][t] for n in self.set_meters) == lpSum(e_pur[n][t] for n in self.set_meters), \
				'Market_equilibrium_' + increment

			if self.total_share_coeffs:
				# Eq. 25
				self.milp += \
					lpSum(e_cmet[n][t] for n in self.set_meters) >= -self._big_m * delta_rec_balance[t], \
					'Check_REC_surplus_' + increment

				# Eq. 26
				self.milp += \
					lpSum(e_cmet[n][t] for n in self.set_meters) <= \
					self._big_m * (1 - delta_rec_balance[t]) + self._small_m, \
					'Check_REC_deficit_' + increment

		for n in self.set_meters:
			increment = f'{n}'

			# Eq. 5
			self.milp += \
				p_cont[n] <= self._p_meter_max[n], \
				'Contracted_power_limit' + increment

			# Eq. 6
			self.milp += \
				p_gn_new[n] == p_gn_total[n] - self._p_gn_init[n], \
				'New_gen_installed_' + increment

			# Eq. 8
			self.milp += \
				self._p_gn_min[n] <= p_gn_new[n], \
				'Min_new_gen_' + increment

			self.milp += \
				p_gn_new[n] <= self._p_gn_max[n], \
				'Max_new_gen_' + increment

			# Eq. 9
			self.milp += \
				e_bn_new[n] == e_bn_total[n] - self._e_bn_init[n], \
				'New_storage_installed_' + increment

			# Eq. 10
			self.milp += \
				self._e_bn_min[n] <= e_bn_new[n], \
				'Min_new_storage_' + increment

			self.milp += \
				e_bn_new[n] <= self._e_bn_max[n], \
				'Max_new_storage_' + increment

		for n, t in itertools.product(self.set_meters, self.time_series):
			increment = f'{n}_t{t:07d}'

			# Eq. 2
			# UPDATED WITH DISAGREGGATED EWH MODULES (ORIGINAL AND OPTIMIZED LOADS)
			self.milp += \
				(e_cmet[n][t] == \
				self._e_c[n][t] - e_g[n][t] + e_bc[n][t] - e_bd[n][t] + \
				lpSum(p_ev_charge[n][ev][t] - p_ev_discharge[n][ev][t] for ev in self.sets_btm_ev[n]) + \
				lpSum(- varBackpack[n][e]['original_load'][t] + energyEWH[n][e][t] for e in self.set_ewh[n]) + \
				+ (lpSum(hvac_power[n][h][t] * self._delta_t for h in self.set_hvac[n]) if not all(not v for v in self.set_hvac.values()) else 0) +
				 (lpSum(self.hp_power[n][hp][t] * self._delta_t for hp in self.set_hp[n]) if not all(not v for v in self.set_hp.values()) else 0)
, \
				'C_met_' + increment)

			# Eq. 3
			match self.regulatory_context:
				# Specific for the portuguese legislation
				case "Portuguese":
					self.milp += \
						e_cmet[n][t] == e_sup[n][t] - e_sur[n][t] + e_slc[n][t] - e_sale[n][t], \
						'Equilibrium_' + increment
				# General case (original formulation)
				case _:
					self.milp += \
						e_cmet[n][t] == e_sup[n][t] - e_sur[n][t] + e_pur[n][t] - e_sale[n][t], \
						'Equilibrium_' + increment

			# Eq. 4
			self.milp += \
				- p_cont[n] <= e_cmet[n][t] * 1 / self._delta_t, \
				'P_flow_low_limit_' + increment

			self.milp += \
				e_cmet[n][t] * 1 / self._delta_t <= p_cont[n], \
				'P_flow_high_limit_' + increment

			# Eq. 7
			self.milp += \
				e_g[n][t] == self._e_g_factor[n][t] * p_gn_total[n] * self._delta_t, \
				'Scaled_generation_' + increment

			# Eq. 11
			self.milp += \
				e_bc[n][t] * 1 / self._delta_t <= e_bn_total[n] * self._storage_ratio, \
				'Charge_rate_limit_' + increment

			# Eq. 12
			self.milp += \
				e_bd[n][t] * 1 / self._delta_t <= e_bn_total[n] * self._storage_ratio, \
				'Discharge_rate_limit' + increment

			energy_update = e_bc[n][t] * self._eff_bc[n] - e_bd[n][t] * 1 / self._eff_bd[n]
			if t == 0:
				# Eq. 13
				init_e_bat = self._soc_min[n] / 100 * e_bn_total[n]

				# Eq. 14
				self.milp += \
					e_bat[n][t] == init_e_bat + energy_update, \
					'Energy_update_' + increment
			else:

				# Eq. 15
				self.milp += \
					e_bat[n][t] == e_bat[n][t - 1] + energy_update, \
					'Energy_update_' + increment

			# Eq. 16
			self.milp += \
				e_bat[n][t] >= self._soc_min[n] / 100 * e_bn_total[n], \
				'Minimum_SOC_' + increment

			self.milp += \
				e_bat[n][t] <= self._soc_max[n] / 100 * e_bn_total[n], \
				'Maximum_SOC_' + increment

			# Eq. 33
			if self._nr_days >= 1:
				if t in self.time_24_subseries:
					self.milp += \
						e_bat[n][t] == init_e_bat, \
						'Daily_SOC_reset_' + increment

			# Eq. 18
			self.milp += \
				e_sup[n][t] <= self._big_m * delta_sup[n][t] + self._small_m, \
				'Supply_ON_' + increment

			self.milp += \
				e_sur[n][t] <= self._big_m * (1 - delta_sup[n][t]) + self._small_m, \
				'Supply_OFF_' + increment

			# Eq. 19
			self.milp += \
				e_consumed[n][t] >= e_cmet[n][t], \
				'Consumption_' + increment

			# Eq. 20
			self.milp += \
				e_alc[n][t] >= e_pur[n][t] - e_sale[n][t], \
				'Allocated_energy_' + increment

			# Eq. 21
			self.milp += \
				e_slc[n][t] >= e_consumed[n][t] - self._big_m * (1 - delta_slc[n][t]), \
				'Self_consumption_1_' + increment

			# Eq. 22
			self.milp += \
				e_slc[n][t] >= e_alc[n][t] - self._big_m * delta_slc[n][t], \
				'Self_consumption_2_' + increment

			if self.strict_pos_coeffs:
				# Eq. 23
				self.milp += \
					e_sale[n][t] - e_pur[n][t] <= -e_cmet[n][t] + self._big_m * delta_coeff[n][t], \
					'Positive_coefficients_1_' + increment

				# Eq. 24
				self.milp += \
					e_sale[n][t] - e_pur[n][t] <= self._big_m * (1 - delta_coeff[n][t]), \
					'Positive_coefficients_2_' + increment

			if self.total_share_coeffs:
				# Eq. 27
				self.milp += \
					e_cmet[n][t] >= - self._big_m * delta_meter_balance[n][t], \
					'Check_meter_surplus_' + increment

				# Eq. 28
				self.milp += \
					e_cmet[n][t] <= self._big_m * (1 - delta_meter_balance[n][t]) + self._small_m, \
					'Check_meter_deficit_' + increment

				# Eq. 29
				self.milp += \
					e_sale[n][t] >= - e_cmet[n][t] - self._big_m * (
							1 - delta_meter_balance[n][t] + delta_rec_balance[t]), \
					'Share_all_surplus_low_' + increment

				# Eq. 30
				self.milp += \
					e_sale[n][t] <= - e_cmet[n][t] + self._big_m * (
							1 - delta_meter_balance[n][t] + delta_rec_balance[t]), \
					'Share_all_surplus_high_' + increment

				# Eq. 31
				self.milp += \
					e_pur[n][t] >= e_cmet[n][t] - self._big_m * (
							1 - delta_rec_balance[t] + delta_meter_balance[n][t]), \
					'Buy_all_deficit_low_' + increment

				# Eq. 32
				self.milp += \
					e_pur[n][t] <= e_cmet[n][t] + self._big_m * (
							1 - delta_rec_balance[t] + delta_meter_balance[n][t]), \
					'Buy_all_deficit_high_' + increment

			# EVs constraints
			for ev in self.sets_btm_ev[n]:
				increment = f'{n}_{ev}_t{t:07d}'
				# Eq. 41
				if t == 0:
					self.milp += ev_stored[n][ev][t] == \
								 self._init_e_ev[n][ev] + \
								 self._eff_bc_ev[n][ev] * p_ev_charge[n][ev][t] - \
								 (1 / self._eff_bd_ev[n][ev]) * p_ev_discharge[n][ev][t] - \
								 self._trip_ev[n][ev][t], \
						'EV_balance_' + increment
				else:
					self.milp += ev_stored[n][ev][t] == \
								 ev_stored[n][ev][t - 1] + \
								 self._eff_bc_ev[n][ev] * p_ev_charge[n][ev][t] - \
								 (1 / self._eff_bd_ev[n][ev]) * p_ev_discharge[n][ev][t] - \
								 self._trip_ev[n][ev][t], \
						'EV_balance_' + increment

				# Eq. 42
				self.milp += (1 / self._eff_bd_ev[n][ev]) * p_ev_discharge[n][ev][t] <= \
							 self._pmax_d_ev[n][ev] * self._bin_ev[n][ev][t] * self._delta_t, \
					'EV_Discharging_limit_' + increment

				# Eq. 43
				self.milp += self._eff_bc_ev[n][ev] * p_ev_charge[n][ev][t] <= \
							 self._pmax_c_ev[n][ev] * self._bin_ev[n][ev][t] * self._delta_t, \
					'EV_Charging_limit_' + increment

				# Eq. 44
				self.milp += ev_stored[n][ev][t] <= self._battery_capacity_ev[n][ev], 'EV_Max_capacity_' + increment

				# Eq. 45
				self.milp += ev_stored[n][ev][t] >= self._min_energy_storage_ev[n][ev], 'EV_Min_capacity_' + increment

		# EWH constraints
		if bool(self._ewh_dataset):
			for n, t in itertools.product(self.set_meters, self.time_series):
				for e in self.set_ewh[n]:
					# Eq. (1)
					if t == 0:
						self.milp += w_tot[n][e][t] == self.wh_init[n][e], \
							f'Constraint_1_{n}_{e}_{t:07d}'
					else:
						self.milp += w_tot[n][e][t] == w_water[n][e][t - 1] + w_in[n][e][t - 1] - w_loss[n][e][t - 1], \
							f'Constraint_1_{n}_{e}_{t:07d}'
					# Eq. (2)
					self.milp += \
						w_in[n][e][t] == \
						self.ewh_power[n][e] * self.delta_t[n][e] * delta_in[n][e][t] * self.delta_t[n][e] * 60, \
							f'Constraint_2_{n}_{e}_{t:07d}'
					# Eq. (3) Pricing/Energy
					self.milp += energyEWH[n][e][t] == delta_in[n][e][t] * self.ewh_power[n][e] * self.delta_t[n][e], \
						f'Constraint_3_{n}_{e}_{t:07d}'
					# Eq. (4)
					if t == 0:
						self.milp += temp[n][e][t] == self.ewh_start_temp[n][e], f'Constraint_4_{n}_{e}_{t:07d}'
					else:
						self.milp += \
							temp[n][e][t] == \
							w_tot[n][e][t] * 3600 / \
							(self.delta_t[n][e] * 60) / \
							(self.ewh_capacity[n][e] * self.waterHeatCap[n][e]), \
								f'Constraint_4_{n}_{e}_{t:07d}'
					# Eq. (5)
					self.milp += \
						w_loss[n][e][t] == \
						self.heatTransferCoeff[n][e] * \
						self.ewh_area[n][e] * \
						(temp[n][e][t] - self.ambTemp[n][e]) * \
						self.delta_t[n][e] * \
						self.delta_t[n][e] * 60, \
							f'Constraint_5_{n}_{e}_{t:07d}'
					# Eq. (6)
					self.milp += self.wh_min[n][e] <= w_tot[n][e][t], f'Constraint_6.1_{n}_{e}_{t:07d}'
					self.milp += w_tot[n][e][t] <= self.wh_max[n][e], f'Constraint_6.2_{n}_{e}_{t:07d}'
					self.milp += self.ewh_min_temp[n][e] <= temp[n][e][t], f'Constraint_6.3_{n}_{e}_{t:07d}'
					self.milp += temp[n][e][t] <= self.ewh_max_temp[n][e], f'Constraint_6.4_{n}_{e}_{t:07d}'

					# Eq.(7) assure that in the (t) period after the end of hot water usage (t-1),
					# the EWH has, at least, 80L @ 45ºC [n][e][t]
					if (self.delta_use[n][e][t] - self.delta_use[n][e][t - 1] != 0) & \
							(self.delta_use[n][e][t] - self.delta_use[n][e][t - 1] == -self.delta_use[n][e][t-1]):
						# if delta_use[n][e][t] - delta_use[t-1] < 0:
						self.milp += \
							w_tot[n][e][t] >= \
							self.tempSet[n][e] * 1.005 * \
							self.ewh_capacity[n][e] * \
							self.waterHeatCap[n][e] / 3600 * \
							self.delta_t[n][e] * 60 - \
							costComfort[n][e][t], \
								f'Constraint_7.1_{n}_{e}_{t:07d}'
						self.milp += \
							w_tot[n][e][t-1] >= \
							self.tempSet[n][e] * 1.005 * \
							self.ewh_capacity[n][e] * \
							self.waterHeatCap[n][e] / 3600 * \
							self.delta_t[n][e] * 60 - \
							costComfort[n][e][t-1], \
								f'Constraint_7.2_{n}_{e}_{t:07d}'

					# Eq.(8) Internal water energy after usage
					if self.delta_use[n][e][t] > 0:
						# binary definition with temp[n][e][t]
						self.milp += temp[n][e][t] >= \
									 self.tempSet[n][e] - self.bigNumber[n][e] * (1 - binAux[n][e][t]), \
							f'Constraint_8.1_{n}_{e}_{t:07d}'
						self.milp += temp[n][e][t] <= \
									 self.tempSet[n][e] + self.bigNumber[n][e] * binAux[n][e][t], \
							f'Constraint_8.2_{n}_{e}_{t:07d}'
						# if temp[n][e][t] > tempSet
						self.milp += w_water[n][e][t] >= \
									 self.regressor_aboveSet_m_temp[n][e] * temp[n][e][t] + \
									 self.regressor_aboveSet_m_delta[n][e] * self.delta_use[n][e][t] + \
									 self.regressor_aboveSet_b[n][e] - \
									 self.bigNumber[n][e] * (1 - binAux[n][e][t]), \
							f'Constraint_8.3_{n}_{e}_{t:07d}'
						self.milp += w_water[n][e][t] <= \
									 self.regressor_aboveSet_m_temp[n][e] * temp[n][e][t] + \
									 self.regressor_aboveSet_m_delta[n][e] * self.delta_use[n][e][t] + \
									 self.regressor_aboveSet_b[n][e] + \
									 self.bigNumber[n][e] * (1 - binAux[n][e][t]), \
							f'Constraint_8.4_{n}_{e}_{t:07d}'
						# else
						self.milp += w_water[n][e][t] >= \
									 self.regressor_belowSet_m_temp[n][e] * temp[n][e][t] + \
									 self.regressor_belowSet_m_delta[n][e] * self.delta_use[n][e][t] + \
									 self.regressor_belowSet_b[n][e] - \
									 self.bigNumber[n][e] * binAux[n][e][t], \
							f'Constraint_8.5_{n}_{e}_{t:07d}'
						self.milp += w_water[n][e][t] <= \
									 self.regressor_belowSet_m_temp[n][e] * temp[n][e][t] + \
									 self.regressor_belowSet_m_delta[n][e] * self.delta_use[n][e][t] + \
									 self.regressor_belowSet_b[n][e] + \
									 self.bigNumber[n][e] * binAux[n][e][t], \
							f'Constraint_8.6_{n}_{e}_{t:07d}'
					else:
						self.milp += w_water[n][e][t] == \
									 temp[n][e][t] * self.ewh_capacity[n][e] * self.waterHeatCap[n][e] / 3600 * \
									 self.delta_t[n][e] * 60, \
							f'Constraint_8.7_{n}_{e}_{t:07d}'

		# HVAC Constraints
		if not all(not v for v in self.set_hvac.values()):
			for n, t in itertools.product(self.set_meters, self.time_series):
				for h in self.set_hvac[n]:
					increment = f'{n}_{h}_t{t:03d}'

					# Temperature Evolution Equation
					if t == 0:
						self.milp += hvac_temp[n][h][t] == self.hvac_init_temp[n][
							h], f'HVAC_Start_Temp_' + increment

					if self.type[n][h] == 'inverter':
						if t != 0:
							# Heating equation
							self.milp += (
									hvac_temp[n][h][t]
									- hvac_temp[n][h][t - 1]
									- self.mu[n][h] * (self.T_out[n][h][t] - hvac_temp[n][h][t - 1])
									- self.psi[n][h] * hvac_power[n][h][t] * self._delta_t
									<= self._big_m * (1 - hvac_mode[n][h][t])
							), f'HVAC_Heating_UB_' + increment
							self.milp += (
									hvac_temp[n][h][t]
									- hvac_temp[n][h][t - 1]
									- self.mu[n][h] * (self.T_out[n][h][t] - hvac_temp[n][h][t - 1])
									- self.psi[n][h] * hvac_power[n][h][t] * self._delta_t
									>= -self._big_m * (1 - hvac_mode[n][h][t])
							), f'HVAC_Heating_LB_' + increment

							# Cooling equation
							self.milp += (
									hvac_temp[n][h][t]
									- hvac_temp[n][h][t - 1]
									- self.mu[n][h] * (self.T_out[n][h][t] - hvac_temp[n][h][t - 1])
									+ self.psi[n][h] * hvac_power[n][h][t] * self._delta_t
									<= self._big_m * hvac_mode[n][h][t]
							), f'HVAC_Cooling_UB_' + increment
							self.milp += (
									hvac_temp[n][h][t]
									- hvac_temp[n][h][t - 1]
									- self.mu[n][h] * (self.T_out[n][h][t] - hvac_temp[n][h][t - 1])
									+ self.psi[n][h] * hvac_power[n][h][t] * self._delta_t
									>= -self._big_m * hvac_mode[n][h][t]
							), f'HVAC_Cooling_LB_' + increment

						self.milp += delta_hvac[n][h][t] <= 5, f'HVAC_Activation_Control_' + increment
						self.milp += hvac_power[n][h][t] == 0.2 * delta_hvac[n][h][t] * self.hvac_capacity[n][
							h], f'HVAC_Power_Level_' + increment

					if self.type[n][h] == 'state':
						if t != 0:
							self.milp += (
										hvac_mode_heat[n][h][t] + hvac_mode_off[n][h][t] + hvac_mode_cool[n][h][
									t] == 1), f'HVAC_mode_sum_' + increment
							# Heating mode
							self.milp += (hvac_temp[n][h][t] <= (
									self.T_out[n][h][t] + hvac_power[n][h][t] * self.thermal_resist[n][h] - (
									self.T_out[n][h][t] + hvac_power[n][h][t] * self.thermal_resist[n][h] -
									hvac_temp[n][h][t - 1]) * math.exp(
								- self._delta_t / (self.thermal_resist[n][h] * self.thermal_cap[n][h])))
										  + self._big_m * (1 - hvac_mode_heat[n][h][
										t])), f'HVAC_Heating_UB_state' + increment
							self.milp += (hvac_temp[n][h][t] >= (
									self.T_out[n][h][t] + hvac_power[n][h][t] * self.thermal_resist[n][h] - (
									self.T_out[n][h][t] + hvac_power[n][h][t] * self.thermal_resist[n][h] -
									hvac_temp[n][h][t - 1]) * math.exp(
								- self._delta_t / (self.thermal_resist[n][h] * self.thermal_cap[n][h])))
										  - self._big_m * (1 - hvac_mode_heat[n][h][
										t])), f'HVAC_Heating_LB_state' + increment

							# off mode
							self.milp += (hvac_temp[n][h][t] <= (
									self.T_out[n][h][t] - (
									self.T_out[n][h][t] -
									hvac_temp[n][h][t - 1]) * math.exp(
								- self._delta_t / (self.thermal_resist[n][h] * self.thermal_cap[n][h])))
										  + self._big_m * (1 - hvac_mode_off[n][h][
										t])), f'HVAC_Off_UB_state' + increment
							self.milp += (hvac_temp[n][h][t] >= (
									self.T_out[n][h][t] - (
									self.T_out[n][h][t] -
									hvac_temp[n][h][t - 1]) * math.exp(
								- self._delta_t / (self.thermal_resist[n][h] * self.thermal_cap[n][h])))
										  - self._big_m * (1 - hvac_mode_off[n][h][
										t])), f'HVAC_Off_LB_state' + increment

							# Cooling mode
							self.milp += (hvac_temp[n][h][t] <= (
									self.T_out[n][h][t] - hvac_power[n][h][t] * self.thermal_resist[n][h] - (
									self.T_out[n][h][t] - hvac_power[n][h][t] * self.thermal_resist[n][h] -
									hvac_temp[n][h][t - 1]) * math.exp(
								- self._delta_t / (self.thermal_resist[n][h] * self.thermal_cap[n][h])))
										  + self._big_m * (1 - hvac_mode_cool[n][h][
										t])), f'HVAC_Cooling_UB_state' + increment
							self.milp += (hvac_temp[n][h][t] >= (
									self.T_out[n][h][t] - hvac_power[n][h][t] * self.thermal_resist[n][h] - (
									self.T_out[n][h][t] - hvac_power[n][h][t] * self.thermal_resist[n][h] -
									hvac_temp[n][h][t - 1]) * math.exp(
								- self._delta_t / (self.thermal_resist[n][h] * self.thermal_cap[n][h])))
										  - self._big_m * (1 - hvac_mode_cool[n][h][
										t])), f'HVAC_Cooling_LB_state' + increment

						self.milp += hvac_active[n][h][t] == hvac_mode_heat[n][h][t] + hvac_mode_cool[n][h][
							t], f'HVAC_Active_Link_' + increment
						self.milp += hvac_power[n][h][t] == hvac_active[n][h][t] * self.hvac_capacity[n][
							h], f'HVAC_On_Off_' + increment

					# Force HVAC Activation If Temperature Exceeds Limits
					# self.milp += hvac_temp[n][h][t] <= self.hvac_temp_max[n][h] + self._big_m * hvac_active[n][h][t], f'HVAC_Turn_On_Above_' + increment
					# self.milp += hvac_temp[n][h][t] >= self.hvac_temp_min[n][h] - self._big_m * hvac_active[n][h][t], f'HVAC_Turn_On_Below_' + increment

					self.milp += hvac_temp[n][h][t] - self.hvac_temp_max[n][h] <= hvac_cost_comfort[n][h][
						t], f'HVAC_Cost_Above_UB' + increment
					self.milp += hvac_temp[n][h][t] - self.hvac_temp_min[n][h] >= -hvac_cost_comfort[n][h][
						t], f'HVAC_Cost_Below_UB' + increment

		#HP constraints
		if not all(not v for v in self.set_hp.values()):
			for n, t in itertools.product(self.set_meters, self.time_series):
				for hp in self.set_hp[n]:

					if self.hp_type[n][hp] == 'inverter':

						increment = f'{n}_{hp}_t{t:03d}'

						self.milp += self.hp_power[n][hp][t] <= self.hp_power_rated[n][hp]

						# HPT-2.1
						self.milp += (self.hp_power[n][hp][t] >= self.heating_kwh[n][hp][t] +
									self.circulation_kw[n][hp][t] + self.tank_heating_kwh[n][hp][t]), f'HP_Total_Power_' + increment

						# HPT-2.2
						self.milp += (self.heating_kwh[n][hp][t] >= self.hp_mass_hw_demand[n][hp][t] * self.hp_c_p[n][hp] * (
									self.hp_temp_desired[n][hp] - self.hp_temp_inlet[n][
								hp])/ 3600 * self._delta_t), f'HP_Heating_Demand_' + increment

						# HPT-2.3
						self.milp += (self.circulation_kw[n][hp][t] >= self.hp_mass_radiator[n][hp][t] * self.hp_c_p[n][hp] * (
									self.hp_temp_outlet[n][hp][t] - self.hp_temp_return[n][hp][
								t])/ 3600 * self._delta_t), f'HP_Circulation_Power_' + increment

						# HPT-2.5
						# if t ==0:
						# 	self.milp += (self.tank_heating_kwh[hp][t] == self.hp_capacity_tank[hp] * self.hp_c_p[hp] * self.hp_temp_out_init[hp]/3600), f'HP_Tank_Init_' + increment
						if t != 0:
							# HPT-2.4
							self.milp += (self.tank_heating_kwh[n][hp][t] >= self.hp_capacity_tank[n][hp] * self.hp_c_p[n][hp] * (
									self.hp_temp_outlet[n][hp][t] - self.hp_temp_outlet[n][hp][
								t - 1])/ 3600 * self._delta_t), f'HPT2.4_Tank_Heating_' + increment

						# HPT-3
						# self.milp += self.circulation_kw[hp][t] == ((self.hp_h_rad[hp] * self.hp_area_rad[hp]) * ((self.hp_temp_outlet[hp][t]
						# 										+ self.hp_temp_return[hp][t])/2 - self.hp_temp_indoor[hp][t])), f'HP_Convective_Limit_' + increment

						self.milp += (self.hp_mass_radiator[n][hp][t] * self.hp_c_p[n][hp] * (
								self.hp_temp_outlet[n][hp][t] - self.hp_temp_return[n][hp][t]) / 3600) == (
												(self.hp_h_rad[n][hp] * self.hp_area_rad[n][hp]) * ((self.hp_temp_outlet[n][hp][t]
												+ self.hp_temp_return[n][hp][t]) / 2 - self.hp_temp_indoor[n][hp][t]) * self._delta_t), f'HP_Convective_Limit_' + increment


						# HPT-4.1/ 4.2: Indoor temperature evolution
						if t == 0:
							self.milp += (self.hp_temp_indoor[n][hp][t] == self.hp_temp_indoor_init[n][hp]), f'HP_Indoor_Init_' + increment
							self.milp += (self.hp_temp_outlet[n][hp][t] == self.hp_temp_out_init[n][hp]), f'HP_Outlet_Init_' + increment
						else:
							# self.milp += ( self.hp_temp_indoor[h][t] == self.hp_temp_indoor[h][t - 1]
							# 					+ (self._delta_t / self.hp_thermal_resistance[h]) * self.hp_u_value[h] * (self.hp_t_out[h][t - 1] - self.hp_temp_indoor[h][t - 1])
							# 					+ self.hp_h_rad[h] * self.hp_area_rad[h] * (self.hp_temp_outlet[h][t - 1] - self.hp_temp_indoor[h][t - 1])
							# 			 ), f'HP_Indoor_Evolution_' + increment

							self.milp += (self.hp_temp_indoor[n][hp][t] == self.hp_temp_indoor[n][hp][t - 1] * self.hp_u_value[n][hp] +
										  self.hp_t_out[n][hp][t - 1] * (self._delta_t / self.hp_thermal_resistance[n][hp])
										  + self.hp_h_rad[n][hp] * self.hp_area_rad[n][hp] * self.hp_temp_outlet[n][hp][
											  t]), f'HP_Indoor_Evolution_' + increment

						# HPT-5
						self.milp += (self.hp_temp_indoor[n][hp][t] + self.hp_cost_comfort[n][hp][t] >= self.hp_temp_indoor_min[n][
							hp]), f'HP_Temp_Min_WithSlack_' + increment
						self.milp += (self.hp_temp_indoor[n][hp][t] + self.hp_cost_comfort[n][hp][t] <= self.hp_temp_indoor_max[n][
							hp]), f'HP_Temp_Max_WithSlack_' + increment
						# HPT-5
						# self.milp += (self.hp_temp_outlet[n][hp][t] + self.hp_cost_comfort[n][hp][t] >= self.hp_temp_out_min[n][
						# 	hp]), f'HP_TempOut_Min_WithSlack_' + increment
						# self.milp += (self.hp_temp_outlet[n][hp][t] + self.hp_cost_comfort[n][hp][t] <= self.hp_temp_out_max[n][
						# 	hp]), f'HP_TempOut_Max_WithSlack_' + increment

		# Write MILP to .lp file
		dir_name = os.path.abspath(os.path.join(__file__, '..'))
		lp_file = os.path.join(dir_name, f'Stage2Pool.lp')
		self.milp.writeLP(lp_file)

		# Set the solver to be called
		if self.solver == 'CBC' and 'PULP_CBC_CMD' in listSolvers(onlyAvailable=True):
			self.milp.setSolver(pulp.PULP_CBC_CMD(msg=False, timeLimit=self.timeout, gapRel=self.mipgap))

		elif self.solver == 'CPLEX' and 'CPLEX_CMD' in listSolvers(onlyAvailable=True):
			# for more info on some available parameters:
			# https://www.ibm.com/docs/en/icos/22.1.1?topic=parameters-mip-emphasis-switch
			# https://www.ibm.com/docs/en/icos/22.1.0?topic=parameters-feasibility-pump-switch
			# https://www.ibm.com/docs/en/icos/20.1.0?topic=parameters-feasibility-tolerance
			# https://www.ibm.com/docs/en/icos/12.9.0?topic=parameters-integrality-tolerance
			# https://www.ibm.com/docs/en/icos/12.9.0?topic=parameters-scale-parameter
			# setting options in cplex though puLP:
			# https://www-eio.upc.es/lceio/manuals/cplex90/relnotescplex/relnotescplex10.html
			# https://www-eio.upc.edu/lceio/manuals/cplex75/doc/refmanccpp/html/baseSystem.html
			# background on "fixed mip" infeasibility over incumbent solution (for duals calculation):
			# https://or.stackexchange.com/questions/6048/avoid-infeasibility-in-fixed-mip-problem-in-cplex
			self.milp.setSolver(CPLEX_CMD(msg=False, timeLimit=self.timeout, gapRel=self.mipgap, options=[
				'set emphasis mip 5',
				# 'set mip strategy fpheur 2',
				# 'set simplex tolerances feasibility 1e-9',
				# 'set mip tolerances integrality 1e-9',
				'set read scale -1'
			]))

		elif self.solver == 'HiGHS' and 'HiGHS_CMD' in listSolvers(onlyAvailable=True):
			self.milp.setSolver(
				HiGHS_CMD(
					msg=False,
					timeLimit=self.timeout,
					gapRel=self.mipgap,
					threads=1,
				)
			)

		else:
			raise ValueError(f'{self.solver}_CMD not available in puLP; '
							 f'please install the required solver or try a different one')

		logger.debug('-- defining the collective (pool) MILP problem... DONE!')

		return

	def solve_milp(self):
		"""
		Function that heads the definition and solution of the second stage MILP.
		"""
		# Define the MILP
		self.__define_milp()

		# Solve the MILP
		logger.debug('-- solving the collective (pool) MILP problem...')

		try:
			self.milp.solve()
			status = LpStatus[self.milp.status]
			opt_value = value(self.milp.objective)

		except Exception as e:
			logger.warning(f'Solver raised an error: \'{e}\'. Considering problem as "Infeasible".')
			status = 'Infeasible'
			opt_value = None

		self.status = status
		self.obj_value = opt_value

		logger.debug('-- solving the collective (pool) MILP problem... DONE!')

		return

	def generate_outputs(self) -> OutputsCollectivePoolDict:
		"""
		Function for generating the outputs of optimization, namely the battery's set points.
		:return: outputs dictionary with MILP variables' and other computed values
		"""
		logger.debug('-- generating outputs from the collective (pool) MILP problem...')

		outputs = {}

		# -- Verification added to avoid raising error whenever encountering a puLP solver error with CBC
		if self.obj_value is None:
			return outputs

		outputs['obj_value'] = round(self.obj_value, 3)
		outputs['milp_status'] = self.status
		outputs['nr_dates'] = self._nr_dates
		outputs['w_clustering'] = self._w_clustering

		outputs['p_cont'] = {meter_id: None for meter_id in self.set_meters}
		outputs['p_gn_new'] = {meter_id: None for meter_id in self.set_meters}
		outputs['p_gn_total'] = {meter_id: None for meter_id in self.set_meters}
		outputs['e_bn_new'] = {meter_id: None for meter_id in self.set_meters}
		outputs['e_bn_total'] = {meter_id: None for meter_id in self.set_meters}

		outputs['e_cmet'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_g'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_bc'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_bd'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_sup'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_sur'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_pur_pool'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_sale_pool'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_slc_pool'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_bat'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['delta_sup'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_consumed'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['e_alc'] = dict_none_lists(self.time_intervals, self.set_meters)
		outputs['delta_slc'] = dict_none_lists(self.time_intervals, self.set_meters)

		for n in self.set_meters:
			meter_btm_ev = self._meters_data[n].get('btm_evs')
			if meter_btm_ev is not None:
				outputs['ev_stored'] = {n: dict_none_lists(self.time_intervals, self.sets_btm_ev[n]) for n in
										self.set_meters}
				outputs['p_ev_charge'] = {n: dict_none_lists(self.time_intervals, self.sets_btm_ev[n]) for n in
										  self.set_meters}
				outputs['p_ev_discharge'] = {n: dict_none_lists(self.time_intervals, self.sets_btm_ev[n]) for n in
											 self.set_meters}

		if self.strict_pos_coeffs:
			outputs['delta_coeff'] = dict_none_lists(self.time_intervals, self.set_meters)
		if self.total_share_coeffs:
			outputs['delta_rec_balance'] = none_lists(self.time_intervals)
			outputs['delta_meter_balance'] = dict_none_lists(self.time_intervals, self.set_meters)

		# EVs______________________________________________________________________________________________
		# Required when vars include "-" since puLP converts it to "_"
		btm_ev_ids = [bid for bids in [v for _, v in self.sets_btm_ev.items()] for bid in bids]
		matchd = {key: key.replace('-', '_') for key in self.set_meters}
		ev_matchd = {key: key.replace('-', '_') for key in btm_ev_ids}

		original_ev_name = \
			lambda v_name: [ori_ev for ori_ev in btm_ev_ids if ev_matchd[ori_ev] + '_' in v_name][0]
		# EVs______________________________________________________________________________________________

		# required when vars include "-" since puLP converts it to "_"
		matchd = {key: key.replace('-', '_') for key in self.set_meters}
		rematchd = {v: k for k, v in matchd.items()}
		var_name = lambda v_str, n_str: rematchd[v_str.split(n_str)[-1]]

		# EWH outputs
		if bool(self._ewh_dataset):
			outputs['ewh_temp'] = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in self.set_meters}
			outputs['ewh_delta_in'] = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in
									   self.set_meters}
			outputs['ewh_optimized_load'] = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in
											 self.set_meters}
			outputs['ewh_original_load'] = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in
											self.set_meters}
			outputs['ewh_delta_use'] = {n: dict_none_lists(self.time_intervals, self.set_ewh[n]) for n in
										self.set_meters}

			ewh_ids = [bid for bids in [v for _, v in self.set_ewh.items()] for bid in bids]
			e_matchd = {key: key.replace('-', '_') for key in ewh_ids}
			original_e_name = lambda v_name: [ori_e for ori_e in ewh_ids if e_matchd[ori_e] + '_' in v_name][0]
			original_n_name = lambda v_name: [ori_n for ori_n in self.set_meters if matchd[ori_n] + '_' in v_name][0]

		# HVAC outputs
		if not all(not v for v in self.set_hvac.values()):
			outputs['hvac_power'] = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in
									 self.set_meters}
			outputs['hvac_temp'] = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in
									self.set_meters}
			outputs['hvac_cost_comfort'] = {n: dict_none_lists(self.time_intervals, self.set_hvac[n]) for n in
									self.set_meters}
			hvac_ids = [bid for bids in [v for _, v in self.set_hvac.items()] for bid in bids]
			h_matchd = {key: key.replace('-', '_') for key in hvac_ids}
			original_h_name = lambda v_name: [ori_h for ori_h in hvac_ids if h_matchd[ori_h] + '_' in v_name][0]

		#HP outputs
		if not all(not v for v in self.set_hp.values()):
			outputs['hp_power'] = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in
									 self.set_meters}
			outputs['hp_temp_indoor'] = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in
									self.set_meters}
			outputs['hp_power_circulation'] = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in
											self.set_meters}
			outputs['hp_power_heating'] = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in
											   self.set_meters}
			outputs['hp_power_tank'] = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in
											   self.set_meters}
			outputs['hp_outlet_temp'] = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in
										self.set_meters}
			outputs['hp_cost_comfort'] = {n: dict_none_lists(self.time_intervals, self.set_hp[n]) for n in
										 self.set_meters}
			hp_ids = [bid for bids in [v for _, v in self.set_hp.items()] for bid in bids]
			hp_matchd = {key: key.replace('-', '_') for key in hp_ids}
			original_hp_name = lambda v_name: [ori_hp for ori_hp in hp_ids if hp_matchd[ori_hp] + '_' in v_name][0]

		for v in self.milp.variables():
			if re.search('dummy', v.name):
				continue
			elif re.search('p_cont_', v.name):
				n = var_name(v.name, 'p_cont_')
				outputs['p_cont'][n] = v.varValue
			elif re.search('p_gn_new_', v.name):
				n = var_name(v.name, 'p_gn_new_')
				outputs['p_gn_new'][n] = v.varValue
			elif re.search('p_gn_total_', v.name):
				n = var_name(v.name, 'p_gn_total_')
				outputs['p_gn_total'][n] = v.varValue
			elif re.search('e_bn_new_', v.name):
				n = var_name(v.name, 'e_bn_new_')
				outputs['e_bn_new'][n] = v.varValue
			elif re.search('e_bn_total_', v.name):
				n = var_name(v.name, 'e_bn_total_')
				outputs['e_bn_total'][n] = v.varValue
			else:
				step_nr = int(v.name[-7:])
				v_name_reduced = v.name[:-9]  # var name without step_nr, i.e., without "_t0000000"

				if re.search(f'delta_rec_balance_', v.name):
					outputs['delta_rec_balance'][step_nr] = v.varValue

				elif re.search(f'e_cmet_', v.name):
					n = var_name(v_name_reduced, 'e_cmet_')
					outputs['e_cmet'][n][step_nr] = v.varValue

				elif re.search(f'ev_stored_', v.name):
					n = v.name.split('ev_stored_')[1].split('_EV')[0]
					ev = original_ev_name(v.name)
					outputs['ev_stored'][n][ev][step_nr] = v.varValue
				elif re.search(f'p_ev_charge_', v.name):
					n = v.name.split('p_ev_charge_')[1].split('_EV')[0]
					ev = original_ev_name(v.name)
					outputs['p_ev_charge'][n][ev][step_nr] = v.varValue
				elif re.search(f'p_ev_discharge_', v.name):
					n = v.name.split('p_ev_discharge_')[1].split('_EV')[0]
					ev = original_ev_name(v.name)
					outputs['p_ev_discharge'][n][ev][step_nr] = v.varValue

				elif re.search(f'e_g_', v.name):
					n = var_name(v_name_reduced, 'e_g_')
					outputs['e_g'][n][step_nr] = v.varValue
				elif re.search(f'e_bc_', v.name):
					n = var_name(v_name_reduced, 'e_bc_')
					outputs['e_bc'][n][step_nr] = v.varValue
				elif re.search(f'e_bd_', v.name):
					n = var_name(v_name_reduced, 'e_bd_')
					outputs['e_bd'][n][step_nr] = v.varValue
				elif re.search(f'e_sup_', v.name):
					n = var_name(v_name_reduced, 'e_sup_')
					outputs['e_sup'][n][step_nr] = v.varValue
				elif re.search(f'e_sur_', v.name):
					n = var_name(v_name_reduced, 'e_sur_')
					outputs['e_sur'][n][step_nr] = v.varValue
				elif re.search(f'e_pur_', v.name):
					n = var_name(v_name_reduced, 'e_pur_')
					outputs['e_pur_pool'][n][step_nr] = v.varValue
				elif re.search(f'e_sale_', v.name):
					n = var_name(v_name_reduced, 'e_sale_')
					outputs['e_sale_pool'][n][step_nr] = v.varValue
				elif re.search(f'e_slc_', v.name):
					n = var_name(v_name_reduced, 'e_slc_')
					outputs['e_slc_pool'][n][step_nr] = v.varValue
				elif re.search(f'e_bat_', v.name):
					n = var_name(v_name_reduced, 'e_bat_')
					outputs['e_bat'][n][step_nr] = v.varValue
				elif re.search(f'delta_sup_', v.name):
					n = var_name(v_name_reduced, 'delta_sup_')
					outputs['delta_sup'][n][step_nr] = v.varValue
				elif re.search(f'e_consumed_', v.name):
					n = var_name(v_name_reduced, 'e_consumed_')
					outputs['e_consumed'][n][step_nr] = v.varValue
				elif re.search(f'e_alc_', v.name):
					n = var_name(v_name_reduced, 'e_alc_')
					outputs['e_alc'][n][step_nr] = v.varValue
				elif re.search(f'delta_slc_', v.name):
					n = var_name(v_name_reduced, 'delta_slc_')
					outputs['delta_slc'][n][step_nr] = v.varValue
				elif re.search(f'delta_coeff_', v.name):
					n = var_name(v_name_reduced, 'delta_coeff_')
					outputs['delta_coeff'][n][step_nr] = v.varValue
				elif re.search(f'delta_meter_balance', v.name):
					n = var_name(v_name_reduced, 'delta_meter_balance_')
					outputs['delta_meter_balance'][n][step_nr] = v.varValue

				# EWH outputs
				elif v.name.startswith('temp_') and not v.name.startswith(('hvac_temp_', 'hp_temp_indoor_')):
					n = original_n_name(v.name)
					e = original_e_name(v.name)
					outputs['ewh_temp'][n][e][step_nr] = v.varValue
				elif re.search(f'delta_in_', v.name):
					n = original_n_name(v.name)
					e = original_e_name(v.name)
					outputs['ewh_delta_in'][n][e][step_nr] = v.varValue
					outputs['ewh_optimized_load'][n][e][step_nr] = v.varValue * varBackpack[n][e]['ewh_power']
					outputs['ewh_original_load'][n][e] = varBackpack[n][e]['original_load']
					outputs['ewh_delta_use'][n][e] = varBackpack[n][e]['delta_use']

				# HVAC
				elif re.search(f'hvac_power_', v.name):
					n = v.name.split('hvac_power_')[1].split('_HVAC')[0]
					h = original_h_name(v.name)
					outputs['hvac_power'][n][h][step_nr] = v.varValue
				elif re.search(f'hvac_temp_', v.name):
					n = v.name.split('hvac_temp_')[1].split('_HVAC')[0]
					h = original_h_name(v.name)
					outputs['hvac_temp'][n][h][step_nr] = v.varValue
				elif re.search(f'hvac_cost_comfort_', v.name):
					n = v.name.split('hvac_cost_comfort_')[1].split('_HVAC')[0]
					h = original_h_name(v.name)
					outputs['hvac_cost_comfort'][n][h][step_nr] = v.varValue

				# HP
				elif re.search(f'power_hp_', v.name):
					n = v.name.split('power_hp_')[1].split('_HP')[0]
					hp = original_hp_name(v.name)
					outputs['hp_power'][n][hp][step_nr] = v.varValue
				elif re.search(f'hp_temp_indoor_', v.name):
					n = v.name.split('hp_temp_indoor_')[1].split('_HP')[0]
					hp = original_hp_name(v.name)
					outputs['hp_temp_indoor'][n][hp][step_nr] = v.varValue
				elif re.search(f'hp_power_heating_', v.name):
					n = v.name.split('hp_power_heating_')[1].split('_HP')[0]
					hp = original_hp_name(v.name)
					outputs['hp_power_heating'][n][hp][step_nr] = v.varValue
				elif re.search(f'hp_power_circulation_', v.name):
					n = v.name.split('hp_power_circulation_')[1].split('_HP')[0]
					hp = original_hp_name(v.name)
					outputs['hp_power_circulation'][n][hp][step_nr] = v.varValue
				elif re.search(f'hp_power_tank_', v.name):
					n = v.name.split('hp_power_tank_')[1].split('_HP')[0]
					hp = original_hp_name(v.name)
					outputs['hp_power_tank'][n][hp][step_nr] = v.varValue
				elif re.search(f'hp_temp_outlet_', v.name):
					n = v.name.split('hp_temp_outlet_')[1].split('_HP')[0]
					hp = original_hp_name(v.name)
					outputs['hp_outlet_temp'][n][hp][step_nr] = v.varValue
				elif re.search(f'hp_cost_comfort_', v.name):
					n = v.name.split('hp_cost_comfort_')[1].split('_HP')[0]
					hp = original_hp_name(v.name)
					outputs['hp_cost_comfort'][n][hp][step_nr] = v.varValue

		# Include other individual cost metrics
		outputs['c_ind2pool'] = {n: None for n in self.set_meters}
		for n in self.set_meters:
			e_sup = np.array(outputs['e_sup'][n])
			l_buy = np.array(self._l_buy[n])
			e_sur = np.array(outputs['e_sur'][n])
			l_sell = np.array(self._l_sell[n])
			e_slc = np.array(outputs['e_slc_pool'][n])
			l_grid = np.array(self._l_grid)
			p_cont = outputs['p_cont'][n]
			l_cont = self._l_cont[n]
			p_gn_new = outputs['p_gn_new'][n]
			l_gic = self._l_gic[n]
			e_bn_new = outputs['e_bn_new'][n]
			l_bic = self._l_bic[n]
			e_bd = np.array(outputs['e_bd'][n])
			deg_cost = self._deg_cost[n]

			c_ind_array = sum((e_sup * l_buy - e_sur * l_sell + e_slc * l_grid + e_bd * deg_cost) * self._w_clustering) + \
						  p_cont * l_cont * self._nr_dates + \
						  p_gn_new * l_gic * self._nr_dates + \
						  e_bn_new * l_bic * self._nr_dates
			outputs['c_ind2pool'][n] = round(c_ind_array, 4)

		# Also retrieve the slack values of the "Market Equilibrium" constraints. These can be considered as the
		# "optimal" market prices.
		dual_prices = \
			[abs(self.milp.constraints[c].pi) for c in self.milp.constraints if c.startswith('Market_equilibrium_')]
		outputs['dual_prices'] = [round(dp, 4) for dp in dual_prices]
		# important step: scale the dual prices by the number of days they represent to achieve daily dual prices
		outputs['dual_prices'] = list(np.array(outputs['dual_prices']) / np.array(self._w_clustering))

		logger.debug('-- generating outputs from the collective (pool) MILP problem... DONE!')

		return outputs
