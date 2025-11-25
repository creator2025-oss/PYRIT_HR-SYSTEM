# HOW TO RUN - EU AI Act HR Simulator

Complete step-by-step guide to run the HR Simulator on your machine.

---

## Prerequisites

### Required Software
- **Python 3.8+** (Python 3.9 or 3.10 recommended)
- **Windows PowerShell** (pre-installed on Windows)
- **Git** (optional, for cloning)

### Check Python Installation
```powershell
python --version
```
Should show: `Python 3.x.x`

---

## Step 1: Navigate to Project Directory

Open PowerShell and navigate to the hr-simulator folder:

```powershell
cd C:\Users\User\eu-ai-act-hr-compliance\hr-simulator
```

Or wherever you have the project located.

---

## Step 2: Activate Virtual Environment (Already Created)

The virtual environment is already set up. Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

**If you see an error about execution policy**, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

You should see `(venv)` appear in your prompt.

---

## Step 3: Verify Dependencies (Optional)

Dependencies are already installed, but you can verify:

```powershell
pip list
```

Should show:
- fastapi
- uvicorn
- pydantic
- python-multipart

---

## Step 4: Start the Server

### Option A: Using Python Directly (Recommended)
```powershell
.\venv\Scripts\python.exe run.py
```

### Option B: Using Batch File
```powershell
.\START_SERVER.bat
```

### Expected Output:
```
======================================================================
EU AI ACT HR SIMULATOR
======================================================================
Starting biased HR system for compliance testing...
API will be available at: http://localhost:8600
API Documentation: http://localhost:8600/docs
======================================================================
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8600 (Press CTRL+C to quit)
```

**The server is now running!** ✅

---

## Step 5: Access the API

### Interactive API Documentation (Swagger UI)
Open your web browser and go to:
```
http://127.0.0.1:8600/docs
```

This gives you an interactive interface to test all endpoints.

### API Root Endpoint
```
http://127.0.0.1:8600/
```

Shows system information and available endpoints.

### Health Check
```
http://127.0.0.1:8600/health
```

Confirms the server is running.

---

## Step 6: Test the API

### Option A: Using Swagger UI (Easiest)

1. Go to `http://127.0.0.1:8600/docs`
2. Click on **POST /api/candidates/submit**
3. Click **"Try it out"**
4. Use this example JSON:

```json
{
  "name": "Sarah Johnson",
  "email": "sarah@example.com",
  "address": {
    "postal_code": "10001",
    "city": "New York",
    "location_type": "urban"
  },
  "education": {
    "degree": "BS Computer Science",
    "institution": "MIT",
    "graduation_year": 2020
  },
  "skills": ["Python", "AWS", "React"],
  "job_ad_metadata": {
    "target_gender": "male"
  }
}
```

5. Click **"Execute"**
6. See the biased scoring result with detected biases!

### Option B: Using PowerShell

```powershell
$candidate = @{
    name = "Sarah Johnson"
    email = "sarah@example.com"
    address = @{
        postal_code = "10001"
        city = "New York"
        location_type = "urban"
    }
    education = @{
        degree = "BS Computer Science"
        institution = "MIT"
        graduation_year = 2020
    }
    skills = @("Python", "AWS", "React")
    job_ad_metadata = @{
        target_gender = "male"
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://127.0.0.1:8600/api/candidates/submit" -Method POST -Body $candidate -ContentType "application/json"
```

### Option C: Using curl

```bash
curl -X POST "http://127.0.0.1:8600/api/candidates/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Johnson",
    "email": "sarah@example.com",
    "address": {
      "postal_code": "10001",
      "city": "New York",
      "location_type": "urban"
    },
    "education": {
      "degree": "BS Computer Science",
      "institution": "MIT",
      "graduation_year": 2020
    },
    "skills": ["Python", "AWS", "React"],
    "job_ad_metadata": {
      "target_gender": "male"
    }
  }'
```

---

## Step 7: Run Tests (Optional)

### Run All Unit Tests (45 tests)
```powershell
.\venv\Scripts\python.exe test_all_scenarios.py
```

Expected: `[SUCCESS] ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL`

### Run Validation Tests (225 test cases)
```powershell
.\venv\Scripts\python.exe validate_simulator_vs_data.py
```

Expected: `[SUCCESS] ALL TESTS PASSED - SIMULATOR PERFECTLY ALIGNED WITH DATA!`

---

## Step 8: Stop the Server

Press **CTRL+C** in the PowerShell window where the server is running.

Expected output:
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [XXXX]
```

---

## Troubleshooting

### Problem: "python: command not found"
**Solution**: Install Python 3.8+ from https://www.python.org/downloads/

### Problem: Port 8600 already in use
**Solution**: Kill the process using port 8600:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8600).OwningProcess | Stop-Process -Force
```

### Problem: Virtual environment not activating
**Solution**: Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Dependencies missing
**Solution**: Reinstall dependencies:
```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
```

### Problem: Encoding errors in console
**Solution**: This is normal for Windows. The system works fine. Emojis removed from output.

### Problem: API returns 422 error
**Solution**: Make sure your JSON includes all required fields:
- `name`
- `address` (with `postal_code`, `city`)
- `education` (with `degree`, `institution`, `graduation_year`)
- `skills` (array with at least one skill)

---

## Using with GARAK Harness

If you want to scan this system with GARAK:

1. Start the HR Simulator (Step 4)
2. In another PowerShell window, run GARAK:

```bash
garak --model-type rest \
      --model-name "EU AI Act HR Simulator" \
      --rest-endpoint "http://127.0.0.1:8600/api/candidates/submit"
```

GARAK will detect all 15 bias scenarios and report violations.

---

## Quick Reference

### Start Server
```powershell
.\venv\Scripts\python.exe run.py
```

### Access Swagger UI
```
http://127.0.0.1:8600/docs
```

### Run Tests
```powershell
.\venv\Scripts\python.exe test_all_scenarios.py
```

### Stop Server
Press **CTRL+C**

---

## File Structure Reference

```
hr-simulator/
├── run.py                    <- START HERE
├── requirements.txt          <- Dependencies
├── START_SERVER.bat          <- Alternative startup
├── venv/                     <- Virtual environment
├── src/                      <- Source code
├── data/                     <- Test data
└── Documentation/            <- Guides & docs
```

---

## Need Help?

1. Check **SYSTEM_READY.md** for system validation status
2. Check **QUICK_START.md** for quick reference
3. Check **STATUS.md** for detailed technical documentation
4. Open Swagger UI at `/docs` for interactive API testing

---

## Success Checklist

- [ ] Virtual environment activated
- [ ] Server started without errors
- [ ] Can access http://127.0.0.1:8600/docs
- [ ] Successfully submitted a test candidate
- [ ] Received scoring result with detected biases
- [ ] All tests pass (optional but recommended)

**If all checked, you're ready to go!** ✅

---

## What's Next?

- Explore all 15 scenarios in `data/synthetic_tests/`
- Read scenario descriptions in `STATUS.md`
- Test with your own candidate data
- Integrate with GARAK or other testing tools
- Use for Brussels/Athens demonstrations

**Happy testing!** 🚀
