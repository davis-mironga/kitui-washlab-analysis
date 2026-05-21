# IoT Pilot Site Scoring Framework

**Source:** WASHLAB IoT Pilot Scoring Framework
**Total points:** 100
**Points available from existing data:** 45
**Points requiring field assessment:** 55

---

## Priority Thresholds

| Threshold | Score | Description |
|-----------|-------|-------------|
| First Priority | 80+ / 100 | Recommended for IoT pilot inclusion |
| Second Priority Shortlist | 65–79 / 100 | Considered if First Priority pool insufficient |
| Conditional | Below 65 | Requires significant additional justification |

No borehole can reach First Priority threshold without a strong field assessment score.
The 55 field-assessed points are not optional — they determine the final shortlist.

---

## The 9 Criteria

### Criteria 1–3: Scoreable from existing data (45 pts total)

---

#### 1. Population Served — 20 points

**Data source:** Population served column in borehole dataset
**Coverage:** Confirm against current dataset before running Notebook 05

| Score | Condition |
|-------|-----------|
| 20 | Tier 1 threshold met (highest population) |
| 15 | Tier 2 |
| 10 | Tier 3 |
| 5  | Tier 4 |
| 2  | Tier 5 (lowest non-zero) |
| 0  | No population data or zero |

```python
# Scoring function (thresholds from Parameters sheet)
def score_population(hhs, params):
    if pd.isna(hhs) or hhs == 0:
        return params['Pop_Zero_Score']
    elif hhs >= params['Pop_Tier1_Min']:
        return params['Pop_Tier1_Score']
    elif hhs >= params['Pop_Tier2_Min']:
        return params['Pop_Tier2_Score']
    # ... etc
```

---

#### 2. Reliable Yield — 15 points

**Data source:** Yield column in borehole dataset
**Coverage:** Confirm against current dataset before running Notebook 05
**Key threshold:** >2.5 m³/hr

| Score | Condition |
|-------|-----------|
| 15 | Highest yield tier |
| 10 | Mid tier |
| 5  | Low but usable |
| 0  | Below minimum or no data |

---

#### 3. Borehole Ownership — 10 points

**Data source:** Management type column in borehole dataset
**Note:** If the project enables WSP registration of community-managed boreholes, reverse scoring applies per framework rules.

| Score | Management Type |
|-------|----------------|
| 10 | Kitwasco / Kimwasco (WSP managed) |
| 8  | Project Maji / FundiFix (professional NGO) |
| 5  | Community (with active WUA) |
| 3  | School / Institution |
| 1  | Private |
| 0  | Unknown |

---

### Criteria 4–9: Require field assessment (55 pts total)

---

#### 4. Additionality Strength — 20 points

**Data source:** Field assessment — **not available in any current dataset**
**Question:** Would safe water and sustainable O&M continue without this project?

Assesses:
- Current tariff income vs O&M costs
- Funded repair or rehabilitation plans
- Water quality intervention status
- Evidence of O&M sustainability without external support

A field sampling protocol should be developed and tested on a representative set of boreholes before the full field campaign begins.

| Score | Condition |
|-------|-----------|
| 20 | No alternative funding path; project is essential for sustainability |
| 15 | Weak alternative; project significantly improves outcomes |
| 10 | Some alternative exists but uncertain |
| 5  | Strong alternative; project is incremental |
| 0  | Fully self-sustaining; project not needed |

---

#### 5. Safe-Water Potential — 10 points

**Data source:** Laboratory water quality tests — **not available**

| Score | Condition |
|-------|-----------|
| 10 | Microbial risk only (no chemical or physical contamination) |
| 7  | Minor treatable chemical issues |
| 4  | Significant treatment required |
| 0  | High salinity, fluoride, or other major contaminants |

---

#### 6. Rehabilitation Cost — 10 points

**Applies to:** Non-functional boreholes only
**Data source:** Engineering site assessment — **not available**

| Score | Condition |
|-------|-----------|
| 10 | Low rehabilitation cost |
| 5  | Medium cost |
| 0  | High cost or not feasible |

---

#### 7. Viable Drinking Water Use — 5 points

**Data source:** Field verification — **not available**

| Score | Condition |
|-------|-----------|
| 5 | Confirmed suitable or easily treatable for drinking |
| 3 | Requires treatment but viable |
| 0 | Not suitable for drinking water use |

---

#### 8. IoT Viability — 5 points

**Data source:** On-site survey — **not available**

Assesses:
- Physical condition of borehole casing
- Space for panel mounting
- Mobile network connectivity (for data transmission)
- Power supply options

| Score | Condition |
|-------|-----------|
| 5 | Fully suitable for IoT installation |
| 3 | Suitable with minor modifications |
| 0 | Not suitable |

---

#### 9. Energy Compliance — 20 points

**Data source:** Field verification — **not available**
**Note:** This is the single largest unscored criterion (20 pts). Solarisation data is absent from all current datasets. Until field verification is available, use management type (Kitwasco or professional management) as an interim proxy and flag this assumption clearly in all outputs.

| Score | Energy source |
|-------|--------------|
| 20 | Solar (standalone) |
| 15 | Solar-hybrid |
| 8  | Grid connected |
| 3  | Diesel / generator |
| 0  | Unknown |

---

## Implementation in Notebook 05

```python
def score_borehole(row, params, field_data=None):
    """
    Score a borehole on the 100-point framework.
    Returns score and breakdown dict.
    field_data: dict with field assessment results (None = not yet collected)
    """
    scores = {}

    # Criterion 1: Population Served (20 pts) — data available
    scores['population'] = score_population(row['Population_Served_HHs'], params)

    # Criterion 2: Reliable Yield (15 pts) — data available
    scores['yield'] = score_yield(row['Yield_m3_hr'], params)

    # Criterion 3: Borehole Ownership (10 pts) — data available
    scores['ownership'] = score_ownership(row['Management_Type'], params)

    # Criteria 4–9: Field assessment required
    if field_data:
        scores['additionality']     = field_data.get('additionality', None)
        scores['water_quality']     = field_data.get('water_quality', None)
        scores['rehab_cost']        = field_data.get('rehab_cost', None)
        scores['drinking_water']    = field_data.get('drinking_water', None)
        scores['iot_viability']     = field_data.get('iot_viability', None)
        scores['energy_compliance'] = field_data.get('energy_compliance', None)
    else:
        # Mark as pending
        for key in ['additionality','water_quality','rehab_cost',
                    'drinking_water','iot_viability','energy_compliance']:
            scores[key] = None

    total = sum(v for v in scores.values() if v is not None)
    max_possible = 45 + sum(
        [20, 10, 10, 5, 5, 20][i]
        for i, v in enumerate(
            [scores['additionality'], scores['water_quality'], scores['rehab_cost'],
             scores['drinking_water'], scores['iot_viability'], scores['energy_compliance']]
        ) if v is not None
    )

    return {
        'total_score': total,
        'max_available': max_possible,
        'pct_of_available': round(total / max_possible * 100, 1) if max_possible > 0 else 0,
        'field_complete': all(v is not None for v in [
            scores['additionality'], scores['water_quality'], scores['rehab_cost'],
            scores['drinking_water'], scores['iot_viability'], scores['energy_compliance']
        ]),
        'breakdown': scores,
    }
```
