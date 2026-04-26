# NextStepCareers

NextStep Careers is a Django web application for job seekers and employers. It includes account registration, secure login/logout, profile management, job posting, job search, application tracking, messaging, and notifications.

## Setup
1. Activate your virtual environment:
   - PowerShell: `.\myworld\Scripts\Activate.ps1`
   - CMD: `myworld\Scripts\activate.bat`
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```powershell
   python manage.py migrate
   ```
4. Run the development server:
   ```powershell
   python manage.py runserver
   ```
5. Open `http://127.0.0.1:8000/` in your browser.

## Documentation
- See `USER_DOCUMENTATION.md` for feature details, usage flows, and requirement coverage.
