# EduPro Learner Analytics Project

This project contains the analysis of the Learner Demographics and Course Enrollment Behavior on the EduPro platform.

## Setup Instructions

1. **Install Requirements:**
   Ensure you have Python installed, then install the required libraries:
   ```bash
   pip install pandas streamlit plotly
   ```

2. **Generate Reports:**
   Run the following script to download the live dataset, perform the Exploratory Data Analysis, and generate the `research_paper.md` and `executive_summary.md` deliverables.
   ```bash
   python generate_reports.py
   ```

3. **Run Streamlit Dashboard:**
   Run the following command to start the live analytics web application:
   ```bash
   streamlit run app.py
   ```

## Deliverables Included
- `app.py`: Streamlit application providing live, interactive demographic and behavioral insights.
- `generate_reports.py`: Script that performs the data integration, calculates KPIs, and generates the required reports dynamically based on the dataset.
- `research_paper.md` (Generated): Detailed EDA, insights, and recommendations.
- `executive_summary.md` (Generated): High-level summary for government stakeholders.
