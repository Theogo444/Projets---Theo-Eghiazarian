# SRT Structuring Tool 🏦

An interactive Streamlit application for structuring **Significant Risk Transfer (SRT)** transactions on loan portfolios — built as a portfolio project demonstrating quantitative finance and Python development skills.

---

## What is SRT?

Synthetic securitisation (SRT) allows a bank to transfer credit risk on a reference portfolio to investors via Credit-Linked Notes or guarantees. For example, on a €1bn portfolio, the bank sells protection on the first €100m of losses to an investor, who receives a high coupon in exchange. The bank benefits from regulatory capital relief under CRR3/Basel IV.

---

## Features

### 📂 Module 1 — Reference Portfolio
- Upload a real CSV portfolio or generate a realistic synthetic one (lognormal notionals, rating-calibrated PDs, beta-distributed LGDs)
- Interactive filters: sector, country, rating, PD cap, minimum notional
- Key metrics: total notional, EL, weighted average PD/LGD/maturity, RWA, HHI concentration index
- Visualisations: notional & EL distributions, sector/rating concentration, PD×LGD risk map

### ⚙️ Module 2 — Tranche Structuring
- Interactive attachment/detachment point sliders
- Real-time calculation: tranche thickness, protected notional, subordination, EL in tranche, investor coupon
- Waterfall chart of portfolio decomposition with EL line
- Coupon sensitivity to spread

### 📊 Module 3 — Monte Carlo Simulation
- **Vasicek single-factor model**: systematic factor Z + idiosyncratic shocks ε per loan
- Vectorised NumPy implementation (no Python loops) — 100k simulations in seconds
- Portfolio-level metrics: EL, std, VaR 99%, Expected Shortfall 99%
- Tranche-level metrics: EL in tranche, VaR, probability of being hit
- Loss distribution with tranche zone highlighted

### 📋 Module 4 — Regulatory Capital (CRR3)
- **IRB Foundation** formula per loan: regulatory correlation R, maturity adjustment MA, conditional PD at 99.9th percentile
- **SEC-IRBA** (CRR3 Art. 263): analytical tranche capital density
- **SEC-SA** (CRR3 Art. 261): standardised approach alternative
- Capital waterfall: RWA before/after protection, CET1 relief
- Side-by-side comparison SEC-IRBA vs SEC-SA

### 📈 Module 5 — Dynamic Projection
- Year-by-year portfolio evolution: amortisation + cumulative defaults
- Tranche erosion mechanics: losses eat through first-loss then the sold tranche
- Investor cashflows: declining annual coupon on remaining tranche notional
- Reinvestment option (constant portfolio size)
- Downloadable cashflow table (CSV)

### 🔥 Module 6 — Stress Tests
- 4 scenarios: Central / Moderate Recession / Severe Recession / Systemic Crisis
- Per-scenario shocks on PD (multiplier), LGD (multiplier), and correlation ρ
- Comparative table: EL, VaR 99%, ES 99%, tranche EL, probability of loss
- Overlaid loss distributions across all scenarios
- Tranche impact chart per scenario

---

## Tech Stack

| Component | Library |
|-----------|---------|
| Web app | `streamlit` |
| Numerical computation | `numpy`, `scipy` |
| Data manipulation | `pandas` |
| Visualisation | `plotly` |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Theogo444/Portfolio---Theo-Eghiazarian.git
cd Portfolio---Theo-Eghiazarian/streamlit_credit-portfolio

# Install dependencies
pip install streamlit plotly pandas numpy scipy

# Run the app
streamlit run srt_app_complet.py
```

---

## Usage

1. **Generate or upload a portfolio** using the sidebar (CSV format or synthetic generation)
2. **Set tranche parameters** in Module 2 (attachment/detachment points, spread)
3. **Run Monte Carlo** in Module 3 to get the loss distribution
4. **Compute regulatory capital** relief in Module 4
5. **Project cashflows** over time in Module 5
6. **Stress test** the transaction in Module 6

### CSV Format

If uploading your own portfolio, the file must contain these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `notionnel_m` | Loan notional (€m) | `25.0` |
| `pd` | Probability of default | `0.003` |
| `lgd` | Loss given default | `0.45` |
| `maturite` | Remaining maturity (years) | `3.5` |

Optional columns: `loan_id`, `secteur`, `pays`, `notation`

---

## Key Models

**Vasicek Single-Factor Model**

Each loan has a latent credit variable:
$$X_i = \sqrt{\rho} \cdot Z + \sqrt{1-\rho} \cdot \varepsilon_i$$

Loan $i$ defaults when $X_i < \Phi^{-1}(PD_i)$, where $Z$ is the common economic factor and $\varepsilon_i$ is the idiosyncratic shock.

**SEC-IRBA Tranche Capital (CRR3 Art. 263)**

$$D(A, D) = \frac{e^{-aL} - e^{-aU}}{a(U-L)} \times 12.5 \quad \text{where } a = \frac{1}{p \cdot K_{IRB}}$$

---

## Project Context

Built as part of a quantitative finance internship preparation, demonstrating skills relevant to:
- Credit structuring desks (SRT, CLO, ABS)
- Regulatory capital optimisation
- Quantitative risk modelling

---

## Author

**Théo Eghiazarian** — M2 Financial Engineering  
[GitHub](https://github.com/Theogo444) · [LinkedIn](#)
