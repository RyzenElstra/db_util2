import urllib2

s = "http://ipinfo.io/ip"
proxy_api = "https://gimmeproxy.com/api/getProxy"

def proxy_off():
	proxy = urllib2.ProxyHandler()
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)

def proxy_new():
	print("before : "+getreq(s).replace('\n', ''))
	proxy_off()
	details = parse_json(getreq(proxy_api))
	while int(details["anonymityLevel"]) < 1:details = parse_json(getreq(proxy_api))
	ipPort = details['ip']+':'+details['port']
	protocol = details['protocol']
	print('new proxy : '+ipPort+' ('+protocol+', speed : '+details['speed']+')')
	proxy = urllib2.ProxyHandler({protocol: ipPort})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	print("after : "+getreq(s).replace('\n', ''))
	
def parse_json(s):
	lines = s.split('\n')
	values = {}
	for line in lines:
		if line.count('"') == 4:
			var = line.split('"')
			values[var[1]] = var[3]
		elif line.count('"') == 2:
			var = line.split('"')
			values[var[1]] = var[2][2:-1]
	return values
	
def getreq(url):
	return urllib2.urlopen(url).read()
	
print("init : "+getreq(s).replace('\n', ''))
proxy_new()
proxy_new()
proxy_off()
print("off : "+getreq(s).replace('\n', ''))
proxy_new()