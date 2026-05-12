import pytest
import requests
import re

WEAK_PASSWORDS = [
    "123456",
    "password",
    "admin",
    "admin123",
    "test",
    "test123",
    "root",
    "toor",
    "qwerty",
    "abc123",
    "letmein",
    "welcome",
    "monkey",
    "dragon",
]

class TestPasswordSecurity:

    def test_weak_password_login(self, base_url, session):
        """Intenta login con passwords débiles comunes."""
        url = f"{base_url}/userinfo.php"
        successful = []

        for password in WEAK_PASSWORDS:
            data = {"uname": "admin", "pass": password}
            try:
                response = session.post(url, data=data, timeout=8)
                body = response.text.lower()

                if any(word in body for word in ["welcome", "logout", "profile", "account"]):
                    successful.append(password)
            except requests.exceptions.RequestException:
                pass

        print(f"\n[PASSWORDS DÉBILES QUE FUNCIONARON]: {successful}")
        assert True  # Reportamos resultados

    def test_no_account_lockout(self, base_url, session):
        """Verifica si el sistema bloquea la cuenta tras múltiples intentos fallidos."""
        url = f"{base_url}/userinfo.php"
        responses_status = []

        for i in range(10):
            data = {"uname": "admin", "pass": f"wrongpassword{i}"}
            try:
                response = session.post(url, data=data, timeout=8)
                responses_status.append(response.status_code)
            except requests.exceptions.RequestException:
                pass

        print(f"\n[STATUS CODES EN 10 INTENTOS FALLIDOS]: {responses_status}")

        # Si todos los status son iguales, probablemente no hay lockout
        unique_statuses = set(responses_status)
        print(f"[STATUS ÚNICOS]: {unique_statuses}")

        if len(unique_statuses) == 1:
            print("[VULNERABILIDAD]: No se detectó bloqueo de cuenta (sin account lockout)")
        else:
            print("[INFO]: El servidor varía su respuesta, puede haber protección")

        assert True

    def test_password_in_url(self, base_url, session):
        """Verifica si credenciales viajan en la URL (GET en lugar de POST)."""
        url = f"{base_url}/login.php"
        params = {"username": "admin", "password": "test123"}

        try:
            response = session.get(url, params=params, timeout=8)
            final_url = response.url

            print(f"\n[URL CON CREDENCIALES]: {final_url}")

            if "password" in final_url.lower():
                print("[VULNERABILIDAD]: Password visible en la URL")
            else:
                print("[OK]: Password no encontrado en la URL")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"Endpoint no disponible: {e}")

        assert True

    def test_password_complexity_feedback(self, base_url, session):
        """Verifica si el registro acepta passwords muy débiles."""
        url = f"{base_url}/signup.php"
        weak_passwords = ["1", "aa", "123"]

        for pwd in weak_passwords:
            data = {
                "uname": "testuser_sec",
                "pass": pwd,
                "repass": pwd,
                "email": "test@test.com"
            }
            try:
                response = session.post(url, data=data, timeout=8)
                body = response.text.lower()

                if "error" in body or "invalid" in body or "weak" in body:
                    print(f"\n[OK] Password '{pwd}' fue rechazado")
                else:
                    print(f"\n[VULNERABILIDAD] Password débil '{pwd}' fue aceptado")

            except requests.exceptions.RequestException:
                pass

        assert True