# Adaptive Coding Mentor AI

An AI-powered coding mentor that helps students identify programming mistakes, understand errors, track learning history, and receive personalized practice recommendations.

## Features

- **AI-Powered Code Analysis:** Explains coding errors and suggests corrections.
- **Error Classification:** Identifies common issues such as syntax errors, logic errors, incorrect conditions, and loop boundary errors.
- **Learning History:** Stores coding attempts and explanations in an SQLite database.
- **Recurring Mistake Detection:** Identifies repeated error patterns.
- **Adaptive Recommendations:** Suggests targeted exercises based on recorded mistakes.
- **Interactive Dashboard:** Visualizes coding attempts, error categories, and learning statistics.

## Technologies Used

- Python
- Google Agent Development Kit (ADK)
- Google Gemini API
- Streamlit
- SQLite
- Pandas

## Project Structure

```text
AdaptiveCodingMentor/
├── adaptive_coding_mentor/
│   ├── __init__.py
│   ├── agent.py
│   ├── attempt_manager.py
│   ├── database.py
│   └── test_database.py
├── dashboard.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup and Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Create and activate a Python virtual environment.
4. Install the dependencies using `pip install -r requirements.txt`.
5. Create a `.env` file and configure your Google Gemini API key:

   `GOOGLE_API_KEY=your_api_key_here`

6. Start the AI agent using `adk web`.
7. In a separate terminal, start the dashboard using `streamlit run dashboard.py`.

## Security

- Never commit your actual API key or `.env` file.
- Local SQLite databases and virtual environment files are excluded through `.gitignore`.

## Future Improvements

- Automated database tests.
- More robust tracking of individual coding submissions.
- Improved learning analytics and progress measurement.
- Additional programming languages and practice topics.