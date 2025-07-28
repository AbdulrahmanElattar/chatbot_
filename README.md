# Abdulrahman Hamada Chatbot

This project is a chatbot application that processes PDF documents to provide context-aware responses using a language model. It features a **FastAPI** backend for handling API requests and a **Streamlit** frontend for an interactive user interface. The chatbot leverages the Together API for language model inference and FAISS for vector-based document retrieval.

## Features
- Upload and process PDF documents for context.
- Interactive chat interface with conversation history.
- Retrieval-Augmented Generation (RAG) using FAISS and SentenceTransformer embeddings.
- Expose local servers publicly using `ngrok` for testing.

## Prerequisites
- Python 3.8+
- `ngrok` installed (for exposing local servers)
- A Together API key (set in a `.env` file)
- A PDF file for context (default: `Hands-On_Large_Language_Models-1.pdf`)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/abdulrahman-hamada-chatbot.git
   cd abdulrahman-hamada-chatbot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root and add your Together API key:
   ```plaintext
   TOGETHER_API_KEY=your-api-key-here
   ```

5. **Install `ngrok`**:
   - Download and install `ngrok` from [ngrok.com](https://ngrok.com/download).
   - Authenticate `ngrok` with your account:
     ```bash
     ngrok authtoken <your-ngrok-auth-token>
     ```

6. **Prepare the PDF file**:
   Place the PDF file (e.g., `Hands-On_Large_Language_Models-1.pdf`) in the specified directory: `/media/elbooody/New_Volume/Chat_bot/`. Update the `PDF_FILE_NAME` path in `Back_end.py` if needed.

## Usage
1. **Run the FastAPI backend**:
   ```bash
   uvicorn Back_end:app --host 127.0.0.1 --port 8000
   ```

2. **Expose the backend with `ngrok`**:
   In a new terminal, start `ngrok` to expose the FastAPI server:
   ```bash
   ngrok http 8000
   ```
   Copy the `ngrok` forwarding URL (e.g., `https://abc123.ngrok.io`) and update `BACKEND_URL` in `Front_end.py` to this URL (e.g., `BACKEND_URL="https://abc123.ngrok.io/api/chat"`).

3. **Run the Streamlit frontend**:
   ```bash
   streamlit run Front_end.py
   ```

4. **Expose the frontend with `ngrok`** (optional):
   To access the Streamlit app publicly:
   ```bash
   ngrok http 8501
   ```
   Access the Streamlit app via the provided `ngrok` URL.

5. **Interact with the chatbot**:
   - Open the Streamlit app in your browser.
   - Type your message in the chat input.
   - View conversation history in the sidebar and switch between chats.

## Project Structure
- `Back_end.py`: FastAPI backend for processing chat requests and integrating with the Together API.
- `Front_end.py`: Streamlit frontend for the chat interface.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables (not tracked in Git).
- `Hands-On_Large_Language_Models-1.pdf`: Sample PDF for context (not included in repo).

## Troubleshooting
- **PDF not found**: Ensure the PDF file exists at the path specified in `Back_end.py`.
- **API errors**: Verify your Together API key in the `.env` file.
- **ngrok issues**: Check your `ngrok` authentication token and ensure the correct ports are exposed.
- **Dependency errors**: Ensure all packages in `requirements.txt` are installed correctly.

## License
This project is licensed under the MIT License.
