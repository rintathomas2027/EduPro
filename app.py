import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EduPro Analytics Dashboard", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border-left: 5px solid #0d6efd;
    }
    .metric-title {
        color: #6c757d;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #0d6efd;
        font-size: 1.8rem;
        font-weight: bold;
    }
    .insight-card {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 5px solid #198754;
    }
    .insight-text {
        font-size: 1.1rem;
        color: #212529;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
if hasattr(st, "cache_data"):
    @st.cache_data
    def fetch_data():
else:
    @st.cache(allow_output_mutation=True)
    def fetch_data():
    sheet_id = "1Ts1Yjt9oiTdOeCeuJPbExNz7N3vmd0Ln"
    users_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=74828563"
    courses_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1284811374"
    transactions_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=722772998"
    
    users = pd.read_csv(users_url)
    courses = pd.read_csv(courses_url)
    transactions = pd.read_csv(transactions_url)
    
    # Merge Data
    df = transactions.merge(users, on="UserID", how="left")
    df = df.merge(courses, on="CourseID", how="left")
    
    # Transformations
    bins = [0, 17, 25, 35, 45, 100]
    labels = ['<18', '18-25', '26-35', '36-45', '45+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)
    
    # Ensure Date format
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], format='%d/%m/%Y', errors='coerce')
    df['MonthYear'] = df['TransactionDate'].dt.to_period('M').astype(str)
    
    return users, courses, transactions, df

try:
    users, courses, transactions, df = fetch_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 EduPro Settings")

PAGES = [
    "📊 1. Executive Dashboard",
    "👥 2. Learner Demographics",
    "📚 3. Course Analytics",
    "🔍 4. Learner Preferences",
    "📈 5. Enrollment Trends",
    "💡 6. Insights & Recommendations",
    "🏛️ 7. Executive Summary",
    "🩺 8. Data Health"
]
page = st.sidebar.radio("Navigation", PAGES)
st.sidebar.markdown("---")

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("**Global Filters**")

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
selected_levels = st.sidebar.multiselect("Levels", level_options)
if not selected_levels: selected_levels = level_options

st.sidebar.markdown("---")
st.sidebar.info("Dashboard developed for EduPro Stakeholders.")

# Apply filters
filtered_df = df[
    (df['Age Group'].isin(selected_age_groups)) &
    (df['Gender'].isin(selected_genders)) &
    (df['CourseCategory'].isin(selected_categories)) &
    (df['CourseLevel'].isin(selected_levels))
]

# Provide fallback if empty
if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust your filters.")
    st.stop()

# --- HELPER FUNCTIONS ---
def draw_kpi(title, value):
    st.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)


# ==========================================
# PAGE 1: EXECUTIVE DASHBOARD
# ==========================================
if page == "📊 1. Executive Dashboard":
    st.title("📊 Executive Dashboard")
    st.markdown("High-level snapshot of EduPro's core metrics.")
    
    total_learners = filtered_df['UserID'].nunique()
    total_enrollments = len(filtered_df)
    total_courses = filtered_df['CourseID'].nunique()
    avg_courses = round(total_enrollments / total_learners, 2) if total_learners > 0 else 0
    top_cat = filtered_df['CourseCategory'].mode()[0] if not filtered_df['CourseCategory'].empty else "N/A"
    top_lvl = filtered_df['CourseLevel'].mode()[0] if not filtered_df['CourseLevel'].empty else "N/A"
    
    c1, c2, c3 = st.columns(3)
    with c1: draw_kpi("Total Learners", f"{total_learners:,}")
    with c2: draw_kpi("Total Enrollments", f"{total_enrollments:,}")
    with c3: draw_kpi("Total Courses", f"{total_courses:,}")
    
    c4, c5, c6 = st.columns(3)
    with c4: draw_kpi("Avg Courses / Learner", avg_courses)
    with c5: draw_kpi("Most Popular Category", top_cat)
    with c6: draw_kpi("Most Popular Level", top_lvl)
    
    # Quick Overview Charts
    colA, colB = st.columns(2)
    with colA:
        cat_counts = filtered_df['CourseCategory'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Enrollments']
        fig = px.bar(cat_counts, x='Category', y='Enrollments', title="Enrollments by Category", template="plotly_white", color='Category')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        lvl_counts = filtered_df['CourseLevel'].value_counts().reset_index()
        lvl_counts.columns = ['Level', 'Enrollments']
        fig2 = px.pie(lvl_counts, names='Level', values='Enrollments', title="Enrollments by Level", hole=0.4, template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# PAGE 2: LEARNER DEMOGRAPHICS
# ==========================================
elif page == "👥 2. Learner Demographics":
    st.title("👥 Learner Demographics")
    
    c1, c2 = st.columns(2)
    with c1:
        age_counts = filtered_df['Age Group'].value_counts().reset_index()
        age_counts.columns = ['Age Group', 'Count']
        age_counts['sort'] = age_counts['Age Group'].map({'<18':0, '18-25':1, '26-35':2, '36-45':3, '45+':4})
        age_counts = age_counts.sort_values('sort')
        fig_age = px.bar(age_counts, x='Age Group', y='Count', title="Age Distribution", template="plotly_white", color='Age Group')
        fig_age.update_layout(showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with c2:
        gen_counts = filtered_df['Gender'].value_counts().reset_index()
        gen_counts.columns = ['Gender', 'Count']
        fig_gen = px.pie(gen_counts, names='Gender', values='Count', title="Gender Distribution", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_gen, use_container_width=True)
        
    st.subheader("Gender × Age Group")
    gen_age = filtered_df.groupby(['Age Group', 'Gender']).size().reset_index(name='Count')
    fig_gen_age = px.bar(gen_age, x='Age Group', y='Count', color='Gender', barmode='group', title="Demographic Breakdown", template="plotly_white")
    st.plotly_chart(fig_gen_age, use_container_width=True)

# ==========================================
# PAGE 3: COURSE ANALYTICS
# ==========================================
elif page == "📚 3. Course Analytics":
    st.title("📚 Course Analytics")
    
    st.subheader("Top 10 Courses")
    top_courses = filtered_df['CourseName'].value_counts().head(10).reset_index()
    top_courses.columns = ['CourseName', 'Enrollments']
    fig_top = px.bar(top_courses, x='Enrollments', y='CourseName', orientation='h', title="Highest Enrolled Courses", template="plotly_white")
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        type_counts = filtered_df['CourseType'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        fig_type = px.pie(type_counts, names='Type', values='Count', title="Enrollment by Course Type (Free vs Paid)", template="plotly_white")
        st.plotly_chart(fig_type, use_container_width=True)
    
    with c2:
        level_counts = filtered_df['CourseLevel'].value_counts().reset_index()
        level_counts.columns = ['Level', 'Count']
        fig_lvl = px.funnel(level_counts, x='Count', y='Level', title="Enrollment by Course Level", template="plotly_white", color='Level')
        fig_lvl.update_layout(showlegend=False)
        st.plotly_chart(fig_lvl, use_container_width=True)

# ==========================================
# PAGE 4: LEARNER PREFERENCES
# ==========================================
elif page == "🔍 4. Learner Preferences":
    st.title("🔍 Learner Preferences & Segmentation")
    
    st.subheader("Heatmap: Age Group × Course Category")
    pivot_age_cat = filtered_df.groupby(['Age Group', 'CourseCategory']).size().reset_index(name='Count')
    fig_heatmap = px.density_heatmap(pivot_age_cat, x='Age Group', y='CourseCategory', z='Count', text_auto=True, color_continuous_scale='Blues', template='plotly_white')
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.subheader("Gender × Course Level")
    pivot_gender_level = filtered_df.groupby(['Gender', 'CourseLevel']).size().reset_index(name='Count')
    fig_bar_gl = px.bar(pivot_gender_level, x='CourseLevel', y='Count', color='Gender', barmode='group', template='plotly_white')
    st.plotly_chart(fig_bar_gl, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Learner Engagement Profile")
    user_counts = filtered_df.groupby('UserID').size()
    
    def classify_learner(n):
        if n == 1: return "Occasional Learner (1)"
        elif 2 <= n <= 3: return "Regular Learner (2-3)"
        elif 4 <= n <= 6: return "Active Learner (4-6)"
        else: return "Highly Active Learner (7+)"
        
    engagement = user_counts.apply(classify_learner).value_counts().reset_index()
    engagement.columns = ['Segment', 'Learners']
    
    fig_eng = px.bar(engagement, x='Learners', y='Segment', orientation='h', title="Learner Segmentation by Courses Taken", template='plotly_white', color='Segment')
    fig_eng.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig_eng, use_container_width=True)

# ==========================================
# PAGE 5: ENROLLMENT TRENDS
# ==========================================
elif page == "📈 5. Enrollment Trends":
    st.title("📈 Enrollment Trends")
    st.markdown("Monitor historical enrollment transactions over time.")
    
    trend_df = filtered_df.dropna(subset=['TransactionDate'])
    if not trend_df.empty:
        monthly = trend_df.groupby('MonthYear').size().reset_index(name='Enrollments')
        monthly = monthly.sort_values('MonthYear')
        
        fig_trend = px.line(monthly, x='MonthYear', y='Enrollments', markers=True, title="Monthly Enrollments Trend", template='plotly_white')
        fig_trend.update_traces(line_color='#0d6efd', line_width=3)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        peak_month = monthly.loc[monthly['Enrollments'].idxmax()]
        st.success(f"**Peak Enrollment Month:** {peak_month['MonthYear']} with {peak_month['Enrollments']} enrollments.")
    else:
        st.write("No valid transaction dates available.")

# ==========================================
# PAGE 6: INSIGHTS & RECOMMENDATIONS
# ==========================================
elif page == "💡 6. Insights & Recommendations":
    st.title("💡 Automatic Insight Cards")
    
    top_age = filtered_df['Age Group'].mode()[0]
    top_cat = filtered_df['CourseCategory'].mode()[0]
    top_lvl = filtered_df['CourseLevel'].mode()[0]
    
    st.markdown(f'<div class="insight-card"><div class="insight-text">🔹 The <b>{top_age}</b> age group represents the largest active learner segment.</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-card"><div class="insight-text">🔹 <b>{top_cat}</b> has the highest overall number of enrollments.</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-card"><div class="insight-text">🔹 <b>{top_lvl}</b>-level courses account for the vast majority of learner interest.</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader('"Who Chooses What?" Analysis')
    st.markdown("Select an exact persona to view their dominant traits.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_age = st.selectbox("Select Age Group:", list(df['Age Group'].dropna().unique()))
    with col2:
        sel_gen = st.selectbox("Select Gender:", list(df['Gender'].dropna().unique()))
        
    persona_df = df[(df['Age Group'] == sel_age) & (df['Gender'] == sel_gen)]
    
    if not persona_df.empty:
        p_users = persona_df['UserID'].nunique()
        p_cat = persona_df['CourseCategory'].mode()[0]
        p_lvl = persona_df['CourseLevel'].mode()[0]
        p_avg = round(len(persona_df) / p_users, 1)
        
        st.info(f"**Learner Profile ({sel_age}, {sel_gen})**\n\n"
                f"- **Total Learners:** {p_users}\n"
                f"- **Favorite Category:** {p_cat}\n"
                f"- **Preferred Level:** {p_lvl}\n"
                f"- **Avg Courses Taken:** {p_avg}\n\n"
                f"*Among {sel_gen} learners aged {sel_age}, {p_cat} is the most enrolled category.*")
    else:
        st.write("No data for this specific persona.")

# ==========================================
# PAGE 7: EXECUTIVE SUMMARY
# ==========================================
elif page == "🏛️ 7. Executive Summary":
    st.title("🏛️ Executive Summary (Stakeholder View)")
    st.markdown("High-level strategic findings intended for Government and Institutional Stakeholders.")
    
    st.subheader("1. Learner Reach & Scale")
    st.write(f"EduPro is currently serving **{filtered_df['UserID'].nunique():,} active learners** who have completed **{len(filtered_df):,} total enrollments** across {filtered_df['CourseID'].nunique()} distinct courses. The platform averages **{round(len(filtered_df)/filtered_df['UserID'].nunique(), 2) if filtered_df['UserID'].nunique() else 0} courses per learner**, indicating strong retention and recurring engagement.")
    
    st.subheader("2. Course Demand")
    st.write(f"The most significant demand lies in the **{filtered_df['CourseCategory'].mode()[0]}** sector, specifically at the **{filtered_df['CourseLevel'].mode()[0]}** level. This suggests that the majority of our audience uses the platform for foundational upskilling rather than advanced specialization.")
    
    st.subheader("3. Inclusion & Demographics")
    st.write(f"Our dominant demographic remains the **{filtered_df['Age Group'].mode()[0]}** age bracket. Stakeholders should review the demographics dashboard to identify underrepresented age groups or gender disparities in technical fields.")
    
    st.subheader("4. Strategic Recommendations")
    st.markdown("""
    * **Recommendation 1:** Expand the catalog of Beginner-level courses, as they act as the primary acquisition funnel for new learners.
    * **Recommendation 2:** Increase marketing efforts and digital literacy campaigns targeted at older demographics (45+) to improve platform inclusivity.
    * **Recommendation 3:** Invest further in top-performing categories (like Programming and Data Science) while investigating barriers to entry in lower-performing subjects.
    """)

# ==========================================
# PAGE 8: DATA HEALTH
# ==========================================
elif page == "🩺 8. Data Health":
    st.title("🩺 Data Quality & Downloads")
    
    c1, c2, c3 = st.columns(3)
    with c1: draw_kpi("Total Users in DB", len(users))
    with c2: draw_kpi("Total Courses in DB", len(courses))
    with c3: draw_kpi("Total Transactions", len(transactions))
    
    st.subheader("Integrity Checks")
    st.write(f"- **Missing User Ages/Genders:** {users['Age'].isnull().sum()} missing ages, {users['Gender'].isnull().sum()} missing genders.")
    st.write(f"- **Duplicate Transactions:** {transactions.duplicated().sum()}")
    
    st.markdown("---")
    st.subheader("📥 Download Analytics")
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name='edupro_filtered_analytics.csv',
        mime='text/csv',
    )
