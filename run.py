import os
import sys
import webbrowser
import uvicorn

def main():
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "127.0.0.1")
    url = f"http://{host}:{port}"
    
    print("=" * 70)
    print("  ✨ SYNTAXA AI — Writing Intelligence Platform ✨")
    print("  AI-Powered Context-Aware Grammar Detection & Writing Analysis")
    print("=" * 70)
    print(f"  ➜ Web Interface: {url}")
    print(f"  ➜ API Documentation: {url}/docs")
    print("=" * 70)
    
    # Try opening browser after a short delay
    if os.environ.get("OPEN_BROWSER", "1") == "1":
        import threading
        import time
        def open_tab():
            time.sleep(1.5)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        threading.Thread(target=open_tab, daemon=True).start()

    uvicorn.run("backend.main:app", host=host, port=port, reload=False, log_level="info")

if __name__ == "__main__":
    main()
