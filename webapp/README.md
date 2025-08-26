# Skillstree Local Web App

This tiny Flask web app serves `skill_tree.json` and stores per-user progress in a data directory outside the repo.

Run locally:

```powershell
python -m pip install -r requirements.txt
python webapp\app.py
```

Open http://127.0.0.1:5000

Data storage:
- Progress is stored in `%LOCALAPPDATA%\.skillstree\progress.json` on Windows or `~/.skillstree/progress.json` on Unix.
- You can override location with `SKILLSTREE_DATA_DIR`.
