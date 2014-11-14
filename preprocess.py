import httplib, urllib

#CLIENT_ID = 'SFBFUH1DMDJE02Y5H355NRC3TYWRIWR3YEZRA1LVFCT2LIVO'
#CLIENT_SECRET = 'VXZHEVFUP0O5MW3C0VSP2ONRORD4G132MBWALO3IQIM4L3T2'
CLIENT_ID = '2QDCK4V50CJF23APRR0LBJNMSS0VWACTXSPP3IATIFQ4SKTK'
CLIENT_SECRET = '343G3ZRHBTCJWBDSQH2B0JZGSOFNOHAJN22HJAYVUB5KRFWK'

HOST = 'foursquare.com'


params = {
    'client_id' : CLIENT_ID,
    'response_type' : 'code',
    'redirect_uri' : 'http://www.ntu.edu.sg/',
    }

path = '/oauth2/authenticate?%s' % urllib.urlencode(params)
print path

conn = httplib.HTTPSConnection(HOST)
conn.request('GET', path)
r = conn.getresponse()

print r.status 
print r.getheaders() 
open('test.html', 'w').write(r.read())
