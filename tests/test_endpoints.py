import pytest
import requests

SENSITIVE_ENDPOINTS = [
    "/admin",
    "/admin/",
    "/administrator",
    "/phpmyadmin",
    "/wp-admin",
    "/config.php",
    "/backup",
    "/backup.sql",
    "/db.sql",
    "/.env",
    "/robots.txt",
    "/sitemap.xml",
    "/server-status",
    "/info.php",
    "/phpinfo.php",
    "/test.php",
    "/login",
    "/api",
    "/api/v1",
    "/console",
]

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]

class TestEndpoints:

    def test_sensitive_endpoints_exposed(self, base_url, session):
        """Escanea endpoints sensibles que no deberían ser accesibles."""
        exposed = []

        for endpoint in SENSITIVE_ENDPOINTS:
            url = f"{base_url}{endpoint}"
            try:
                response = session.get(url, timeout=8, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    exposed.append({
                        "endpoint": endpoint,
                        "status": response.status_code
                    })
            except requests.exceptions.RequestException:
                pass

        print(f"\n[ENDPOINTS EXPUESTOS]: {len(exposed)}")
        for e in exposed:
            print(f"  -> {e['endpoint']} | Status: {e['status']}")

        assert len(exposed) > 0, "No se encontraron endpoints expuestos"

    def test_http_methods_allowed(self, base_url, session):
        """Verifica qué métodos HTTP acepta el servidor."""
        allowed = []

        for method in HTTP_METHODS:
            try:
                response = session.request(method, base_url, timeout=8)
                if response.status_code not in [405, 501]:
                    allowed.append({
                        "method": method,
                        "status": response.status_code
                    })
            except requests.exceptions.RequestException:
                pass

        print(f"\n[MÉTODOS HTTP PERMITIDOS]:")
        for m in allowed:
            print(f"  -> {m['method']} | Status: {m['status']}")

        print(f"[INFO]: Métodos detectados: {[m['method'] for m in allowed]}")
        assert True

    def test_directory_listing(self, base_url, session):
        """Detecta si hay directory listing habilitado."""
        dirs_to_check = ["/images/", "/uploads/", "/files/", "/static/"]
        listing_enabled = []

        for path in dirs_to_check:
            url = f"{base_url}{path}"
            try:
                response = session.get(url, timeout=8)
                if "index of" in response.text.lower() or "parent directory" in response.text.lower():
                    listing_enabled.append(path)
            except requests.exceptions.RequestException:
                pass

        print(f"\n[DIRECTORY LISTING HABILITADO EN]: {listing_enabled}")
        assert True  # Solo reportamos

    def test_robots_txt_reveals_paths(self, base_url, session):
        """Analiza robots.txt en busca de rutas sensibles."""
        url = f"{base_url}/robots.txt"
        try:
            response = session.get(url, timeout=8)
            if response.status_code == 200:
                print(f"\n[ROBOTS.TXT ENCONTRADO]:\n{response.text}")
                assert True
            else:
                print(f"\n[ROBOTS.TXT]: No encontrado (status {response.status_code})")
                assert True
        except requests.exceptions.RequestException as e:
            pytest.skip(f"No se pudo conectar: {e}")