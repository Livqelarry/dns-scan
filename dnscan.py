import requests, json, http.client

BASE_URL = "https://crt.sh/?q={}&output=json"
subdomains = set()
wildcardsubdomains = set()

domain = str(input("Masukkan subdomain: "))

def crtsh(domain):
    try:
        response = requests.get(BASE_URL.format(domain), timeout=25)
        if response.ok:
            content = response.content.decode('UTF-8')
            jsondata = json.loads(content)
            for i in range(len(jsondata)):
                name_value = jsondata[i]['name_value']
                if name_value.find('\n'):
                    subname_value = name_value.split('\n')
                    for subname_value in subname_value:
                        if subname_value.find('*'):
                            if subname_value not in subdomains:
                                subdomains.add(subname_value)
                        else:
                            if subname_value not in wildcardsubdomains:
                                wildcardsubdomains.add(subname_value)
    except:
        pass

crtsh(domain)

number = 1
if domain:
    for subdomain in subdomains:
        try:
            connection = http.client.HTTPSConnection(f"{subdomain}")
            connection.request("GET", "/") 
            response = connection.getresponse()
            print(f"{number}. {subdomain} - {response.status} {response.reason}")
        except KeyboardInterrupt:
            print("-"*30)
            print("Kode diberhentikan")
            quit()
        except:
            print(f"{number}. {subdomain} - ERROR")
            pass
        connection.close()
        number += 1
