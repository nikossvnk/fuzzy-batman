#Pre-alpha version


import httplib, urllib

servers = {}
servers['s1'] = {
            'server' : 'DOMAIN1.COM', \
            'path' : '/',\
            'port' : 443, \
            'recipient' : 'MOBILE_PHONE_1' \
        }
servers['s2'] = {
            'server' : 'DOMAIN2.COM', \
            'path' : '/',\
            'port' : 80, \
            'recipient' : 'MOBILE_PHONE_2' \
        }


def nexmo( to, message ):

    # DEBUG
    print "sends to ", to, "message: ", message  
"""
    params = urllib.urlencode({
            'api_key' : '<NEXMO_API_KEY>',
            'api_secret' : '<NEXMO_API_SECRET>',
            'from' : '<FROM>',
            'to' : to,
            'text' : message
    })

    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"}

    nex = httplib.HTTPSConnection("rest.nexmo.com", 443)
    nex.request("POST", "/sms/json", params, headers)
    r2 = nex.getresponse()
"""
def open_file():
    try:
        fh = open('status.dat', 'r+')
    except:
        print "error on file handling"
        exit()
    
    return fh
    
def status_on_file(fh):
    status = {}

    for line in fh:
        if line.strip():
            l = line.split(' ')
            status[l[0]] = int(l[1])

    return status
    
def current_status(server, path, port):
    if port == 443:
        conn = httplib.HTTPSConnection(server, port)
    if port == 80:
        conn = httplib.HTTPConnection(server, port)
    
    conn.request("GET", path)
    r1 = conn.getresponse()
    
    return r1.status

# start
   
fl = open_file()
previus_status = status_on_file(fl)
c_status = ""

for s in servers:
    current_status = current_status(servers[s]['server'], servers[s]['path'], servers[s]['port'])

    if current_status != 200 and previus_status[s] == 200:
        nexmo(servers[s]['recipient'], 'down')
    
    if current_status == 200 and previus_status[s] != 200:
        nexmo(servers[s]['recipient'], 'up')
    
    c_status+= s + ' ' + str(current_status) + "\n"

fl.seek(0)    
fl.write( c_status )
fl.truncate()
fl.close()
