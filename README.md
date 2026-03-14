CSCI 5300 Software Engineering Project
# Melody Matrix 🎵

**AI Music Generator** - A web application for generating music using artificial intelligence.

## 📋 Overview

Melody Matrix is a modern web application that allows users to generate music using AI. The project currently includes authentication pages (login and signup) with a beautiful, animated UI featuring floating music notes.

## 🎨 Features

### Current Features
- **Login Page** (`login.html`)
  - Email and password authentication
  - Google OAuth login option
  - Guest login option
  - Beautiful animated UI with floating music notes
  - Form validation and error handling
  - Link to signup page for new users

- **Signup Page** (`index.html`)
  - User registration with full name, email, and password
  - Password confirmation validation (checks if passwords match)
  - Google OAuth signup option
  - Email verification support
  - Link to login page for existing users

### Design
- Modern, clean UI with pastel color scheme
- Animated floating music notes (♪ ♫ ♩ ♬)
- Responsive design
- Smooth transitions and hover effects
- Poppins font family for a modern look

## 🔐 Security Note

**IMPORTANT**: This repository uses a secure configuration system. Sensitive credentials are stored in `config.js`, which is excluded from version control via `.gitignore`. Before using the application, you must create `config.js` with your own Supabase credentials. Never commit real API keys or secrets to version control.

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A Supabase account (free tier available at [supabase.com](https://supabase.com))

### Setup Instructions

#### 1. Clone or Download the Repository
```bash
git clone <repository-url>
cd "Melody Matrix"
```

#### 2. Set Up Supabase

1. **Create a Supabase Account**
   - Go to [https://supabase.com](https://supabase.com)
   - Sign up for a free account

2. **Create a New Project**
   - Click "New Project"
   - Enter a project name (e.g., "melody-matrix")
   - Set a database password (save this securely)
   - Choose a region closest to you
   - Click "Create new project"

3. **Get Your Supabase Credentials**
   - Once your project is created, go to **Settings** → **API**
   - Copy your **Project URL** (looks like: `https://xxxxxxxxxxxxx.supabase.co`)
   - Copy your **anon/public key** (starts with `eyJ...`)

#### 3. Configure Authentication

**Create `config.js` file:**

1. Copy the example configuration file:
   ```bash
   cp config.example.js config.js
   ```
   Or manually create a new file named `config.js`

2. Open `config.js` and fill in your Supabase credentials:
   ```javascript
   const CONFIG = {
       SUPABASE_URL: 'https://your-project-id.supabase.co',
       SUPABASE_ANON_KEY: 'your-actual-anon-key-here'
   };
   ```

3. Replace the placeholder values:
   - `SUPABASE_URL`: Your Supabase Project URL (from Settings → API → Project URL)
   - `SUPABASE_ANON_KEY`: Your Supabase anon/public key (from Settings → API → Project API keys → anon public)

4. **Important**: 
   - `config.js` is already in `.gitignore` and will NOT be committed to Git
   - `config.example.js` is safe to commit (it's just a template)
   - Never share your `config.js` file or commit it to version control

#### 4. Configure Google OAuth (Optional but Recommended)

To enable Google sign-in and sign-up:

1. **Set Up Google Cloud Console**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Go to **APIs & Services** → **Credentials**
   - Click **Create Credentials** → **OAuth client ID**
   - Configure OAuth consent screen (if prompted)
   - Application type: **Web application**
   - Add authorized JavaScript origins: `http://localhost:8000` (or your port)
   - Add authorized redirect URI: `https://YOUR_SUPABASE_PROJECT_ID.supabase.co/auth/v1/callback`
   - Copy the **Client ID** and **Client secret**

2. **Configure Google Provider in Supabase**
   - In Supabase dashboard → **Authentication** → **Providers**
   - Find **Google** and click it
   - Enable Google: Toggle **ON**
   - Paste your **Client ID** and **Client secret** from Google Cloud Console
   - Click **Save**

3. **Configure Redirect URLs in Supabase**
   - Go to **Authentication** → **URL Configuration**
   - **Site URL**: `http://localhost:8000` (or your development port)
   - **Redirect URLs**: Add `http://localhost:8000/**` (or specific paths like `http://localhost:8000/dashboard.html`)

#### 5. Configure Supabase Authentication Settings

1. **Enable Email Authentication**
   - In Supabase dashboard, go to **Authentication** → **Providers**
   - Ensure **Email** provider is enabled
   - Configure email templates if needed (optional)

2. **Optional: Enable Anonymous Authentication (for Guest Login)**
   - In Supabase dashboard, go to **Authentication** → **Providers**
   - Scroll down and enable **Anonymous** provider
   - This allows true anonymous guest login
   - If not enabled, guest login will use local storage fallback

3. **Configure Email Settings (Optional)**
   - Go to **Authentication** → **Email Templates**
   - Customize confirmation and password reset emails
   - Or use Supabase's default templates

#### 6. Run the Application

Simply open `login.html` in your web browser:
- Double-click `login.html`, or
- Right-click → Open with → Your preferred browser
- Or use a local server:
  ```bash
  # Using Python
  python -m http.server 8000
  
  # Using Node.js (if you have http-server installed)
  npx http-server
  
  # Then navigate to http://localhost:8000/login.html
  ```

## 📁 Project Structure

```
Melody Matrix/
│
├── index.html          # Signup page
├── login.html          # Login page (entry point)
├── config.example.js   # Configuration template (safe to commit)
├── config.js           # Your actual config (NOT committed - in .gitignore)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔐 Authentication Flow

1. **New Users (Email/Password)**
   - Start at `login.html`
   - Click "Sign Up" link → Redirects to `index.html`
   - Fill in registration form (name, email, password, confirm password)
   - Password validation: Checks if passwords match and meet minimum length (6 characters)
   - Account created in Supabase
   - Email verification sent (if enabled)
   - Redirected back to login page (user must log in separately)

2. **New Users (Google OAuth)**
   - Start at `index.html` (signup page)
   - Click "Sign up with Google" button
   - Redirected to Google OAuth consent screen
   - After approval, account created and user logged in
   - Redirected to dashboard (when implemented)

3. **Existing Users (Email/Password)**
   - Start at `login.html`
   - Enter email and password
   - Authenticated via Supabase
   - Session stored in localStorage
   - Redirected to dashboard (when implemented)

4. **Existing Users (Google OAuth)**
   - Start at `login.html`
   - Click "Continue with Google" button
   - Redirected to Google OAuth consent screen
   - After approval, authenticated and logged in
   - Redirected to dashboard (when implemented)

5. **Guest Users**
   - Start at `login.html`
   - Click "Login as Guest" button
   - Creates anonymous session (if enabled in Supabase) or local guest session
   - Guest status stored in localStorage
   - Redirected to dashboard (when implemented)

## 🌿 Branch Information

- **Current Branch**: Contains login page implementation
- **Main Branch**: Contains signup page (`index.html`)

## 🔧 Configuration Notes

### Configuration System
- **External Config**: All Supabase credentials are stored in `config.js` (not committed to Git)
- **Template File**: `config.example.js` shows the required configuration structure
- **Security**: `config.js` is in `.gitignore` to prevent accidental commits of sensitive data

### Supabase Configuration
- **Email Authentication**: Enabled by default
- **Google OAuth**: Optional but recommended (requires Google Cloud Console setup)
- **Anonymous Authentication**: Optional (for guest login)
- **Email Verification**: Can be enabled/disabled in Supabase settings
- **Password Requirements**: 
  - Minimum 6 characters (enforced in code)
  - Password and confirm password must match (validated on signup)

### Local Storage
The application uses browser localStorage to store:
- User session data
- Guest status flag
- Authentication tokens

## 🚧 Future Development

- [ ] Dashboard/main application page
- [ ] Music generation functionality
- [ ] User profile management
- [ ] Password reset functionality
- [ ] Session management improvements

## 📝 Notes

- **Configuration**: Must create `config.js` from `config.example.js` before use
- **Redirect URLs**: Currently redirects to `dashboard.html` (not yet implemented)
- **Guest Login**: Falls back to local storage if anonymous auth is not enabled in Supabase
- **Email Verification**: Users may need to verify their email before logging in (depending on Supabase settings)
- **Password Validation**: Signup form validates password match and minimum length before submission
- **Google OAuth**: Requires both Google Cloud Console and Supabase configuration

## 🐛 Troubleshooting

### Authentication Not Working
- **Missing Configuration**: Ensure `config.js` exists and contains valid Supabase credentials
- **Config Error**: Check browser console for "Configuration not found" errors
- Verify Supabase URL and anon key are correctly set in `config.js`
- Check browser console for errors
- Ensure Supabase project is active
- Verify email provider is enabled in Supabase dashboard

### Configuration Issues
- **"Configuration missing" alert**: Create `config.js` by copying `config.example.js`
- **Config not loading**: Ensure `config.js` is in the same directory as `index.html` and `login.html`
- **Invalid credentials**: Verify your Supabase URL and anon key in Supabase Dashboard → Settings → API

### Google OAuth Issues
- **"redirect_uri_mismatch"**: Ensure Supabase callback URL is added in Google Cloud Console → Authorized redirect URIs
- **"access_denied"**: Check OAuth consent screen is published or you're added as a test user
- **"invalid_client"**: Verify Client ID and Client secret are correct in Supabase → Authentication → Providers → Google

### Guest Login Issues
- Enable anonymous authentication in Supabase if you want true anonymous sessions
- Otherwise, guest login will use local storage fallback (works without Supabase)

### Email Verification
- Check spam folder for verification emails
- Verify email templates are configured in Supabase
- Check Supabase logs for email sending errors


**Note**: This project is currently in development. The authentication pages are functional, but the main application (dashboard and music generation) is yet to be implemented.
