# How to Run Locally

Since you have already built the frontend and installed dependencies, you only need to run one command to start the application.

### 1. Open Terminal
Navigate to your project folder:
```powershell
cd f:\rad-application
```

### 2. Run the Application
```powershell
python app.py
```

### 3. Access in Browser
Open: [http://localhost:8000](http://localhost:8000)

---

## Troubleshooting
If it says "Module not found", re-install dependencies:
```powershell
pip install -r requirements.txt
```

If the frontend doesn't load:
```powershell
cd frontend
npm run build
cd ..
python app.py
```
