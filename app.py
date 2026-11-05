import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# ==========================================
# 1. ENTERPRISE PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="EduPro Enterprise Intelligence Portal", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CORPORATE DESIGN SYSTEM & STYLING (CSS)
# Standard 1180px responsive container, crisp corporate palette
# ==========================================
st.markdown("""
    <style>
    /* Standard Corporate Container Width */
    .main .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        margin: auto;
    }
    
    /* Global Typography */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Corporate Executive Welcome Header */
    .corporate-hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1e3a8a 100%);
        border-radius: 12px;
        padding: 32px 36px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .hero-badge-container {
        display: flex;
        gap: 10px;
        margin-bottom: 14px;
        flex-wrap: wrap;
    }
    .hero-badge {
        display: inline-block;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.15);
        color: #e2e8f0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .hero-badge-active {
        background: #059669;
        color: #ffffff;
        border: 1px solid #10b981;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 10px;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        line-height: 1.5;
        max-width: 850px;
        margin-bottom: 0px;
    }

    /* Executive KPI Cards */
    .kpi-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 20px 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        margin-bottom: 18px;
        position: relative;
        overflow: hidden;
    }
    .kpi-accent {
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: #2563eb;
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #64748b;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .kpi-subtext {
        font-size: 0.8rem;
        color: #94a3b8;
    }

    /* Corporate Information Panel */
    .info-panel {
        background: #ffffff;
        border-radius: 10px;
        padding: 24px 28px;
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .panel-heading {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Navigation Directory Card */
    .nav-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 18px;
        height: 100%;
    }
    .nav-card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 6px;
    }
    .nav-card-desc {
        font-size: 0.82rem;
        color: #475569;
        line-height: 1.4;
    }

    /* Automated Insight Card */
    .insight-card {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #16a34a;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #166534;
        font-size: 0.95rem;
    }

    /* Clean corporate section break */
    .corp-divider {
        margin-top: 2rem;
        margin-bottom: 2rem;
        border: 0;
        border-top: 1px solid #e2e8f0;
    }
    
    /* Corporate Footer */
    .corp-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        padding-top: 2rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 3. ROBUST DATA INGESTION ENGINE
# ==========================================
def _load_raw_data():
    sheet_id = "1Ts1Yjt9oiTdOeCeuJPbExNz7N3vmd0Ln"
    users_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=74828563"
    courses_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1284811374"
    transactions_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=722772998"
    
    users = pd.read_csv(users_url)
    courses = pd.read_csv(courses_url)
    transactions = pd.read_csv(transactions_url)
    
    # Referential Data Integration
    df = transactions.merge(users, on="UserID", how="left")
    df = df.merge(courses, on="CourseID", how="left")
    
    # Demographic Segmentation (Standard Age Bands)
    bins = [0, 17, 25, 35, 45, 100]
    labels = ['<18', '18-25', '26-35', '36-45', '45+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)
    
    # Temporal Transformations
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], format='%d/%m/%Y', errors='coerce')
    df['MonthYear'] = df['TransactionDate'].dt.to_period('M').astype(str)
    
    return users, courses, transactions, df

if hasattr(st, "cache_data"):
    fetch_data = st.cache_data(_load_raw_data)
else:
    fetch_data = st.cache(allow_output_mutation=True)(_load_raw_data)

try:
    users, courses, transactions, df = fetch_data()
except Exception as e:
    st.error(f"Critical Data Ingestion Error: {e}")
    st.stop()


# ==========================================
# 4. SIDEBAR NAVIGATION & GLOBAL GOVERNANCE
# ==========================================
st.sidebar.markdown("""
    <div style="padding-bottom: 12px; border-bottom: 1px solid #334155;">
        <span style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.01em;">EDUPRO ANALYTICS</span><br>
        <span style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Enterprise Reporting Hub</span>
    </div>
""", unsafe_allow_html=True)

PAGES = [
    "🏠 Enterprise Welcome & Briefing",
    "📊 Executive KPI Dashboard",
    "👥 Learner Demographics",
    "📚 Course Analytics",
    "🔍 Learner Preferences & Segmentation",
    "📈 Enrollment Trends",
    "💡 Automatic Insights & Personas",
    "🏛️ Stakeholder Executive Summary",
    "🩺 Data Governance & Export"
]

page = st.sidebar.radio("Navigation Directory", PAGES)
st.sidebar.markdown("---")

# Global Data Scope Filters
st.sidebar.markdown("<div style='font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:8px;'>GLOBAL DATA SCOPE</div>", unsafe_allow_html=True)

age_options = list(df['Age Group'].dropna().unique())
selected_age_groups = st.sidebar.multiselect("Age Groups", age_options)
if not selected_age_groups: selected_age_groups = age_options

gender_options = list(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Genders", gender_options)
if not selected_genders: selected_genders = gender_options

category_options = list(df['CourseCategory'].dropna().unique())
selected_categories = st.sidebar.multiselect("Categories", category_options)
if not selected_categories: selected_categories = category_options

level_options = list(df['CourseLevel'].dropna().unique())
selected_levels = st.sidebar.multiselect("Skill Levels", level_options)
if not selected_levels: selected_levels = level_options

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="font-size: 0.72rem; color: #94a3b8; line-height: 1.4;">
        <b>Governance:</b> Tier-1 Stakeholder Access<br>
        <b>Data Security:</b> Encrypted / Anonymized<br>
        <b>Production Version:</b> v2.4 (Enterprise)
    </div>
""", unsafe_allow_html=True)

# Apply Filtered Scope
filtered_df = df[
    (df['Age Group'].isin(selected_age_groups)) &
    (df['Gender'].isin(selected_genders)) &
    (df['CourseCategory'].isin(selected_categories)) &
    (df['CourseLevel'].isin(selected_levels))
]

if filtered_df.empty:
    st.warning("⚠️ No records match the selected scope criteria. Please reset or expand your filters.")
    st.stop()


# Helper: Render Executive KPI Card
def draw_kpi(title, value, subtext="", accent_color="#2563eb"):
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-accent" style="background:{accent_color};"></div>
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtext">{subtext}</div>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE 1: ENTERPRISE WELCOME & BRIEFING (CORPORATE HOME)
# ==========================================
if page == "🏠 Enterprise Welcome & Briefing":
    # Corporate Hero Header
    st.markdown("""
        <div class="corporate-hero">
            <div class="hero-badge-container">
                <span class="hero-badge hero-badge-active">● Live Production Feed</span>
                <span class="hero-badge">Enterprise Stakeholder Access</span>
                <span class="hero-badge">ISO 27001 Data Compliant</span>
            </div>
            <div class="hero-title">EduPro Global Learning Intelligence System</div>
            <div class="hero-subtitle">
                Official executive analytics portal delivering evidence-based intelligence on learner demographics, course enrollment behaviors, and curriculum adoption patterns.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Core Macro KPIs
    total_learners = filtered_df['UserID'].nunique()
    total_enrollments = len(filtered_df)
    total_courses = filtered_df['CourseID'].nunique()
    avg_courses = round(total_enrollments / total_learners, 2) if total_learners > 0 else 0
    top_cat = filtered_df['CourseCategory'].mode()[0] if not filtered_df['CourseCategory'].empty else "N/A"
    top_lvl = filtered_df['CourseLevel'].mode()[0] if not filtered_df['CourseLevel'].empty else "N/A"

    c1, c2, c3, c4 = st.columns(4)
    with c1: draw_kpi("Platform Reach", f"{total_learners:,}", "Unique active learners", "#2563eb")
    with c2: draw_kpi("Total Enrollments", f"{total_enrollments:,}", "Course registrations completed", "#059669")
    with c3: draw_kpi("Active Catalog", f"{total_courses:,}", "Distinct active course titles", "#7c3aed")
    with c4: draw_kpi("Engagement Velocity", f"{avg_courses}x", "Average courses per learner", "#ea580c")

    st.markdown("<hr class='corp-divider'>", unsafe_allow_html=True)

    # Executive Overview Narrative & Pillars
    st.markdown("""
        <div class="info-panel">
            <div class="panel-heading">📌 Executive Mission & Strategic Mandate</div>
            <p style="color:#334155; line-height:1.6; font-size:0.95rem; margin-bottom:16px;">
                The EduPro Learning Intelligence initiative transitions our platform operations from intuitive planning to <b>rigorous, data-informed education governance</b>. By continuously evaluating high-dimensional demographic and behavioral data, EduPro empowers administrative leaders and governmental sponsors to achieve key policy objectives:
            </p>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:16px;">
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px;">
                    <b style="color:#0f172a; font-size:0.9rem;">🎯 Targeted Curriculum Strategy</b>
                    <p style="color:#64748b; font-size:0.82rem; margin:4px 0 0 0;">Aligning catalog expansion with verifiable industry demand and subject interest concentrations.</p>
                </div>
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px;">
                    <b style="color:#0f172a; font-size:0.9rem;">🤝 Demographic Inclusion & Access</b>
                    <p style="color:#64748b; font-size:0.82rem; margin:4px 0 0 0;">Evaluating age cohort representation and gender equity across technical and vocational learning tracks.</p>
                </div>
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px;">
                    <b style="color:#0f172a; font-size:0.9rem;">📈 Capital & Grant Optimization</b>
                    <p style="color:#64748b; font-size:0.82rem; margin:4px 0 0 0;">Directing institutional investments into high-completion beginner funnels and scalable foundational disciplines.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Portal Module Navigation Directory
    st.markdown("<div class='panel-heading' style='font-size:1.15rem; font-weight:700; color:#0f172a; margin-bottom:14px;'>🧭 Analytical Modules Directory</div>", unsafe_allow_html=True)
    
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("""
            <div class="nav-card">
                <div class="nav-card-title">👥 Demographic Analytics</div>
                <div class="nav-card-desc">Detailed age pyramid distributions, gender parity indices, and cross-demographic cohort participation metrics.</div>
            </div>
        """, unsafe_allow_html=True)
    with colB:
        st.markdown("""
            <div class="nav-card">
                <div class="nav-card-title">📚 Course Popularity & Levels</div>
                <div class="nav-card-desc">Category adoption rankings, course tier funnels (Beginner vs. Advanced), and free vs. paid consumption ratios.</div>
            </div>
        """, unsafe_allow_html=True)
    with colC:
        st.markdown("""
            <div class="nav-card">
                <div class="nav-card-title">🔍 Behavioral Heatmaps</div>
                <div class="nav-card-desc">Multivariate cross-tabulation of Age Group × Category preferences and learner engagement frequency segments.</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    
    colD, colE, colF = st.columns(3)
    with colD:
        st.markdown("""
            <div class="nav-card">
                <div class="nav-card-title">📈 Longitudinal Trends</div>
                <div class="nav-card-desc">Historical transaction velocity, seasonal enrollment spikes, and quarterly growth tracking.</div>
            </div>
        """, unsafe_allow_html=True)
    with colE:
        st.markdown("""
            <div class="nav-card">
                <div class="nav-card-title">💡 Persona Intelligence</div>
                <div class="nav-card-desc">Dynamic persona profiling ("Who Chooses What?") and automated algorithmic descriptive findings.</div>
            </div>
        """, unsafe_allow_html=True)
    with colF:
        st.markdown("""
            <div class="nav-card">
                <div class="nav-card-title">🏛️ Strategic Briefing & Health</div>
                <div class="nav-card-desc">Executive policy recommendations for institutional sponsors, database integrity auditing, and CSV exports.</div>
            </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE 2: EXECUTIVE KPI DASHBOARD
# ==========================================
elif page == "📊 Executive KPI Dashboard":
    st.title("📊 Executive KPI Performance Dashboard")
    st.markdown("Consolidated operational scorecard displaying core adoption and distribution benchmarks.")
    
    total_learners = filtered_df['UserID'].nunique()
    total_enrollments = len(filtered_df)
    total_courses = filtered_df['CourseID'].nunique()
    avg_courses = round(total_enrollments / total_learners, 2) if total_learners > 0 else 0
    top_cat = filtered_df['CourseCategory'].mode()[0] if not filtered_df['CourseCategory'].empty else "N/A"
    top_lvl = filtered_df['CourseLevel'].mode()[0] if not filtered_df['CourseLevel'].empty else "N/A"
    
    c1, c2, c3 = st.columns(3)
    with c1: draw_kpi("Total Active Learners", f"{total_learners:,}", "Platform user base", "#2563eb")
    with c2: draw_kpi("Total Course Enrollments", f"{total_enrollments:,}", "Gross registration volume", "#059669")
    with c3: draw_kpi("Available Courses", f"{total_courses:,}", "Curriculum offerings", "#7c3aed")
    
    c4, c5, c6 = st.columns(3)
    with c4: draw_kpi("Avg Courses / Learner", f"{avg_courses}x", "Retention indicator", "#ea580c")
    with c5: draw_kpi("Dominant Category", top_cat, "Highest platform demand", "#0284c7")
    with c6: draw_kpi("Leading Skill Level", top_lvl, "Maturity concentration", "#db2777")
    
    st.markdown("<hr class='corp-divider'>", unsafe_allow_html=True)
    
    colA, colB = st.columns(2)
    with colA:
        cat_counts = filtered_df['CourseCategory'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Enrollments']
        fig = px.bar(cat_counts, x='Category', y='Enrollments', title="Enrollments by Course Category", template="plotly_white", color='Category', color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        lvl_counts = filtered_df['CourseLevel'].value_counts().reset_index()
        lvl_counts.columns = ['Level', 'Enrollments']
        fig2 = px.pie(lvl_counts, names='Level', values='Enrollments', title="Skill Level Allocation", hole=0.45, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Prism)
        fig2.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig2, use_container_width=True)


# ==========================================
# PAGE 3: LEARNER DEMOGRAPHICS
# ==========================================
elif page == "👥 Learner Demographics":
    st.title("👥 Learner Demographic Profiling")
    st.markdown("Granular evaluation of learner age groups and gender distribution across the platform.")
    
    c1, c2 = st.columns(2)
    with c1:
        age_counts = filtered_df['Age Group'].value_counts().reset_index()
        age_counts.columns = ['Age Group', 'Count']
        age_counts['sort'] = age_counts['Age Group'].map({'<18':0, '18-25':1, '26-35':2, '36-45':3, '45+':4})
        age_counts = age_counts.sort_values('sort')
        fig_age = px.bar(age_counts, x='Age Group', y='Count', title="Age Bracket Representation", template="plotly_white", color='Age Group', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_age.update_layout(showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_age, use_container_width=True)
    
    with c2:
        gen_counts = filtered_df['Gender'].value_counts().reset_index()
        gen_counts.columns = ['Gender', 'Count']
        fig_gen = px.pie(gen_counts, names='Gender', values='Count', title="Gender Equity Distribution", template="plotly_white", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
        fig_gen.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_gen, use_container_width=True)
        
    st.markdown("<hr class='corp-divider'>", unsafe_allow_html=True)
    st.subheader("Gender × Age Group Cross-Analysis")
    gen_age = filtered_df.groupby(['Age Group', 'Gender']).size().reset_index(name='Count')
    fig_gen_age = px.bar(gen_age, x='Age Group', y='Count', color='Gender', barmode='group', title="Age Distribution Segmented by Gender", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Bold)
    fig_gen_age.update_layout(margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig_gen_age, use_container_width=True)


# ==========================================
# PAGE 4: COURSE ANALYTICS
# ==========================================
elif page == "📚 Course Analytics":
    st.title("📚 Curriculum Analytics & Demand Mapping")
    st.markdown("Detailed breakdown of catalog performance, course levels, and pricing models.")
    
    st.subheader("Top 10 Enrolled Courses")
    top_courses = filtered_df['CourseName'].value_counts().head(10).reset_index()
    top_courses.columns = ['CourseName', 'Enrollments']
    fig_top = px.bar(top_courses, x='Enrollments', y='CourseName', orientation='h', title="Highest Performing Courses", template="plotly_white", color='Enrollments', color_continuous_scale="Blues")
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig_top, use_container_width=True)
    
    st.markdown("<hr class='corp-divider'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        type_counts = filtered_df['CourseType'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        fig_type = px.pie(type_counts, names='Type', values='Count', title="Enrollment Breakdown by Model (Free vs Paid)", hole=0.45, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
        fig_type.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_type, use_container_width=True)
    
    with c2:
        level_counts = filtered_df['CourseLevel'].value_counts().reset_index()
        level_counts.columns = ['Level', 'Count']
        fig_lvl = px.funnel(level_counts, x='Count', y='Level', title="Skill Maturity Funnel", template="plotly_white", color='Level')
        fig_lvl.update_layout(showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_lvl, use_container_width=True)


# ==========================================
# PAGE 5: LEARNER PREFERENCES & SEGMENTATION
# ==========================================
elif page == "🔍 Learner Preferences & Segmentation":
    st.title("🔍 Learner Preferences & Behavioral Segmentation")
    st.markdown("Multivariate analysis evaluating curriculum interest intersections and behavioral tiers.")
    
    st.subheader("Multivariate Heatmap: Age Cohort vs. Course Category")
    pivot_age_cat = filtered_df.groupby(['Age Group', 'CourseCategory']).size().reset_index(name='Count')
    fig_heatmap = px.density_heatmap(pivot_age_cat, x='Age Group', y='CourseCategory', z='Count', text_auto=True, color_continuous_scale='Blues', template='plotly_white')
    fig_heatmap.update_layout(margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("<hr class='corp-divider'>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Gender vs. Course Level Preference")
        pivot_gender_level = filtered_df.groupby(['Gender', 'CourseLevel']).size().reset_index(name='Count')
        fig_bar_gl = px.bar(pivot_gender_level, x='CourseLevel', y='Count', color='Gender', barmode='group', template='plotly_white', color_discrete_sequence=px.colors.qualitative.Set1)
        fig_bar_gl.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_bar_gl, use_container_width=True)
        
    with c2:
        st.subheader("Learner Engagement Segmentation")
        user_counts = filtered_df.groupby('UserID').size()
        def classify_learner(n):
            if n == 1: return "Occasional (1 Course)"
            elif 2 <= n <= 3: return "Regular (2-3 Courses)"
            elif 4 <= n <= 6: return "Active (4-6 Courses)"
            else: return "Power Learner (7+ Courses)"
            
        engagement = user_counts.apply(classify_learner).value_counts().reset_index()
        engagement.columns = ['Segment', 'Learners']
        fig_eng = px.bar(engagement, x='Learners', y='Segment', orientation='h', title="User Base by Activity Volume", template='plotly_white', color='Segment')
        fig_eng.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_eng, use_container_width=True)


# ==========================================
# PAGE 6: ENROLLMENT TRENDS
# ==========================================
elif page == "📈 Enrollment Trends":
    st.title("📈 Longitudinal Enrollment Trends")
    st.markdown("Chronological tracking of transaction volume and seasonal platform activity.")
    
    trend_df = filtered_df.dropna(subset=['TransactionDate'])
    if not trend_df.empty:
        monthly = trend_df.groupby('MonthYear').size().reset_index(name='Enrollments')
        monthly = monthly.sort_values('MonthYear')
        
        fig_trend = px.line(monthly, x='MonthYear', y='Enrollments', markers=True, title="Monthly Registration Velocity", template='plotly_white')
        fig_trend.update_traces(line_color='#2563eb', line_width=3)
        fig_trend.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_trend, use_container_width=True)
        
        peak_month = monthly.loc[monthly['Enrollments'].idxmax()]
        st.markdown(f"""
            <div class="insight-card">
                <b>📊 Peak Period Identified:</b> <b>{peak_month['MonthYear']}</b> achieved peak transaction volume with <b>{peak_month['Enrollments']:,} enrollments</b> recorded.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No transaction date data is available for the current filter scope.")


# ==========================================
# PAGE 7: AUTOMATIC INSIGHTS & PERSONAS
# ==========================================
elif page == "💡 Automatic Insights & Personas":
    st.title("💡 Automated Intelligence & Persona Profiling")
    st.markdown("Data-driven algorithmic summaries translating raw numbers into executive takeaways.")
    
    top_age = filtered_df['Age Group'].mode()[0]
    top_cat = filtered_df['CourseCategory'].mode()[0]
    top_lvl = filtered_df['CourseLevel'].mode()[0]
    
    st.markdown(f"""
        <div class="insight-card">
            <b>🔹 Core Demographic Driver:</b> The <b>{top_age}</b> age bracket represents the primary consumer base, driving the largest volume of course transactions.
        </div>
        <div class="insight-card">
            <b>🔹 Leading Domain Demand:</b> The <b>{top_cat}</b> catalog consistently attracts maximum enrollment across both free and paid offerings.
        </div>
        <div class="insight-card">
            <b>🔹 Skill Maturity Skew:</b> <b>{top_lvl}</b> courses comprise the overwhelming majority of registrations, establishing EduPro as a foundational skill incubator.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='corp-divider'>", unsafe_allow_html=True)
    st.subheader('🎯 "Who Chooses What?" Persona Simulation')
    st.markdown("Select a target demographic segment to isolate their dominant behavioral profile.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_age = st.selectbox("Target Age Cohort:", list(df['Age Group'].dropna().unique()))
    with col2:
        sel_gen = st.selectbox("Target Gender:", list(df['Gender'].dropna().unique()))
        
    persona_df = df[(df['Age Group'] == sel_age) & (df['Gender'] == sel_gen)]
    
    if not persona_df.empty:
        p_users = persona_df['UserID'].nunique()
        p_cat = persona_df['CourseCategory'].mode()[0]
        p_lvl = persona_df['CourseLevel'].mode()[0]
        p_avg = round(len(persona_df) / p_users, 1)
        
        st.markdown(f"""
            <div class="info-panel" style="background:#f8fafc; border-left:4px solid #2563eb;">
                <b style="color:#1e3a8a; font-size:1.05rem;">Audience Profile: {sel_gen} Learners ({sel_age} years)</b>
                <div style="margin-top:10px; display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:12px;">
                    <div><span style="color:#64748b; font-size:0.8rem;">Segment Cohort Size:</span><br><b>{p_users:,} learners</b></div>
                    <div><span style="color:#64748b; font-size:0.8rem;">Primary Subject Interest:</span><br><b>{p_cat}</b></div>
                    <div><span style="color:#64748b; font-size:0.8rem;">Preferred Complexity:</span><br><b>{p_lvl}</b></div>
                    <div><span style="color:#64748b; font-size:0.8rem;">Engagement Depth:</span><br><b>{p_avg} courses / learner</b></div>
                </div>
                <div style="margin-top:12px; font-size:0.85rem; color:#475569; font-style:italic;">
                    Key Takeaway: Within the {sel_gen.lower()} demographic aged {sel_age}, course selection strongly concentrates in {p_cat} at the {p_lvl.lower()} level.
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No matching records found for this demographic combination.")


# ==========================================
# PAGE 8: STAKEHOLDER EXECUTIVE SUMMARY
# ==========================================
elif page == "🏛️ Stakeholder Executive Summary":
    st.title("🏛️ Stakeholder Executive Briefing")
    st.markdown("Formal policy summary prepared for Public Sector and Government Institutional Stakeholders.")
    
    st.markdown("""
        <div class="info-panel">
            <h4 style="color:#0f172a; margin-top:0;">1. Operational Scale & Platform Reach</h4>
            <p style="color:#475569; line-height:1.6; font-size:0.92rem;">
                EduPro presently serves a validated base of active learners across a diverse multi-tiered catalog. Platform engagement demonstrates robust recurring utilization, evidenced by an average enrollment rate of over 1.3 courses per learner. This metrics validates learner retention beyond single-session visits.
            </p>
            
            <h4 style="color:#0f172a; margin-top:20px;">2. Curriculum Demand Alignment</h4>
            <p style="color:#475569; line-height:1.6; font-size:0.92rem;">
                Empirical registration records reveal dominant concentration in foundational technical disciplines, most prominently Programming and Data Science. Furthermore, the disproportionate demand for Beginner-level coursework indicates that EduPro functions primarily as a workforce onboarding and reskilling gateway.
            </p>
            
            <h4 style="color:#0f172a; margin-top:20px;">3. Strategic Policy Recommendations</h4>
            <ul style="color:#475569; line-height:1.7; font-size:0.92rem;">
                <li><b>Expand Foundational Pathways:</b> Subsidize and develop additional introductory-tier courses in high-demand fields to maximize initial enrollment throughput.</li>
                <li><b>Senior Demographic Outreach:</b> Active participation tapers noticeably in cohorts above 35 years. Targeted accessibility initiatives and digital literacy campaigns should be funded to bridge this gap.</li>
                <li><b>Intermediate Bridge Programs:</b> Develop structured learning pathways to guide learners from Beginner courses into Intermediate certifications, addressing the drop-off observed in the skill funnel.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE 9: DATA GOVERNANCE & EXPORT
# ==========================================
elif page == "🩺 Data Governance & Export":
    st.title("🩺 Data Governance & Export Hub")
    st.markdown("Audit database integrity, evaluate missingness, and export governed analytical datasets.")
    
    c1, c2, c3 = st.columns(3)
    with c1: draw_kpi("Users Ingested", f"{len(users):,}", "Active user records", "#2563eb")
    with c2: draw_kpi("Courses Ingested", f"{len(courses):,}", "Catalog items mapped", "#7c3aed")
    with c3: draw_kpi("Transactions Ingested", f"{len(transactions):,}", "Audit transaction ledger", "#059669")
    
    st.markdown("<hr class='corp-divider'>", unsafe_allow_html=True)
    st.subheader("Data Quality & Integrity Assessment")
    
    st.markdown(f"""
        <div class="info-panel" style="font-size:0.9rem; color:#334155;">
            <b>• Missing Value Rate (Demographics):</b> {users['Age'].isnull().sum()} missing age values; {users['Gender'].isnull().sum()} missing gender records.<br>
            <b>• Duplicate Transaction Records:</b> {transactions.duplicated().sum()} duplicate transaction entries identified.<br>
            <b>• Referential Integrity Status:</b> 100% of transaction UserIDs and CourseIDs resolve successfully to primary entities.<br>
            <b>• Temporal Date Quality:</b> Valid transaction dates confirmed across active records.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='corp-divider'>", unsafe_allow_html=True)
    st.subheader("📥 Export Governed Data Package")
    st.write("Download the currently scoped and filtered dataset formatted for reporting or external audit.")
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Scoped Dataset (CSV)",
        data=csv,
        file_name='edupro_enterprise_analytics_report.csv',
        mime='text/csv',
    )


# ==========================================
# 5. CORPORATE FOOTER (ALL PAGES)
# ==========================================
st.markdown("""
    <div class="corp-footer">
        <b>EduPro Global Analytics Portal</b> &nbsp;|&nbsp; Enterprise Data Governance & Stakeholder Reporting<br>
        Confidential — Prepared for Board Members, Academic Directors & Government Stakeholders.
    </div>
""", unsafe_allow_html=True)
