import threading
import uvicorn
import app  # Dash
import main  # FastAPI

def run_dash():
    app.app.run_server(host="0.0.0.0", port=8050, debug=False)

def run_api():
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_api)
    t2 = threading.Thread(target=run_dash)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
