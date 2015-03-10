#Pre-alpha version


import httplib, urllib

def nexmo( message ):    
    params = urllib.urlencode({
            'api_key' : '<NEXMO_API_KEY>',
            'api_secret' : '<NEXMO_API_SECRET>',
            'from' : '<FROM>',
            'to' : '<TO>',
            'text' : message
    })

    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"}

    nex = httplib.HTTPSConnection("rest.nexmo.com", 443)
    nex.request("POST", "/sms/json", params, headers)
    r2 = nex.getresponse()

def open_file():
    try:
        fh = open('status.dat', 'r+')
    except:
        print "error on file handling"
        exit()
    
    return fh
    
def status_on_file(fh):
    for line in fh:
        return int(line)
    
def current_status():
    conn = httplib.HTTPSConnection("<SERVER_DOMAIN>", 443)
    conn.request("GET", "/")
    r1 = conn.getresponse()
    
    return r1.status

# start
   
fl = open_file()

previus_status = status_on_file(fl)
current_status = current_status()

if current_status != 200 and previus_status == 200:
    nexmo('down')
    
if current_status == 200 and previus_status != 200:
    nexmo('up')
    
fl.seek(0)    
fl.write( str(current_status) )
fl.truncate()
fl.close()
