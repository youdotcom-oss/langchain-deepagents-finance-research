# EU-27 Real GDP Growth — Anomaly Analysis (2025)
**Prepared:** 21 May 2026  
**Analyst:** Quantitative Anomaly Detection  
**Source data:** `/workpapers/landscape_scan.md` (Eurostat `nama_10_gdp`, vintage 2026-05-20)  
**Scope:** All 27 EU member states, 2025 real GDP growth (chain-linked volumes, % change on previous year)

---

## 1. Summary Statistics

| Statistic | Value |
|---|---:|
| **Simple (unweighted) mean** | **2.163%** |
| **Median** | **1.800%** |
| **Population std dev (σ, n=27)** | **2.314 pp** |
| **Sample std dev (s, n−1=26)** | **2.358 pp** |
| **Min** | 0.2% (Finland, Germany) |
| **Max** | 12.3% (Ireland) |
| **Range** | 12.1 pp |

> **Methodology note:** The mean-vs-median gap (2.163 vs 1.800, a spread of 0.363 pp) signals a right-skewed distribution driven almost entirely by Ireland's MNC-distorted headline figure. The standard deviation is itself inflated by the same outlier; σ without Ireland drops to approximately **1.17 pp**. All thresholds below are applied against the full-sample mean of **2.163%** as stated in the analysis mandate.

### Computation Workings

**2025 GDP growth rates used (all 27 member states):**

| Country | 2025 (%) |
|---|---:|
| Austria | 0.6 |
| Belgium | 1.0 |
| Bulgaria | 3.1 |
| Croatia | 3.4 |
| Cyprus | 3.8 |
| Czech Republic | 2.6 |
| Denmark | 2.9 |
| Estonia | 0.6 |
| Finland | 0.2 |
| France | 0.8 |
| Germany | 0.2 |
| Greece | 2.1 |
| Hungary | 0.5 |
| Ireland | 12.3 |
| Italy | 0.5 |
| Latvia | 2.1 |
| Lithuania | 2.9 |
| Luxembourg | 0.6 |
| Malta | 4.0 |
| Netherlands | 1.8 |
| Poland | 3.6 |
| Portugal | 1.9 |
| Romania | 0.7 |
| Slovakia | 0.8 |
| Slovenia | 1.1 |
| Spain | 2.8 |
| Sweden | 1.5 |

**Sum = 58.4** | **N = 27** | **Mean = 58.4 ÷ 27 = 2.1630% (rounded to 2.163%)**

**Sorted for median (position 14 of 27):**  
0.2, 0.2, 0.5, 0.5, 0.6, 0.6, 0.6, 0.7, 0.8, 0.8, 1.0, 1.1, 1.5, **1.8**, 1.9, 2.1, 2.1, 2.6, 2.8, 2.9, 2.9, 3.1, 3.4, 3.6, 3.8, 4.0, 12.3  
→ **Median = 1.8% (Netherlands)**

**Sum of squared deviations from mean = 144.524**  
**Population variance = 144.524 ÷ 27 = 5.353** | **σ = √5.353 = 2.314 pp**  
**Sample variance = 144.524 ÷ 26 = 5.559** | **s = √5.559 = 2.358 pp**

---

## 2. Full Country Rankings — 2025 GDP Growth with Deviations

Sorted descending by 2025 growth rate. Anomaly flags applied at ≥2.0 pp deviation from mean (2.163%). Borderline flags at ≥1.5 pp and <2.0 pp deviation.

| Rank | Country | 2025 (%) | Deviation from Mean (pp) | Flag |
|---:|---|---:|---:|---|
| 1 | **Ireland** | 12.3 | **+10.14** | 🔴 HIGH ANOMALY |
| 2 | Malta | 4.0 | +1.84 | 🟡 BORDERLINE HIGH |
| 3 | Cyprus | 3.8 | +1.64 | 🟡 BORDERLINE HIGH |
| 4 | Poland | 3.6 | +1.44 | — |
| 5 | Croatia | 3.4 | +1.24 | — |
| 6 | Bulgaria | 3.1 | +0.94 | — |
| 7 | Denmark | 2.9 | +0.74 | — |
| 8 | Lithuania | 2.9 | +0.74 | — |
| 9 | Spain | 2.8 | +0.64 | — |
| 10 | Czech Republic | 2.6 | +0.44 | — |
| 11 | Greece | 2.1 | −0.06 | — |
| 12 | Latvia | 2.1 | −0.06 | — |
| 13 | Portugal | 1.9 | −0.26 | — |
| 14 | Netherlands | 1.8 | −0.36 | — |
| 15 | Sweden | 1.5 | −0.66 | — |
| 16 | Slovenia | 1.1 | −1.06 | — |
| 17 | Belgium | 1.0 | −1.16 | — |
| 18 | Slovakia | 0.8 | −1.36 | — |
| 19 | France | 0.8 | −1.36 | — |
| 20 | Romania | 0.7 | −1.46 | — |
| 21 | Austria | 0.6 | −1.56 | 🟡 BORDERLINE LOW |
| 22 | Estonia | 0.6 | −1.56 | 🟡 BORDERLINE LOW |
| 23 | Luxembourg | 0.6 | −1.56 | 🟡 BORDERLINE LOW |
| 24 | Hungary | 0.5 | −1.66 | 🟡 BORDERLINE LOW |
| 25 | Italy | 0.5 | −1.66 | 🟡 BORDERLINE LOW |
| 26 | Finland | 0.2 | −1.96 | 🟡 BORDERLINE LOW |
| 27 | Germany | 0.2 | −1.96 | 🟡 BORDERLINE LOW |

> **Threshold note:** No country other than Ireland clears the ≥2.0 pp threshold in either direction. However, Finland (−1.96 pp) and Germany (−1.96 pp) sit only **0.04 pp** below the formal anomaly threshold and are treated as high-priority borderline cases. Malta (+1.84 pp) is the closest borderline on the high side.

---

## 3. Anomaly and Borderline Flag Details

### 3.1 Formal Anomaly (≥2.0 pp deviation)

#### 🔴 IRELAND — HIGH-GROWTH ANOMALY
| Metric | Value |
|---|---|
| 2025 GDP growth | +12.3% |
| Deviation from mean | **+10.14 pp** |
| Direction | High |

**Multi-year pattern (2021–2025):**

| Year | GDP Growth |
|---:|---:|
| 2021 | +16.3% |
| 2022 | +7.5% |
| 2023 | −2.5% |
| 2024 | +2.6% |
| 2025 | +12.3% |

**Pattern assessment:** Ireland exhibits extreme volatility that is structurally disconnected from domestic economic conditions. The 2021 spike (+16.3%) was driven by a large-scale intellectual property (IP) transfer by multinationals into Irish domiciled entities. The 2023 contraction (−2.5%) and subsequent 2025 surge (+12.3%) are consistent with another round of MNC balance-sheet restructuring — likely contract manufacturing reclassifications or further IP flows — rather than genuine domestic expansion. The gap between headline GDP and Modified GNI (GNI*) is the tell: Irish personal consumption, investment ex-MNC, and labour market data do not remotely corroborate +12.3% aggregate growth. The Eurostat source data footnote in the landscape scan explicitly flags this distortion.

**Investigation priority:** HIGH — but the investigation should focus on *decomposing* the MNC statistical effect (IP transfers, contract manufacturing) rather than treating the figure as a genuine economic signal.

---

### 3.2 Borderline Cases (1.5 pp ≤ deviation < 2.0 pp)

#### 🟡 GERMANY — BORDERLINE LOW (deviation: −1.96 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +0.2% |
| Deviation from mean | −1.96 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +3.9% |
| 2022 | +1.8% |
| 2023 | −0.9% |
| 2024 | −0.5% |
| 2025 | +0.2% |

**Pattern assessment:** Germany shows a clear and persistent stagnation trajectory — the only EU27 member state (alongside Austria) to record back-to-back contractions in 2023–2024 followed by near-zero growth in 2025. The pattern reflects structural headwinds: energy-intensive manufacturing exposed to high post-2022 energy costs, weak export demand from China, automotive sector transition pressures, and chronic infrastructure underinvestment. Three consecutive years of sub-zero or near-zero growth (2023: −0.9%, 2024: −0.5%, 2025: +0.2%) constitute the weakest sustained growth period for Germany since reunification outside of the 2008–09 and 2020 shocks. The borderline classification is close enough to formal anomaly status (gap of 0.04 pp) that it warrants full investigation.

**Investigation priority:** HIGH

---

#### 🟡 FINLAND — BORDERLINE LOW (deviation: −1.96 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +0.2% |
| Deviation from mean | −1.96 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +2.7% |
| 2022 | +0.8% |
| 2023 | −1.3% |
| 2024 | +0.4% |
| 2025 | +0.2% |

**Pattern assessment:** Finland's trajectory echoes Germany's but has an additional dimension: deep exposure to Russian trade and energy links that were severed after February 2022, a pulp/paper and forestry sector under competitive stress, and a technology sector that has not replicated the Nokia-era dynamism. Finland contracted in 2023 (−1.3%), recovered marginally in 2024 (+0.4%), and has stalled again at +0.2% in 2025. The near-stagnation 2022–2025 average of ~0.025%/year marks a prolonged growth deficit against the EU mean.

**Investigation priority:** HIGH

---

#### 🟡 ITALY — BORDERLINE LOW (deviation: −1.66 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +0.5% |
| Deviation from mean | −1.66 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +8.9% |
| 2022 | +4.8% |
| 2023 | +0.9% |
| 2024 | +0.8% |
| 2025 | +0.5% |

**Pattern assessment:** Italy displays a classic post-bounce deceleration: a large post-COVID rebound in 2021 (+8.9%) followed by a relentless downward glide to near-stagnation by 2025 (+0.5%). The three-year trend from 2023–2025 (0.9%, 0.8%, 0.5%) is consistently below the EU mean and decelerating, suggesting structural rather than cyclical drag. Debt sustainability concerns (public debt >135% GDP), weak productivity growth, ageing demographics, and reliance on NRRP transfers that may be tapering all contribute. This is a slow-burn stagnation story rather than a shock anomaly, but the persistence makes it important.

**Investigation priority:** MEDIUM-HIGH

---

#### 🟡 HUNGARY — BORDERLINE LOW (deviation: −1.66 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +0.5% |
| Deviation from mean | −1.66 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +7.2% |
| 2022 | +4.2% |
| 2023 | −0.8% |
| 2024 | +0.7% |
| 2025 | +0.5% |

**Pattern assessment:** Hungary contracted in 2023 and has bounced only weakly since. The pattern — strong post-COVID rebound, contraction, tepid recovery — is consistent with a manufacturing-dependent economy facing German industrial weakness (Hungary is deeply embedded in German automotive supply chains), elevated inflation (HICP 4.4% in 2025), and tightening EU fund disbursements due to rule-of-law conditionality. The combination of below-average growth and above-average inflation (stagflationary configuration) distinguishes Hungary from peers.

**Investigation priority:** MEDIUM

---

#### 🟡 AUSTRIA — BORDERLINE LOW (deviation: −1.56 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +0.6% |
| Deviation from mean | −1.56 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +4.9% |
| 2022 | +5.3% |
| 2023 | −0.8% |
| 2024 | −0.7% |
| 2025 | +0.6% |

**Pattern assessment:** Austria is the only EU27 country besides Germany to post back-to-back contractions in 2023–2024. The recovery to +0.6% in 2025 is the weakest positive print in the post-COVID period and barely above zero. Austria shares Germany's structural vulnerabilities (energy-intensive manufacturing, exposure to the automotive transition, high real wages) and is closely coupled to the German business cycle. The three-year stagnation (−0.8%, −0.7%, +0.6%) warrants attention as a secondary indicator of the Central European manufacturing bloc's underperformance.

**Investigation priority:** MEDIUM (secondary to Germany analysis — the two are co-determined)

---

#### 🟡 ESTONIA — BORDERLINE LOW (deviation: −1.56 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +0.6% |
| Deviation from mean | −1.56 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +8.3% |
| 2022 | −1.2% |
| 2023 | −2.7% |
| 2024 | −0.1% |
| 2025 | +0.6% |

**Pattern assessment:** Estonia experienced the sharpest and most prolonged contraction cycle among the Baltic states: contraction in 2022 (−1.2%), deeper contraction in 2023 (−2.7%), near-zero in 2024 (−0.1%), and only just positive in 2025 (+0.6%). The cumulative growth from 2022–2025 is approximately −3.4%, meaning Estonia has not recovered its pre-2022 GDP level. This is the worst multi-year growth trajectory in the EU27 over this period (excluding the artificial Irish swings). Drivers include the sharp trade/energy shock from Russia's invasion of Ukraine (Estonia was highly exposed), high inflation (HICP 4.8% in 2025, highest in the EU), and weak external demand. Despite the near-recovery in 2025, the multi-year hole remains unrepaired.

**Investigation priority:** HIGH (multi-year cumulative contraction is distinctive)

---

#### 🟡 LUXEMBOURG — BORDERLINE LOW (deviation: −1.56 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +0.6% |
| Deviation from mean | −1.56 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +6.9% |
| 2022 | −1.1% |
| 2023 | +0.1% |
| 2024 | +0.4% |
| 2025 | +0.6% |

**Pattern assessment:** Luxembourg contracted in 2022 (−1.1%) and has been limping along near zero ever since (0.1%, 0.4%, 0.6%). Its outsized financial services sector is sensitive to global interest rate cycles; the post-2022 high-rate environment compressed asset valuations, fund inflows, and fee revenues. The 2025 tick-up is consistent with easing rate expectations, but cumulative 2022–2025 growth of only ~0.0% for what is nominally one of the EU's most prosperous economies is notable. Luxembourg also merits scrutiny as a MNC-hosting economy where headline GDP may not fully capture domestic activity.

**Investigation priority:** MEDIUM

---

#### 🟡 MALTA — BORDERLINE HIGH (deviation: +1.84 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +4.0% |
| Deviation from mean | +1.84 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +13.4% |
| 2022 | +2.6% |
| 2023 | +10.6% |
| 2024 | +6.2% |
| 2025 | +4.0% |

**Pattern assessment:** Malta is the EU's most consistently above-average performer in recent years, with the sole exception of 2022. The 2023 print of +10.6% (the highest in the EU that year) and continued above-average growth in 2024–2025 suggest structural rather than cyclical drivers. Malta's small open economy is driven by tourism, iGaming and financial services, and strong net migration expanding the labour force and consumer base. The volatility (2021: +13.4%, 2022: +2.6%, 2023: +10.6%) points to concentration risk and sensitivity to global travel/services flows. The 2025 reading of +4.0% is a deceleration from the 2023–2024 highs but still nearly 2 pp above the EU mean.

**Investigation priority:** MEDIUM (positive anomaly with clear mechanism, but concentration risk warrants monitoring)

---

#### 🟡 CYPRUS — BORDERLINE HIGH (deviation: +1.64 pp)
| Metric | Value |
|---|---|
| 2025 GDP growth | +3.8% |
| Deviation from mean | +1.64 pp |

**Multi-year pattern:**

| Year | GDP Growth |
|---:|---:|
| 2021 | +11.4% |
| 2022 | +8.7% |
| 2023 | +3.6% |
| 2024 | +3.9% |
| 2025 | +3.8% |

**Pattern assessment:** Cyprus has decelerated from the spectacular post-COVID rebounds of 2021–2022 to a stable ~3.7–3.9% growth corridor in 2023–2025. Unlike Malta, this represents a gentle normalisation rather than volatility. The sustained above-average growth reflects tourism recovery, financial services, and the influx of Russian and Ukrainian relocations post-2022 (providing labour supply and demand). The current account deficit (−6.4% GDP in 2025) and the lowest inflation in the EU (HICP 0.8%) co-existing with solid growth is an interesting configuration — low inflation despite strong growth may reflect terms-of-trade effects or subdued domestic wage dynamics.

**Investigation priority:** MEDIUM (positive growth story but current account deficit warrants monitoring)

---

## 4. Mechanism Groupings

### Group A: MNC-Distorted Economies (statistical artefact)
| Country | 2025 | Deviation | Notes |
|---|---:|---:|---|
| Ireland | +12.3% | +10.14 pp | IP transfers / contract manufacturing reclassification |
| Luxembourg | +0.6% | −1.56 pp | Financial sector sensitivity; MNC hosting |

**Shared mechanism:** Headline GDP figures are substantially detached from domestic economic conditions due to the statistical footprint of multinational corporations. Ireland's distortion is acute and directional (high); Luxembourg's may reflect the reverse — financial sector contraction dragging measured GDP below underlying domestic activity.

---

### Group B: Manufacturing-Exposed / German-Cycle Economies (persistent stagnation)
| Country | 2025 | Deviation | Notes |
|---|---:|---:|---|
| Germany | +0.2% | −1.96 pp | Energy-intensive manufacturing, automotive transition, China exposure |
| Austria | +0.6% | −1.56 pp | Tightly coupled to German industrial cycle |
| Hungary | +0.5% | −1.66 pp | German automotive supply chain, EU fund pressures |

**Shared mechanism:** Deep integration into Germany's industrial supply chain means that Germany's structural slowdown propagates directly to its CEE and Alpine neighbours. All three show 2023 contractions or near-contractions and weak recoveries through 2025. The automotive transition (internal combustion to EV) is restructuring demand for the manufactured goods these economies produce.

---

### Group C: Baltic/Northern Trade-Shock Economies (cumulative contraction)
| Country | 2025 | Deviation | Notes |
|---|---:|---:|---|
| Estonia | +0.6% | −1.56 pp | Deepest Baltic contraction cycle; Russia trade/energy shock |
| Finland | +0.2% | −1.96 pp | Russian trade severance; pulp/paper sector stress; tech stagnation |

**Shared mechanism:** Both economies suffered disproportionate exposure to the Russia-Ukraine shock. Finland's land border with Russia and deep historical trade ties, combined with Estonia's role as a transit and trade hub, amplified the initial shock. High inflation (Estonia HICP 4.8% in 2025) further crimped real purchasing power, weighing on domestic demand. Multi-year cumulative growth since 2022 is deeply negative for both.

---

### Group D: Tourism / Services-Driven Small Open Economies (above-average growth)
| Country | 2025 | Deviation | Notes |
|---|---:|---:|---|
| Malta | +4.0% | +1.84 pp | Tourism, iGaming, migration-driven demand |
| Cyprus | +3.8% | +1.64 pp | Tourism, financial services, Russian/Ukrainian diasporas |
| Croatia | +3.4% | +1.24 pp | Tourism recovery, EU convergence dynamic |

**Shared mechanism:** Small Mediterranean/island economies with high tourism multipliers and services-oriented GDP. The post-COVID normalisation of international travel has sustained growth well above the EU mean. Growth is structurally above average but also concentrated and therefore fragile to demand shocks.

---

### Group E: CEE Convergence Economies (near-average to above-average)
| Country | 2025 | Deviation | Notes |
|---|---:|---:|---|
| Poland | +3.6% | +1.44 pp | Domestic demand resilience, EU fund absorption |
| Bulgaria | +3.1% | +0.94 pp | Convergence dynamic, services growth |
| Czech Rep | +2.6% | +0.44 pp | Recovery from 2022–2023 weakness |

**Shared mechanism:** CEE economies benefiting from EU convergence transfers, wage-driven domestic consumption, and partial insulation from the German industrial slowdown (Poland in particular has diversified beyond manufacturing). Not anomalous, but Poland's strong performance alongside Germany's weakness is a structural divergence worth noting.

---

## 5. Investigation Recommendations

### Priority Matrix

| Country | Deviation | Multi-year Pattern | Mechanism Clarity | Investigation Priority |
|---|---|---|---|---|
| **Ireland** | +10.14 pp (ANOMALY) | Extreme volatility; MNC-driven swings | MNC statistical artefact | **HIGH** |
| **Germany** | −1.96 pp (borderline) | 3-year stagnation; deepening structural drag | Manufacturing/energy/automotive | **HIGH** |
| **Finland** | −1.96 pp (borderline) | Prolonged contraction + weak recovery | Russia shock + structural weakness | **HIGH** |
| **Estonia** | −1.56 pp (borderline) | Worst cumulative 2022–2025 trajectory in EU | Russia shock; inflation erosion | **HIGH** |
| **Italy** | −1.66 pp (borderline) | Consistent deceleration 2021→2025 | Structural stagnation; debt drag | **MEDIUM-HIGH** |
| Malta | +1.84 pp (borderline) | Volatile high-performer; concentration risk | Tourism/iGaming/migration | **MEDIUM** |
| Hungary | −1.66 pp (borderline) | Contraction + stagflationary configuration | German supply chain; EU funds | **MEDIUM** |
| Cyprus | +1.64 pp (borderline) | Stable outperformer; CA deficit rising | Tourism/diaspora-driven | **MEDIUM** |

---

### Top 4 Recommended Deep-Dive Investigations (Shape B)

#### 1. 🔴 Ireland — "The MNC Mirage"
**Why investigate:** The +12.3% headline figure is the single largest deviation from the EU mean (+10.14 pp) and is almost certainly a statistical artefact. However, the *type* of artefact matters: which MNC activity drove the 2025 surge (IP transfer? Contract manufacturing re-booking? Pharma sector reclassification?)? The investigation should decompose the GDP figure using GNI* data, sectoral national accounts, and corporate tax receipts to determine the size and nature of the MNC effect, and isolate underlying Irish domestic growth (likely in the +2.5–3.5% range). Without this decomposition, Irish data contaminates EU-wide aggregates.

**Shape B focus:** Sectoral GDP decomposition; comparison of headline GDP vs GNI* vs domestic demand; identification of the specific MNC transaction type.

---

#### 2. 🟡 Germany — "The Industrial Patient"
**Why investigate:** At −1.96 pp deviation, Germany narrowly misses the formal 2.0 pp threshold but is the EU's largest economy (accounting for ~25% of EU GDP). Three consecutive years of near-stagnation or contraction represent a structural break. The investigation should examine whether the slowdown is cyclical (reversible with ECB rate cuts and China recovery) or structural (permanent loss of energy-intensive industrial competitiveness, automotive transition drag, demographic contraction of labour supply). The answer has systemic implications for the entire EU, particularly Group B economies (Austria, Hungary) that are tightly coupled to German industrial output.

**Shape B focus:** Industrial production decomposition; energy cost pass-through; automotive sector transition exposure; comparison with German GNI and domestic demand vs export contribution.

---

#### 3. 🟡 Estonia — "The Baltic Attrition"
**Why investigate:** Estonia's cumulative GDP trajectory from 2022–2025 is the worst in the EU27 excluding artificial Irish swings: −1.2% (2022), −2.7% (2023), −0.1% (2024), +0.6% (2025) — a net cumulative decline of approximately −3.4% over four years. No other EU economy has absorbed a multi-year contraction of this magnitude in the post-GFC period outside of crisis conditions. Simultaneously, HICP inflation of 4.8% in 2025 (highest in the EU) means real living standards are being doubly compressed. The investigation should assess whether the 2025 stabilisation marks genuine recovery or a temporary pause before further deterioration.

**Shape B focus:** Cumulative output gap quantification; real wage dynamics vs inflation; Russia-severance trade channel impact; comparison with Latvia and Lithuania (who recovered earlier).

---

#### 4. 🟡 Finland — "The Nordic Laggard"
**Why investigate:** Finland's near-zero growth (+0.2%) in 2025 following a contraction year (−1.3% in 2023) places it in a distinct cohort of persistently weak Nordic/Northern economies. Unlike Sweden (+1.5%) or Denmark (+2.9%), Finland has failed to participate in the Northern European recovery trend. The Russia severance, forestry/paper sector decline, and absence of a tech sector rebound distinguish Finland's structural position. Critically, Finland shares the −1.96 pp borderline deviation with Germany — both sitting 0.04 pp from formal anomaly status — suggesting a cluster of northern/central stagnation that may warrant consolidated analysis.

**Shape B focus:** Sectoral contribution analysis (which sectors dragged 2025 growth?); Russia trade exposure quantification; comparison with Sweden and Denmark on divergence drivers; fiscal position and NRRP absorption rate.

---

## 6. Analytical Caveats

1. **Ireland's outlier effect on the mean:** The EU27 unweighted mean of 2.163% is elevated by Ireland's MNC-distorted +12.3% reading. The mean excluding Ireland is **1.695%**, which would materially change which countries are flagged as low-growth anomalies. Under the Ireland-excluded mean, **Germany and Finland** (at +0.2%) would both clear the 2.0 pp threshold formally (deviation: −1.495 pp against the lower mean — still borderline but closer). The investigation team should consider whether to weight or trim the mean.

2. **Unweighted mean vs GDP-weighted mean:** The unweighted simple mean used here treats Malta (GDP ~€20bn) identically to Germany (~€4,000bn). A GDP-weighted mean would be approximately **1.1–1.3%** (dominated by France, Germany, Italy, Spain — all weak performers), which would shift *more* countries to the high-growth flagged side and reduce low-growth flags. Both perspectives are analytically valid for different purposes.

3. **Chain-linked volume data and base-year effects:** Small, open economies with large service sectors (Ireland, Luxembourg, Malta) are more susceptible to measured GDP volatility that does not reflect genuine welfare changes.

4. **2025 data vintage:** Eurostat vintage is 2026-05-20. For several member states, 2025 annual data may still be a first release estimate subject to revision.

---

## 7. Machine-Readable Summary

```json
{
  "eu27_mean_gdp_growth_2025": 2.163,
  "eu27_median_gdp_growth_2025": 1.8,
  "std_dev": 2.314,
  "sample_std_dev": 2.358,
  "n_countries": 27,
  "sum_of_growth_rates": 58.4,
  "formal_anomalies_count": 1,
  "borderline_count": 9,
  "investigation_targets": [
    {
      "country": "Ireland",
      "gdp_growth_2025": 12.3,
      "deviation_from_mean": 10.137,
      "direction": "high",
      "priority": "high",
      "mechanism_group": "MNC-distorted economies",
      "multi_year_pattern": "extreme_volatility_mnc_driven",
      "note": "MNC IP transfer and contract manufacturing statistical artefact; GNI* diverges materially from GDP"
    },
    {
      "country": "Germany",
      "gdp_growth_2025": 0.2,
      "deviation_from_mean": -1.963,
      "direction": "low",
      "priority": "high",
      "mechanism_group": "Manufacturing-exposed German-cycle economies",
      "multi_year_pattern": "persistent_stagnation_2023_2025",
      "note": "Three consecutive years of near-zero or negative growth; structural manufacturing and energy headwinds; 0.04 pp below formal 2.0 pp threshold"
    },
    {
      "country": "Finland",
      "gdp_growth_2025": 0.2,
      "deviation_from_mean": -1.963,
      "direction": "low",
      "priority": "high",
      "mechanism_group": "Baltic-Northern trade-shock economies",
      "multi_year_pattern": "contraction_then_stalled_recovery",
      "note": "Russia trade severance; forestry/paper sector stress; 0.04 pp below formal 2.0 pp threshold"
    },
    {
      "country": "Estonia",
      "gdp_growth_2025": 0.6,
      "deviation_from_mean": -1.563,
      "direction": "low",
      "priority": "high",
      "mechanism_group": "Baltic-Northern trade-shock economies",
      "multi_year_pattern": "worst_cumulative_contraction_eu27_2022_2025",
      "note": "Cumulative ~-3.4% GDP 2022-2025; highest HICP in EU (4.8%); Russia shock worst-affected Baltic state"
    },
    {
      "country": "Italy",
      "gdp_growth_2025": 0.5,
      "deviation_from_mean": -1.663,
      "direction": "low",
      "priority": "medium",
      "mechanism_group": "Manufacturing-exposed stagnation",
      "multi_year_pattern": "relentless_deceleration_2021_2025",
      "note": "Post-COVID bounce fully unwound; 2023-2025 average ~0.7%; structural debt and productivity drag"
    },
    {
      "country": "Malta",
      "gdp_growth_2025": 4.0,
      "deviation_from_mean": 1.837,
      "direction": "high",
      "priority": "medium",
      "mechanism_group": "Tourism-services small open economies",
      "multi_year_pattern": "volatile_high_performer",
      "note": "Consistently above EU mean; tourism, iGaming, migration-driven demand; concentration risk"
    },
    {
      "country": "Hungary",
      "gdp_growth_2025": 0.5,
      "deviation_from_mean": -1.663,
      "direction": "low",
      "priority": "medium",
      "mechanism_group": "Manufacturing-exposed German-cycle economies",
      "multi_year_pattern": "contraction_2023_weak_recovery",
      "note": "German automotive supply chain exposure; HICP 4.4%; EU fund conditionality pressures; stagflationary configuration"
    },
    {
      "country": "Cyprus",
      "gdp_growth_2025": 3.8,
      "deviation_from_mean": 1.637,
      "direction": "high",
      "priority": "medium",
      "mechanism_group": "Tourism-services small open economies",
      "multi_year_pattern": "stable_outperformer_post_covid",
      "note": "Sustained ~3.7-3.9% growth 2023-2025; diaspora and tourism driven; CA deficit -6.4% GDP warrants monitoring"
    },
    {
      "country": "Austria",
      "gdp_growth_2025": 0.6,
      "deviation_from_mean": -1.563,
      "direction": "low",
      "priority": "medium",
      "mechanism_group": "Manufacturing-exposed German-cycle economies",
      "multi_year_pattern": "back_to_back_contractions_2023_2024_then_weak_recovery",
      "note": "Only EU country besides Germany with consecutive contractions; tightly coupled to German industrial cycle"
    }
  ]
}
```
