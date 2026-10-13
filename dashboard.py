
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
DB_PATH = PROJECT_DIR / "learning_history.db"

st.set_page_config(
    page_title="Adaptive Coding Mentor",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Adaptive Coding Mentor")
st.subheader("Learner Progress Dashboard")

# Load saved learning history
with sqlite3.connect(DB_PATH) as connection:
    df = pd.read_sql_query(
        """
        SELECT id, language, topic, error_category,
               explanation, created_at
        FROM learning_history
        ORDER BY id DESC
        """,
        connection,
    )

if df.empty:
    st.info("No learning attempts found yet.")
    st.stop()

# Normalize text for reliable statistics
for column in ["language", "topic", "error_category"]:
    df[column] = df[column].fillna("Unknown").astype(str).str.strip()

df["error_category"] = df["error_category"].replace("", "Unknown")
df["language"] = df["language"].replace("", "Unknown")
df["topic"] = df["topic"].replace("", "Unknown")

df["is_correct"] = (
    df["error_category"].str.casefold() == "no error"
)

st.sidebar.header("Filter Learning History")

languages = ["All"] + sorted(df["language"].unique().tolist())
selected_language = st.sidebar.selectbox(
    "Programming language",
    languages,
)

filtered_df = df.copy()

if selected_language != "All":
    filtered_df = filtered_df[
        filtered_df["language"] == selected_language
    ]

topics = ["All"] + sorted(filtered_df["topic"].unique().tolist())
selected_topic = st.sidebar.selectbox("Topic", topics)

if selected_topic != "All":
    filtered_df = filtered_df[
        filtered_df["topic"] == selected_topic
    ]

total = len(filtered_df)
correct = int(filtered_df["is_correct"].sum())
with_errors = total - correct
accuracy = (correct / total * 100) if total else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Attempts", total)
col2.metric("Correct Attempts", correct)
col3.metric("Attempts With Errors", with_errors)
col4.metric("Recorded Accuracy", f"{accuracy:.1f}%")

st.caption(
    "Statistics reflect saved records, including any test data. "
    "They do not necessarily represent unique coding submissions."
)

st.divider()

st.subheader("Most Frequent Mistakes")

mistakes = filtered_df[~filtered_df["is_correct"]]

if mistakes.empty:
    st.success("No recorded mistakes for these filters.")
else:
    mistake_counts = mistakes["error_category"].value_counts()
    st.bar_chart(mistake_counts)

st.subheader("Performance by Topic")

if filtered_df.empty:
    st.info("No records match these filters.")
else:
    topic_counts = (
        filtered_df.groupby(["topic", "error_category"])
        .size()
        .unstack(fill_value=0)
    )
    st.bar_chart(topic_counts)


st.subheader("Learning Progress Over Time")

progress_df = filtered_df.copy()

progress_df["created_at"] = pd.to_datetime(
    progress_df["created_at"],
    errors="coerce"
)

progress_df = progress_df.dropna(subset=["created_at"])
progress_df = progress_df.sort_values(["created_at", "id"])

if progress_df.empty:
    st.info("Not enough valid timestamps to display progress.")
else:
    progress_df["attempt_number"] = range(1, len(progress_df) + 1)
    progress_df["correct_value"] = (
        progress_df["is_correct"].astype(int)
    )

    st.line_chart(
        progress_df.set_index("attempt_number")["correct_value"]
    )

    st.caption(
        "1 = attempt marked No error; 0 = attempt with a recorded error. "
        "This shows individual results, not a smoothed accuracy trend."
    )


st.subheader("Complete Learning History")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.caption("All data is stored locally in SQLite.")
