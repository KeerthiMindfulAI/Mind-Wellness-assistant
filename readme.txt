## Features
* Interactive chat interface similar to WhatsApp.
* AI-driven empathetic responses using Gemini (Google Generative AI).
* Dynamic wellness report generation based on user conversation.
* User session management with Flask sessions.

## Prerequisites
* Python 3.7 or above
* A Google Generative AI API key (Gemini)
## Installation
1. Clone this repository:

   ```bash
   git clone https://github.com/KeerthiMindfulAI/Mind-Wellness-assistant.git
   cd mental-wellness-assistant
   ```
2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Configure your Gemini API key in the `app.py` file:

   ```python
   genai.configure(api_key="YOUR_API_KEY")
   ```

## Usage
1. Run the Flask application:
   ```
   python app.py
   ```
2. Access the application in your web browser at:
   ```
   http://127.0.0.1:5000/
   ```
## Project Structure

```
mental_wellness_assistant/
├── app.py           # Main Flask application
├── requirements.txt # Required Python libraries
└── templates/
    └── index.html   # HTML template for the chat interface
```

