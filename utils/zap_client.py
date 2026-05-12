import time
import requests


ZAP_API_KEY = "changeme123"
ZAP_BASE_URL = "http://localhost:8080"


class ZAPClient:

    def __init__(self, api_key=ZAP_API_KEY, base_url=ZAP_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()

    def _request(self, endpoint, params=None):
        """Realiza una request a la API de ZAP."""
        if params is None:
            params = {}
        params["apikey"] = self.api_key
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ZAP ERROR]: {e}")
            return None

    def is_running(self):
        """Verifica si ZAP está corriendo."""
        try:
            response = self.session.get(
                f"{self.base_url}/JSON/core/view/version/",
                params={"apikey": self.api_key},
                timeout=5
            )
            data = response.json()
            print(f"[ZAP]: Versión {data.get('version', 'desconocida')}")
            return True
        except Exception:
            print("[ZAP]: No está corriendo o no es accesible")
            return False

    def spider_scan(self, target_url):
        """Lanza un spider scan sobre el target."""
        print(f"\n[ZAP SPIDER]: Iniciando en {target_url}...")
        result = self._request(
            "/JSON/spider/action/scan/",
            {"url": target_url, "maxChildren": 5}
        )
        if not result:
            return None

        scan_id = result.get("scan")
        print(f"[ZAP SPIDER]: Scan ID: {scan_id}")

        while True:
            status = self._request(
                "/JSON/spider/view/status/",
                {"scanId": scan_id}
            )
            progress = int(status.get("status", 0))
            print(f"  Progreso: {progress}%")
            if progress >= 100:
                break
            time.sleep(3)

        print("[ZAP SPIDER]: Completado")
        return scan_id

    def active_scan(self, target_url):
        """Lanza un active scan sobre el target."""
        print(f"\n[ZAP ACTIVE SCAN]: Iniciando en {target_url}...")
        result = self._request(
            "/JSON/ascan/action/scan/",
            {"url": target_url}
        )
        if not result:
            return None

        scan_id = result.get("scan")
        print(f"[ZAP ACTIVE SCAN]: Scan ID: {scan_id}")

        while True:
            status = self._request(
                "/JSON/ascan/view/status/",
                {"scanId": scan_id}
            )
            progress = int(status.get("status", 0))
            print(f"  Progreso: {progress}%")
            if progress >= 100:
                break
            time.sleep(5)

        print("[ZAP ACTIVE SCAN]: Completado")
        return scan_id

    def get_alerts(self, target_url):
        """Obtiene todas las alertas/vulnerabilidades encontradas."""
        result = self._request(
            "/JSON/core/view/alerts/",
            {"baseurl": target_url}
        )
        if not result:
            return []

        alerts = result.get("alerts", [])
        print(f"\n[ZAP ALERTAS]: {len(alerts)} vulnerabilidades encontradas")

        for alert in alerts:
            risk = alert.get("risk", "")
            name = alert.get("alert", "")
            url  = alert.get("url", "")
            print(f"  [{risk}] {name} -> {url}")

        return alerts

    def get_summary(self, target_url):
        """Retorna un resumen de riesgos."""
        alerts = self.get_alerts(target_url)
        summary = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}

        for alert in alerts:
            risk = alert.get("risk", "Informational")
            if risk in summary:
                summary[risk] += 1

        print(f"\n[ZAP RESUMEN DE RIESGOS]:")
        for level, count in summary.items():
            print(f"  {level}: {count}")

        return summary