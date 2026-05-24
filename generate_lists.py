import os
import json
import requests
import time

API_TOKEN = os.environ.get('CF_RADAR_TOKEN')
HEADERS = {'Authorization': f'Bearer {API_TOKEN}'}

# Comprehensive list of ISO 3166-1 alpha-2 country codes
COUNTRIES = [
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW"
]

def get_top_domains(location=None):
    # Fetching top 100 ordered domains.
    url = "https://api.cloudflare.com/client/v4/radar/ranking/top?limit=100"
    if location:
        url += f"&location={location}"
        
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"Failed to fetch {location or 'global'}: {response.status_code}")
            return []
            
        data = response.json()
        if data.get('success') and 'result' in data:
            results = []
            if 'top_0' in data['result']:
                results = data['result']['top_0']
            else:
                for key, val in data['result'].items():
                    if isinstance(val, list):
                        results = val
                        break

            domains = []
            for item in results:
                d = item.get('domain', '')
                if d:
                    name = d.split('.')[0]
                    domains.append({"domain": d, "brand": name})
            return domains
    except Exception as e:
        print(f"Error fetching {location or 'global'}: {e}")
    return []

def main():
    os.makedirs('lists', exist_ok=True)
    
    print("Fetching Global Top Domains...")
    global_domains = get_top_domains()
    if global_domains:
        with open('global.json', 'w') as f:
            json.dump(global_domains, f)
        print(f"Saved {len(global_domains)} global domains.")
        
    for code in COUNTRIES:
        print(f"Fetching Top Domains for {code}...")
        domains = get_top_domains(code)
        if domains:
            with open(f"lists/{code}.json", 'w') as f:
                json.dump(domains, f)
            print(f"Saved {len(domains)} domains for {code}.")
        else:
            print(f"Skipping {code} due to missing or empty data.")
        
        # Take some time to respect Cloudflare API limits
        time.sleep(1.5)

if __name__ == "__main__":
    if not API_TOKEN:
        print("ERROR: CF_RADAR_TOKEN environment variable not set.")
        exit(1)
    main()
