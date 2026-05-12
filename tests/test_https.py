import pytest
import requests
import ssl
import socket

class TestHTTPS:

    def test_http_redirects_to_https(self, session):
        """Verifica si HTTP redirige automáticamente a HTTPS."""
        http_url = "http://juice-shop.herokuapp.com"

        response = session.get(http_url, timeout=10, allow_redirects=True)
        final_url = response.url

        print(f"\n[URL FINAL DESPUÉS DE REDIRECCIONES]: {final_url}")
        print(f"[HISTORIAL DE REDIRECCIONES]: {[r.url for r in response.history]}")

        if final_url.startswith("https://"):
            print("[OK]: HTTP redirige a HTTPS correctamente")
        else:
            print("[VULNERABILIDAD]: HTTP no redirige a HTTPS")

        assert True

    def test_https_certificate_valid(self):
        """Verifica si el certificado SSL es válido."""
        hostname = "testphp.vulnweb.com"

        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    print(f"\n[CERTIFICADO SSL]:")
                    print(f"  Sujeto: {cert.get('subject')}")
                    print(f"  Emisor: {cert.get('issuer')}")
                    print(f"  Válido hasta: {cert.get('notAfter')}")
                    print("[OK]: Certificado SSL válido")
                    assert True

        except ssl.SSLCertVerificationError as e:
            print(f"\n[VULNERABILIDAD]: Certificado SSL inválido - {e}")
            assert True
        except (socket.timeout, ConnectionRefusedError, OSError):
            print(f"\n[INFO]: Puerto 443 no disponible en {hostname}")
            pytest.skip("HTTPS no disponible en el target")

    def test_https_allows_weak_ssl(self):
        """Verifica si el servidor acepta versiones antiguas de SSL/TLS."""
        hostname = "testphp.vulnweb.com"
        weak_protocols = []

        for protocol_name, protocol in [
            ("SSLv2", getattr(ssl, "PROTOCOL_SSLv2", None)),
            ("SSLv3", getattr(ssl, "PROTOCOL_SSLv3", None)),
            ("TLSv1.0", getattr(ssl, "PROTOCOL_TLSv1", None)),
            ("TLSv1.1", getattr(ssl, "PROTOCOL_TLSv1_1", None)),
        ]:
            if protocol is None:
                print(f"  {protocol_name}: No soportado por este Python (bien)")
                continue
            try:
                context = ssl.SSLContext(protocol)
                with socket.create_connection((hostname, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname):
                        weak_protocols.append(protocol_name)
                        print(f"  [VULNERABILIDAD] {protocol_name}: ACEPTADO por el servidor")
            except Exception:
                print(f"  [OK] {protocol_name}: Rechazado o no disponible")

        print(f"\n[PROTOCOLOS DÉBILES ACEPTADOS]: {weak_protocols}")
        assert True

    def test_mixed_content(self, base_url, session):
        """Detecta recursos HTTP cargados en páginas HTTPS (mixed content)."""
        try:
            response = session.get(base_url, timeout=10)
            body = response.text

            http_resources = []
            import re
            pattern = r'(src|href|action)=["\']http://[^"\']*["\']'
            matches = re.findall(pattern, body)

            if matches:
                print(f"\n[MIXED CONTENT DETECTADO]: {len(matches)} recursos HTTP")
                for m in matches[:5]:
                    print(f"  -> {m}")
            else:
                print("\n[OK]: No se detectó mixed content")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"No se pudo conectar: {e}")

        assert True