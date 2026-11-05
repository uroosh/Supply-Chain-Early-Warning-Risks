# Critical Supply-Chain Risk Early-Warning Framework

**Research question:** can a transparent, data-driven risk framework identify supply-chain conditions that warrant earlier operational review and resilience planning?

Dashboard:(https://public.tableau.com/app/profile/uroosh.niazi2790/viz/SupplyChainEarlyWarningDashboard/Supply-ChainEarly-WarningDashboard) | Report: `report/`

![Dashboard](tableau/dashboard.png)

## What it does
Scores supplier-part items on 10 risk dimensions (0-100 each), combines them with weights that sum to 1, and applies transparent rules.

| Step | Setting |
|---|---|
| Tiers | Low < 38, Moderate < 48, Elevated < 57, High >= 57 |
| Early warning | criticality >= 4 and any single dimension >= 90 |
| Review queue | early-warning items plus High tier |
| Priority quadrants | Act now, Monitor closely, Protect (critical, stable), Routine (likelihood >= 53 vs criticality >= 4) |
| Validation | Score compared with simulated disruption rate |

All parameters live in [`src/scrisk/config.py`](src/scrisk/config.py).

## Layout
```
src/scrisk/   config.py  synthetic.py  scoring.py  rules.py  simulation.py  validation.py  pipeline.py
scripts/      run_pipeline.py
notebooks/    01_run_pipeline.ipynb
data/         raw/  processed/scored_items.csv
tests/        weights, bounds, tier boundaries, rules, reproducibility
docs/         assumptions.md  data_dictionary.md
tableau/      dashboard.twbx  dashboard.png
report/
```

## Run it
```bash
pip install -e ".[dev]"
python scripts/run_pipeline.py        # rescores data/raw, checks it against the published CSV
pytest -q
```
`data/processed/scored_items.csv` is the published file the dashboard uses. The pipeline rescores `data/raw` into `scored_items_rebuilt.csv` and confirms that every column matches, apart from `sim_disruption_rate`, which is regenerated from a fitted simulation and matches only statistically (see `docs/assumptions.md`).

## Headline results (n = 300)
Low 52, Moderate 133, Elevated 84, High 31 | early warning 36 | review queue 55 | Act now 25

## Data and limitations
- The data is **synthetic** (see `docs/assumptions.md`), so results are illustrative and not evidence about real firms.
- Weights are expert priors, not estimated.
- Outcomes used for validation are simulated, and thresholds were tuned on the same data. Treat validation as in-sample.

## Citation
See `LICENSE` (MIT). Cite as: _Critical Supply-Chain Risk Early-Warning Framework_, v1.0.
