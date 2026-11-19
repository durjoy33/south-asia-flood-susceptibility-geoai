"""Estimated class/cluster areas = country percentage (mapped cells) x official total national area.
Inputs: summaries from 03 (run in "orig" mode: mapped cells only) (quintile classes) and 04 (Jenks classes). Output: CSV tables in POST/area_estimates/.
Estimates assume the unmapped part of each country has the same composition as the mapped part."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); from config import *
import pandas as pd
out = POST / "area_estimates"; out.mkdir(exist_ok=True)
TA = TOTAL_AREA_KM2; tot = sum(TA.values())
est = lambda pct, n: pct / 100 * TA[n]
cs = pd.read_csv(SUMM / "orig" / "country_susceptibility_summary.csv").set_index("Country")
cg = pd.read_csv(SUMM / "orig" / "country_gistar_summary.csv").set_index("Country")
cj = pd.read_csv(JENKS / "country_susceptibility_jenks.csv").set_index("Country")
rows = []
for n in COUNTRIES:
    rows.append(dict(Country=n, total_area_km2=TA[n], mapped_cells=int(cs.mapped_cells[n]),
        mapped_coverage_pct=100 * cs.mapped_cells[n] / TA[n],
        quintile_high_plus_very_high_pct=cs.HighPlusVeryHigh_pct[n], quintile_high_plus_very_high_km2_est=est(cs.HighPlusVeryHigh_pct[n], n),
        jenks_high_plus_very_high_pct=cj.HighPlusVeryHigh_pct[n], jenks_high_plus_very_high_km2_est=est(cj.HighPlusVeryHigh_pct[n], n),
        gistar_high_cluster_pct=cg.high_total_cluster_pct_of_mapped[n], gistar_high_cluster_km2_est=est(cg.high_total_cluster_pct_of_mapped[n], n),
        gistar_low_cluster_pct=cg.low_total_cluster_pct_of_mapped[n], gistar_low_cluster_km2_est=est(cg.low_total_cluster_pct_of_mapped[n], n)))
df = pd.DataFrame(rows); df.to_csv(out / "country_area_estimates.csv", index=False)
print(df.round(2).to_string())
