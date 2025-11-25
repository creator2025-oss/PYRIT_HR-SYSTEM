# GitHub Setup Instructions

## Pushing to GitHub

### Option 1: Create New Repository (Recommended)

1. **Go to GitHub** and create a new repository:
   - Name: `EU-AI-Act-HR-Compliance-Testing`
   - Description: `PYRIT harness for EU AI Act Annex III-4 HR compliance testing with live simulator and dashboard`
   - Public or Private (your choice)
   - **Don't** initialize with README (we have one)

2. **In your terminal, navigate to this folder:**
   ```bash
   cd EU_AI_Act_HR_Compliance_Demo
   ```

3. **Initialize and push:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Complete EU AI Act HR compliance testing system"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/EU-AI-Act-HR-Compliance-Testing.git
   git push -u origin main
   ```

### Option 2: Add to Existing Repository

```bash
cd EU_AI_Act_HR_Compliance_Demo
git init
git add .
git commit -m "Add EU AI Act compliance testing system"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Sharing with Your Colleague

### Option A: GitHub (Clean, Recommended)

1. **Push to GitHub** (see above)
2. **Share the repository URL** with your colleague
3. **They clone it:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/EU-AI-Act-HR-Compliance-Testing.git
   cd EU-AI-Act-HR-Compliance-Testing
   ```
4. **They follow QUICK_START.md**

### Option B: Direct ZIP File

1. **Zip this entire folder** (`EU_AI_Act_HR_Compliance_Demo`)
2. **Share via email/drive/etc.**
3. **They extract and follow QUICK_START.md**

## Repository Description (for GitHub)

```
Complete EU AI Act Annex III-4 HR compliance testing system with:
- PYRIT harness for automated testing
- Live biased HR simulator (FastAPI)
- Schema-compliant evidence generation
- Interactive Streamlit dashboard
- 5 pre-configured test scenarios
- Full documentation and setup scripts
```

## Repository Topics (for GitHub)

Add these topics to make it discoverable:
- `eu-ai-act`
- `compliance-testing`
- `pyrit`
- `hr-systems`
- `bias-detection`
- `streamlit`
- `fastapi`
- `regulatory-compliance`

## What's Included

✅ **Complete PYRIT Harness**
- Scenario loader, orchestrators, scorers
- Evidence builder (13-field schema)
- 5 test scenarios with full configs

✅ **HR Simulator**
- FastAPI server with biased scoring
- 5 violation types (SELF, NEG, DEM, EMO, INT)
- Synthetic test data

✅ **Streamlit Dashboard**
- 4 interactive pages
- Live test execution
- Evidence explorer
- Violation visualization

✅ **Documentation**
- Complete README
- Quick start guide
- Troubleshooting
- Architecture diagrams

✅ **Setup Scripts**
- One-click installation (SETUP.bat)
- Simulator launcher (RUN_SIMULATOR.bat)
- Dashboard launcher (RUN_DASHBOARD.bat)

## Files Your Colleague Needs

**Minimum required:**
- `pyrit_demo_harness/` (entire folder)
- `hr_simulator/` (entire folder)
- `requirements.txt`
- `README.md`
- `QUICK_START.md`

**Nice to have:**
- `.gitignore`
- `SETUP.bat`, `RUN_SIMULATOR.bat`, `RUN_DASHBOARD.bat`
- This file (GITHUB_SETUP.md)

## After Sharing

Tell your colleague to:

1. ✅ Read `QUICK_START.md`
2. ✅ Run `SETUP.bat` or `pip install -r requirements.txt`
3. ✅ Start simulator: `RUN_SIMULATOR.bat`
4. ✅ Start dashboard: `RUN_DASHBOARD.bat`
5. ✅ Run first test in dashboard

That's it! System is fully self-contained and ready to use.

## Support

If your colleague has issues:
1. Check `QUICK_START.md` troubleshooting section
2. Verify simulator is running: http://127.0.0.1:8600/health
3. Check Python version (3.9+ required)
4. Try reinstalling: `pip install -r requirements.txt --force-reinstall`

---

**Ready to share!** Push to GitHub and send the link.
