import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SRT Structuring Tool",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Background général */
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}

/* Titres */
h1 { font-family: 'IBM Plex Mono', monospace; color: #58a6ff; font-size: 1.6rem !important; }
h2 { font-family: 'IBM Plex Mono', monospace; color: #e6edf3; font-size: 1.2rem !important; }
h3 { font-family: 'IBM Plex Sans', sans-serif; color: #8b949e; font-size: 1rem !important; font-weight: 600; }

/* Métriques */
[data-testid="metric-container"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 16px;
}
[data-testid="metric-container"] label { color: #8b949e !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #58a6ff !important; font-family: 'IBM Plex Mono', monospace; font-size: 1.4rem !important; }

/* Cards */
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}
.card-accent {
    background: #161b22;
    border: 1px solid #58a6ff44;
    border-left: 3px solid #58a6ff;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}

/* Boutons */
.stButton > button {
    background: #58a6ff;
    color: #0d1117;
    border: none;
    border-radius: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 8px 20px;
    transition: background 0.2s;
}
.stButton > button:hover { background: #79b8ff; }

/* Sliders */
.stSlider > div > div > div { background: #58a6ff !important; }

/* Tables */
.stDataFrame { border: 1px solid #30363d; border-radius: 8px; }

/* Tags */
.tag {
    display: inline-block;
    background: #1f3c5c;
    color: #58a6ff;
    border: 1px solid #2d5a8e;
    border-radius: 4px;
    padding: 2px 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    margin-right: 6px;
}
.tag-green { background: #1a3a2a; color: #3fb950; border-color: #2ea043; }
.tag-orange { background: #3a2a1a; color: #d29922; border-color: #9e6a03; }
.tag-red { background: #3a1a1a; color: #f85149; border-color: #da3633; }

/* Section header */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid #30363d;
    margin-bottom: 20px;
}
.step-badge {
    background: #58a6ff;
    color: #0d1117;
    border-radius: 50%;
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.85rem;
    flex-shrink: 0;
}

/* Selectbox / radio */
.stSelectbox > div, .stRadio > div { color: #e6edf3; }

/* Upload zone */
[data-testid="stFileUploader"] {
    border: 1px dashed #30363d;
    border-radius: 8px;
    padding: 10px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #161b22; border-bottom: 1px solid #30363d; gap: 0; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #8b949e; border-bottom: 2px solid transparent; padding: 10px 20px; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; }
.stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; background: transparent !important; }

/* Divider */
hr { border-color: #30363d; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

SECTEURS = ["Corporate", "PME", "Immobilier Commercial", "Immobilier Résidentiel",
            "Infrastructure", "Leveraged Finance", "Trade Finance"]

NOTATIONS = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]

PD_PAR_NOTATION = {
    "AAA": 0.0002, "AA": 0.0005, "A": 0.001,
    "BBB": 0.003,  "BB": 0.015,  "B": 0.05, "CCC": 0.15
}

def generer_portefeuille(n_loans: int, seed: int = 42) -> pd.DataFrame:
    """Génère un portefeuille de loans fictif mais réaliste."""
    rng = np.random.default_rng(seed)
    
    notations = rng.choice(NOTATIONS, size=n_loans, p=[0.03, 0.07, 0.15, 0.30, 0.25, 0.15, 0.05])
    secteurs  = rng.choice(SECTEURS, size=n_loans,
                           p=[0.30, 0.20, 0.15, 0.15, 0.08, 0.07, 0.05])
    
    # Notionnel entre 1M€ et 50M€, lognormal
    notionnels = np.round(rng.lognormal(mean=np.log(10), sigma=0.8, size=n_loans), 2)
    notionnels = np.clip(notionnels, 1, 80)
    
    # PD selon notation + bruit
    pd_base = np.array([PD_PAR_NOTATION[n] for n in notations])
    pd_vals  = np.clip(pd_base * rng.lognormal(0, 0.2, size=n_loans), 0.0001, 0.40)
    
    # LGD entre 25% et 75%
    lgd_vals = np.clip(rng.beta(a=2, b=3, size=n_loans) * 0.6 + 0.2, 0.20, 0.75)
    
    # Maturité 1–7 ans
    maturites = np.round(rng.uniform(1, 7, size=n_loans), 1)
    
    # Pays
    pays = rng.choice(["France", "Allemagne", "Italie", "Espagne", "Benelux", "Autres EU"],
                      size=n_loans, p=[0.40, 0.20, 0.15, 0.12, 0.08, 0.05])
    
    df = pd.DataFrame({
        "loan_id":    [f"LOAN-{i+1:04d}" for i in range(n_loans)],
        "secteur":    secteurs,
        "pays":       pays,
        "notation":   notations,
        "notionnel_m": notionnels,          # en M€
        "pd":         np.round(pd_vals, 5),
        "lgd":        np.round(lgd_vals, 4),
        "maturite":   maturites,
    })
    
    df["el"] = df["pd"] * df["lgd"] * df["notionnel_m"]   # EL en M€
    df["rwa_approx"] = df["notionnel_m"] * df["pd"] * 12.5 * 0.06  # approx Basel
    
    return df


def stats_portefeuille(df: pd.DataFrame) -> dict:
    total = df["notionnel_m"].sum()
    el_total = df["el"].sum()
    el_pct = el_total / total * 100
    pd_moyen = (df["pd"] * df["notionnel_m"]).sum() / total
    lgd_moyen = (df["lgd"] * df["notionnel_m"]).sum() / total
    mat_moyen = (df["maturite"] * df["notionnel_m"]).sum() / total
    rwa_total = df["rwa_approx"].sum()
    hhi = ((df["notionnel_m"] / total) ** 2).sum()   # concentration Herfindahl
    
    return {
        "total": total,
        "n_loans": len(df),
        "el_total": el_total,
        "el_pct": el_pct,
        "pd_moyen": pd_moyen,
        "lgd_moyen": lgd_moyen,
        "mat_moyen": mat_moyen,
        "rwa_total": rwa_total,
        "hhi": hhi,
    }


def format_m(val: float) -> str:
    if val >= 1000:
        return f"{val/1000:.2f} Md€"
    return f"{val:.1f} M€"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🏦 SRT Structuring Tool")
    st.markdown("<small style='color:#8b949e'>v0.1 — Étape 1 : Portefeuille</small>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("**Navigation**")
    page = st.radio(
        label="",
        options=["📂 Portefeuille de référence", "⚙️ Structuration tranche",
                 "📊 Monte Carlo", "📋 Réglementaire", "📈 Dynamique", "🔥 Stress tests"],
        label_visibility="collapsed",
    )
    
    st.divider()
    
    # Mode de chargement
    st.markdown("**Source du portefeuille**")
    source = st.radio("", ["🎲 Générer un portefeuille fictif", "📤 Uploader un CSV"],
                      label_visibility="collapsed")
    
    if source == "🎲 Générer un portefeuille fictif":
        n_loans = st.slider("Nombre de loans", 20, 500, 100, step=10)
        seed    = st.number_input("Seed aléatoire", value=42, step=1)
        if st.button("Générer le portefeuille"):
            st.session_state["df"] = generer_portefeuille(int(n_loans), int(seed))
            st.success(f"{n_loans} loans générés ✓")
    else:
        uploaded = st.file_uploader("Fichier CSV", type=["csv"])
        if uploaded:
            try:
                df_up = pd.read_csv(uploaded)
                required = {"notionnel_m", "pd", "lgd", "maturite"}
                if not required.issubset(df_up.columns):
                    st.error(f"Colonnes manquantes : {required - set(df_up.columns)}")
                else:
                    if "el" not in df_up.columns:
                        df_up["el"] = df_up["pd"] * df_up["lgd"] * df_up["notionnel_m"]
                    if "rwa_approx" not in df_up.columns:
                        df_up["rwa_approx"] = df_up["notionnel_m"] * df_up["pd"] * 12.5 * 0.06
                    st.session_state["df"] = df_up
                    st.success(f"{len(df_up)} loans chargés ✓")
            except Exception as e:
                st.error(f"Erreur lecture : {e}")
    
    st.divider()
    st.markdown("<small style='color:#8b949e'>Anthropic × Finance — usage interne</small>",
                unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GUARD : portefeuille chargé ?
# ─────────────────────────────────────────────

if page != "📂 Portefeuille de référence" and "df" not in st.session_state:
    st.warning("⬅️ Commence par charger ou générer un portefeuille dans la sidebar.")
    st.stop()


# ═══════════════════════════════════════════════════════════════════
# PAGE 1 — PORTEFEUILLE DE RÉFÉRENCE
# ═══════════════════════════════════════════════════════════════════

if page == "📂 Portefeuille de référence":

    st.markdown("# Portefeuille de référence")
    st.markdown("<p style='color:#8b949e'>Chargement, filtrage et analyse statistique du portefeuille de loans.</p>",
                unsafe_allow_html=True)
    
    if "df" not in st.session_state:
        st.markdown("""
        <div class='card-accent'>
        <b>Aucun portefeuille chargé.</b><br>
        Utilise la sidebar à gauche pour générer un portefeuille fictif ou uploader un CSV.
        </div>
        """, unsafe_allow_html=True)
        
        # Montrer le format attendu
        st.markdown("#### Format CSV attendu")
        exemple = pd.DataFrame({
            "loan_id":     ["LOAN-0001", "LOAN-0002"],
            "secteur":     ["Corporate", "PME"],
            "pays":        ["France", "Allemagne"],
            "notation":    ["BBB", "BB"],
            "notionnel_m": [25.0, 8.5],
            "pd":          [0.003, 0.015],
            "lgd":         [0.45, 0.40],
            "maturite":    [3.5, 5.0],
        })
        st.dataframe(exemple, use_container_width=True)
        st.stop()

    df = st.session_state["df"]

    # ── Filtres ──────────────────────────────
    with st.expander("🔍 Filtres du portefeuille", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if "secteur" in df.columns:
                secteurs_dispo = ["Tous"] + sorted(df["secteur"].unique().tolist())
                filtre_secteur = st.selectbox("Secteur", secteurs_dispo)
            else:
                filtre_secteur = "Tous"
        
        with col2:
            if "pays" in df.columns:
                pays_dispo = ["Tous"] + sorted(df["pays"].unique().tolist())
                filtre_pays = st.selectbox("Pays", pays_dispo)
            else:
                filtre_pays = "Tous"
        
        with col3:
            if "notation" in df.columns:
                notations_dispo = ["Toutes"] + [n for n in NOTATIONS if n in df["notation"].unique()]
                filtre_notation = st.selectbox("Notation minimale (ou meilleure)", notations_dispo)
            else:
                filtre_notation = "Toutes"
        
        col4, col5 = st.columns(2)
        with col4:
            pd_max = st.slider("PD maximum", 0.0, 0.40, float(df["pd"].max()), 0.005,
                               format="%.3f")
        with col5:
            notionnel_min = st.slider("Notionnel minimum (M€)", 0.0,
                                      float(df["notionnel_m"].max()), 0.0, 0.5)
        
        # Appliquer filtres
        df_f = df.copy()
        if filtre_secteur != "Tous" and "secteur" in df.columns:
            df_f = df_f[df_f["secteur"] == filtre_secteur]
        if filtre_pays != "Tous" and "pays" in df.columns:
            df_f = df_f[df_f["pays"] == filtre_pays]
        if filtre_notation != "Toutes" and "notation" in df.columns:
            idx = NOTATIONS.index(filtre_notation)
            df_f = df_f[df_f["notation"].isin(NOTATIONS[:idx+1])]
        df_f = df_f[(df_f["pd"] <= pd_max) & (df_f["notionnel_m"] >= notionnel_min)]
        
        st.markdown(f"<span class='tag'>{len(df_f)} / {len(df)} loans sélectionnés</span>",
                    unsafe_allow_html=True)
        
        if st.button("Appliquer la sélection comme portefeuille actif"):
            st.session_state["df_actif"] = df_f
            st.success("Portefeuille filtré enregistré ✓")
    
    # Portefeuille actif
    df_actif = st.session_state.get("df_actif", df)
    stats = stats_portefeuille(df_actif)

    # ── KPIs ─────────────────────────────────
    st.markdown("#### 📊 Métriques clés")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Notionnel total",    format_m(stats["total"]))
    c2.metric("Nombre de loans",    f"{stats['n_loans']}")
    c3.metric("EL total",           format_m(stats["el_total"]))
    c4.metric("EL / Notionnel",     f"{stats['el_pct']:.2f}%")
    c5.metric("RWA approx.",        format_m(stats["rwa_total"]))
    
    st.markdown("<br>", unsafe_allow_html=True)
    c6, c7, c8, c9 = st.columns(4)
    c6.metric("PD moyen (pondéré)", f"{stats['pd_moyen']*100:.3f}%")
    c7.metric("LGD moyen (pondéré)", f"{stats['lgd_moyen']*100:.1f}%")
    c8.metric("Maturité moyenne",   f"{stats['mat_moyen']:.1f} ans")
    hhi_pct = stats["hhi"] * 100
    hhi_label = "Faible ✓" if hhi_pct < 1 else ("Modéré" if hhi_pct < 2 else "Élevé ⚠️")
    c9.metric("Concentration HHI",  f"{hhi_pct:.2f}%", delta=hhi_label,
              delta_color="normal" if hhi_pct < 1 else "inverse")

    st.divider()

    # ── Graphiques ───────────────────────────
    tabs = st.tabs(["Distribution des pertes", "Concentration", "Carte de risque", "Données brutes"])
    
    with tabs[0]:
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Distribution des notionnels
            fig = px.histogram(df_actif, x="notionnel_m", nbins=40,
                               title="Distribution des notionnels (M€)",
                               color_discrete_sequence=["#58a6ff"])
            fig.update_layout(
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#e6edf3", title_font_color="#58a6ff",
                xaxis=dict(gridcolor="#30363d"), yaxis=dict(gridcolor="#30363d"),
                showlegend=False
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            # Distribution des EL
            fig2 = px.histogram(df_actif, x="el", nbins=40,
                                title="Distribution des EL individuels (M€)",
                                color_discrete_sequence=["#3fb950"])
            fig2.update_layout(
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#e6edf3", title_font_color="#58a6ff",
                xaxis=dict(gridcolor="#30363d"), yaxis=dict(gridcolor="#30363d"),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tabs[1]:
        col_a, col_b = st.columns(2)
        
        with col_a:
            if "secteur" in df_actif.columns:
                by_sect = df_actif.groupby("secteur")["notionnel_m"].sum().reset_index()
                by_sect.columns = ["Secteur", "Notionnel (M€)"]
                fig = px.pie(by_sect, values="Notionnel (M€)", names="Secteur",
                             title="Concentration par secteur",
                             color_discrete_sequence=px.colors.sequential.Blues_r)
                fig.update_layout(paper_bgcolor="#161b22", font_color="#e6edf3",
                                  title_font_color="#58a6ff")
                st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            if "notation" in df_actif.columns:
                by_not = df_actif.groupby("notation")["notionnel_m"].sum().reindex(NOTATIONS).dropna().reset_index()
                by_not.columns = ["Notation", "Notionnel (M€)"]
                colors = ["#3fb950","#3fb950","#58a6ff","#58a6ff","#d29922","#f85149","#f85149"]
                fig = px.bar(by_not, x="Notation", y="Notionnel (M€)",
                             title="Concentration par notation",
                             color="Notation",
                             color_discrete_sequence=colors)
                fig.update_layout(
                    plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                    font_color="#e6edf3", title_font_color="#58a6ff",
                    xaxis=dict(gridcolor="#30363d"), yaxis=dict(gridcolor="#30363d"),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        # Scatter PD vs LGD, taille = notionnel
        fig = px.scatter(df_actif, x="pd", y="lgd",
                         size="notionnel_m", color="el",
                         hover_data=["loan_id"] if "loan_id" in df_actif.columns else None,
                         title="Carte de risque : PD × LGD (taille = notionnel, couleur = EL)",
                         labels={"pd": "Probabilité de défaut (PD)",
                                 "lgd": "Perte en cas de défaut (LGD)",
                                 "el": "EL (M€)"},
                         color_continuous_scale="Blues")
        fig.update_layout(
            plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
            font_color="#e6edf3", title_font_color="#58a6ff",
            xaxis=dict(gridcolor="#30363d", tickformat=".1%"),
            yaxis=dict(gridcolor="#30363d", tickformat=".0%"),
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        cols_show = [c for c in ["loan_id","secteur","pays","notation","notionnel_m","pd","lgd","maturite","el","rwa_approx"]
                     if c in df_actif.columns]
        st.dataframe(
            df_actif[cols_show].sort_values("notionnel_m", ascending=False).reset_index(drop=True),
            use_container_width=True,
            height=400
        )
        
        csv = df_actif[cols_show].to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Télécharger le portefeuille filtré (CSV)",
                           csv, "portefeuille_filtre.csv", "text/csv")


# ═══════════════════════════════════════════════════════════════════
# PAGES SUIVANTES — placeholders
# ═══════════════════════════════════════════════════════════════════

elif page == "⚙️ Structuration tranche":

    st.markdown("# ⚙️ Structuration de la tranche")
    st.markdown("<p style='color:#8b949e'>Définition des points d'attache/détachement, calcul du notionnel protégé et du coupon théorique.</p>", unsafe_allow_html=True)

    df_actif = st.session_state.get("df_actif", st.session_state["df"])
    stats = stats_portefeuille(df_actif)
    notionnel_total = stats["total"]
    el_pct          = stats["el_pct"]       # en %
    pd_moy          = stats["pd_moyen"]
    lgd_moy         = stats["lgd_moyen"]

    st.divider()

    # ── Paramètres de la tranche ─────────────────────────────────────
    st.markdown("#### 🎚️ Paramètres de la tranche")

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        attachment  = st.slider(
            "Point d'attache (Attachment Point) — % du portefeuille",
            min_value=0.0, max_value=20.0, value=0.0, step=0.1,
            help="Les premières pertes jusqu'à ce seuil sont absorbées par le vendeur de protection (vous)."
        )
        detachment = st.slider(
            "Point de détachement (Detachment Point) — % du portefeuille",
            min_value=0.1, max_value=30.0, value=10.0, step=0.1,
            help="Au-delà de ce seuil, les pertes supplémentaires retombent sur le vendeur de protection."
        )

        if detachment <= attachment:
            st.error("⚠️ Le point de détachement doit être supérieur au point d'attache.")
            st.stop()

        spread_bps = st.slider(
            "Coupon investisseur (spread, bps)",
            min_value=50, max_value=2000, value=600, step=25,
            help="Rémunération annuelle versée à l'investisseur sur le notionnel de la tranche."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Calculs ──────────────────────────────────────────────────────
    epaisseur_pct      = detachment - attachment                          # % du portef.
    notionnel_tranche  = notionnel_total * epaisseur_pct / 100            # M€
    notionnel_attach   = notionnel_total * attachment   / 100             # M€
    notionnel_detach   = notionnel_total * detachment   / 100             # M€

    # EL absorbé par la tranche
    # EL total du portefeuille en M€
    el_total_m = stats["el_total"]
    # Part de l'EL qui tombe dans la tranche (approx linéaire)
    el_sous_attach  = min(el_total_m, notionnel_attach)
    el_sous_detach  = min(el_total_m, notionnel_detach)
    el_tranche_m    = max(0.0, el_sous_detach - el_sous_attach)
    el_tranche_pct  = el_tranche_m / notionnel_tranche * 100 if notionnel_tranche > 0 else 0

    # Coupon annuel versé à l'investisseur
    coupon_annuel_m = notionnel_tranche * spread_bps / 10_000

    # Subordination = coussin absorbant les pertes avant la tranche
    subordination_pct = attachment

    # Ratio EL/Epaisseur : mesure de "tension" de la tranche
    ratio_tension = el_tranche_pct / epaisseur_pct if epaisseur_pct > 0 else 0

    with col_right:
        st.markdown("#### 📐 Résultats de structuration")
        r1, r2 = st.columns(2)
        r1.metric("Épaisseur de la tranche",  f"{epaisseur_pct:.1f}%")
        r2.metric("Notionnel protégé",         format_m(notionnel_tranche))
        r3, r4 = st.columns(2)
        r3.metric("Subordination",             f"{subordination_pct:.1f}%",
                  help="Pertes absorbées avant que la tranche soit touchée.")
        r4.metric("EL dans la tranche",        f"{el_tranche_pct:.3f}%")
        r5, r6 = st.columns(2)
        r5.metric("Coupon annuel (investisseur)", format_m(coupon_annuel_m),
                  help=f"{spread_bps} bps × {format_m(notionnel_tranche)}")
        r6.metric("Spread / EL (ratio protection)", f"{spread_bps/max(el_tranche_pct*100,0.01):.1f}×",
                  help="Plus ce ratio est élevé, plus l'investisseur est bien rémunéré par unité de risque.")

    # Sauvegarder pour les étapes suivantes
    st.session_state["tranche"] = {
        "attachment":         attachment,
        "detachment":         detachment,
        "epaisseur_pct":      epaisseur_pct,
        "notionnel_tranche":  notionnel_tranche,
        "notionnel_attach":   notionnel_attach,
        "notionnel_detach":   notionnel_detach,
        "spread_bps":         spread_bps,
        "coupon_annuel_m":    coupon_annuel_m,
        "el_tranche_pct":     el_tranche_pct,
        "subordination_pct":  subordination_pct,
    }

    st.divider()

    # ── Visualisations ───────────────────────────────────────────────
    st.markdown("#### 📊 Visualisation de la tranche")

    tab1, tab2 = st.tabs(["Structure en waterfall", "Sensibilité au spread"])

    with tab1:
        # Waterfall : décomposition du portefeuille en tranches
        labels = []
        values = []
        colors = []

        if attachment > 0:
            labels.append(f"Première perte<br>(0% → {attachment:.1f}%)")
            values.append(notionnel_attach)
            colors.append("#f85149")   # rouge = risque max

        labels.append(f"Tranche vendue<br>({attachment:.1f}% → {detachment:.1f}%)")
        values.append(notionnel_tranche)
        colors.append("#58a6ff")       # bleu = tranche SRT

        reste_pct = 100 - detachment
        if reste_pct > 0:
            labels.append(f"Senior / Banque<br>({detachment:.1f}% → 100%)")
            values.append(notionnel_total * reste_pct / 100)
            colors.append("#3fb950")   # vert = senior, peu risqué

        fig_waterfall = go.Figure(go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=[format_m(v) for v in values],
            textposition="auto",
            textfont=dict(color="#e6edf3", size=12),
        ))

        # Ligne EL total
        fig_waterfall.add_hline(
            y=el_total_m,
            line_dash="dash", line_color="#d29922",
            annotation_text=f"EL total portefeuille : {format_m(el_total_m)}",
            annotation_font_color="#d29922",
        )

        fig_waterfall.update_layout(
            title="Décomposition du portefeuille (M€)",
            plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
            font_color="#e6edf3", title_font_color="#58a6ff",
            xaxis=dict(gridcolor="#30363d"),
            yaxis=dict(gridcolor="#30363d", title="Notionnel (M€)"),
            showlegend=False,
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

        # Légende couleurs
        st.markdown("""
        <span class='tag-red'>🔴 Première perte — retenue par la banque</span>
        <span class='tag' style='margin-left:8px'>🔵 Tranche vendue — couverte par l'investisseur</span>
        <span class='tag-green' style='margin-left:8px'>🟢 Senior — reste sur le bilan banque</span>
        """, unsafe_allow_html=True)

    with tab2:
        # Sensibilité du coupon annuel au spread
        spreads   = np.arange(100, 2001, 25)
        coupons   = notionnel_tranche * spreads / 10_000

        fig_sens = go.Figure()
        fig_sens.add_trace(go.Scatter(
            x=spreads, y=coupons,
            mode="lines",
            line=dict(color="#58a6ff", width=2),
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.08)",
            name="Coupon annuel (M€)"
        ))
        # Point courant
        fig_sens.add_trace(go.Scatter(
            x=[spread_bps], y=[coupon_annuel_m],
            mode="markers",
            marker=dict(color="#f85149", size=10, symbol="circle"),
            name=f"Coupon actuel ({spread_bps} bps)"
        ))
        fig_sens.update_layout(
            title="Coupon annuel investisseur selon le spread (M€)",
            plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
            font_color="#e6edf3", title_font_color="#58a6ff",
            xaxis=dict(gridcolor="#30363d", title="Spread (bps)"),
            yaxis=dict(gridcolor="#30363d", title="Coupon annuel (M€)"),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
        )
        st.plotly_chart(fig_sens, use_container_width=True)

    # ── Synthèse textuelle ───────────────────────────────────────────
    st.divider()
    st.markdown("#### 📝 Synthèse de la transaction")
    st.markdown(f"""
    <div class='card-accent'>
    Sur un portefeuille de <b>{format_m(notionnel_total)}</b>, la banque cède à l'investisseur
    la protection sur la tranche <b>[{attachment:.1f}% — {detachment:.1f}%]</b>,
    soit <b>{format_m(notionnel_tranche)}</b> de risque de crédit.<br><br>
    L'investisseur reçoit un coupon annuel de <b>{spread_bps} bps</b>
    ({format_m(coupon_annuel_m)}/an) en échange d'une exposition à l'EL estimé
    de <b>{el_tranche_pct:.3f}%</b> dans sa tranche.<br><br>
    La subordination de <b>{subordination_pct:.1f}%</b> ({format_m(notionnel_attach)}) protège
    la tranche vendue des premières pertes du portefeuille.
    </div>
    """, unsafe_allow_html=True)

elif page == "📊 Monte Carlo":

    st.markdown("# 📊 Simulation Monte Carlo")
    st.markdown("<p style='color:#8b949e'>Modèle gaussien à un facteur (Vasicek) — simulation de la distribution des pertes du portefeuille.</p>", unsafe_allow_html=True)

    if "tranche" not in st.session_state:
        st.markdown("<div class='card-accent'>Configure d'abord la tranche dans le module Structuration tranche.</div>", unsafe_allow_html=True)
        st.stop()

    df_actif  = st.session_state.get("df_actif", st.session_state["df"])
    tranche   = st.session_state["tranche"]
    stats     = stats_portefeuille(df_actif)
    N_total   = stats["total"]
    n_loans   = len(df_actif)
    attach_m  = tranche["notionnel_attach"]
    detach_m  = tranche["notionnel_detach"]
    epaisseur = tranche["notionnel_tranche"]

    st.divider()
    st.markdown("#### Parametres de simulation")
    col1, col2, col3 = st.columns(3)
    with col1:
        n_sims = st.select_slider("Nombre de simulations",
            options=[1_000, 5_000, 10_000, 50_000, 100_000], value=10_000)
    with col2:
        rho = st.slider("Correlation systemique rho", 0.05, 0.50, 0.20, 0.01,
            help="Correlation entre defauts due au facteur economique commun. Typiquement 0.15-0.25 en corporate.")
    with col3:
        seed_mc = st.number_input("Seed", value=42, step=1)

    run = st.button("Lancer la simulation")

    if run or "mc_results" in st.session_state:
        if run:
            with st.spinner("Simulation en cours..."):
                from scipy.stats import norm
                rng        = np.random.default_rng(int(seed_mc))
                pds        = df_actif["pd"].values
                lgds       = df_actif["lgd"].values
                nots       = df_actif["notionnel_m"].values
                thresholds = norm.ppf(pds)
                Z          = rng.standard_normal(n_sims)
                eps        = rng.standard_normal((n_sims, n_loans))
                X          = np.sqrt(rho) * Z[:, None] + np.sqrt(1 - rho) * eps
                defaults   = X < thresholds[None, :]
                loss_matrix   = defaults * lgds[None, :] * nots[None, :]
                total_losses  = loss_matrix.sum(axis=1)
                tranche_losses = np.clip(total_losses - attach_m, 0, epaisseur)
                st.session_state["mc_results"] = {
                    "total_losses": total_losses,
                    "tranche_losses": tranche_losses,
                    "n_sims": n_sims,
                    "rho": rho,
                }

        res            = st.session_state["mc_results"]
        total_losses   = res["total_losses"]
        tranche_losses = res["tranche_losses"]
        n_sims_used    = res["n_sims"]

        st.divider()
        st.markdown("#### Resultats")

        el_mc      = total_losses.mean()
        el_mc_pct  = el_mc / N_total * 100
        std_loss   = total_losses.std()
        var_99     = np.percentile(total_losses, 99)
        es_99      = total_losses[total_losses >= var_99].mean()
        el_tr      = tranche_losses.mean()
        el_tr_pct  = el_tr / epaisseur * 100 if epaisseur > 0 else 0
        var_tr_99  = np.percentile(tranche_losses, 99)
        prob_touche = (tranche_losses > 0).mean() * 100

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("EL moyen portefeuille",  format_m(el_mc),   f"{el_mc_pct:.3f}%")
        c2.metric("Ecart-type des pertes",  format_m(std_loss))
        c3.metric("VaR 99% portefeuille",   format_m(var_99))
        c4.metric("Expected Shortfall 99%", format_m(es_99))

        st.markdown("<br>", unsafe_allow_html=True)
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("EL tranche (MC)",        format_m(el_tr),   f"{el_tr_pct:.3f}%")
        d2.metric("VaR 99% tranche",        format_m(var_tr_99))
        d3.metric("Prob. tranche touchee",  f"{prob_touche:.2f}%")
        d4.metric("Simulations",            f"{n_sims_used:,}")

        st.divider()
        tab1, tab2 = st.tabs(["Distribution des pertes", "Pertes dans la tranche"])

        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=total_losses, nbinsx=120,
                marker_color="#58a6ff", opacity=0.7, histnorm="probability density",
            ))
            fig.add_vrect(x0=attach_m, x1=detach_m,
                fillcolor="rgba(248,81,73,0.15)", line_width=0,
                annotation_text="Tranche vendue", annotation_position="top left",
                annotation_font_color="#f85149")
            fig.add_vline(x=attach_m, line_dash="dash", line_color="#f85149",
                annotation_text=f"Attach {tranche['attachment']:.1f}%", annotation_font_color="#f85149")
            fig.add_vline(x=detach_m, line_dash="dash", line_color="#d29922",
                annotation_text=f"Detach {tranche['detachment']:.1f}%", annotation_font_color="#d29922")
            fig.add_vline(x=var_99, line_dash="dot", line_color="#3fb950",
                annotation_text="VaR 99%", annotation_font_color="#3fb950")
            fig.add_vline(x=el_mc, line_dash="dot", line_color="#8b949e",
                annotation_text="EL moyen", annotation_font_color="#8b949e")
            fig.update_layout(
                title=f"Distribution des pertes ({n_sims_used:,} simulations — Vasicek rho={rho})",
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#e6edf3", title_font_color="#58a6ff",
                xaxis=dict(gridcolor="#30363d", title="Pertes (M€)"),
                yaxis=dict(gridcolor="#30363d", title="Densite"),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            pct_zero  = (tranche_losses == 0).mean() * 100
            pertes_pos = tranche_losses[tranche_losses > 0]
            fig2 = go.Figure()
            if len(pertes_pos) > 0:
                fig2.add_trace(go.Histogram(
                    x=pertes_pos, nbinsx=80,
                    marker_color="#f85149", opacity=0.8, histnorm="probability density",
                ))
            fig2.add_vline(x=el_tr, line_dash="dot", line_color="#58a6ff",
                annotation_text=f"EL tranche {el_tr:.1f} M", annotation_font_color="#58a6ff")
            fig2.add_vline(x=var_tr_99, line_dash="dash", line_color="#d29922",
                annotation_text="VaR 99%", annotation_font_color="#d29922")
            fig2.update_layout(
                title=f"Pertes dans la tranche (conditionnelle perte > 0 — {100-pct_zero:.1f}% des scenarios)",
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#e6edf3", title_font_color="#58a6ff",
                xaxis=dict(gridcolor="#30363d", title="Pertes dans la tranche (M€)"),
                yaxis=dict(gridcolor="#30363d", title="Densite"),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(f"""
            <div class='card'>
            Dans <b>{pct_zero:.1f}%</b> des scenarios, la tranche n'est pas touchee.<br>
            Dans les <b>{100-pct_zero:.1f}%</b> restants, l'investisseur subit une perte moyenne de <b>{format_m(pertes_pos.mean() if len(pertes_pos)>0 else 0)}</b>.
            </div>
            """, unsafe_allow_html=True)

elif page == "📋 Réglementaire":

    st.markdown("# 📋 Calculs réglementaires CRR3")
    st.markdown("<p style='color:#8b949e'>RWA avant/après protection, capital libéré, SEC-SA et SEC-IRBA.</p>", unsafe_allow_html=True)

    if "tranche" not in st.session_state:
        st.markdown("<div class='card-accent'>Configure d'abord la tranche dans Structuration tranche.</div>", unsafe_allow_html=True)
        st.stop()

    df_actif = st.session_state.get("df_actif", st.session_state["df"])
    tranche  = st.session_state["tranche"]
    stats    = stats_portefeuille(df_actif)
    N_total  = stats["total"]

    attach_pct  = tranche["attachment"] / 100
    detach_pct  = tranche["detachment"] / 100
    attach_m    = tranche["notionnel_attach"]
    detach_m    = tranche["notionnel_detach"]
    epaisseur_m = tranche["notionnel_tranche"]

    from scipy.stats import norm as sp_norm

    def rwa_kirb_loan(pd, lgd, mat=2.5):
        if pd <= 0:
            pd = 1e-5
        R  = 0.12*(1-np.exp(-50*pd))/(1-np.exp(-50)) + 0.24*(1-(1-np.exp(-50*pd))/(1-np.exp(-50)))
        b  = (0.11852 - 0.05478*np.log(pd))**2
        MA = (1 + (mat-2.5)*b) / (1 - 1.5*b)
        N_inv_pd = sp_norm.ppf(pd)
        PD_cond  = sp_norm.cdf((N_inv_pd + np.sqrt(R)*sp_norm.ppf(0.999)) / np.sqrt(1-R))
        K = lgd*PD_cond - lgd*pd
        return max(K * MA * 12.5, 0.0)

    def kirb_portefeuille(df):
        rwa_t = 0.0; k_t = 0.0
        for _, row in df.iterrows():
            rd    = rwa_kirb_loan(row["pd"], row["lgd"], mat=row.get("maturite", 2.5))
            rwa_t += rd * row["notionnel_m"]
            k_t   += (rd/12.5) * row["notionnel_m"]
        k_irb = k_t / df["notionnel_m"].sum()
        return rwa_t, k_irb

    def sec_irba_density(k_irb, attach, detach, p=0.5):
        # CRR3 Art.263 - a positif, exponentielle decroissante
        a = 1/(p*k_irb) if k_irb > 0 else 1e6
        u = detach - k_irb
        l = max(attach - k_irb, 0)
        if u <= 0: return 1.0
        if u <= l: return 0.0
        if abs(u-l) < 1e-10: return 0.0
        num = (np.exp(-a*l) - np.exp(-a*u)) / (a*(u-l))
        return float(np.clip(num*12.5, 0, 12.5))

    def sec_sa_density(attach, detach, kg, p=1.0):
        # CRR3 Art.261 - meme structure que SEC-IRBA avec K_G
        a = 1/(p*kg) if kg > 0 else 1e6
        u = detach - kg
        l = max(attach - kg, 0)
        if u <= 0: return 1.0
        if u <= l: return 0.0
        if abs(u-l) < 1e-10: return 0.0
        num = (np.exp(-a*l) - np.exp(-a*u)) / (a*(u-l))
        return float(np.clip(num*12.5, 0, 12.5))

    st.divider()
    st.markdown("#### Parametres reglementaires")
    col1, col2, col3 = st.columns(3)
    with col1:
        approche = st.selectbox("Approche", ["SEC-IRBA", "SEC-SA", "Comparer les deux"])
    with col2:
        ratio_cet1 = st.slider("Ratio CET1 cible (%)", 8.0, 16.0, 12.0, 0.5)
    with col3:
        rw_sa = st.slider("Risk weight SA moyen (%)", 50, 150, 100, 5)

    with st.spinner("Calcul des RWA..."):
        rwa_avant_irba, k_irb = kirb_portefeuille(df_actif)
        capital_avant_irba    = rwa_avant_irba * ratio_cet1 / 100

        kg_sa            = rw_sa / 100 / 12.5
        rwa_avant_sa     = N_total * rw_sa / 100
        capital_avant_sa = rwa_avant_sa * ratio_cet1 / 100

        dens_irba        = sec_irba_density(k_irb, attach_pct, detach_pct)
        rwa_tranche_irba = epaisseur_m * dens_irba
        dens_sa          = sec_sa_density(attach_pct, detach_pct, kg_sa)
        rwa_tranche_sa   = epaisseur_m * dens_sa

        rwa_apres_irba     = max(rwa_avant_irba - (N_total*k_irb*12.5*(detach_pct-attach_pct)), 0)
        capital_apres_irba = rwa_apres_irba * ratio_cet1 / 100
        capital_libere_irba = capital_avant_irba - capital_apres_irba
        relief_pct_irba    = capital_libere_irba / capital_avant_irba * 100 if capital_avant_irba > 0 else 0

        rwa_apres_sa       = max(rwa_avant_sa*(1-(detach_pct-attach_pct)), 0)
        capital_apres_sa   = rwa_apres_sa * ratio_cet1 / 100
        capital_libere_sa  = capital_avant_sa - capital_apres_sa
        relief_pct_sa      = capital_libere_sa / capital_avant_sa * 100 if capital_avant_sa > 0 else 0

    st.divider()

    if approche == "SEC-IRBA":
        blocs = [("SEC-IRBA", rwa_avant_irba, rwa_apres_irba, rwa_tranche_irba,
                  capital_avant_irba, capital_apres_irba, capital_libere_irba, relief_pct_irba, k_irb, dens_irba)]
    elif approche == "SEC-SA":
        blocs = [("SEC-SA", rwa_avant_sa, rwa_apres_sa, rwa_tranche_sa,
                  capital_avant_sa, capital_apres_sa, capital_libere_sa, relief_pct_sa, kg_sa, dens_sa)]
    else:
        blocs = [
            ("SEC-IRBA", rwa_avant_irba, rwa_apres_irba, rwa_tranche_irba,
             capital_avant_irba, capital_apres_irba, capital_libere_irba, relief_pct_irba, k_irb, dens_irba),
            ("SEC-SA",   rwa_avant_sa,   rwa_apres_sa,   rwa_tranche_sa,
             capital_avant_sa, capital_apres_sa, capital_libere_sa, relief_pct_sa, kg_sa, dens_sa),
        ]

    for (nom, rwa_av, rwa_ap, rwa_tr, cap_av, cap_ap, cap_lib, relief_pct, k_val, dens) in blocs:
        st.markdown(f"#### Approche {nom}")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("RWA avant protection",  format_m(rwa_av))
        c2.metric("RWA apres protection",  format_m(rwa_ap),
                  delta=f"-{format_m(rwa_av-rwa_ap)}", delta_color="inverse")
        c3.metric("Capital avant",         format_m(cap_av))
        c4.metric("Capital libere",        format_m(cap_lib),
                  delta=f"{relief_pct:.1f}% du capital initial", delta_color="inverse")
        st.markdown("<br>", unsafe_allow_html=True)
        e1,e2,e3 = st.columns(3)
        e1.metric("K_IRB / K_G moyen",    f"{k_val*100:.3f}%")
        e2.metric("RWA density tranche",  f"{dens*100:.1f}%")
        e3.metric("RWA tranche residuel", format_m(rwa_tr))

        fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute","relative","total"],
            x=["Capital avant SRT","Capital libere","Capital apres SRT"],
            y=[cap_av, -cap_lib, 0],
            connector=dict(line=dict(color="#30363d")),
            decreasing=dict(marker_color="#3fb950"),
            totals=dict(marker_color="#58a6ff"),
            increasing=dict(marker_color="#f85149"),
            text=[format_m(cap_av), f"-{format_m(cap_lib)}", format_m(cap_ap)],
            textposition="outside",
        ))
        fig.update_layout(
            title=f"Waterfall capital reglementaire - {nom} (CET1 {ratio_cet1}%)",
            plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
            font_color="#e6edf3", title_font_color="#58a6ff",
            yaxis=dict(gridcolor="#30363d", title="Capital (M€)"),
            xaxis=dict(gridcolor="#30363d"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
        <div class='card-accent'>
        En appliquant la protection SRT sur la tranche [{tranche['attachment']:.1f}%-{tranche['detachment']:.1f}%],
        la banque libere <b>{format_m(cap_lib)}</b> de capital CET1 ({relief_pct:.1f}% du capital initial).<br><br>
        Ce capital libere peut etre redéploye sur de nouvelles originations.
        Le coupon verse a l'investisseur (<b>{format_m(tranche['coupon_annuel_m'])}/an</b>)
        doit etre compare au cout de ce capital pour evaluer l'attractivite de la transaction.
        </div>
        """, unsafe_allow_html=True)
        if approche == "Comparer les deux":
            st.divider()

    if approche == "Comparer les deux":
        st.markdown("#### Comparaison SEC-IRBA vs SEC-SA")
        comp = pd.DataFrame({
            "Metrique": ["RWA avant (M)", "RWA apres (M)", "Capital libere (M)",
                         "Relief (%)", "RWA density tranche (%)"],
            "SEC-IRBA": [f"{rwa_avant_irba:.0f}", f"{rwa_apres_irba:.0f}",
                         f"{capital_libere_irba:.0f}", f"{relief_pct_irba:.1f}%",
                         f"{dens_irba*100:.1f}%"],
            "SEC-SA":   [f"{rwa_avant_sa:.0f}", f"{rwa_apres_sa:.0f}",
                         f"{capital_libere_sa:.0f}", f"{relief_pct_sa:.1f}%",
                         f"{dens_sa*100:.1f}%"],
        })
        st.dataframe(comp, use_container_width=True, hide_index=True)

    st.session_state["reglem"] = {
        "rwa_avant_irba": rwa_avant_irba, "rwa_apres_irba": rwa_apres_irba,
        "capital_libere_irba": capital_libere_irba, "relief_pct_irba": relief_pct_irba,
        "rwa_avant_sa": rwa_avant_sa, "rwa_apres_sa": rwa_apres_sa,
        "capital_libere_sa": capital_libere_sa, "relief_pct_sa": relief_pct_sa,
        "k_irb": k_irb, "ratio_cet1": ratio_cet1,
    }



elif page == "📈 Dynamique":

    st.markdown("# 📈 Evolution dynamique")
    st.markdown("<p style='color:#8b949e'>Amortissement du portefeuille, erosion de la tranche, cashflows investisseur au fil du temps.</p>", unsafe_allow_html=True)

    if "tranche" not in st.session_state:
        st.markdown("<div class='card-accent'>Configure d'abord la tranche dans Structuration tranche.</div>", unsafe_allow_html=True)
        st.stop()

    df_actif = st.session_state.get("df_actif", st.session_state["df"])
    tranche  = st.session_state["tranche"]
    stats    = stats_portefeuille(df_actif)
    N_total  = stats["total"]
    pd_moy   = stats["pd_moyen"]
    lgd_moy  = stats["lgd_moyen"]

    attach_pct  = tranche["attachment"] / 100
    detach_pct  = tranche["detachment"] / 100
    spread_bps  = tranche["spread_bps"]

    st.divider()
    st.markdown("#### Parametres de projection")

    col1, col2, col3 = st.columns(3)
    with col1:
        horizon     = st.slider("Horizon (annees)", 1, 10, 5, 1)
        tx_amort    = st.slider("Taux d'amortissement annuel (%)", 0.0, 30.0, 15.0, 1.0,
                                help="Part du portefeuille remboursee chaque annee (hors defauts).") / 100
    with col2:
        pd_stress   = st.slider("Multiplicateur PD (base=1x)", 0.5, 3.0, 1.0, 0.1,
                                help="1x = scenario central. 2x = recession.")
        lgd_stress  = st.slider("Multiplicateur LGD (base=1x)", 0.5, 2.0, 1.0, 0.1) 
    with col3:
        reinvest    = st.checkbox("Reinvestissement (portefeuille constant)", value=False,
                                  help="Si coche, les remboursements sont reinvestis — le notionnel reste constant.")

    st.divider()

    # ── Simulation annee par annee ────────────────────────────────
    pd_eff  = min(pd_moy  * pd_stress,  0.99)
    lgd_eff = min(lgd_moy * lgd_stress, 0.99)

    annees          = list(range(horizon + 1))
    notionnel_port  = [N_total]
    pertes_cumul    = [0.0]
    notionnel_tranche_t = [tranche["notionnel_tranche"]]
    cashflows_invest = [0.0]        # coupon annuel recu par l'investisseur
    protection_restante = [tranche["notionnel_tranche"]]

    for t in range(1, horizon + 1):
        N_prev = notionnel_port[-1]
        P_cum  = pertes_cumul[-1]

        # Defauts cette annee
        defauts_annee = N_prev * pd_eff * lgd_eff
        # Amortissement (hors defauts)
        amort_annee   = N_prev * tx_amort if not reinvest else 0.0

        N_new  = max(N_prev - defauts_annee - amort_annee, 0.0)
        P_new  = P_cum + defauts_annee
        notionnel_port.append(N_new)
        pertes_cumul.append(P_new)

        # Montants absolus attachment/detachment (suivent le portefeuille)
        attach_m_t = N_new * attach_pct
        detach_m_t = N_new * detach_pct

        # Erosion de la tranche par les pertes cumulees
        # Les pertes rongent d'abord la premiere perte, puis la tranche
        attach_abs_0 = N_total * attach_pct
        detach_abs_0 = N_total * detach_pct

        perte_dans_tranche = max(0.0, min(P_new, detach_abs_0) - attach_abs_0)
        prot_restante = max(tranche["notionnel_tranche"] - perte_dans_tranche, 0.0)
        protection_restante.append(prot_restante)

        # Notionnel de la tranche = min(protection restante, detach_m_t - attach_m_t)
        notionnel_tr_t = max(min(prot_restante, detach_m_t - attach_m_t), 0.0)
        notionnel_tranche_t.append(notionnel_tr_t)

        # Coupon verse a l'investisseur sur le notionnel restant
        coupon_t = notionnel_tr_t * spread_bps / 10_000
        cashflows_invest.append(coupon_t)

    coupon_total = sum(cashflows_invest)

    # ── KPIs ─────────────────────────────────────────────────────
    st.markdown("#### Resultats de projection")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Notionnel final (an %d)" % horizon,
              format_m(notionnel_port[-1]),
              delta=f"-{format_m(N_total - notionnel_port[-1])}")
    c2.metric("Pertes cumulees",
              format_m(pertes_cumul[-1]),
              delta=f"{pertes_cumul[-1]/N_total*100:.2f}% du portef.")
    c3.metric("Protection restante (an %d)" % horizon,
              format_m(protection_restante[-1]))
    c4.metric("Coupons totaux investisseur",
              format_m(coupon_total))

    st.divider()

    # ── Graphiques ───────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["Portefeuille & pertes", "Evolution tranche", "Cashflows investisseur"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=annees, y=notionnel_port,
            name="Notionnel portefeuille", mode="lines+markers",
            line=dict(color="#58a6ff", width=2),
            fill="tozeroy", fillcolor="rgba(88,166,255,0.08)"
        ))
        fig.add_trace(go.Scatter(
            x=annees, y=pertes_cumul,
            name="Pertes cumulees", mode="lines+markers",
            line=dict(color="#f85149", width=2, dash="dot"),
        ))
        # Zone tranche
        attach_abs = [n * attach_pct for n in notionnel_port]
        detach_abs = [n * detach_pct for n in notionnel_port]
        fig.add_trace(go.Scatter(
            x=annees + annees[::-1],
            y=detach_abs + attach_abs[::-1],
            fill="toself", fillcolor="rgba(248,81,73,0.12)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Zone tranche vendue",
        ))
        fig.update_layout(
            title="Evolution du portefeuille et des pertes cumulees",
            plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
            font_color="#e6edf3", title_font_color="#58a6ff",
            xaxis=dict(gridcolor="#30363d", title="Annee", tickvals=annees),
            yaxis=dict(gridcolor="#30363d", title="M€"),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=annees, y=notionnel_tranche_t,
            name="Notionnel tranche", marker_color="#58a6ff", opacity=0.8,
        ))
        fig2.add_trace(go.Scatter(
            x=annees, y=protection_restante,
            name="Protection restante", mode="lines+markers",
            line=dict(color="#d29922", width=2, dash="dash"),
        ))
        fig2.update_layout(
            title="Evolution du notionnel et de la protection restante",
            plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
            font_color="#e6edf3", title_font_color="#58a6ff",
            xaxis=dict(gridcolor="#30363d", title="Annee", tickvals=annees),
            yaxis=dict(gridcolor="#30363d", title="M€"),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=annees[1:], y=cashflows_invest[1:],
            name="Coupon annuel", marker_color="#3fb950", opacity=0.85,
            text=[format_m(c) for c in cashflows_invest[1:]],
            textposition="auto",
        ))
        # Cumul
        cumul = np.cumsum(cashflows_invest[1:]).tolist()
        fig3.add_trace(go.Scatter(
            x=annees[1:], y=cumul,
            name="Cumul coupons", mode="lines+markers",
            line=dict(color="#58a6ff", width=2),
            yaxis="y2",
        ))
        fig3.update_layout(
            title="Cashflows investisseur (coupon annuel + cumul)",
            plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
            font_color="#e6edf3", title_font_color="#58a6ff",
            xaxis=dict(gridcolor="#30363d", title="Annee", tickvals=annees[1:]),
            yaxis=dict(gridcolor="#30363d", title="Coupon annuel (M€)"),
            yaxis2=dict(overlaying="y", side="right", title="Cumul (M€)",
                        gridcolor="#30363d", showgrid=False),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Tableau recapitulatif
        df_cf = pd.DataFrame({
            "Annee":               annees,
            "Notionnel portef. (M)": [round(x,1) for x in notionnel_port],
            "Pertes cumulees (M)": [round(x,2) for x in pertes_cumul],
            "Notionnel tranche (M)": [round(x,2) for x in notionnel_tranche_t],
            "Protection restante (M)": [round(x,2) for x in protection_restante],
            "Coupon investisseur (M)": [round(x,3) for x in cashflows_invest],
        })
        st.dataframe(df_cf, use_container_width=True, hide_index=True)
        csv_cf = df_cf.to_csv(index=False).encode("utf-8")
        st.download_button("Telecharger le tableau (CSV)", csv_cf, "cashflows.csv", "text/csv")


elif page == "🔥 Stress tests":

    st.markdown("# Stress Tests")
    st.markdown("<p style='color:#8b949e'>Impact de chocs PD, LGD et correlation sur les pertes et le capital reglementaire.</p>", unsafe_allow_html=True)

    if "tranche" not in st.session_state:
        st.markdown("<div class='card-accent'>Configure d'abord la tranche dans Structuration tranche.</div>", unsafe_allow_html=True)
        st.stop()

    df_actif = st.session_state.get("df_actif", st.session_state["df"])
    tranche  = st.session_state["tranche"]
    stats    = stats_portefeuille(df_actif)
    N_total  = stats["total"]
    attach_m = tranche["notionnel_attach"]
    detach_m = tranche["notionnel_detach"]
    epaisseur= tranche["notionnel_tranche"]

    from scipy.stats import norm as sp_norm

    # ── Parametres ────────────────────────────────────────────────
    st.divider()
    st.markdown("#### Definition des scenarios de stress")

    col1, col2 = st.columns(2)
    with col1:
        n_sims_stress = st.select_slider("Simulations par scenario",
                        options=[1_000, 5_000, 10_000], value=5_000)
        rho_base = st.slider("Correlation base rho", 0.05, 0.40, 0.20, 0.01)
    with col2:
        seed_stress = st.number_input("Seed", value=99, step=1)

    st.markdown("##### Scenarios")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**Scenario 1 — Recession moderee**")
        pd_m1  = st.slider("Choc PD (x)",  0.5, 5.0, 2.0, 0.1, key="pd_s1")
        lgd_m1 = st.slider("Choc LGD (x)", 0.5, 2.0, 1.2, 0.1, key="lgd_s1")
        rho_s1 = st.slider("Correlation",  0.05, 0.50, 0.25, 0.01, key="rho_s1")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**Scenario 2 — Recession severe**")
        pd_m2  = st.slider("Choc PD (x)",  0.5, 5.0, 3.0, 0.1, key="pd_s2")
        lgd_m2 = st.slider("Choc LGD (x)", 0.5, 2.0, 1.5, 0.1, key="lgd_s2")
        rho_s2 = st.slider("Correlation",  0.05, 0.50, 0.35, 0.01, key="rho_s2")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_c:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**Scenario 3 — Crise systemique**")
        pd_m3  = st.slider("Choc PD (x)",  0.5, 5.0, 4.0, 0.1, key="pd_s3")
        lgd_m3 = st.slider("Choc LGD (x)", 0.5, 2.0, 1.8, 0.1, key="lgd_s3")
        rho_s3 = st.slider("Correlation",  0.05, 0.50, 0.45, 0.01, key="rho_s3")
        st.markdown("</div>", unsafe_allow_html=True)

    run_stress = st.button("Lancer les stress tests")

    # ── Fonction MC rapide ────────────────────────────────────────
    def run_mc(pds, lgds, nots, rho, n_sims, seed):
        rng        = np.random.default_rng(int(seed))
        thresholds = sp_norm.ppf(np.clip(pds, 1e-6, 1-1e-6))
        Z          = rng.standard_normal(n_sims)
        eps        = rng.standard_normal((n_sims, len(pds)))
        X          = np.sqrt(rho)*Z[:,None] + np.sqrt(1-rho)*eps
        defaults   = X < thresholds[None,:]
        losses     = (defaults * lgds[None,:] * nots[None,:]).sum(axis=1)
        tr_losses  = np.clip(losses - attach_m, 0, epaisseur)
        return losses, tr_losses

    if run_stress or "stress_results" in st.session_state:

        if run_stress:
            pds_base  = df_actif["pd"].values
            lgds_base = df_actif["lgd"].values
            nots      = df_actif["notionnel_m"].values

            scenarios = [
                ("Central",           pds_base,                          lgds_base,                          rho_base),
                ("Recession moderee", np.clip(pds_base*pd_m1,  0, 0.99), np.clip(lgds_base*lgd_m1, 0, 0.99), rho_s1),
                ("Recession severe",  np.clip(pds_base*pd_m2,  0, 0.99), np.clip(lgds_base*lgd_m2, 0, 0.99), rho_s2),
                ("Crise systemique",  np.clip(pds_base*pd_m3,  0, 0.99), np.clip(lgds_base*lgd_m3, 0, 0.99), rho_s3),
            ]

            results = {}
            with st.spinner("Stress tests en cours (4 scenarios)..."):
                for name, pds_s, lgds_s, rho_s in scenarios:
                    losses, tr_losses = run_mc(pds_s, lgds_s, nots, rho_s, n_sims_stress, seed_stress)
                    results[name] = {
                        "el":          losses.mean(),
                        "el_pct":      losses.mean() / N_total * 100,
                        "var99":       np.percentile(losses, 99),
                        "es99":        losses[losses >= np.percentile(losses,99)].mean(),
                        "el_tr":       tr_losses.mean(),
                        "el_tr_pct":   tr_losses.mean() / epaisseur * 100 if epaisseur > 0 else 0,
                        "var99_tr":    np.percentile(tr_losses, 99),
                        "prob_touche": (tr_losses > 0).mean() * 100,
                        "losses":      losses,
                        "tr_losses":   tr_losses,
                    }
            st.session_state["stress_results"] = results

        results = st.session_state["stress_results"]
        st.divider()

        # ── Tableau comparatif ────────────────────────────────────
        st.markdown("#### Tableau comparatif des scenarios")

        rows = []
        for name, r in results.items():
            rows.append({
                "Scenario":          name,
                "EL portef. (M)":    f"{r['el']:.1f}",
                "EL portef. (%)":    f"{r['el_pct']:.3f}%",
                "VaR 99% (M)":       f"{r['var99']:.1f}",
                "ES 99% (M)":        f"{r['es99']:.1f}",
                "EL tranche (M)":    f"{r['el_tr']:.2f}",
                "EL tranche (%)":    f"{r['el_tr_pct']:.3f}%",
                "VaR 99% tranche":   f"{r['var99_tr']:.1f}",
                "Prob. touchee (%)": f"{r['prob_touche']:.2f}%",
            })
        df_stress = pd.DataFrame(rows)
        st.dataframe(df_stress, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("#### Visualisation des scenarios")
        tab1, tab2, tab3 = st.tabs(["EL et VaR par scenario", "Distributions superposees", "Impact sur la tranche"])

        colors_scen = {
            "Central":           "#58a6ff",
            "Recession moderee": "#d29922",
            "Recession severe":  "#f0883e",
            "Crise systemique":  "#f85149",
        }

        with tab1:
            noms   = list(results.keys())
            el_v   = [results[n]["el"]    for n in noms]
            var_v  = [results[n]["var99"] for n in noms]
            es_v   = [results[n]["es99"]  for n in noms]

            fig = go.Figure()
            fig.add_trace(go.Bar(name="EL moyen",    x=noms, y=el_v,
                                 marker_color=[colors_scen[n] for n in noms], opacity=0.9))
            fig.add_trace(go.Scatter(name="VaR 99%", x=noms, y=var_v,
                                     mode="markers", marker=dict(color="#e6edf3", size=10, symbol="diamond")))
            fig.add_trace(go.Scatter(name="ES 99%",  x=noms, y=es_v,
                                     mode="markers", marker=dict(color="#3fb950", size=10, symbol="triangle-up")))
            fig.add_hline(y=attach_m, line_dash="dash", line_color="#58a6ff",
                          annotation_text=f"Attachment {tranche['attachment']:.1f}%",
                          annotation_font_color="#58a6ff")
            fig.add_hline(y=detach_m, line_dash="dash", line_color="#f85149",
                          annotation_text=f"Detachment {tranche['detachment']:.1f}%",
                          annotation_font_color="#f85149")
            fig.update_layout(
                title="EL moyen, VaR 99% et ES 99% par scenario",
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#e6edf3", title_font_color="#58a6ff",
                xaxis=dict(gridcolor="#30363d"),
                yaxis=dict(gridcolor="#30363d", title="Pertes (M€)"),
                legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
                barmode="group",
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig2 = go.Figure()
            for name, r in results.items():
                fig2.add_trace(go.Histogram(
                    x=r["losses"], nbinsx=80, name=name,
                    opacity=0.55, histnorm="probability density",
                    marker_color=colors_scen[name],
                ))
            fig2.add_vline(x=attach_m, line_dash="dash", line_color="#58a6ff",
                           annotation_text="Attach", annotation_font_color="#58a6ff")
            fig2.add_vline(x=detach_m, line_dash="dash", line_color="#f85149",
                           annotation_text="Detach", annotation_font_color="#f85149")
            fig2.update_layout(
                title="Distributions des pertes — tous scenarios superposes",
                barmode="overlay",
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#e6edf3", title_font_color="#58a6ff",
                xaxis=dict(gridcolor="#30363d", title="Pertes portefeuille (M€)"),
                yaxis=dict(gridcolor="#30363d", title="Densite"),
                legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
            )
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            noms   = list(results.keys())
            el_tr  = [results[n]["el_tr"]       for n in noms]
            var_tr = [results[n]["var99_tr"]     for n in noms]
            prob_t = [results[n]["prob_touche"]  for n in noms]

            fig3 = go.Figure()
            fig3.add_trace(go.Bar(
                name="EL tranche (M)", x=noms, y=el_tr,
                marker_color=[colors_scen[n] for n in noms], opacity=0.9,
            ))
            fig3.add_trace(go.Scatter(
                name="VaR 99% tranche", x=noms, y=var_tr,
                mode="markers+lines",
                marker=dict(color="#e6edf3", size=10, symbol="diamond"),
                line=dict(color="#e6edf3", dash="dot"),
            ))
            fig3.update_layout(
                title="Impact sur la tranche par scenario",
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#e6edf3", title_font_color="#58a6ff",
                xaxis=dict(gridcolor="#30363d"),
                yaxis=dict(gridcolor="#30363d", title="Pertes tranche (M€)"),
                legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
            )
            st.plotly_chart(fig3, use_container_width=True)

            # Probabilite d'etre touchee
            fig4 = go.Figure(go.Bar(
                x=noms, y=prob_t,
                marker_color=[colors_scen[n] for n in noms],
                text=[f"{p:.1f}%" for p in prob_t], textposition="auto",
            ))
            fig4.update_layout(
                title="Probabilite que la tranche soit touchee (%)",
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#e6edf3", title_font_color="#58a6ff",
                xaxis=dict(gridcolor="#30363d"),
                yaxis=dict(gridcolor="#30363d", title="%"),
                showlegend=False,
            )
            st.plotly_chart(fig4, use_container_width=True)
