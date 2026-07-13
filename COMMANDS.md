# Useful Commands

## Playwright

### Codegen — record locators / generate code

```bash
playwright codegen https://testing001.devccl-billzweb.crystalbillz.com
```

Opens a browser + code panel. Click elements to get their locators automatically.

### Install browsers

```bash
playwright install
```

### Codegen — already logged in, on the dashboard

Double-click **`codegen.bat`**, or run:

```bash
python codegen.py
```

Logs in headlessly, saves the session, and opens codegen already authenticated
on the dashboard — no manual login. Defaults to the admin creds in
`utils/constants.py`.

Pass different credentials inline:

```bash
python codegen.py --email user@example.com --password "YourPasswordHere"
```

Record on a different page:

```bash
python codegen.py --url https://testing001.devccl-billzweb.crystalbillz.com/cities
```

### Codegen — save login session manually

Login in the browser yourself, then save the session to `auth.json`:

```bash
python -m playwright codegen https://testing001.devccl-billzweb.crystalbillz.com/login --save-storage=auth.json
```

### Codegen — load saved session and record on dashboard

Use the saved `auth.json` to open codegen already logged in:

```bash
python -m playwright codegen https://testing001.devccl-billzweb.crystalbillz.com/dashboard --load-storage=auth.json
```

---

python -m pytest tests/master_menu/test_cities.py::test_add_city --headed

### Run all tests

```bash
pytest
```

### Run a specific file

```bash
pytest tests/test_auth.py
```

### Run a specific test function

```bash
pytest tests/test_auth.py::test_successful_login
```

### Run a specific folder

```bash
pytest tests/master_menu/
```

### Run with verbose output (see each test name)

```bash
pytest -v
```

### Run with print statements visible

```bash
pytest -s
```

### Combine flags

```bash
pytest tests/test_auth.py -v -s
```

### Run tests matching a keyword

```bash
pytest -k "login"
```

### Stop after first failure

```bash
pytest -x
```

### Run in headed mode (see the browser)

```bash
pytest --headed
```

### Run in slow motion (easier to follow)

```bash
pytest --headed --slowmo 1000
```

### Run with a specific browser

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

---

## Shareable report — one HTML file for the team

`pytest` writes `results.xml` automatically after every run (set in `pytest.ini`).
`report.py` reads that and produces a single self-contained `reports/report.html` —
pass/fail/duration per test, grouped by suite. Send it over Slack / email / drive,
anyone opens it in a browser, no server needed.

### Full flow — run tests then build the shareable file

```bash
pytest && python report.py
```

```bash
python report.py
```

### Custom input / output paths

```bash
python report.py --results results.xml --out reports/report.html
```

---

## pip — managing packages

### Install dependencies

```bash
pip install -r requirements.txt
```

### Check installed packages

```bash
pip list
```

---

## Quick reference — what each flag does

| Flag                 | What it does                               |
| -------------------- | ------------------------------------------ |
| `-v`                 | Verbose — shows each test name and result  |
| `-s`                 | Shows print() output in terminal           |
| `-x`                 | Stops at first failure                     |
| `-k "word"`          | Runs only tests whose name contains "word" |
| `--headed`           | Opens a real browser window                |
| `--slowmo 1000`      | Slows browser actions by 1000ms            |
| `--browser chromium` | Picks the browser to use                   |
