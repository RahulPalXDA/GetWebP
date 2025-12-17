# GetWebP - Image Optimization API

A Flask-based image optimization API that converts images to WebP format.

## Features

- User registration with admin approval
- API key authentication
- Image to WebP conversion
- Usage quota management
- Admin dashboard for user management

## Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://127.0.0.1:5000`

## Default Admin Credentials

- **Email:** `admin`
- **Password:** `admin@1234`

## API Usage

### Optimize Image

```bash
curl -X POST http://your-domain.com/api/v1/optimize \
  -F "api_key=YOUR_API_KEY" \
  -F "image_url=https://example.com/image.jpg" \
  -F "quality=80" \
  --output optimized.webp
```

## PythonAnywhere Deployment

1. **Upload files** to PythonAnywhere (via Git or manual upload)

2. **Create a virtual environment** in Bash console:
   ```bash
   cd ~/GetWebP
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Web App:**
   - Go to Web tab → Add a new web app
   - Choose "Manual configuration" → Python 3.10+
   - Set Source code directory: `/home/YOUR_USERNAME/GetWebP`
   - Set Working directory: `/home/YOUR_USERNAME/GetWebP`

4. **Configure WSGI file:**
   - Click on the WSGI configuration file link
   - Replace contents with:
   ```python
   import sys
   project_home = '/home/YOUR_USERNAME/GetWebP'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)
   
   from app import app as application, init_db
   init_db()
   ```

5. **Set Virtual Environment path:**
   - In Web tab, set Virtualenv: `/home/YOUR_USERNAME/GetWebP/.venv`

6. **Reload** the web app

## File Structure

```
GetWebP/
├── app.py              # Main application
├── models.py           # Database models
├── wsgi.py             # WSGI configuration
├── requirements.txt    # Dependencies
├── routes/
│   ├── admin.py        # Admin routes
│   ├── api.py          # API routes
│   ├── auth.py         # Authentication routes
│   ├── dashboard.py    # Dashboard routes
│   └── main.py         # Main routes
├── templates/
│   ├── layout.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── dashboard_api.html
│   ├── dashboard_settings.html
│   └── admin.html
└── instance/
    └── db.sqlite3      # Database (auto-created)
```

## License

MIT
