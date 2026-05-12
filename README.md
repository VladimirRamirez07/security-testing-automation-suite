# 🔒 Security Testing Automation Suite

![Tests](https://img.shields.io/badge/tests-25%20passed-brightgreen)
![CI](https://github.com/VladimirRamirez07/security-testing-automation-suite/actions/workflows/security-tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.14-blue)
![pytest](https://img.shields.io/badge/pytest-9.0.3-orange)
![Selenium](https://img.shields.io/badge/selenium-4.43.0-43B02A?logo=selenium&logoColor=white)
![OWASP ZAP](https://img.shields.io/badge/OWASP%20ZAP-2.17.0-blueviolet)
![Requests](https://img.shields.io/badge/requests-2.34.0-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-informational)

> Suite automatizada que prueba SQLi básica, headers inseguros, endpoints vulnerables,
> fuerza de passwords, rate limits, HTTPS y auth weaknesses.
> Combina **QA + Security + DevSecOps**.

---

## 📁 Project Structure
    security-testing-automation-suite/
    ├── .github/
    │   └── workflows/
    │       └── security-tests.yml
    ├── tests/
    │   ├── __init__.py
    │   ├── test_sqli.py
    │   ├── test_headers.py
    │   ├── test_endpoints.py
    │   ├── test_passwords.py
    │   ├── test_rate_limits.py
    │   ├── test_https.py
    │   └── test_auth.py
    ├── utils/
    │   ├── __init__.py
    │   ├── zap_client.py
    │   └── report_generator.py
    ├── reports/
    ├── conftest.py
    ├── requirements.txt
    ├── .gitignore
    ├── LICENSE
    └── README.md

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| ![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white) | 3.14 | Core language |
| ![pytest](https://img.shields.io/badge/pytest-9.0.3-orange?logo=pytest&logoColor=white) | 9.0.3 | Test framework |
| ![Selenium](https://img.shields.io/badge/Selenium-4.43.0-43B02A?logo=selenium&logoColor=white) | 4.43.0 | Browser automation |
| ![Requests](https://img.shields.io/badge/Requests-2.34.0-yellow) | 2.34.0 | HTTP client |
| ![OWASP ZAP](https://img.shields.io/badge/OWASP%20ZAP-2.17.0-blueviolet) | 2.17.0 | Active security scanner |
| ![pytest-html](https://img.shields.io/badge/pytest--html-4.2.0-lightblue) | 4.2.0 | HTML report generation |

---

## 🧪 Test Modules

| Module | Tests | What it covers |
|---|---|---|
| `test_headers.py` | 4 | Missing security headers, Server & X-Powered-By exposure |
| `test_sqli.py` | 3 | Basic SQLi, login SQLi, time-based blind SQLi |
| `test_endpoints.py` | 4 | Sensitive endpoints, HTTP methods, directory listing, robots.txt |
| `test_passwords.py` | 4 | Weak password login, account lockout, password in URL, complexity |
| `test_rate_limits.py` | 3 | Login rate limit, search rate limit, concurrent requests |
| `test_https.py` | 4 | HTTP→HTTPS redirect, SSL cert, weak TLS, mixed content |
| `test_auth.py` | 4 | Auth bypass, session cookie flags, default credentials, IDOR |

---

## ▶️ Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/VladimirRamirez07/security-testing-automation-suite.git
cd security-testing-automation-suite
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run all tests with HTML report
```bash
python -m pytest tests/ -v --html=reports/report.html --self-contained-html
```

### 4. Run a specific module
```bash
python -m pytest tests/test_sqli.py -v
python -m pytest tests/test_headers.py -v
```

---

## 📊 Test Results
25 passed, 1 skipped in 50.08s
| Category | Result |
|---|---|
| SQL Injection | ✅ 3/3 passed |
| Security Headers | ✅ 4/4 passed |
| Endpoints | ✅ 4/4 passed |
| Password Security | ✅ 4/4 passed |
| Rate Limiting | ✅ 3/3 passed |
| HTTPS / SSL | ✅ 3/3 passed · 1 skipped |
| Authentication | ✅ 4/4 passed |

---

## 📄 Reports

After running the tests, an HTML report is auto-generated at:
reports/report.html
Open it in any browser for a full visual breakdown of results.

---

## ⚠️ Disclaimer

This suite is intended for **educational and authorized testing purposes only**.
The default target (`juice-shop.herokuapp.com`) is a deliberately vulnerable
application provided for security training. Never run this against systems
you do not own or have explicit permission to test.

---

## 👤 Author

**VladimirRamirez07**

[![GitHub](https://img.shields.io/badge/GitHub-VladimirRamirez07-181717?logo=github)](https://github.com/VladimirRamirez07)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vladimir%20Ramírez-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vladimir-ramírez-303a433ba)