import subprocess
import webbrowser
import time
import socket
import sys
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_PUBLIC_DIR = ROOT / "frontend" / "public"

BACKEND_FILE = BACKEND_DIR / "main.py"
LOGIN_FILE = FRONTEND_PUBLIC_DIR / "login.html"
DASHBOARD_FILE = FRONTEND_PUBLIC_DIR / "dashboard.html"
CONFIG_FILE = FRONTEND_PUBLIC_DIR / "config.js"

BACKEND_PORT = 5001
FRONTEND_PORT = 8000

BACKEND_HEALTH_URL = f"http://127.0.0.1:{BACKEND_PORT}/api/health"
LOGIN_URL = f"http://127.0.0.1:{FRONTEND_PORT}/login.html"
DASHBOARD_URL = f"http://127.0.0.1:{FRONTEND_PORT}/dashboard.html"
OLLAMA_URL = "http://127.0.0.1:11434"


def log(message: str) -> None:
    print(f"[MelodyMatrix] {message}")


def fail(message: str) -> None:
    print(f"[MelodyMatrix] ERROR: {message}")
    sys.exit(1)


def ensure_files() -> None:
    required = [
        BACKEND_DIR,
        FRONTEND_PUBLIC_DIR,
        BACKEND_FILE,
        LOGIN_FILE,
        DASHBOARD_FILE,
    ]
    for path in required:
        if not path.exists():
            fail(f"Missing required path: {path}")

    if not CONFIG_FILE.exists():
        log(
            "Warning: frontend/public/config.js was not found. "
            "The site can open, but login/auth will not work until config.js exists."
        )


def is_port_open(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def wait_for_http(url: str, timeout: int = 20) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urlopen(url, timeout=2) as response:
                if 200 <= response.status < 500:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def ollama_running() -> bool:
    try:
        with urlopen(OLLAMA_URL, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


def start_backend():
    if is_port_open(BACKEND_PORT):
        log(f"Backend already running on port {BACKEND_PORT}")
        return None

    log("Starting FastAPI backend...")
    process = subprocess.Popen(
        ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(BACKEND_PORT)],
        cwd=BACKEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if not wait_for_http(BACKEND_HEALTH_URL, timeout=20):
        process.terminate()
        fail("Backend failed to start. Check backend/main.py.")

    log(f"Backend ready at http://127.0.0.1:{BACKEND_PORT}")
    return process


def start_frontend_server():
    if is_port_open(FRONTEND_PORT):
        log(f"Frontend server already running on port {FRONTEND_PORT}")
        return None

    log("Starting local web server...")
    process = subprocess.Popen(
        ["python3", "-m", "http.server", str(FRONTEND_PORT)],
        cwd=FRONTEND_PUBLIC_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if not wait_for_http(LOGIN_URL, timeout=20):
        process.terminate()
        fail("Frontend server failed to start. Check frontend/public.")

    log(f"Frontend ready at http://127.0.0.1:{FRONTEND_PORT}")
    return process


def main() -> None:
    log("Initializing project...")
    ensure_files()

    if ollama_running():
        log("Ollama is running")
    else:
        log(
            "Ollama is not running on port 11434. "
            "The chatbot can still open, but AI replies may fall back to non-AI answers."
        )

    backend_process = start_backend()
    frontend_process = start_frontend_server()

    log("Opening login page...")
    webbrowser.open(LOGIN_URL)

    log("Website is ready")
    log(f"Login page: {LOGIN_URL}")
    log(f"Dashboard page: {DASHBOARD_URL}")

    try:
        while True:
            time.sleep(1)
            if backend_process and backend_process.poll() is not None:
                fail("Backend stopped unexpectedly.")
            if frontend_process and frontend_process.poll() is not None:
                fail("Frontend server stopped unexpectedly.")
    except KeyboardInterrupt:
        log("Shutting down...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        log("Stopped")


if __name__ == "__main__":
    main()