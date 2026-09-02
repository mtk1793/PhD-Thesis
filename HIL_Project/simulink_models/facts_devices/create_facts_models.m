%% CAPSM FACTS Device Simulink Models
% Generates Simulink subsystem models for SVC, STATCOM, TCSC, UPFC
% devices for integration with IEEE 9/39/118 bus systems.
%
% Author: CAPSM Thesis Project
% Date: 2026

clc; clear; close all;

%% =================================================================
%% 1. SVC (Static Var Compensator) Subsystem
%% =================================================================
function svc_subsystem = create_svc_model(bus_num, base_kv, q_max_mvar)
% Creates an SVC Simulink subsystem model
%
svc_params = struct(...)
    "bus", bus_num,...
    "base_kv", base_kv,...
    "q_max", q_max_mvar,...
    "q_min", -q_max_mvar,...
    "v_ref", 1.0,...
    "time_const", 0.01,...
    "droop_coeff", 50,...
    "alpha_min", 90,...
    "alpha_max", 160...
);

mdl = sprintf("CAPSM_SVC_Bus%d", bus_num);
fprintf("Creating SVC for Bus %d\n", bus_num);
end
