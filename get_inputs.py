import requests
import sys
if len(sys.argv)<3:
    print("arguments: avendtofcode format url; session cookie")
    exit(1)
url = sys.argv[1]
session = sys.argv[2]

for i in range(1,26):
    site = requests.get(url.format(i), cookies={"session":session})
    with open(f"inputs/{('0'+str(i))[-2:]}.txt", "w") as f:
        f.write(site.text)