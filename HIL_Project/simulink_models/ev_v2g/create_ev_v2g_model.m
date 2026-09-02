%% CAPSM EV V2G/G2V Bidirectional Charger Simulink Model
% Creates a Simulink subsystem model for a bidirectional
% EV charger supporting both V2G (vehicle-to-grid) and
% G2V (grid-to-vehicle) operation modes.
%
% This subsystem integrates with the IEEE bus system models
% and connects to the CAPSM System-2 QIRL controller for
% coordinated charging/discharging scheduling.
%
% Author: CAPSM Thesis Project
% Date: 2026

function ev_model = create_ev_v2g_model(bus_num, p_max_kw, cap_kwh)

ev_params = struct( ...
    "bus", bus_num, ...
    "p_max", p_max_kw, ...
    "capacity", cap_kwh, ...
    "soc_init", 0.5, ...
    "soc_min", 0.2, ...
    "soc_max", 0.9, ...
    "efficiency_ch", 0.92, ...
    "efficiency_dis", 0.88, ...
    "v2g_enabled", 1, ...
    "response_time", 0.1 ...
);

fprintf("Creating EV V2G model for Bus %d\n", bus_num);

mdl = sprintf("CAPSM_EV_Bus%d", bus_num);
new_system(mdl);

add_block("simulink/Subsystems/Subsystem", [mdl "/EV_Charger"]);

add_block("simulink/Sources/Constant", [mdl "/EV_Charger/SOC_ref"]);
set_param([mdl "/EV_Charger/SOC_ref"], "Value", "0.5");

add_block("simulink/Sources/Constant", [mdl "/EV_Charger/P_grid"]);
set_param([mdl "/EV_Charger/P_grid"], "Value", "0");

add_block("simulink/Discontinuities/Step", [mdl "/EV_Charger/P_cmd"]);
set_param([mdl "/EV_Charger/P_cmd"], "Time", "0");

add_block("simulink/Continuous/PID Controller", [mdl "/EV_Charger/SoC_Control"]);

add_block("simulink/Electrical Elements/Battery", [mdl "/EV_Charger/Battery"]);
set_param([mdl "/EV_Charger/Battery"], ...
    "SOC_init", "0.5", ...
    "Capacity", num2str(cap_kwh * 3.6e6));

add_block("simulink/Power Electronics/Bidirectional DC-DC Converter", [mdl "/EV_Charger/BiDir_DCDC"]);

add_line(mdl, "EV_Charger/P_cmd/1", "EV_Charger/SoC_Control/1");
add_line(mdl, "EV_Charger/SOC_ref/1", "EV_Charger/SoC_Control/2");
add_line(mdl, "EV_Charger/SoC_Control/1", "EV_Charger/BiDir_DCDC/1");
add_line(mdl, "EV_Charger/P_grid/1", "EV_Charger/BiDir_DCDC/2");
add_line(mdl, "EV_Charger/Battery/1", "EV_Charger/BiDir_DCDC/2");

fprintf("  EV V2G model created: %s\n", mdl);
end

fprintf("\n=== Creating EV V2G fleets for IEEE 39-bus ===\N");

ev1 = create_ev_v2g_model(3, 19.2, 40);
ev2 = create_ev_v2g_model(8, 19.2, 40);
ev3 = create_ev_v2g_model(15, 19.2, 40);

fprintf("\nEV V2G fleet created: 3 charging stations\n");
fprintf("Ready for integration with CAPSM controller\n");
