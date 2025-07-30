import re
import requests


def get_server_location_from_log(line):
    parts = line.split()
    ud_index = parts.index("udmux")
    ip = parts[ud_index + 3].strip(",")

    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown")
            region = data.get("region", "")
            country = data.get("country", "")
            res = f"{city}, {region}, {country}"
            return res
    except Exception as e:
        return f"Server IP: {ip} — Error fetching location: {e}"