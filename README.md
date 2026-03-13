# Melody Matrix 🎵

**AI Music Generator** - A web application for generating music using artificial intelligence.

## 📋 Overview

Melody Matrix is a modern web application that allows users to generate music using AI. The project currently includes authentication pages (login and signup) with a beautiful, animated UI featuring floating music notes.

## 🎨 Features

### Current Features
- **Login Page** (`login.html`)
  - Email and password authentication
  - Guest login option
  - Beautiful animated UI with floating music notes
  - Form validation and error handling
  - Link to signup page for new users

- **Signup Page** (`index.html`)
  - User registration with full name, email, and password
  - Password confirmation validation
  - Email verification support
  - Link to login page for existing users

### Design
- Modern, clean UI with pastel color scheme
- Animated floating music notes (♪ ♫ ♩ ♬)
- Responsive design
- Smooth transitions and hover effects
- Poppins font family for a modern look

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

1. **Update `login.html`**
   - Open `login.html` in a text editor
   - Find lines 265-266:
   ```javascript
   const SUPABASE_URL = 'YOUR_SUPABASE_URL';
   const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
   ```
   - Replace `YOUR_SUPABASE_URL` with your actual Supabase Project URL
   - Replace `YOUR_SUPABASE_ANON_KEY` with your actual Supabase anon key

2. **Update `index.html`**
   - Open `index.html` in a text editor
   - Find lines 264-265:
   ```javascript
   const SUPABASE_URL = 'YOUR_SUPABASE_URL';
   const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
   ```
   - Replace `YOUR_SUPABASE_URL` with your actual Supabase Project URL
   - Replace `YOUR_SUPABASE_ANON_KEY` with your actual Supabase anon key

#### 4. Configure Supabase Authentication Settings

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

#### 5. Run the Application

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
└── README.md          # This file
```

## 🔐 Authentication Flow

1. **New Users**
   - Start at `login.html`
   - Click "Sign Up" link → Redirects to `index.html`
   - Fill in registration form
   - Account created in Supabase
   - Email verification sent (if enabled)
   - Redirected back to login page

2. **Existing Users**
   - Start at `login.html`
   - Enter email and password
   - Authenticated via Supabase
   - Session stored in localStorage
   - Redirected to dashboard (when implemented)

3. **Guest Users**
   - Start at `login.html`
   - Click "Login as Guest" button
   - Creates anonymous session (if enabled) or local guest session
   - Guest status stored in localStorage
   - Redirected to dashboard (when implemented)

## 🌿 Branch Information

- **Current Branch**: Contains login page implementation
- **Main Branch**: Contains signup page (`index.html`)

## 🔧 Configuration Notes

### Supabase Configuration
- **Email Authentication**: Enabled by default
- **Anonymous Authentication**: Optional (for guest login)
- **Email Verification**: Can be enabled/disabled in Supabase settings
- **Password Requirements**: Minimum 6 characters (enforced in code)

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
- [ ] Social login options
- [ ] Session management improvements

## 📝 Notes

- **Supabase URLs**: Currently using placeholder values. Must be configured before use.
- **Redirect URLs**: Currently redirects to `dashboard.html` (not yet implemented)
- **Guest Login**: Falls back to local storage if anonymous auth is not enabled in Supabase
- **Email Verification**: Users may need to verify their email before logging in (depending on Supabase settings)

## 🐛 Troubleshooting

### Authentication Not Working
- Verify Supabase URL and anon key are correctly set
- Check browser console for errors
- Ensure Supabase project is active
- Verify email provider is enabled in Supabase dashboard

### Guest Login Issues
- Enable anonymous authentication in Supabase if you want true anonymous sessions
- Otherwise, guest login will use local storage fallback (works without Supabase)

### Email Verification
- Check spam folder for verification emails
- Verify email templates are configured in Supabase
- Check Supabase logs for email sending errors

## 📄 License

[Add your license here]

## 👤 Author

[Add your name/contact information here]

---

**Note**: This project is currently in development. The authentication pages are functional, but the main application (dashboard and music generation) is yet to be implemented.
