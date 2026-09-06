# OPSD Data Integrity Report

Generated from verified raw files (see `data/raw/provenance_manifest.json`).

Dataset: Open Power System Data - Time series v2020-10-06
DOI: https://doi.org/10.25832/time_series/2020-10-06

## 60min (h)

- Coverage: 2014-12-31 23:00:00+00:00 to 2020-09-30 23:00:00+00:00
- Expected points: 50,401; actual unique: 50,401; missing timestamps: 0; duplicates: 0

| Column | Present | NaN | NaN % | Gaps >2 steps | Longest gap | Min | Mean | Max |
|---|---|---|---|---|---|---|---|---|
| DE_load_actual_entsoe_transparency | yes | 1 | 0.002 | 0 | 1 | 31,307.0 | 55,492.5 | 77,549.0 |
| DE_load_forecast_entsoe_transparency | yes | 25 | 0.05 | 1 | 24 | 28,824.0 | 54,791.4 | 75,912.0 |
| DE_solar_generation_actual | yes | 104 | 0.206 | 5 | 24 | 0.0 | 4,566.0 | 32,947.0 |
| DE_wind_generation_actual | yes | 75 | 0.149 | 3 | 24 | 135.0 | 11,552.2 | 46,064.0 |
| DE_wind_onshore_generation_actual | yes | 73 | 0.145 | 3 | 24 | 119.0 | 9,581.5 | 40,752.0 |
| DE_wind_offshore_generation_actual | yes | 75 | 0.149 | 3 | 24 | 0.0 | 1,970.5 | 6,901.0 |
| DE_LU_price_day_ahead | yes | 32,861 | 65.199 | 1 | 32856 | -90.0 | 35.8 | 200.0 |
| DE_50hertz_load_actual_entsoe_transparency | yes | 1 | 0.002 | 0 | 1 | 106.0 | 10,404.5 | 16,581.0 |
| DE_amprion_load_actual_entsoe_transparency | yes | 1 | 0.002 | 0 | 1 | 11,598.0 | 20,943.0 | 32,060.0 |
| DE_tennet_load_actual_entsoe_transparency | yes | 1 | 0.002 | 0 | 1 | 9,495.0 | 17,184.7 | 24,577.0 |
| DE_transnetbw_load_actual_entsoe_transparency | yes | 1 | 0.002 | 0 | 1 | 3,452.0 | 6,960.5 | 11,733.0 |
| DE_50hertz_solar_generation_actual | yes | 15 | 0.03 | 2 | 8 | 0.0 | 1,177.3 | 9,121.0 |
| DE_amprion_solar_generation_actual | yes | 14 | 0.028 | 2 | 8 | 0.0 | 1,051.5 | 7,609.0 |
| DE_tennet_solar_generation_actual | yes | 8 | 0.016 | 1 | 8 | 0.0 | 1,692.7 | 12,301.0 |
| DE_transnetbw_solar_generation_actual | yes | 15 | 0.03 | 2 | 8 | 0.0 | 641.0 | 4,453.0 |
| DE_50hertz_wind_generation_actual | yes | 1 | 0.002 | 0 | 1 | 8.0 | 3,724.3 | 16,153.0 |
| DE_amprion_wind_onshore_generation_actual | yes | 1 | 0.002 | 0 | 1 | 0.0 | 1,857.2 | 9,443.0 |
| DE_tennet_wind_generation_actual | yes | 1 | 0.002 | 0 | 1 | 20.0 | 5,725.3 | 20,631.0 |
| DE_transnetbw_wind_onshore_generation_actual | yes | 1 | 0.002 | 0 | 1 | 0.0 | 248.0 | 1,474.0 |

## 15min (15min)

- Coverage: 2014-12-31 23:00:00+00:00 to 2020-09-30 23:45:00+00:00
- Expected points: 201,604; actual unique: 201,604; missing timestamps: 0; duplicates: 0

| Column | Present | NaN | NaN % | Gaps >2 steps | Longest gap | Min | Mean | Max |
|---|---|---|---|---|---|---|---|---|
| DE_load_actual_entsoe_transparency | yes | 6 | 0.003 | 1 | 5 | 29,158.1 | 55,492.6 | 77,852.9 |
| DE_load_forecast_entsoe_transparency | yes | 102 | 0.051 | 2 | 96 | 28,675.4 | 54,791.5 | 76,392.5 |
| DE_solar_generation_actual | yes | 420 | 0.208 | 6 | 96 | 0.0 | 4,566.1 | 33,193.8 |
| DE_wind_generation_actual | yes | 304 | 0.151 | 5 | 96 | 104.7 | 11,552.3 | 46,205.6 |
| DE_wind_offshore_generation_actual | yes | 304 | 0.151 | 5 | 96 | 0.0 | 1,970.5 | 6,990.4 |
| DE_wind_onshore_generation_actual | yes | 294 | 0.146 | 4 | 96 | 87.8 | 9,581.5 | 40,929.7 |
