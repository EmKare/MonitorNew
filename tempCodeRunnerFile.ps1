import webbrowser

#url = 'http://docs.python.org/'
url = 'http://www.google.com/maps/dir/Half-Way-Tree+Clock,+Constant+Spring+Road,+Kingston,+Jamaica/X684%2B77V+UDC+Multi-storey+parking+lot,+Port+Royal+St,+Kingston,+Jamaica/@17.9897083,-76.8114051,14z/'
#http://www.google.com/maps/dir/Half-Way-Tree+Clock,+Constant+Spring+Rd,+Kingston,+Jamaica/UDC+Multi-storey+parking+lot,+X684%2B77V,+Port+Royal+St,+Kingston,+Jamaica/@17.9882064,-76.8263867,14z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x8edb3fb6cdf7efd7:0x5be619917d5a67a1!2m2!1d-76.7972958!2d18.0109386!1m5!1m1!1s0x8edb414c18fc07e9:0xcf609aab817ff47!2m2!1d-76.7943394!2d17.9657268!3e0!5m1!1e1?entry=ttu&g_ep=EgoyMDI0MTAwNy4xIKXMDSoASAFQAw%3D%3D

#http://www.google.com/maps/dir/Half-Way-Tree+Clock,+Constant+Spring+Rd,+Kingston,+Jamaica/UDC+Multi-storey+parking+lot,+X684%2B77V,+Port+Royal+St,+Kingston,+Jamaica/@17.9883724,-76.8122628,14z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x8edb3fb6cdf7efd7:0x5be619917d5a67a1!2m2!1d-76.7972958!2d18.0109386!1m5!1m1!1s0x8edb414c18fc07e9:0xcf609aab817ff47!2m2!1d-76.7943394!2d17.9657268!3e2!5m1!1e1?entry=ttu&g_ep=EgoyMDI0MTAwNy4xIKXMDSoASAFQAw%3D%3D

# MacOS
#chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s' #C:\Program Files\Google\Chrome\Application

# Linux
# chrome_path = '/usr/bin/google-chrome %s'

webbrowser.get(chrome_path).open(url)