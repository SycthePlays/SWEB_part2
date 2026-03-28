import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# -------------------------------
# 🎨 Page Config & Global Styling
# -------------------------------
st.set_page_config(
    page_title="Candidate Assessment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Main background ── */
.stApp {
    background: linear-gradient(135deg, #0A1628 0%, #0D1F3C 50%, #0A1628 100%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1F3C 0%, #091729 100%);
    border-right: 1px solid rgba(74, 144, 217, 0.15);
}

[data-testid="stSidebar"] .stSlider > div > div > div {
    background: rgba(74, 144, 217, 0.2);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* ── Sidebar title ── */
[data-testid="stSidebar"] h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem !important;
    color: #E8EDF5 !important;
    letter-spacing: 0.02em;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(74, 144, 217, 0.4);
    margin-bottom: 1.5rem !important;
}

[data-testid="stSidebar"] h3 {
    color: #4A90D9 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 1.5rem !important;
    margin-bottom: 0.5rem !important;
    padding-left: 2px;
}

/* ── Slider label color ── */
[data-testid="stSidebar"] label {
    color: #A8B8D0 !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
}

/* ── Slider accent ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background-color: #4A90D9 !important;
    border-color: #4A90D9 !important;
    box-shadow: 0 0 8px rgba(74, 144, 217, 0.5) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(74, 144, 217, 0.06) !important;
    border: 1px dashed rgba(74, 144, 217, 0.3) !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] label {
    color: #A8B8D0 !important;
}

/* ── Main area heading ── */
.main-header {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #E8EDF5;
    letter-spacing: 0.01em;
    margin-bottom: 0.25rem;
    line-height: 1.2;
}

.main-subheader {
    color: #4A90D9;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #E8EDF5;
    margin-top: 2rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(74, 144, 217, 0.2);
}

/* ── Search / Selectbox ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(13, 31, 60, 0.8) !important;
    border: 1px solid rgba(74, 144, 217, 0.2) !important;
    border-radius: 6px !important;
    color: #E8EDF5 !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: rgba(74, 144, 217, 0.6) !important;
    box-shadow: 0 0 0 2px rgba(74, 144, 217, 0.12) !important;
}

/* ── Warning / Info box ── */
.stAlert {
    background: rgba(74, 144, 217, 0.08) !important;
    border: 1px solid rgba(74, 144, 217, 0.25) !important;
    border-radius: 8px !important;
    color: #A8B8D0 !important;
}

/* ── Plotly chart background ── */
.js-plotly-plot .plotly .bg {
    fill: transparent !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0A1628; }
::-webkit-scrollbar-thumb { background: rgba(74, 144, 217, 0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(74, 144, 217, 0.55); }

/* ── Controls row ── */
.controls-row {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
    margin-bottom: 1.25rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🎯 Sidebar: Upload & Parameters
# -------------------------------

st.sidebar.title("Parameter Penilaian")

uploaded_file = st.sidebar.file_uploader("Pilih file CSV kandidat", type=["csv"])

# Logical Thinking
st.sidebar.subheader("Logical Thinking")
w_uni = st.sidebar.slider("Bobot University", 0.0, 1.0, 0.7, 0.01)
w_gpa = st.sidebar.slider("Bobot GPA", 0.0, 1.0, 0.3, 0.01)

# Analytical Skills
st.sidebar.subheader("Analytical Skills")
w_intern = st.sidebar.slider("Bobot Internship", 0.0, 1.0, 0.6, 0.01)
w_ach = st.sidebar.slider("Bobot Academic Achievement", 0.0, 1.0, 0.2, 0.01)
w_case = st.sidebar.slider("Bobot Business Case", 0.0, 1.0, 0.2, 0.01)

# Leadership
st.sidebar.subheader("Leadership")
w_type = st.sidebar.slider("Bobot Org Type", 0.0, 1.0, 0.3, 0.01)
w_role = st.sidebar.slider("Bobot Org Role", 0.0, 1.0, 0.7, 0.01)

# Overall Score
st.sidebar.subheader("Overall Score")
w_LT = st.sidebar.slider("Bobot Logical Thinking", 0.0, 1.0, 0.3, 0.01)
w_ANA = st.sidebar.slider("Bobot Analytical Skills", 0.0, 1.0, 0.4, 0.01)
w_LS = st.sidebar.slider("Bobot Leadership", 0.0, 1.0, 0.4, 0.01)

# -------------------------------
# 🧠 Evaluation Function
# -------------------------------
def evaluate_candidates(df_sorted, weights):
    w_uni, w_gpa, w_intern, w_ach, w_case, w_type, w_role, w_LT, w_ANA, w_LS = weights

    n = len(df_sorted)
    data_Uni = [0]*n; data_GPA = [0]*n; data_LT = [0]*n
    data_in = [0]*n; data_ach = [0]*n; data_ach_busi = [0]*n; data_ana = [0]*n
    data_Exp = [0]*n; data_Role = [0]*n; data_LS = [0]*n

    for x in range(n):
        s = df_sorted["Degree|radio-4"].iloc[x]
        if s == "S2 - Master Degree":
            data_Uni[x] = 100
        else:
            s1 = df_sorted["Name of University|radio-2"].iloc[x]
            if df_sorted["Country in which the university is located|radio-3"].iloc[x] == "Other":
                data_Uni[x] = 100
            elif s1 in ["Universitas Indonesia (UI)", "Institut Teknologi Bandung (ITB)", "Universitas Gadjah Mada (UGM)"]:
                data_Uni[x] = 100
            elif any(k in s1 for k in ["Brawijaya", "ITS", "UNAIR", "UNDIP", "IPB", "UNPAD", "PRASMUL"]):
                data_Uni[x] = 70
            elif s1 == "Other":
                s2 = str(df_sorted["University Name|text-6"].iloc[x]).lower()
                if any(k in s2 for k in ["binus", "prasetiya", "prasetya", "prasmul"]):
                    data_Uni[x] = 70
                else:
                    data_Uni[x] = 40

        try:
            s_gpa = float(df_sorted["GPA|number-3"].iloc[x])
        except Exception:
            s_gpa = 0.0
        if s_gpa >= 3.75: data_GPA[x] = 100
        elif s_gpa >= 3.5: data_GPA[x] = 70
        elif s_gpa >= 3.2: data_GPA[x] = 40
        else: data_GPA[x] = 0

        denom_lt = (w_uni + w_gpa) if (w_uni + w_gpa) != 0 else 1
        data_LT[x] = (data_Uni[x]*w_uni + data_GPA[x]*w_gpa) / denom_lt

        s_org = df_sorted["Have you ever had organizational experience?|radio-18"].iloc[x]
        if s_org == "No":
            data_Exp[x] = 0; data_Role[x] = 0
        else:
            s_type = df_sorted["Organization Type|radio-21"].iloc[x]
            data_Exp[x] = {"International": 100, "National": 70}.get(s_type, 40)
            s_role = df_sorted["Organization Role|radio-19"].iloc[x]
            data_Role[x] = {"Chief or Core Management": 100, "Team Leader (Division or Department Head)": 70}.get(s_role, 40)

        denom_ls = (w_type + w_role) if (w_type + w_role) != 0 else 1
        data_LS[x] = (data_Exp[x]*w_type + data_Role[x]*w_role) / denom_ls

        s_intern = df_sorted["Have you completed any internship?|radio-7"].iloc[x]
        s6 = df_sorted["Have you had any full-time work experience?|radio-5"].iloc[x]
        if s_intern == "No" and s6 == "No":
            data_in[x] = 0
        else:
            if s_intern == "Consulting Firm" or s6 == "Yes": data_in[x] = 100
            elif s_intern in ["Private Companies", "Startup / Tech Companies"]: data_in[x] = 70
            else: data_in[x] = 40

        s_ach = df_sorted["Have you received any academic related achievements?|radio-10"].iloc[x]
        if s_ach == "No":
            data_ach[x] = 0; data_ach_busi[x] = 0
        else:
            data_ach[x] = {"International Level": 100, "National Level": 85}.get(s_ach, 70)
            s_case = df_sorted["Have you ever participated in a business case competition?|radio-15"].iloc[x]
            data_ach_busi[x] = {"Yes, as a winner/finalist": 100, "Yes, as a participant": 50}.get(s_case, 0)

        denom_ana = (w_intern + w_ach + w_case) if (w_intern + w_ach + w_case) != 0 else 1
        data_ana[x] = (data_in[x]*w_intern + data_ach[x]*w_ach + data_ach_busi[x]*w_case) / denom_ana

    df_out = pd.DataFrame({
        "Email": df_sorted.get("Email Address|email-1", pd.Series([""]*n)),
        "Name": df_sorted["Full Name|name-1"],
        "Submission Date": df_sorted.get("Submission Date|hidden-3", pd.Series([""]*n)),
        "LT_score": data_LT, "AS_score": data_ana, "LS_score": data_LS,
        "Uni_score": data_Uni, "GPA_score": data_GPA,
        "Internship_score": data_in, "Achievement_score": data_ach,
        "BusinessCase_score": data_ach_busi, "OrgType_score": data_Exp, "OrgRole_score": data_Role
    })

    denom_overall = (w_LT + w_ANA + w_LS) if (w_LT + w_ANA + w_LS) != 0 else 1
    df_out["Overall"] = (df_out["LT_score"]*w_LT + df_out["AS_score"]*w_ANA + df_out["LS_score"]*w_LS) / denom_overall
    df_out["Overall"] = df_out["Overall"].round(2)

    df_out["Logical Thinking_display"] = df_out.apply(lambda r: {"title": "Logical Thinking", "rows": [("University", int(r['Uni_score'])), ("GPA", int(r['GPA_score'])), ("OVR", round(r['LT_score'], 2))]}, axis=1)
    df_out["Analytical Skills_display"] = df_out.apply(lambda r: {"title": "Analytical Skills", "rows": [("Internship", int(r['Internship_score'])), ("Achievement", int(r['Achievement_score'])), ("Business Case", int(r['BusinessCase_score'])), ("OVR", round(r['AS_score'], 2))]}, axis=1)
    df_out["Leadership_display"] = df_out.apply(lambda r: {"title": "Leadership", "rows": [("Org Type", int(r['OrgType_score'])), ("Org Role", int(r['OrgRole_score'])), ("OVR", round(r['LS_score'], 2))]}, axis=1)

    return df_out

# -------------------------------
# Helper: Score color gradient
# -------------------------------
def score_color(val):
    """Returns a color for a 0–100 score: red → amber → blue-green."""
    try:
        v = float(val)
    except Exception:
        return "#A8B8D0"
    if v >= 80:
        return "#4A90D9"
    elif v >= 60:
        return "#5BB8A0"
    elif v >= 40:
        return "#E0A030"
    else:
        return "#C85A5A"

def overall_badge_color(val):
    try:
        v = float(val)
    except Exception:
        return "#A8B8D0"
    if v >= 80: return "linear-gradient(135deg,#4A90D9,#2E6EBF)"
    elif v >= 60: return "linear-gradient(135deg,#5BB8A0,#3A9880)"
    elif v >= 40: return "linear-gradient(135deg,#E0A030,#C08020)"
    else: return "linear-gradient(135deg,#C85A5A,#A03A3A)"

# -------------------------------
# Helper: render HTML table
# -------------------------------
def render_summary_html(df_display):
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
        background: transparent;
        font-family: 'DM Sans', sans-serif;
        color: #E8EDF5;
    }

    .tbl-wrap {
        width: 100%;
        overflow-x: auto;
    }

    .summary-table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        color: #E8EDF5;
        background: transparent;
    }

    /* ── Header ── */
    .summary-table thead tr {
        background: linear-gradient(90deg, #0D1F3C 0%, #112340 100%);
    }
    .summary-table th {
        padding: 14px 16px;
        text-align: left;
        font-weight: 600;
        font-size: 11px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #4A90D9;
        border-bottom: 1px solid rgba(74,144,217,0.25);
        white-space: nowrap;
        position: sticky;
        top: 0;
        z-index: 2;
        background: #0D1F3C;
    }
    .summary-table th:first-child { border-radius: 8px 0 0 0; }
    .summary-table th:last-child  { border-radius: 0 8px 0 0; }

    /* ── Rows ── */
    .summary-table tbody tr {
        background: rgba(13,31,60,0.6);
        transition: background 0.2s ease;
        border-bottom: 1px solid rgba(74,144,217,0.08);
    }
    .summary-table tbody tr:hover {
        background: rgba(74,144,217,0.08);
    }
    .summary-table tbody tr:nth-child(even) {
        background: rgba(10,22,40,0.7);
    }
    .summary-table tbody tr:nth-child(even):hover {
        background: rgba(74,144,217,0.08);
    }

    .summary-table td {
        padding: 14px 16px;
        vertical-align: top;
        border-bottom: 1px solid rgba(74,144,217,0.07);
    }

    /* ── Index ── */
    .index-cell {
        text-align: center;
        color: rgba(74,144,217,0.6);
        font-weight: 600;
        font-size: 12px;
        width: 44px;
        min-width: 44px;
    }

    /* ── Name ── */
    .name-cell {
        font-weight: 600;
        color: #E8EDF5;
        white-space: nowrap;
        min-width: 140px;
    }

    /* ── Meta (email, date) ── */
    .meta {
        color: #6B8BAF;
        font-size: 12px;
        font-weight: 400;
    }

    /* ── Category card ── */
    .cat-card {
        background: rgba(74,144,217,0.05);
        border: 1px solid rgba(74,144,217,0.12);
        border-radius: 8px;
        padding: 10px 12px;
        min-width: 150px;
    }

    .cat-title {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #4A90D9;
        margin-bottom: 8px;
        display: block;
    }

    .sub-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 4px 0;
        gap: 12px;
    }

    .sub-label {
        font-size: 12px;
        color: #8AA8CC;
        font-weight: 400;
        flex: 1;
    }

    .sub-value {
        font-size: 12px;
        font-weight: 700;
        text-align: right;
        min-width: 32px;
    }

    .ovr-row {
        margin-top: 6px;
        padding-top: 6px;
        border-top: 1px solid rgba(74,144,217,0.15);
    }

    .ovr-label {
        font-size: 11px;
        font-weight: 700;
        color: #4A90D9;
        letter-spacing: 0.05em;
    }

    .ovr-value {
        font-size: 13px;
        font-weight: 700;
        color: #E8EDF5;
    }

    /* ── Overall badge ── */
    .overall-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
        color: #fff;
        text-align: center;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .overall-cell {
        text-align: center;
        vertical-align: middle !important;
        min-width: 80px;
    }

    /* ── Scrollbar inside table ── */
    .tbl-wrap::-webkit-scrollbar { height: 4px; }
    .tbl-wrap::-webkit-scrollbar-track { background: transparent; }
    .tbl-wrap::-webkit-scrollbar-thumb { background: rgba(74,144,217,0.25); border-radius: 2px; }
    </style>
    """

    header = """
    <div class="tbl-wrap">
    <table class="summary-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Email</th>
          <th>Name</th>
          <th>Submission Date</th>
          <th>Logical Thinking</th>
          <th>Analytical Skills</th>
          <th>Leadership</th>
          <th>Overall</th>
        </tr>
      </thead>
      <tbody>
    """

    rows_html = ""
    for idx, (_, r) in enumerate(df_display.iterrows(), start=1):
        lt = r["Logical Thinking_display"]
        an = r["Analytical Skills_display"]
        ls = r["Leadership_display"]

        def render_cat(cat):
            inner = f'<div class="cat-card"><span class="cat-title">{cat["title"]}</span>'
            rows = cat["rows"]
            for i, (label, val) in enumerate(rows):
                is_ovr = (label == "OVR")
                color = score_color(val) if not is_ovr else "#E8EDF5"
                if is_ovr:
                    inner += f'<div class="sub-row ovr-row"><span class="sub-label ovr-label">OVR</span><span class="sub-value ovr-value" style="color:{color}">{val}</span></div>'
                else:
                    inner += f'<div class="sub-row"><span class="sub-label">{label}</span><span class="sub-value" style="color:{color}">{val}</span></div>'
            inner += '</div>'
            return inner

        lt_html = render_cat(lt)
        an_html = render_cat(an)
        ls_html = render_cat(ls)

        badge_bg = overall_badge_color(r['Overall'])
        overall_html = f'<span class="overall-badge" style="background:{badge_bg}">{r["Overall"]}</span>'

        rows_html += f"""
        <tr>
          <td class="index-cell">{idx}</td>
          <td class="meta">{r.get('Email','')}</td>
          <td class="name-cell">{r['Name']}</td>
          <td class="meta">{r.get('Submission Date','')}</td>
          <td>{lt_html}</td>
          <td>{an_html}</td>
          <td>{ls_html}</td>
          <td class="overall-cell">{overall_html}</td>
        </tr>
        """

    footer = """
      </tbody>
    </table>
    </div>
    """

    return css + header + rows_html + footer

# -------------------------------
# 📊 Main App Logic
# -------------------------------

# Page header
st.markdown('<p class="main-subheader">Candidate Evaluation Dashboard</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">Penilaian Kandidat</h1>', unsafe_allow_html=True)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df_sorted = df.sort_values(by="Full Name|name-1").reset_index(drop=True)
    weights = (w_uni, w_gpa, w_intern, w_ach, w_case, w_type, w_role, w_LT, w_ANA, w_LS)
    temp1 = evaluate_candidates(df_sorted, weights)

    st.markdown('<div class="section-heading">Tabel Ringkasan Penilaian</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍  Cari nama kandidat", value="", placeholder="Ketik nama...")
    with col2:
        sort_by = st.selectbox(
            "Urutkan berdasarkan",
            options=["Nama A → Z", "Nama Z → A", "Overall Tertinggi", "Overall Terendah"],
            index=0
        )

    if search_query.strip() != "":
        mask = temp1["Name"].str.contains(search_query.strip(), case=False, na=False)
        filtered = temp1[mask].copy()
    else:
        filtered = temp1.copy()

    if sort_by == "Nama A → Z":
        filtered = filtered.sort_values(by="Name", ascending=True).reset_index(drop=True)
    elif sort_by == "Nama Z → A":
        filtered = filtered.sort_values(by="Name", ascending=False).reset_index(drop=True)
    elif sort_by == "Overall Tertinggi":
        filtered = filtered.sort_values(by="Overall", ascending=False).reset_index(drop=True)
    else:
        filtered = filtered.sort_values(by="Overall", ascending=True).reset_index(drop=True)

    html_table = render_summary_html(filtered)
    approx_height = 160 + len(filtered) * 130
    height = min(max(approx_height, 300), 2400)
    components.html(html_table, height=height, scrolling=True)

    # ── Radar Chart ──
    st.markdown('<div class="section-heading">Visualisasi Radar Kandidat</div>', unsafe_allow_html=True)

    names_list = filtered["Name"].tolist()
    if names_list:
        selected_name = st.selectbox("Pilih kandidat:", names_list)
        row = filtered[filtered["Name"] == selected_name].iloc[0]

        categories = ["Logical Thinking", "Analytical Skills", "Leadership"]
        values = [row["LT_score"], row["AS_score"], row["LS_score"]]
        values_closed = values + [values[0]]
        categories_closed = categories + [categories[0]]

        fig = go.Figure(data=[
            go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                name=row["Name"],
                line=dict(color='#4A90D9', width=2),
                fillcolor='rgba(74,144,217,0.18)',
                marker=dict(color='#4A90D9', size=7)
            )
        ])

        fig.update_layout(
            polar=dict(
                bgcolor='rgba(13,31,60,0.6)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color='#6B8BAF', size=10),
                    gridcolor='rgba(74,144,217,0.15)',
                    linecolor='rgba(74,144,217,0.2)',
                ),
                angularaxis=dict(
                    tickfont=dict(color='#A8B8D0', size=12, family='DM Sans'),
                    gridcolor='rgba(74,144,217,0.12)',
                    linecolor='rgba(74,144,217,0.2)',
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            title=dict(
                text=f"{row['Name']}",
                font=dict(color='#E8EDF5', size=16, family='DM Sans'),
                x=0.5
            ),
            margin=dict(t=60, b=40, l=40, r=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada kandidat yang cocok dengan pencarian.")

else:
    # Empty state
    st.markdown("""
    <div style="
        margin-top: 4rem;
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(13,31,60,0.5);
        border: 1px solid rgba(74,144,217,0.15);
        border-radius: 16px;
        max-width: 540px;
        margin-left: auto;
        margin-right: auto;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">📂</div>
        <div style="
            font-family: 'DM Sans', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #E8EDF5;
            margin-bottom: 0.5rem;
        ">Unggah File CSV</div>
        <div style="
            font-size: 0.875rem;
            color: #6B8BAF;
            line-height: 1.6;
        ">Silakan unggah file CSV kandidat<br>melalui sidebar untuk memulai penilaian.</div>
    </div>
    """, unsafe_allow_html=True)
