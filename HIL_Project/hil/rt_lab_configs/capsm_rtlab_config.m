%% CAPSM RT-LAB 4-CPU Configuration for OPAL-RT
% Defines the subsystem splitting strategy for IEEE 39-bus
% model across 4 CPU cores on OPAL-RT OP5700/OP4510.
%
% This script configures the ARTEMIS solver settings, core assignment,
% and communication interfaces for real-time simulation
% of the IEEE 39-bus system with FACTS + EV + CAPSM controllers.
%
% Core Allocation (4 CPUs):
%   Core 1: North region (buses 1-19) + System-1 CNN-LSTM
%   Core 2: South region (buses 20-39) + System-2 QIRL
%   Core 3: CAPSM Arbitration + Communication
%   Core 4: Data acquisition + Logging + HIL interface
%
% Author: CAPSM Thesis Project
% Date: 2026

clc; clear;

%% =================================================================
%% 1. Configuration Parameters
%% =================================================================
config = struct();

% Solver settings
config.solver_type    = 'ARTEMIS';      % ARTEMIS solver for real-time
config.time_step      = 50e-6;         % 50 microseconds (EMT)
config.phasor_step   = 1e-3;            % 1 millisecond (phasor)
config.sim_time       = 10;               % Simulation time (seconds)
config.decimation    = 50;               % Decimation factor

% OPAL-RT hardware settings
config.target       = 'OP5700';         % Target simulator
config.n_cores       = 4;                  % Number of CPU cores
config.fpga_mode     = 'eFPGASIM';     % FPGA-based power electronics

% Communication settings
config.protocol      = 'IEC61850';      % Substation communication
config.latency_budget = 20e-3;            % 20 ms max latency
config.sync_mode       = 'PTP';             % IEEE 1588 Precision Time Protocol

%% =================================================================
%% 2. Subsystem Assignment
%% =================================================================
% Define which parts of the model run on which core
subsystems = struct();

% --- Core 1: North Region + System-1 (Fast Response) ---
subsystems.core1.name        = 'sm_master';
subsystems.core1.region      = 'north';          % Buses 1-19
subsystems.core1.buses       = [1:19];
subsystems.core1.component  = 'System1_CNN_LSTM';
subsystems.core1.task_time   = 5e-3;             % 5 ms budget
subsystems.core1.priority    = 1;                 % Highest priority (protection)

% --- Core 2: South Region + System-2 (Deliberative) ---
subsystems.core2.name        = 'sm_slave1';
subsystems.core2.region      = 'south';          % Buses 20-39
subsystems.core2.buses       = [20:39];
subsystems.core2.component  = 'System2_QIRL';
subsystems.core2.task_time   = 50e-3;            % 50 ms budget
subsystems.core2.priority    = 2;                 % Medium priority

% --- Core 3: Arbitration + Communication ---
subsystems.core3.name        = 'sm_slave2';
subsystems.core3.region      = 'global';         % System-wide
subsystems.core3.buses       = 'all';
subsystems.core3.component  = 'Metacognitive_Arbiter';
subsystems.core3.task_time   = 10e-3;           % 10 ms budget
subsystems.core3.priority    = 3;                 % Coordination priority

% --- Core 4: I/O + Logging + HIL Interface ---
subsystems.core4.name        = 'sm_slave3';
subsystems.core4.region      = 'io';             % I/O interface
subsystems.core4.buses       = 'sensors';
subsystems.core4.component  = 'HIL_Interface';
subsystems.core4.task_time   = 1e-3;             % 1 ms budget
subsystems.core4.priority    = 4;                 % Lowest priority

%% =================================================================
%% 3. Communication Channels
%% =================================================================
channels = struct();

% Core1 <-> Core3 (System-1 commands)
channels.c1_c3.name      = 'ch_sys1_to_arbiter';
channels.c1_c3.from      = 'sm_master';
channels.c1_c3.to        = 'sm_slave2';
channels.c1_c3.signal     = 'control_actions';
channels.c1_c3.latency    = 5e-3;

% Core2 <-> Core3 (System-2 proposals)
channels.c2_c3.name      = 'ch_sys2_to_arbiter';
channels.c2_c3.from      = 'sm_slave1';
channels.c2_c3.to        = 'sm_slave2';
channels.c2_c3.signal     = 'optimal_setpoints';
channels.c2_c3.latency    = 50e-3;

% Core3 <-> Core4 (Final commands to HIL interface)
channels.c3_c4.name      = 'ch_commands_to_io';
channels.c3_c4.from      = 'sm_slave2';
channels.c3_c4.to        = 'sm_slave3';
channels.c3_c4.signal     = 'final_control';
channels.c3_c4.latency    = 10e-3;

% Core3 <-> Core1 (Feedback: confidence + urgency)
channels.c3_c1_fb.name   = 'ch_feedback_s1';
channels.c3_c1_fb.from     = 'sm_slave2';
channels.c3_c1_fb.to       = 'sm_master';
channels.c3_c1_fb.signal  = 'confidence_urgency';
channels.c3_c1_fb.latency = 5e-3;

% PMU data -> Core4 (Sensor input)
channels.pmu_c4.name      = 'ch_pmu_data';
channels.pmu_c4.from      = 'field';
channels.pmu_c4.to        = 'sm_slave3';
channels.pmu_c4.signal     = 'pmu_measurements';
channels.pmu_c4.latency  = 20e-3;

%% =================================================================
%% 4. Scenario Configuration
%% =================================================================
scenarios = struct();

% Normal operation
scenarios.normal.name        = 'normal_op';
scenarios.normal.duration    = 3600;       % 1 hour
scenarios.normal.load_profile = 'opsd';
scenarios.normal.renewable    = 'opsd';
scenarios.normal.events      = {};

% Fault scenario
scenarios.fault.name        = 'fault_test';
scenarios.fault.duration    = 60;           % 1 minute
scenarios.fault.fault_bus     = 14;
scenarios.fault.fault_type    = 'three_phase';
scenarios.fault.fault_time    = 30;          % at t=30s

% Renewable intermittency
scenarios.renewable.name    = 'renewable_drop';
scenarios.renewable.duration = 120;
scenarios.renewable.drop_bus  = 33;
scenarios.renewable.drop_pct   = 60;           % 60% drop
scenarios.renewable.drop_time = 10;          % at t=10s

% Cyber attack (FDI)
scenarios.cyber.name        = 'cyber_fdi';
scenarios.cyber.duration    = 60;
scenarios.cyber.attack_buses = [5, 10];
scenarios.cyber.magnitude   = 0.05;
scenarios.cyber.attack_time   = 20;          % at t=20s

% EV V2G coordination
scenarios.ev.name         = 'ev_v2g';
scenarios.ev.duration      = 300;
scenarios.ev.ev_buses      = [3, 8, 15];
scenarios.ev.mode           = 'v2g_g2v';
scenarios.ev.start_time     = 60;

%% =================================================================
%% 5. Save Configuration
%% =================================================================
config.subsystems  = subsystems;
config.channels   = channels;
config.scenarios  = scenarios;

save('capsm_rtlab_config.mat', 'config');
fprintf('CAPSM RT-LAB configuration saved.\n');
fprintf('Core allocation: 4 CPUs configured\n');
fprintf('Scenarios: 5 test scenarios defined\n');
fprintf('Ready for OPAL-RT deployment\n');
