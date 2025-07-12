import requests
import json
import os

grafana_url = "http://localhost:3000"
api_key = os.environ.get("GRAFANA_API_KEY", "admin:admin")

def import_dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), '../configs/grafana/sample_dashboard.json')
    with open(dashboard_path) as f:
        dashboard = json.load(f)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key.encode('utf-8').hex()}"
    }
    payload = {"dashboard": dashboard, "overwrite": True}
    resp = requests.post(f"{grafana_url}/api/dashboards/db", headers=headers, json=payload)
    if resp.status_code == 200:
        print("Dashboard imported successfully!")
    else:
        print(f"Failed to import dashboard: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    import_dashboard() 