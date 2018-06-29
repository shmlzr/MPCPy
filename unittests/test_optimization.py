# -*- coding: utf-8 -*-
"""
This module contains the classes for testing the optimization module of mpcpy.

"""
import unittest
import os
import pandas as pd
from matplotlib import pyplot as plt
from mpcpy import models
from mpcpy import optimization
from mpcpy import exodata
from mpcpy import utility
from mpcpy import variables
from mpcpy import units
import numpy as np

from testing import TestCaseMPCPy

#%%
class OptimizeSimpleFromJModelica(TestCaseMPCPy):
    '''Test simple model optimization functions.
    
    '''
    
    def setUp(self):
        self.start_time = '1/1/2017';
        self.final_time = '1/2/2017';
        # Set .mo path
        self.mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        # Gather inputs
        start_time_exo = '1/1/2017';
        final_time_exo = '1/10/2017';
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        control_variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        self.controls = exodata.ControlFromCSV(control_csv_filepath, control_variable_map);
        self.controls.collect_data(start_time_exo, final_time_exo);
        # Set measurements
        self.measurements = {};
        self.measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        self.measurements['q_flow'] = {'Sample' : variables.Static('q_flow_sample', 1800, units.s)};
        # Gather constraints       
        constraint_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'SimpleRC_Constraints.csv');
        constraint_variable_map = {'q_flow_min' : ('q_flow', 'GTE', units.W), \
                                   'T_db_min' : ('T_db', 'GTE', units.K), \
                                   'T_db_max' : ('T_db', 'LTE', units.K)};
        self.constraints = exodata.ConstraintFromCSV(constraint_csv_filepath, constraint_variable_map);
        self.constraints.collect_data(start_time_exo, final_time_exo);

#    def test_optimize(self):
#        '''Test the optimization of a model.
#        
#        '''
#        
#        modelpath = 'Simple.RC';        
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);                              
#        # Solve optimization problem with default res_control_step                   
#        opt_problem.optimize(self.start_time, self.final_time);
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_measurements.csv');
#        df_test = model.control_data['q_flow'].display_data().to_frame();
#        df_test.index.name = 'Time'
#        self.check_df(df_test, 'optimize_control_default.csv');
#        # Simulate model with optimal control
#        model.simulate(self.start_time, self.final_time)
#        # Check references
#        df_test = model.display_measurements('Simulated');
#        self.check_df(df_test, 'simulate_optimal_default.csv');
#        # Solve optimization problem with user-defined res_control_step 
#        opt_problem.optimize(self.start_time, self.final_time, res_control_step = 60.0);
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_measurements.csv');
#        df_test = model.control_data['q_flow'].display_data().to_frame();
#        df_test.index.name = 'Time'
#        self.check_df(df_test, 'optimize_control_userdefined.csv');
#        # Simulate model with optimal control
#        model.simulate(self.start_time, self.final_time)
#        # Check references
#        df_test = model.display_measurements('Simulated');
#        self.check_df(df_test, 'simulate_optimal_userdefined.csv');
#        # Get opt input object and create dataframe
#        time = np.linspace(0,3600,3601);
#        df_test = pd.DataFrame();
#        data = [];
#        opt_input_traj = opt_problem.opt_input[1]
#        names = opt_problem.opt_input[0]
#        # Create data
#        for t in time:
#            data.append(opt_input_traj(t))
#        # Create index
#        timedelta = pd.to_timedelta(time, 's');
#        index = pd.to_datetime(self.start_time) + timedelta;
#        df_test = pd.DataFrame(data=data, index=index, columns=names)
#        df_test.index.name = 'Time'
#        # Check references
#        self.check_df(df_test, 'optimize_opt_input.csv');
        
    def test_optimize_penalty(self):
        '''Test the optimization of a model.
        
        '''
        
        modelpath = 'Simple.RC';        
        # Instantiate model
        model = models.Modelica(models.JModelica, \
                                models.RMSE, \
                                self.measurements, \
                                moinfo = (self.mopath, modelpath, {}), \
                                control_data = self.controls.data);
        # Instantiate optimization problem
        opt_problem = optimization.Optimization(model, \
                                                optimization.EnergyMin, \
                                                optimization.JModelica, \
                                                {'Power':'q_flow','Penalty':'T_db'}, \
                                                constraint_data = self.constraints.data);                              
        # Solve optimization problem with default res_control_step                   
        opt_problem.optimize(self.start_time, self.final_time);
        # Check references
        df_test = opt_problem.display_measurements('Simulated');
        self.check_df(df_test, 'optimize_measurements.csv');
        df_test = model.control_data['q_flow'].display_data().to_frame();
        df_test.index.name = 'Time'
        self.check_df(df_test, 'optimize_control_default.csv');
        
#    def test_set_problem_type(self):
#        '''Test the dynamic setting of a problem type.
#
#        '''
#        
#        modelpath = 'Simple.RC';        
#        # Instantiate model
#        parameter_data = {};
#        parameter_data['heatCapacitor.C'] = {};
#        parameter_data['heatCapacitor.C']['Free'] = variables.Static('C_free', False, units.boolean);
#        parameter_data['heatCapacitor.C']['Value'] = variables.Static('C_value', 3e6, units.boolean);
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data, \
#                                parameter_data = parameter_data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Solve optimization problem                     
#        opt_problem.optimize(self.start_time, self.final_time);
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_energy.csv');
#        # Set new problem type
#        opt_problem.set_problem_type(optimization.EnergyCostMin);
#        # Gather prices
#        price_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'SimpleRC_Prices.csv');
#        price_variable_map = {'energy' : ('pi_e', units.unit1)};
#        price = exodata.PriceFromCSV(price_csv_filepath, price_variable_map);
#        price.collect_data(self.start_time, self.final_time);
#        opt_problem.optimize(self.start_time, self.final_time, price_data = price.data)
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_energycost.csv');
#        
#    def test_optimize_subpackage(self):
#        '''Test the optimization of a model within a subpackage.
#        
#        '''
#        
#        modelpath = 'Simple.SubPackage.RC';     
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Solve optimization problem                     
#        opt_problem.optimize(self.start_time, self.final_time);
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_subpackage.csv');
#        
#    def test_get_options(self):
#        '''Test the getting of optimization options.
#        
#        '''
#        
#        modelpath = 'Simple.RC';        
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Get options
#        opt_options = opt_problem.get_optimization_options();
#        # Check references
#        json_test = opt_options;
#        self.check_json(json_test, 'initial_options.txt');
#        
#    def test_set_options(self):
#        '''Test the setting of optimization options.
#        
#        '''
#        
#        modelpath = 'Simple.RC';
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Get initial options
#        opt_options = opt_problem.get_optimization_options();
#        # Set new options
#        opt_options['IPOPT_options']['max_iter'] = 2;
#        opt_options['n_e'] = 2;
#        opt_options['result_mode'] = 'mesh_points';
#        opt_problem.set_optimization_options(opt_options)
#        # Get new options
#        opt_options = opt_problem.get_optimization_options();
#        # Check references
#        json_test = opt_options;
#        self.check_json(json_test, 'new_options.txt');
#        # Solve optimization problem                     
#        opt_problem.optimize(self.start_time, self.final_time);
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_new_options.csv');
#
#    def test_set_options_error(self):
#        '''Test the setting of optimization options cannot occur with auto options.
#        
#        '''
#        
#        modelpath = 'Simple.RC';        
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        for key in ['external_data', 'init_traj', 'nominal_traj']:
#            # Get initial options
#            opt_options = opt_problem.get_optimization_options();
#            # Set new options and check KeyError raised
#            with self.assertRaises(KeyError):
#                opt_options[key] = 2;
#                opt_problem.set_optimization_options(opt_options);
#        
#    def test_get_statistics(self):
#        '''Test the getting of optimization result statistics.
#        
#        '''
#        
#        modelpath = 'Simple.RC';
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Solve optimization problem                     
#        opt_problem.optimize(self.start_time, self.final_time);
#        # Get statistics
#        opt_statistics = opt_problem.get_optimization_statistics();
#        # Check references (except execution time)
#        df_test = pd.DataFrame(columns=['message', 'iterations', 'objective'], index = [0])
#        df_test.loc[0] = opt_statistics[:-1]
#        self.check_df(df_test, 'statistics.csv', timeseries=False);
#        
#    def test_set_parameters(self):
#        '''Test the dynamic setting of parameters.
#        
#        '''
#        
#        modelpath = 'Simple.RC';        
#        # Instantiate model
#        parameter_data = {'heatCapacitor.C' : {'Free' : variables.Static('C_free', False, units.boolean), \
#                                               'Value' : variables.Static('C_new', 1e5, units.J_K)}, \
#                          'To' : {'Free' : variables.Static('To_free', False, units.boolean), \
#                                  'Value' : variables.Static('To', 24, units.degC)}};
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data, 
#                                parameter_data = parameter_data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Solve optimization problem                     
#        opt_problem.optimize(self.start_time, self.final_time);
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_set_parameters_1.csv');
#        # Set new parameters of model
#        parameter_data['heatCapacitor.C']['Value'] = variables.Static('C_new', 1e7, units.J_K);
#        parameter_data['To']['Value'] = variables.Static('To', 22, units.degC);
#        opt_problem.Model.parameter_data = parameter_data;
#        # Solve optimization problem                     
#        opt_problem.optimize(self.start_time, self.final_time);
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_set_parameters_2.csv');
#        
#    def test_initial_constraint(self):
#        '''Test the optimization of a model with an initial constraint.
#        
#        '''
#        
#        modelpath = 'Simple.RC_nostart';        
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Add initial constraint
#        self.constraints.data['T_db']['Initial'] = variables.Static('T_db_initial', 21, units.degC);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Solve optimization problem                     
#        opt_problem.optimize(self.start_time, self.final_time);
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_initial_constraint.csv');
#        opt_statistics = opt_problem.get_optimization_statistics();
#        # Check references (except execution time)
#        df_test = pd.DataFrame(columns=['message', 'iterations', 'objective'], index = [0])
#        df_test.loc[0] = opt_statistics[:-1]
#        self.check_df(df_test, 'statistics_initial_constraint.csv', timeseries=False);
#        
#    def test_continue_error(self):
#        '''Test a ValueError is raised if try to use the "continue" keyword.
#        
#        '''
#        modelpath = 'Simple.RC_nostart';        
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Check ValueError raised
#        with self.assertRaises(ValueError):
#            opt_problem.optimize('continue', self.final_time);
#    
#    def test_optimize_long(self):
#        '''Test update of control data with opt horizon longer than initial.
#        
#        '''
#        
#        modelpath = 'Simple.RC';
#        # Instantiate model
#        model = models.Modelica(models.JModelica, \
#                                models.RMSE, \
#                                self.measurements, \
#                                moinfo = (self.mopath, modelpath, {}), \
#                                control_data = self.controls.data);
#        # Instantiate optimization problem
#        opt_problem = optimization.Optimization(model, \
#                                                optimization.EnergyMin, \
#                                                optimization.JModelica, \
#                                                {'Power':'q_flow','Penalty':None}, \
#                                                constraint_data = self.constraints.data);
#        # Solve optimization problem                     
#        opt_problem.optimize('1/10/2017 00:00:00', '1/11/2017 02:00:00');
#        # Check references
#        df_test = opt_problem.display_measurements('Simulated');
#        self.check_df(df_test, 'optimize_long_measurements.csv');
#        df_test = model.control_data['q_flow'].display_data().to_frame();
#        df_test.index.name = 'Time'
#        self.check_df(df_test, 'optimize_long_control.csv');

class EnergyPlusDemand(TestCaseMPCPy):
    '''Test simple model optimization functions.
    
    '''
    
    def setUp(self):
        self.start_time = '1/1/2017';
        self.final_time = '1/2/2017';
        # Set .mo path
        self.mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'Simple.mo');
        # Gather inputs
        start_time_exo = '1/1/2017';
        final_time_exo = '1/10/2017';
        control_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'SimpleRC_Input.csv');
        control_variable_map = {'q_flow_csv' : ('q_flow', units.W)};
        self.controls = exodata.ControlFromCSV(control_csv_filepath, control_variable_map);
        self.controls.collect_data(start_time_exo, final_time_exo);
        # Set measurements
        self.measurements = {};
        self.measurements['T_db'] = {'Sample' : variables.Static('T_db_sample', 1800, units.s)};
        self.measurements['q_flow'] = {'Sample' : variables.Static('q_flow_sample', 1800, units.s)};
        self.measurements['Tamb.y'] = {'Sample' : variables.Static('T_amb_sample', 1800, units.s)};
        # Gather constraints       
        constraint_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'SimpleRC_Constraints.csv');
        constraint_variable_map = {'q_flow_min' : ('q_flow', 'GTE', units.W), \
                                   'T_db_min' : ('T_db', 'GTE', units.K), \
                                   'T_db_max' : ('T_db', 'LTE', units.K)};
        self.constraints = exodata.ConstraintFromCSV(constraint_csv_filepath, constraint_variable_map);
        self.constraints.collect_data(start_time_exo, final_time_exo);   
        
    def test_energyplusdemandcostmin(self):
        '''Test the energy plus demand cost minimization problem.

        '''

        start_time = '1/2/2017';
        final_time = '1/3/2017';
        
        modelpath = 'Simple.RC';        
        # Instantiate model
        parameter_data = {};
        parameter_data['heatCapacitor.C'] = {};
        parameter_data['heatCapacitor.C']['Free'] = variables.Static('C_free', False, units.boolean);
        parameter_data['heatCapacitor.C']['Value'] = variables.Static('C_value', 1e6, units.boolean);
        model = models.Modelica(models.JModelica, \
                                models.RMSE, \
                                self.measurements, \
                                moinfo = (self.mopath, modelpath, {}), \
                                control_data = self.controls.data, \
                                parameter_data = parameter_data);
        # Instantiate optimization problem
        opt_problem = optimization.Optimization(model, \
                                                optimization.EnergyPlusDemandCostMin, \
                                                optimization.JModelica, \
                                                {'Power':'q_flow','Penalty':None}, \
                                                constraint_data = self.constraints.data,
                                                demand_periods=3);
        # Gather prices
        price_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'SimpleRC_Prices.csv');
        price_variable_map = {'energy' : ('pi_e', units.unit1),
                              'demand' : ('pi_d', units.unit1)};
        price = exodata.PriceFromCSV(price_csv_filepath, price_variable_map);
        price.collect_data(start_time, final_time);
        opt_problem.optimize(start_time, final_time, price_data = price.data)
        # Check references
        df_test = opt_problem.display_measurements('Simulated');
        self.check_df(df_test, 'optimize_energyplusdemandcost.csv');
        fig,ax = plt.subplots(2,1,sharex=True)
        ax[0].plot(df_test['T_db'])
        ax[0].plot(df_test['Tamb.y'])
        ax[1].plot(df_test['q_flow'])
        ax[0].plot([df_test.index[0], df_test.index[-1]], [293, 293])
        ax[0].plot([df_test.index[0], df_test.index[-1]], [298, 298])
        plt.show()
        
    def test_energyplusdemandcostmin_penalty(self):
        '''Test the energy plus demand cost minimization problem.

        '''

        start_time = '1/2/2017';
        final_time = '1/3/2017';
        
        modelpath = 'Simple.RC';        
        # Instantiate model
        parameter_data = {};
        parameter_data['heatCapacitor.C'] = {};
        parameter_data['heatCapacitor.C']['Free'] = variables.Static('C_free', False, units.boolean);
        parameter_data['heatCapacitor.C']['Value'] = variables.Static('C_value', 1e6, units.boolean);
        model = models.Modelica(models.JModelica, \
                                models.RMSE, \
                                self.measurements, \
                                moinfo = (self.mopath, modelpath, {}), \
                                control_data = self.controls.data, \
                                parameter_data = parameter_data);
        # Instantiate optimization problem
        opt_problem = optimization.Optimization(model, \
                                                optimization.EnergyPlusDemandCostMin, \
                                                optimization.JModelica, \
                                                {'Power':'q_flow','Penalty':'T_db'}, \
                                                constraint_data = self.constraints.data,
                                                demand_periods=3);
        # Gather prices
        price_csv_filepath = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'SimpleRC_Prices.csv');
        price_variable_map = {'energy' : ('pi_e', units.unit1),
                              'demand' : ('pi_d', units.unit1)};
        price = exodata.PriceFromCSV(price_csv_filepath, price_variable_map);
        price.collect_data(start_time, final_time);
        opt_problem.optimize(start_time, final_time, price_data = price.data)
        # Check references
        df_test = opt_problem.display_measurements('Simulated');
        self.check_df(df_test, 'optimize_energyplusdemandcost_penalty.csv');
        fig,ax = plt.subplots(2,1,sharex=True)
        ax[0].plot(df_test['T_db'])
        ax[0].plot(df_test['Tamb.y'])
        ax[1].plot(df_test['q_flow'])
        ax[0].plot([df_test.index[0], df_test.index[-1]], [293, 293])
        ax[0].plot([df_test.index[0], df_test.index[-1]], [298, 298])
        plt.show()
        
        
    def test_update_constraints(self):
        '''Test the updating of constraints in the optimization.
        
        '''
        
        modelpath = 'Simple.RC';        
        # Instantiate model
        model = models.Modelica(models.JModelica, \
                                models.RMSE, \
                                self.measurements, \
                                moinfo = (self.mopath, modelpath, {}), \
                                control_data = self.controls.data);
        # Instantiate optimization problem
        opt_problem = optimization.Optimization(model, \
                                                optimization.EnergyMin, \
                                                optimization.JModelica, \
                                                {'Power':'q_flow','Penalty':None}, \
                                                constraint_data = self.constraints.data);                              
        # Solve optimization problem with default constraints                   
        opt_problem.optimize(self.start_time, self.final_time);
        # Check references
        df_test = opt_problem.display_measurements('Simulated');
        self.check_df(df_test, 'optimize_measurements.csv');
        df_test = model.control_data['q_flow'].display_data().to_frame();
        df_test.index.name = 'Time'
        self.check_df(df_test, 'optimize_control_default.csv');
        # Update constraints and control data
        self.constraints.collect_data('1/11/2017', '1/12/2017');
        opt_problem.constraint_data = self.constraints.data;
        self.controls.collect_data('1/11/2017', '1/12/2017');
        # Solve optimization problem with updated constraints
        opt_problem.optimize('1/11/2017', '1/12/2017');
        # Check references
        df_test = opt_problem.display_measurements('Simulated');
        self.check_df(df_test, 'optimize_measurements_updated_constraints.csv');
        df_test = model.control_data['q_flow'].display_data().to_frame();
        df_test.index.name = 'Time'
        self.check_df(df_test, 'optimize_control_default_updated_constraints.csv');
        # Check new constraint key raises error
        self.constraints.data['New_Constraint'] = opt_problem.constraint_data['q_flow']
        opt_problem.constraint_data = self.constraints.data
        with self.assertRaises(ValueError):
            opt_problem.optimize('1/11/2017', '1/12/2017');
        
#%% Temperature tests
class OptimizeAdvancedFromJModelica(TestCaseMPCPy):
    '''Tests for the optimization of a model using JModelica.
    
    '''

    def setUp(self):
        ## Setup model
        self.mopath = os.path.join(self.get_unittest_path(), 'resources', 'model', 'LBNL71T_MPC.mo');
        self.modelpath = 'LBNL71T_MPC.MPC';
        self.libraries = os.environ.get('MODELICAPATH');
        self.estimate_method = models.JModelica; 
        self.validation_method = models.RMSE;
        self.zone_names = ['wes', 'hal', 'eas'];                   
        # Measurements
        self.measurements = {};
        self.measurements['wesTdb'] = {'Sample' : variables.Static('wesTdb_sample', 1800, units.s)};
        self.measurements['halTdb'] = {'Sample' : variables.Static('halTdb_sample', 1800, units.s)};
        self.measurements['easTdb'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['wesPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['halPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};     
        self.measurements['easPhvac'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};
        self.measurements['Ptot'] = {'Sample' : variables.Static('easTdb_sample', 1800, units.s)};        
        
        ## Exodata
        # Exogenous collection time
        self.start_time_exodata = '1/1/2015';
        self.final_time_exodata = '1/30/2015';
        # Optimization time
        self.start_time_optimization = '1/2/2015';
        self.final_time_optimization = '1/3/2015';       
        # Weather
        self.weather_path = os.path.join(self.get_unittest_path(), 'resources', 'weather', 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw');
        self.weather = exodata.WeatherFromEPW(self.weather_path);
        self.weather.collect_data(self.start_time_exodata, self.final_time_exodata);
        # Internal
        self.internal_path = os.path.join(self.get_unittest_path(), 'resources', 'internal', 'sampleCSV.csv');
        self.internal_variable_map = {'intRad_wes' : ('wes', 'intRad', units.W_m2), \
                                      'intCon_wes' : ('wes', 'intCon', units.W_m2), \
                                      'intLat_wes' : ('wes', 'intLat', units.W_m2), \
                                      'intRad_hal' : ('hal', 'intRad', units.W_m2), \
                                      'intCon_hal' : ('hal', 'intCon', units.W_m2), \
                                      'intLat_hal' : ('hal', 'intLat', units.W_m2), \
                                      'intRad_eas' : ('eas', 'intRad', units.W_m2), \
                                      'intCon_eas' : ('eas', 'intCon', units.W_m2), \
                                      'intLat_eas' : ('eas', 'intLat', units.W_m2)};           
        self.internal = exodata.InternalFromCSV(self.internal_path, self.internal_variable_map, tz_name = self.weather.tz_name);
        self.internal.collect_data(self.start_time_exodata, self.final_time_exodata);
        # Control (as initialization)
        self.control_path = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'ControlCSV.csv');
        self.control_variable_map = {'conHeat_wes' : ('conHeat_wes', units.unit1), \
                                     'conHeat_hal' : ('conHeat_hal', units.unit1), \
                                     'conHeat_eas' : ('conHeat_eas', units.unit1)};        
        self.control = exodata.ControlFromCSV(self.control_path, self.control_variable_map, tz_name = self.weather.tz_name);
        self.control.collect_data(self.start_time_exodata, self.final_time_exodata);
        # Parameters
        self.parameters_path = os.path.join(self.get_unittest_path(), 'outputs', 'model_parameters.txt');
        self.parameters = exodata.ParameterFromCSV(self.parameters_path);
        self.parameters.collect_data();
        # Constraints
        self.constraints_path = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'sampleConstraintCSV_Constant.csv');   
        self.constraints_variable_map = {'wesTdb_min' : ('wesTdb', 'GTE', units.degC), \
                                         'wesTdb_max' : ('wesTdb', 'LTE', units.degC), \
                                         'easTdb_min' : ('easTdb', 'GTE', units.degC), \
                                         'easTdb_max' : ('easTdb', 'LTE', units.degC), \
                                         'halTdb_min' : ('halTdb', 'GTE', units.degC), \
                                         'halTdb_max' : ('halTdb', 'LTE', units.degC), \
                                         'der_wesTdb_min' : ('wesTdb', 'dGTE', units.K), \
                                         'der_wesTdb_max' : ('wesTdb', 'dLTE', units.K), \
                                         'der_easTdb_min' : ('easTdb', 'dGTE', units.K), \
                                         'der_easTdb_max' : ('easTdb', 'dLTE', units.K), \
                                         'der_halTdb_min' : ('halTdb', 'dGTE', units.K), \
                                         'der_halTdb_max' : ('halTdb', 'dLTE', units.K), \
                                         'conHeat_wes_min' : ('conHeat_wes', 'GTE', units.unit1), \
                                         'conHeat_wes_max' : ('conHeat_wes', 'LTE', units.unit1), \
                                         'conHeat_hal_min' : ('conHeat_hal', 'GTE', units.unit1), \
                                         'conHeat_hal_max' : ('conHeat_hal', 'LTE', units.unit1), \
                                         'conHeat_eas_min' : ('conHeat_eas', 'GTE', units.unit1), \
                                         'conHeat_eas_max' : ('conHeat_eas', 'LTE', units.unit1)};
        self.constraints = exodata.ConstraintFromCSV(self.constraints_path, self.constraints_variable_map, tz_name = self.weather.tz_name);
        self.constraints.collect_data(self.start_time_exodata, self.final_time_exodata);
        self.constraints.data['wesTdb']['Cyclic'] = variables.Static('wesTdb_cyclic', 1, units.boolean_integer);
        self.constraints.data['easTdb']['Cyclic'] = variables.Static('easTdb_cyclic', 1, units.boolean_integer);
        self.constraints.data['halTdb']['Cyclic'] = variables.Static('halTdb_cyclic', 1, units.boolean_integer);
        # Prices
        self.prices_path = os.path.join(self.get_unittest_path(), 'resources', 'optimization', 'PriceCSV.csv');
        self.price_variable_map = {'pi_e' : ('pi_e', units.unit1)};        
        self.prices = exodata.PriceFromCSV(self.prices_path, self.price_variable_map, tz_name = self.weather.tz_name);
        self.prices.collect_data(self.start_time_exodata, self.final_time_exodata);        
        
        ## Parameters
        self.parameters.data['lat'] = {};
        self.parameters.data['lat']['Value'] = self.weather.lat;     
        ## Instantiate model
        self.model = models.Modelica(self.estimate_method, \
                                     self.validation_method, \
                                     self.measurements, \
                                     moinfo = (self.mopath, self.modelpath, self.libraries), \
                                     zone_names = self.zone_names, \
                                     weather_data = self.weather.data, \
                                     internal_data = self.internal.data, \
                                     control_data = self.control.data, \
                                     parameter_data = self.parameters.data, \
                                     tz_name = self.weather.tz_name);                                     
    def test_energymin(self):
        '''Test energy minimization of a model.'''
        plt.close('all');        
        # Instanatiate optimization problem
        self.opt_problem = optimization.Optimization(self.model, \
                                                     optimization.EnergyMin, \
                                                     optimization.JModelica, \
                                                     {'Power':'Ptot','Penalty':None}, \
                                                     constraint_data = self.constraints.data)
        # Optimize
        self.opt_problem.optimize(self.start_time_optimization, self.final_time_optimization);
        # Check references
        df_test = self.opt_problem.display_measurements('Simulated');
        self.check_df(df_test, 'energymin.csv');

    def test_energycostmin(self):
        '''Test energy cost minimization of a model.'''
        plt.close('all');
        # Instanatiate optimization problem
        self.opt_problem = optimization.Optimization(self.model, \
                                                     optimization.EnergyCostMin, \
                                                     optimization.JModelica, \
                                                     {'Power':'Ptot','Penalty':None}, \
                                                     constraint_data = self.constraints.data)
        # Optimize
        self.opt_problem.optimize(self.start_time_optimization, self.final_time_optimization, price_data = self.prices.data);
        # Check references
        df_test = self.opt_problem.display_measurements('Simulated');
        self.check_df(df_test, 'energycostmin.csv');
        
if __name__ == '__main__':
    unittest.main()