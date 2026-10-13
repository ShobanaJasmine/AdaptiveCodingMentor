
import sqlite3
from pathlib import Path

# Store the database in the main project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "learning_history.db"


def create_database():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            topic TEXT NOT NULL,
            error_category TEXT NOT NULL,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def save_attempt(language, topic, error_category, explanation):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO learning_history
        (language, topic, error_category, explanation)
        VALUES (?, ?, ?, ?)
    """, (language, topic, error_category, explanation))

    connection.commit()
    connection.close()


def get_learning_history():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, language, topic, error_category,
               explanation, created_at
        FROM learning_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return records


def get_recurring_mistakes():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT language, topic, error_category, COUNT(*) AS occurrences
        FROM learning_history
        WHERE error_category != 'No error'
        GROUP BY language, topic, error_category
        HAVING COUNT(*) >= 2
        ORDER BY occurrences DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return records


def get_learning_summary():
    mistakes = get_recurring_mistakes()

    if not mistakes:
        return "No recurring mistakes found yet."

    summary = []

    for language, topic, error_category, count in mistakes:
        summary.append(
            f"{language} - {topic}: "
            f"{error_category} ({count} occurrences)"
        )

    return "\n".join(summary)


def get_adaptive_recommendation():
    """Recommend practice based on recurring mistakes."""

    mistakes = get_recurring_mistakes()

    if not mistakes:
        return (
            "No recurring mistakes detected yet. "
            "Give the learner a beginner-level diagnostic exercise."
        )

    language, topic, error_category, count = mistakes[0]

    return (
        f"Prioritize {language} practice on {topic}. "
        f"The recurring error is '{error_category}', "
        f"recorded {count} times. "
        f"Generate one targeted exercise for this error. "
        f"Give hints before revealing the solution."
    )


def get_learning_history_for_agent():
    """Return the learner's recurring mistakes in readable form."""
    return get_learning_summary()




def save_attempt_for_agent(
    language: str,
    topic: str,
    error_category: str,
    explanation: str,
    attempt_id: str,
) -> str:
    """Save a coding attempt once for a given attempt ID."""

    if not attempt_id or not attempt_id.strip():
        return "Error: attempt_id is required."

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_attempt_ids (
            attempt_id TEXT PRIMARY KEY
        )
    """)

    try:
        cursor.execute(
            "INSERT INTO saved_attempt_ids (attempt_id) VALUES (?)",
            (attempt_id,)
        )

        cursor.execute("""
            INSERT INTO learning_history
            (language, topic, error_category, explanation)
            VALUES (?, ?, ?, ?)
        """, (language, topic, error_category, explanation))

        connection.commit()

    except sqlite3.IntegrityError:
        connection.rollback()
        connection.close()
        return "This attempt was already saved. No duplicate was added."

    connection.close()
    return "Coding attempt saved successfully."




if __name__ == "__main__":
    create_database()
    print("Learning history database created successfully!")
    print(f"Database location: {DB_PATH}")
