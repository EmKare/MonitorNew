import requests as req

url = 'http://www.google.com/maps/dir/Half-Way-Tree+Clock,+Constant+Spring+Road,+Kingston,+Jamaica/X684%2B77V+UDC+Multi-storey+parking+lot,+Port+Royal+St,+Kingston,+Jamaica/@17.9897083,-76.8114051,14z/'

r = req.get(url)

print(r.content)