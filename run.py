import subprocess
import time
import requests

# Start Django Server
print("🚀 Starting Django Backend (analytics)...")
django_process = subprocess.Popen(["python", "manage.py", "runserver"])

# Wait for Django to be ready
django_url = "http://127.0.0.1:8000/"
while True:
    try:
        response = requests.get(django_url)
        if response.status_code == 200:
            print("✅ Django is ready!")
            break
    except requests.ConnectionError:
        print("⏳ Waiting for Django to start...")
        time.sleep(2)

# Start Streamlit App after Django is ready
print("🚀 Starting Streamlit Analytics Dashboard...")
streamlit_process = subprocess.Popen(["streamlit", "run", "Summary.py"])

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Stopping applications...")
    django_process.terminate()
    streamlit_process.terminate()
