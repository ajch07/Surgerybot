# Chatbot Flask App

This project is a Flask-based chatbot application that integrates with a PostgreSQL database. It reads data from PDF files, embeds the information into a PostgreSQL vector database, and implements Retrieval-Augmented Generation (RAG) using Langchain and OpenAI models.

## Project Structure

```
chatbot-flask-app
├── app
│   ├── __init__.py          # Initializes the Flask application and sets up the application context.
│   ├── routes.py            # Defines the API routes for the chatbot.
│   ├── models.py            # Contains the database models for the application.
│   ├── db.py                # Handles the database connection and session management.
│   ├── pdf_reader.py        # Contains functions to read data from PDF files.
│   ├── embeddings.py         # Implements the logic for embedding extracted PDF data.
│   ├── rag.py               # Implements the RAG logic using Langchain.
│   └── config.py            # Contains configuration settings for the application.
├── migrations
│   └── README.md            # Documentation on handling database migrations.
├── requirements.txt         # Lists the dependencies required for the project.
├── .gitignore               # Specifies files and directories to be ignored by Git.
├── README.md                # Documentation for the project.
└── run.py                   # Entry point for running the Flask application.
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd chatbot-flask-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Configure the application:**
   Update the `app/config.py` file with your PostgreSQL database connection details and any necessary API keys.

6. **Run database migrations:**
   Follow the instructions in `migrations/README.md` to set up your database schema.

7. **Start the application:**
   ```
   python run.py
   ```

## Usage

Once the application is running, you can interact with the chatbot through the defined API endpoints in `app/routes.py`. The chatbot will fetch data from the PostgreSQL database and utilize the embedded PDF data to provide responses.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.