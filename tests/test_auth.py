import pytest
import requests

class TestAuthWeaknesses:

    def test_access_protected_page_without_login(self, base_url, session):
        """Verifica si páginas protegidas son accesibles sin autenticación."""
        protected_pages = [
            "/userinfo.php",
            "/admin/",
            "/account.php",
            "/dashboard.php",
            "/profile.php",
        ]
        exposed = []

        for page in protected_pages:
            url = f"{base_url}{page}"
            try:
                fresh = requests.Session()
                response = fresh.get(url, timeout=8, allow_redirects=False)

                if response.status_code == 200:
                    exposed.append({"page": page, "status": 200})
                    print(f"  [VULNERABILIDAD] {page} accesible sin login (200)")
                elif response.status_code in [301, 302]:
                    location = response.headers.get("Location", "")
                    print(f"  [OK] {page} redirige a: {location}")
                else:
                    print(f"  [INFO] {page} -> Status: {response.status_code}")

            except requests.exceptions.RequestException:
                pass

        print(f"\n[PÁGINAS EXPUESTAS SIN LOGIN]: {len(exposed)}")
        assert True

    def test_session_cookie_security(self, base_url, session):
        """Verifica atributos de seguridad en las cookies de sesión."""
        url = f"{base_url}/userinfo.php"

        try:
            response = session.post(
                url,
                data={"uname": "test", "pass": "test"},
                timeout=8
            )

            print(f"\n[COOKIES RECIBIDAS]:")
            for cookie in response.cookies:
                print(f"\n  Nombre : {cookie.name}")
                print(f"  Valor  : {cookie.value[:20]}..." if len(cookie.value) > 20 else f"  Valor  : {cookie.value}")
                print(f"  HttpOnly: {cookie.has_nonstandard_attr('HttpOnly')}")
                print(f"  Secure  : {cookie.secure}")
                print(f"  SameSite: {cookie.get_nonstandard_attr('SameSite', 'No definido')}")

                if not cookie.secure:
                    print(f"  [VULNERABILIDAD] Cookie '{cookie.name}' sin flag Secure")
                if not cookie.has_nonstandard_attr("HttpOnly"):
                    print(f"  [VULNERABILIDAD] Cookie '{cookie.name}' sin flag HttpOnly")

            if not response.cookies:
                print("  [INFO] No se recibieron cookies")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"No se pudo conectar: {e}")

        assert True

    def test_default_credentials(self, base_url, session):
        """Prueba credenciales por defecto comunes."""
        url = f"{base_url}/userinfo.php"
        default_creds = [
            ("admin", "admin"),
            ("admin", "password"),
            ("admin", "1234"),
            ("test", "test"),
            ("user", "user"),
            ("root", "root"),
            ("guest", "guest"),
        ]
        working = []

        for username, password in default_creds:
            try:
                response = session.post(
                    url,
                    data={"uname": username, "pass": password},
                    timeout=8
                )
                body = response.text.lower()

                if any(w in body for w in ["welcome", "logout", "profile", "your profile"]):
                    working.append((username, password))
                    print(f"  [VULNERABILIDAD] Credenciales válidas: {username}:{password}")

            except requests.exceptions.RequestException:
                pass

        print(f"\n[CREDENCIALES POR DEFECTO QUE FUNCIONARON]: {working}")
        assert True

    def test_broken_object_level_auth(self, base_url, session):
        """Prueba BOLA/IDOR: acceso a recursos de otros usuarios por ID."""
        exposed_ids = []

        for user_id in range(1, 10):
            url = f"{base_url}/userinfo.php"
            try:
                response = session.get(
                    url,
                    params={"id": user_id},
                    timeout=8
                )
                body = response.text.lower()

                if response.status_code == 200 and len(response.text) > 100:
                    if any(w in body for w in ["name", "email", "user", "address"]):
                        exposed_ids.append(user_id)
                        print(f"  [POSIBLE IDOR] ID {user_id} expone datos de usuario")

            except requests.exceptions.RequestException:
                pass

        print(f"\n[IDs CON POSIBLE IDOR]: {exposed_ids}")
        assert True