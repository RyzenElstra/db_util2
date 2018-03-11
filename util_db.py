import urllib2, sys, os

mark0 = '</thead>'
mark1 = '</table>'
sep = '</tr>'
file = ['db/page', '.txt']

def setup_new_proxy():
	proxy = urllib2.ProxyHandler({'http': '127.0.0.1'})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)

def getreq(url):
	return urllib2.urlopen(url).read()
	
def parse_resp(resp):
	table = resp.split(mark0)[1].split(mark1)[0].split(sep)
	final = []
	for i in table:
		if i.find('/privatekey/') != -1:
			p1 = i.split('">\r\n')[0].split('<tr id="row-')[1]
			p2 = i.split('target="_blank">')[1].split('</a></td>\r\n')[0].replace('0x', '')
			print(len(p1), len(p2))
			final.append(p1+p2)
	return final

def search(start, stop, string):
	i = start-1
	while i < stop:
		i+=1
		page = open(str(i).join(file), 'r').read()
		if page.find(string) != -1:
			lines = page.split('\n')
			for j in lines:
				if j.find(string) != -1:print('found in '+str(i).join(file)+' - line '+str(lines.index(j))+':\n'+j[:64]+' : 0x'+j[64:])
		del page
	
args = sys.argv
base_site = args[args.index('util_db.py')+1]

if '--grab-db' in args:
	init = int(args[args.index('-start')+1])
	current = init + int(init == 0)
	limit = int(args[args.index('-stop')+1])
	while current <= limit:
		text = '\n'.join(parse_resp(getreq(base_site+str(current))))
		if current == init:print('first page :\n'+text)
		open(str(current).join(file), 'w').write(text)
		print('ok : '+str(current))
		current += 1
elif '--search-all' in args:
	string = args[args.index('--search-all')+1]
	pages = os.listdir('db/')
	length = len(pages) * 32
	print(str(len(pages))+' pages and '+str(length)+' combinations in db/')
	search(1, len(pages), string)
elif '--search' in args:
	string = args[args.index('--search-all')+1]
	start = int(args[args.index('-start')+1])
	stop = int(args[args.index('-stop')+1])
	search(start, stop, string)
else:print('no args specified')