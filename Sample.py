
import streamlit as st 
import pandas as pd
import mysql.connector
# Establising connection with sql 
config = {
    'host': 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
    'port': 4000,
    'user': '31ZrixPLoJcBFtY.root',
    'password': 'xAwaevomY9b1ldSM',
    'database': 'Placement_Portal'
    
}

sethu = mysql.connector.connect(**config)
raman = sethu.cursor()

import streamlit as st

# Custom CSS for bordered container
st.markdown("""
    <style>
        .bordered-heading {
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }
        .bordered-heading h1 {
            color: #2E7D32;
            margin-bottom: 5px;
        }
        .bordered-heading p {
            color: #555;
            font-size: 18px;
        }
    </style>

    <div class="bordered-heading">
        <h1>🎯 Career Readiness & Placement Portal</h1>
        <p>Track student success by batch, skills, and placement outcomes</p>
    </div>
""", unsafe_allow_html=True)


#SQL query
query = """
SELECT 
    s.name AS Name,
    s.course_batch AS `Batch Name`,
    p.problems_solved AS `Problems Solved`,
    p.assessments_completed AS `Assessments Completion`,
    p.mini_projects AS `Mini Projects`,
    p.certifications_earned AS Certificates, 
    p.latest_project_score AS `Latest Project`
FROM student_table s
JOIN programming_table p ON s.student_id = p.student_id;
"""

# Fetch data using query
dashboard_data = pd.read_sql(query, sethu)

# Close the connection (optional, but good practice)
#sethu.close()

st.title("🧠 Programming Skill Excellence")
st.subheader("Top 10 Performers in Each Category")

# Select metric from dropdown
select_metric = st.selectbox("Choose Performance Metric:", [
    "Problems Solved",
    "Assessments Completion",
    "Mini Projects",
    "Certificates",
    "Latest Project"
])


# Top 10 based on selected metric

top10 = dashboard_data.sort_values(by=select_metric, ascending=False).head(10)


# Display result

st.dataframe(top10[['Name', 'Batch Name', select_metric]])




# Streamlit UI

st.subheader("🧠 Soft Skill Excellence")
st.markdown("### 🎯 Top 10 Performers by Selected Soft Skill")

# Soft Skill options
skills = [
    "communication",
    "team_work",
    "presentation",
    "leadership",
    "critical_thinking",
    "interpersonal_skill"
]

# Radio button
select_skill = st.radio("Select a Soft Skill to View Top Performers:", skills, horizontal=True)

# SQL Query using f-string
query = f"""
SELECT 
    s.name AS Name,
    s.course_batch AS `Batch Name`,
    sk.{select_skill} AS Score
FROM student_table s
JOIN soft_skill_table sk ON s.student_id = sk.student_id
#WHERE sk.{select_skill} IS NOT NULL AND sk.{select_skill} > 0
ORDER BY sk.{select_skill} DESC
LIMIT 10;
"""

df = pd.read_sql(query, sethu)
st.dataframe(df)



# Streamlit UI
st.subheader("🏆 Successful Batch based on Placement")

# Add Submit button
if st.button("🔍 Show Top Placed Batch Students"):
    
   
    # SQL query
    query = """
    SELECT 
        s.name AS Name,
        s.course_batch AS `Batch Name`
    FROM student_table s
    JOIN placement_table p ON s.student_id = p.student_id
    WHERE p.placement_status = 'Placed'
      AND s.course_batch = (
          SELECT s2.course_batch
          FROM student_table s2
          JOIN placement_table p2 ON s2.student_id = p2.student_id
          WHERE p2.placement_status = 'Placed'
          GROUP BY s2.course_batch
          ORDER BY COUNT(*) DESC
          LIMIT 1 
      );
    """

    df = pd.read_sql(query, sethu)

    if not df.empty:
        st.success(f"✅ Batch: {df['Batch Name'].iloc[0]} has the most placements")
        st.table(df)
    else:
        st.warning("⚠️ No placement data found.")

    
if st.button("Show 2nd Most Successful Batch"):
    query = """ 
    SELECT 
    s.name AS Name,
    s.course_batch As `Batch Name`
FROM student_table s
JOIN placement_table p ON s.student_id = p.student_id
WHERE p.placement_status = 'Placed'
  AND s.course_batch = (
      SELECT s2.course_batch
      FROM student_table s2
      JOIN placement_table p2 ON s2.student_id = p2.student_id
      WHERE p2.placement_status = 'Placed'
      GROUP BY s2.course_batch
      ORDER BY COUNT(*) DESC
      LIMIT 1 OFFSET 1
  );
"""
    df = pd.read_sql(query, sethu)
    st.dataframe(df)

st.markdown("</div>", unsafe_allow_html=True)



st.subheader("📊 Average Performance by Batch")
# Run the query
avg_query = """SELECT 
    s.course_batch AS Batch,
    ROUND(AVG(p.problems_solved), 1) AS `Avg Problems Solved`,
    ROUND(AVG(p.assessments_completed), 1) AS `Avg Assessments`,
    ROUND(AVG(p.mini_projects), 1) AS `Avg Mini Projects`,
    ROUND(AVG(p.certifications_earned), 1) AS `Avg Certificates`,
    ROUND(AVG(p.latest_project_score), 1) AS `Avg Project Score`,
    ROUND(AVG(sk.communication), 1) AS `Avg Communication`,
    ROUND(AVG(sk.team_work), 1) AS `Avg Team Work`,
    ROUND(AVG(sk.presentation), 1) AS `Avg Presentation`,
    ROUND(AVG(sk.leadership), 1) AS `Avg Leadership`,
    ROUND(AVG(sk.critical_thinking), 1) AS `Avg Critical Thinking`,
    ROUND(AVG(sk.interpersonal_skill), 1) AS `Avg Interpersonal Skill`
FROM student_table s
JOIN programming_table p ON s.student_id = p.student_id
JOIN soft_skill_table sk ON s.student_id = sk.student_id
GROUP BY s.course_batch
ORDER BY s.course_batch;
"""
avg_df = pd.read_sql(avg_query, sethu)

# Show as a table
st.dataframe(avg_df)
