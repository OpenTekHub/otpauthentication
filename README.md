OTP Authentication with Twilio and FastAPI
A simple and scalable OTP (One-Time Password) authentication system for logging into web or mobile apps using FastAPI and Twilio.

🔧 Features
✅ Send OTP via SMS using Twilio
✅ Verify OTP for secure login
✅ FastAPI-based backend
✅ Interactive API docs with Swagger and ReDoc
🚀 Getting Started
1. Clone the Repository
git clone https://github.com/yourusername/otpauthentication.git
cd otpauthentication
2. Create & Activate Virtual Environment
On Windows
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
On macOS/Linux
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
To save updated packages:

bash
Copy
Edit
pip freeze > requirements.txt
4. Configure Twilio Credentials
Create a .env file in the root directory:

env
Copy
Edit
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
5. Run the App
bash
Copy
Edit
uvicorn app.main:app --reload
📑 API Documentation
Swagger UI: http://127.0.0.1:8000/docs

ReDoc UI: http://127.0.0.1:8000/redoc
