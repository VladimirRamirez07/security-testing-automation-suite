import pytest
import requests

SECURITY_HEADERS = [
    "X-Content-Type-Options",
    "X-Frame-Options",
    "X-XSS-Protection",
    "Strict-Transport-Security",
    "Content-Security-Policy",
]

class TestSecurityHeaders:

    def test_missing_security_headers(self, base_url, session):
        """Detecta headers de seguridad ausentes en la respuesta HTTP."""
        response = session.get(base_url, timeout=10)
        missing = []

        for header in SECURITY_HEADERS:
            if header not in response.headers:
                missing.append(header)

        print(f"\n[HEADERS PRESENTES]: {dict(response.headers)}")
        print(f"[HEADERS FALTANTES]: {missing}")

        assert len(missing) > 0, "El sitio tiene todos los headers (inesperado en sitio vulnerable)"

    def test_server_header_exposed(self, base_url, session):
        """Verifica si el header Server expone información del servidor."""
        response = session.get(base_url, timeout=10)
        server = response.headers.get("Server", "")

        print(f"\n[SERVER HEADER]: {server}")
        assert server != "", "Header Server no encontrado"

    def test_x_powered_by_exposed(self, base_url, session):
        """Verifica si X-Powered-By expone tecnología del backend."""
        response = session.get(base_url, timeout=10)
        powered_by = response.headers.get("X-Powered-By", "No expuesto")

        print(f"\n[X-Powered-By]: {powered_by}")
        # En un sitio seguro esto debería estar oculto
        assert True  # Solo reportamos, no fallamos

    def test_content_type_header_present(self, base_url, session):
        """Verifica que Content-Type esté presente."""
        response = session.get(base_url, timeout=10)
        assert "Content-Type" in response.headers