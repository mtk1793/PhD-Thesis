"""Offline CAPSM simulation tests, independent of licensed PSS/E."""
import random
import pytest
from psse_capsm.case import RawCase
from psse_capsm.controls import EVFleet, clamp_action
from psse_capsm.psse_adapter import Psse35
from psse_capsm.run_simulation import candidate_actions, reward, sample_born, read_profiles

SYNTH_RAW = """0, 100.0, 33, 0, 0, 60
CAPSM TEST
synthetic
1, 'BUS 1', 345, 3, 1, 1, 1, 1.0, 0, 1.1, 0.9
2, 'BUS 2', 345, 1, 1, 1, 1, 1.0, 0, 1.1, 0.9
0 / END OF BUS DATA, BEGIN LOAD DATA
2, '1', 1, 1, 1, 100.0, 40.0, 0, 0, 0, 0, 1, 1, 0
0 / END OF LOAD DATA, BEGIN FIXED SHUNT DATA
0 / END OF FIXED SHUNT DATA, BEGIN GENERATOR DATA
1, '1', 100, 0, 300, -300, 1.0, 0, 100, 0, 0, 0, 0, 1, 1, 100, 200, 0
0 / END OF GENERATOR DATA, BEGIN BRANCH DATA
1, 2, '1', 0.01, 0.1, 0.0, 110, 110, 110, 0, 0, 0, 0, 1
0 / END OF BRANCH DATA, BEGIN TRANSFORMER DATA
1, 2, 0, '2', 1, 1, 1, 0, 0, 1, 'TX', 1
0.01, 0.09, 100
1.0, 345, 0, 120, 120, 120, 0, 0
1.0, 345
0 / END OF TRANSFORMER DATA, BEGIN AREA INTERCHANGE DATA
0 / END OF AREA INTERCHANGE DATA, BEGIN TWO-TERMINAL DC DATA
Q
"""

def test_raw_39_feature_branch_definition():
    r = RawCase(SYNTH_RAW)
    assert r.bus_ids() == [1,2]
    assert len(r.generators()) == 1
    assert len(r.branch_records()) == 2
    assert sorted(v[3] for v in r.branch_records()) == [110.0,120.0]

def test_load_scale_immutable():
    original = RawCase(SYNTH_RAW)
    trial = original.clone()
    trial.set_load_scale(0.5)
    assert "50.0" in trial.lines[trial.section_indices["LOAD"][0]]
    assert "100.0" in original.lines[original.section_indices["LOAD"][0]]
    trial.add_load(2,"EV",-10)
    assert len(trial.section_indices["LOAD"]) == 2
    assert len(original.section_indices["LOAD"]) == 1

def test_shunt_pu_to_mvar():
    case = RawCase(SYNTH_RAW)
    case.set_fixed_shunt(2,"SV",0.5)
    assert "50.0" in case.lines[case.section_indices["FIXED SHUNT"][0]]
    case.set_fixed_shunt(2,"SV",-0.5)
    assert "-50.0" in case.lines[case.section_indices["FIXED SHUNT"][0]]
    assert len(case.section_indices["FIXED SHUNT"]) == 1

def test_series_reactance_trip():
    case = RawCase(SYNTH_RAW)
    case.set_branch_x(1,2,"1",0.3)
    assert abs(float(case.branch_records()[0][3])-110.0)<1e-9
    case.trip_branch(1,2,"1")
    assert case.branch_records()[0][-1] == 0

def test_ev_soc_invariant_and_no_preview_mutation():
    fleet = EVFleet(soc=(0.89,0.21,0.5))
    p, soc = fleet.dispatch((50,-50,0),commit=False)
    assert p[0]<2 and p[1]>-2
    assert abs(soc[0]-.9)<1e-10 and abs(soc[1]-.2)<1e-10
    assert fleet.soc == (0.89,0.21,0.5)
    fleet.dispatch((50,-50,0),commit=True)
    assert fleet.soc[0] <=.9 and fleet.soc[1] >=.2

def test_reserved_action():
    a=clamp_action((5,5,.1,5,5,500,200,-200,0))
    assert a[5]==0 and a[2]==.3 and a[6]==50 and a[7]==-50
    with pytest.raises(ValueError): clamp_action([0]*8)

def test_candidates_reward_born():
    candidates=candidate_actions(random.Random(1),32)
    assert len(candidates)==32 and all(a[5]==0 for a in candidates)
    assert 0 <= sample_born([0,-2,-4],random.Random(1))<3
    good={"converged":True,"voltage_deviation_pu":.01,
          "voltage_violation_severity":0,"losses_mw":35,"thermal_overload_severity":0}
    assert reward(good, (0,0,.3,0,0,0,0,0,0)) > reward(dict(good,voltage_violation_severity=1),(0,0,.3,0,0,0,0,0,0))

def test_csv_profiles(tmp_path):
    p=tmp_path/"profile.csv"
    p.write_text("timestamp,load_scale,wind_mw,solar_mw\n2019-01-01T00:00Z,1.0,20,10\n")
    assert list(read_profiles(p))[0]["wind_mw"] == 20
    p.write_text("timestamp,load_scale,wind_mw,solar_mw\n2019-01-01T00:00Z,-1,20,10\n")
    with pytest.raises(ValueError): list(read_profiles(p))

class FakePsse:
    def psseinit(self,n):return 0
    def read(self,i,path):return 0
    def fnsl(self,options):return 0
    def solved(self):return 0
    def busdat(self,bus,key):return (0,1.0 if key=="PU" else 0.0)
    def macdat(self,bus,gid,key):return (0,100.0 if key=="P" else 5.0)
    def brnflo(self,i,j,ckt):return (0,complex(80,10) if i==1 else complex(-78,-9))

def test_psse_adapter_contract_with_fake():
    result=Psse35(psspy_module=FakePsse()).solve("fake.raw",[1,2],[(1,2,"1",100,1)],[(1,"1")])
    assert result["converged"] and result["losses_mw"]==2.0
    assert result["thermal_overload_count"]==0
