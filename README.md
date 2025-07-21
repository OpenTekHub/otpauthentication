# FastAPI Backend with OTP Authentication

This is a FastAPI backend application with MySQL database integration and Twilio OTP authentication.

An authentication system built using Twilio and FastAPI to login into webapp or mobile app using OTP authentication.

## Project Structure

```
backend/
├── main.py                 # Main FastAPI application
├── database.py            # Database connection and utilities
├── routes.py              # OTP authentication API routes
├── twilio_service.py      # Twilio SMS service integration
├── .env                   # Environment variables (configure your database & Twilio)
├── requirements.txt       # Python dependencies
└── database_setup.sql     # SQL script to set up database tables
```

## Setup Instructions

### 1. Configure Database
1. Open MySQL Workbench
2. Create a database named `harish` (or update DB_NAME in .env)
3. Run the SQL script in `database_setup.sql` to create tables
4. Update the `.env` file with your database credentials

### 2. Configure Twilio (for SMS OTP)
1. Sign up at [Twilio Console](https://console.twilio.com/)
2. Get your Account SID, Auth Token, and Phone Number
3. Update the `.env` file with Twilio credentials:
   ```
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   ```

### 3. Install Dependencies
```bash
pip install twilio
```

### 4. Run the Application
```bash
python main.py
```

### 5. Access the API
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## OTP Authentication API Endpoints

### Authentication Flow
1. **Send OTP**: `POST /api/send-otp`
2. **Verify OTP**: `POST /api/verify-otp`
3. **Login**: `POST /api/login`

### Detailed Endpoints

#### 1. Send OTP
- **URL**: `POST /api/send-otp`
- **Body**: 
  ```json
  {
    "phone_number": "9876543210"
  }
  ```
- **Response**: 
  ```json
  {
    "message": "OTP sent successfully",
    "expires_in_minutes": 5
  }
  ```

#### 2. Verify OTP
- **URL**: `POST /api/verify-otp`
- **Body**: 
  ```json
  {
    "phone_number": "9876543210",
    "otp": "123456"
  }
  ```
- **Response**: 
  ```json
  {
    "message": "OTP verified successfully",
    "user_id": 1,
    "phone_number": "9876543210",
    "is_verified": true
  }
  ```

#### 3. Login User
- **URL**: `POST /api/login`
- **Body**: 
  ```json
  {
    "phone_number": "9876543210"
  }
  ```
- **Response**: 
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "phone_number": "9876543210",
      "is_verified": true,
      "created_at": "2025-07-19 10:30:00"
    }
  }
  ```

#### 4. Get User by Phone
- **URL**: `GET /api/user/{phone_number}`
- **Response**: User details

#### 5. Authentication Health Check
- **URL**: `GET /api/auth/health`
- **Response**: Service status

## Frontend Integration

For your React Native frontend, use these API endpoints:

1. **Send OTP**: Call `/api/send-otp` when user clicks "Send OTP"
2. **Verify OTP**: Call `/api/verify-otp` when user clicks "Verify OTP"
3. **Login**: Call `/api/login` when user clicks "Login"

## Environment Variables

Configure these in your `.env` file:

### Database
- `DB_HOST` - Database host (default: localhost)
- `DB_NAME` - Database name (harish)
- `DB_USER` - Database username (root)
- `DB_PASSWORD` - Database password
- `DB_PORT` - Database port (default: 3306)

### Twilio SMS
- `TWILIO_ACCOUNT_SID` - Your Twilio Account SID
- `TWILIO_AUTH_TOKEN` - Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER` - Your Twilio Phone Number

## Testing the API

1. Use the interactive documentation at http://localhost:8000/docs
2. Test the authentication flow:
   - Send OTP to a phone number
   - Verify the OTP (check console for OTP if Twilio not configured)
   - Login with the verified phone number

## Database Schema

### Users Table
- `id` - Auto-increment primary key
- `phone_number` - Unique phone number
- `otp` - Current OTP (cleared after verification)
- `otp_expires_at` - OTP expiration timestamp
- `otp_verified` - Boolean flag for OTP verification
- `is_verified` - Boolean flag for user verification status
- `created_at` - User creation timestamp
- `updated_at` - Last update timestamp
