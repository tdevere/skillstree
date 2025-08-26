1. Add "Run validation" endpoint and UI button for single node/rank — small
2. Add `--simulate` mode to `run_validation.py` and sample outputs — small
3. Implement per-user config file (`~/.skillstree/config.json`) and wire to template expansion — small
4. Add unit tests for `assert_expected` (happy path + edge cases) — small
5. Pin dependencies in `requirements.txt` (include MarkupSafe 2.0.1) — small
6. Add pytest-based smoke tests for runner CLI — small
7. Update `run_validation.py` to support `--nodes-file` and `--output` (JSON) — small
8. Add results modal to web UI showing last run stdout and assertions — small
9. Replace placeholder values (`<pipeline-name>`) in skill_tree.json with config templates — small
10. Add GitHub Action to create issues for nightly failures (already added) — verify
11. Improve README with local setup steps and how to run the web UI — small
12. Add ability in web UI to mark a rank as `needs-review` and store annotation — small
13. Add a smoke test that checks Flask app starts and `/api/skill_tree` returns 200 — small
14. Add `tasks/` tag to issue templates for easy triage — small
15. Add a CONTRIBUTING.md with coding standards and test guidance — small
16. Create a 'simulation' job that runs runner in simulate mode for PR checks — small
17. Add a cron that posts a daily status summary to the repo Discussions — small
18. Add a helper script to populate `nightly_nodes.txt` from `skill_tree.json` (top N nodes) — small
19. Add a check that validates `progress.json` is not committed into repo (gitignore) — small
20. Triage existing runner assertion failures and convert obvious ones to manual_check — small

> Tip: each morning, pick the top unfinished task from this list and work it for 30–90 minutes.
