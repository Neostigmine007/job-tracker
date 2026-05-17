import urllib.request
import os

# 1. Put the exact URL of the job page you want to track inside the quotes:
URL = "https://www.healthjobsuk.com/job_list?JobSearch_q=&JobSearch_d=&JobSearch_g=255&JobSearch_re=_POST&JobSearch_re_0=1&JobSearch_re_1=1-_-_-&JobSearch_re_2=1-_-_--_-_-&JobSearch_Submit=Search&_tr=JobSearch&_ts=1361" 

# 2. Download the webpage content
try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req) as response:
        current_html = response.read().decode('utf-8')
except Exception as e:
    print(f"Error loading page: {e}")
    exit()

# 3. Check if we have seen this page before
HISTORY_FILE = "last_seen.txt"

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        old_html = f.read()
    
    # Compare old page with new page
    if current_html != old_html:
        print("⚠️ CHANGE DETECTED! New jobs might be posted.")
        # This forces the GitHub Action to fail, which triggers an email alert to you!
        exit(1) 
    else:
        print("✅ No changes detected.")
else:
    print("First run: Saving page history.")

# 4. Save the current page for the next check
with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    f.write(current_html)
