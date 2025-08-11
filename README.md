# OTP Authentication Service

This project is a FastAPI-based OTP authentication service that integrates with Twilio for sending and verifying OTPs. It uses PostgreSQL as the database (Neon in this example).

---

## 🚀 Features
- OTP sending via Twilio SMS
- OTP verification
- Secure database storage
- Environment-based configuration

---

## 📦 Setup Instructions

Follow the steps below to set up and run the project.

---

### 1️⃣ Create and Activate a Virtual Environment

#### On **Windows**:
```bash
python -m venv venv
venv\Scripts\activate
On macOS/Linux:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
```
2️⃣ Install Dependencies
Make sure your virtual environment is activated, then install the required Python packages:

```bash
Copy
Edit
pip install -r requirements.txt
```
3️⃣ Configure Environment Variables
Create a .env file in the root directory of the project with the following variables:
```
env
Copy
Edit
# Twilio Credentials
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Database URL (PostgreSQL)
DATABASE_URL=postgresql://<username>:<password>@<host>/<database>?sslmode=require&channel_binding=require
```

4️⃣ Start the Application
Run the FastAPI server:

```bash
Copy
Edit
uvicorn main:app --reload
```
5️⃣ Access the API
Once the server is running, open:

Swagger UI docs: http://127.0.0.1:8000/docs

Redoc docs: http://127.0.0.1:8000/redoc

🛠 Development Tips
Always activate your virtual environment before running commands.

Store your credentials in .env and never commit them to Git.

Make sure you have a working Twilio account with SMS enabled.

Ensure your PostgreSQL instance (Neon) is active and accessible.

📜 License
This project is licensed under the MIT License.

