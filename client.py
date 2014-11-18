import httplib, urllib, socket
import time, os
import json

CLIENT_ID = '2QDCK4V50CJF23APRR0LBJNMSS0VWACTXSPP3IATIFQ4SKTK'
CLIENT_SECRET = '343G3ZRHBTCJWBDSQH2B0JZGSOFNOHAJN22HJAYVUB5KRFWK'
REDIRECT_URI = 'http://www.ntu.edu.sg/'

HOST = 'foursquare.com'
API_HOST = 'api.foursquare.com'
TIMEOUT = 60

socket.setdefaulttimeout(TIMEOUT)

def get_access_token():
    while True:
        try:
            conn = httplib.HTTPSConnection(HOST, timeout=TIMEOUT)

            params = {
                'client_id' : CLIENT_ID,
                'response_type' : 'code',
                'redirect_uri' : REDIRECT_URI,
                }

            path = '/oauth2/authenticate?%s' % urllib.urlencode(params)

            conn.request('GET', path)
            r = conn.getresponse()

            break
        except:
            time.sleep(10)

    data = r.read()
    pos = data.find('name="fs-request-signature"')
    pos = data.find('value="', pos) + 7
    pos1 = data.find('"',pos)
    signature = data[pos:pos1]

    #open('test.html','w').write(data)

    pos = data.rfind('img src="') + 9
    pos1 = data.find('"', pos)
    path1 = data[pos:pos1]
    headers = {'Cookie': r.getheader('set-cookie')}

    conn.request('GET', path1, headers=headers)
    r = conn.getresponse()
    r.read()

    sessionid = r.getheader('set-cookie').split('XSESSIONID=')[1].split(';')[0]
    headers['Cookie'] += '; XSESSIONID=' + sessionid
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    body = 'fs-request-signature=' + urllib.quote(signature) + '&shouldAuthorize=true&emailOrPhone=pnta1986%40yahoo.com.vn&password=123456' 
    conn.request('POST', path, body=body, headers=headers)
    r = conn.getresponse()
    r.read()
    location = r.getheader('location')
    code = location.split('code=')[1].split('#')[0]

    params = {
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'grant_type' : 'authorization_code',
        'redirect_uri' : 'http://www.ntu.edu.sg/',
        'code' : code,
        }
    path = '/oauth2/access_token?%s' % urllib.urlencode(params)
    conn.request('GET', path) 
    r = conn.getresponse()

    js = json.loads(r.read())
    return js['access_token']

ACCESS_TOKEN = get_access_token()
print ACCESS_TOKEN

VENUE_PATH = '/v2/venues/%%s?oauth_token=%s&v=20141113' % ACCESS_TOKEN

conn = httplib.HTTPSConnection(API_HOST, timeout=TIMEOUT)

f = open('venues.txt', 'w')
c = 1
for line in open('VenueInfo_Coordinate.txt'):
    venue = line.split('\t')[0]
    print c, venue

    path = VENUE_PATH % venue

    retry = 3
    while retry:
        try:
            conn.request('GET', path)
            r = conn.getresponse()

            js = r.read()
            pos = js.find('code') + 6
            #pos1 = js.find('}', pos)
            #code = js[pos:pos1]
            code = js[pos:pos+3]
            if code != '200':
                print code
                print js
                retry -= 1
                time.sleep(5)
                continue
            f.write(js) 
            f.write('\n')
            break
        except:
            retry -= 1
            time.sleep(5)

            ACCESS_TOKEN = get_access_token()
            conn = httplib.HTTPSConnection(API_HOST, timeout=TIMEOUT)
            continue


    c += 1
    if c%100 == 0:
        f.flush()
        os.fsync(f.fileno())

    time.sleep(8)
