 🎥 AI Reel Generator

An AI-powered web app that automatically generates engaging short video reels from user input.
Built with **Flask**, **Python**, and AI/ML models.

 🚀 Features
📝 Upload text or script → get AI-generated reels.
🎶 Add background music automatically.
🖼 Supports image & video uploads.
⚡ Fast generation using AI models.
🌐 Web-based UI (Flask backend).

🛠️ Tech Stack
**Backend:** Flask (Python)
**AI/ML:** OpenAI / HuggingFace (customizable)
**Frontend:** HTML, CSS, JS
**Storage:** Local file system (can extend to S3, Firebase, etc.)

- Project Structure
AI_reels_maker/
│-- app.py                # Flask main app
│-- requirements.txt      # Dependencies
│-- Procfile              # For Render deployment
│-- static/               # CSS, JS, images
│-- templates/            # HTML files
│-- uploads/              # User uploads (ignored in Git)
│-- reels/                # Generated reels (ignored in Git)

 ⚙️ Installation & Setup

1. Clone the repo:

   bash
   https://github.com/NikeshRaipalle/AI-Reel-Generator.git
   cd AI_reels_maker

3. Create virtual environment & install dependencies:

   bash
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)

   pip install -r requirements.txt
   ```

4. Run the app:

   bash
   python app.py
   ```

5. Open in browser:
   http://127.0.0.1:5000/
   ```


## 🚀 Deployment

You can deploy for **free** using:

* [Render](https://render.com)
* [Railway](https://railway.app)
* [Heroku](https://heroku.com)

Example start command for Render:

gunicorn app:app


📸 Demo Screenshots

(Add some screenshots or demo GIF here)



## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

