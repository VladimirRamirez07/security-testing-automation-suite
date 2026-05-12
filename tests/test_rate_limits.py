import pytest
import requests
import time
import threading

class TestRateLimits:

    def test_login_rate_limit(self, base_url, session):
        """Verifica si existe rate limiting en el endpoint de login."""
        url = f"{base_url}/userinfo.php"
        response_times = []
        status_codes = []

        print("\n[Enviando 20 requests al login...]")

        for i in range(20):
            start = time.time()
            try:
                response = session.post(
                    url,
                    data={"uname": "admin", "pass": f"wrong{i}"},
                    timeout=10
                )
                elapsed = time.time() - start
                response_times.append(elapsed)
                status_codes.append(response.status_code)

            except requests.exceptions.RequestException as e:
                print(f"  Request {i+1}: ERROR - {e}")

        print(f"\n[STATUS CODES]: {status_codes}")
        avg = sum(response_times)/len(response_times) if response_times else 0
        print(f"[TIEMPO PROMEDIO]: {avg:.3f}s")
        print(f"[STATUS ÚNICOS]: {set(status_codes)}")

        # Si en algún momento devuelve 429 = hay rate limiting
        if 429 in status_codes:
            print("[PROTEGIDO]: Se detectó rate limiting (429 Too Many Requests)")
        else:
            print("[VULNERABILIDAD]: No se detectó rate limiting en login")

        assert True

    def test_search_rate_limit(self, base_url, session):
        """Verifica rate limiting en búsquedas."""
        url = f"{base_url}/search.php"
        status_codes = []

        for i in range(15):
            try:
                response = session.get(
                    url,
                    params={"test": f"query{i}"},
                    timeout=10
                )
                status_codes.append(response.status_code)
            except requests.exceptions.RequestException:
                pass

        print(f"\n[BÚSQUEDAS - STATUS CODES]: {status_codes}")

        if 429 in status_codes:
            print("[PROTEGIDO]: Rate limiting activo en búsquedas")
        else:
            print("[VULNERABILIDAD]: Sin rate limiting en búsquedas")

        assert True

    def test_concurrent_requests(self, base_url):
        """Simula múltiples usuarios simultáneos (stress básico)."""
        url = f"{base_url}/index.php"
        results = []

        def make_request():
            try:
                start = time.time()
                response = requests.get(url, timeout=10)
                elapsed = time.time() - start
                results.append({
                    "status": response.status_code,
                    "time": elapsed
                })
            except requests.exceptions.RequestException as e:
                results.append({"status": "ERROR", "time": 0})

        threads = [threading.Thread(target=make_request) for _ in range(10)]

        start_all = time.time()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        total_time = time.time() - start_all

        success = [r for r in results if r["status"] == 200]
        errors = [r for r in results if r["status"] == "ERROR"]
        avg_time = sum(r["time"] for r in results) / len(results)

        print(f"\n[REQUESTS CONCURRENTES]: 10")
        print(f"[EXITOSOS]: {len(success)}")
        print(f"[ERRORES]: {len(errors)}")
        print(f"[TIEMPO TOTAL]: {total_time:.2f}s")
        print(f"[TIEMPO PROMEDIO POR REQUEST]: {avg_time:.3f}s")

        assert len(success) > 0, "Ningún request concurrente tuvo éxito"