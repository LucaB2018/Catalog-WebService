import cherrypy
import json
import time

global path
path='database.json'


class CatalogWebService(object):
@cherrypy.expose
	
	def POST(self):
		f=open(path,'r')
		cherrypy.session['data']=f.read()
		f.close()
		return cherrypy.session['data']

	def GET(self, *uri, **params):
		data=json.loads(cherrypy.session['data'])
		try:
			if len(uri)==1:
				out=json.dumps(data[uri[0]])
				return out
			elif len(uri)==2:
				if uri[0]=='devices':
					out=json.dumps(data[uri[0]])
					index=-1
					b=data[uri[0]]
					for i in range(len(b)):
						tmp=b[i]					
						if tmp['deviceID']==uri[1]:
							index=i
					if index!=-1:
						return json.dumps(b[index])
					else:
						return 'device not found'
				elif uri[0]=='users':
					out=json.dumps(data[uri[0]])
					index=-1
					b=data[uri[0]]
					for i in range(len(b)):
						tmp=b[i]					
						if tmp['userID']==uri[1]:
							index=i
					if index!=-1:
						return json.dumps(b[index])
					else:
						return 'user not found'
				raise cherrypy.HTTPError(404)
		except:
			raise cherrypy.HTTPError(404)
			
	def PUT(self,*uri,**params):
		if uri[0]=="new_device":
			try:
				data=json.loads(cherrypy.session['data'])
				dev=data["devices"]
				for i in range(len(dev)):
					if dev[i]["deviceID"]==params["deviceID"]:
						return 'deviceID is already used'
					if dev[i]["endpoints"]==params["endpoints"]:
						return 'inserted end-points is already used'
				current_time=time.time()
				params['timestamp']=current_time
				data['devices'].append(params)
				data=json.dumps(data)
				f=open(path,'w')
				f.write(data)
				f.close()
				cherrypy.session['data']=data
				return data
			except:
				raise cherrypy.HTTPError(400)
		elif uri[0]=="new_user":
			try:
				data=json.loads(cherrypy.session['data'])
				dev=data["users"]
				for i in range(len(dev)):
					if dev[i]["userID"]==params["userID"]:
						return 'userID is already used'
					if dev[i]["email"]==params["email"]:
						return 'inserted e-mail is already used'
				data['users'].append(params)
				data=json.dumps(data)
				f=open(path,'w')
				f.write(data)
				f.close()
				cherrypy.session['data']=data
				return data
			except:
				raise cherrypy.HTTPError(400)
		else:
			raise cherrypy.HTTPError(404)
			
	def DELETE(self,*uri,**params):
		data=json.loads(cherrypy.session['data'])
		devices=data["devices"]
		current_time=time.time()
		dev=[]
		for device in devices:
			if current_time-device["timestamp"]<60:
				dev.append(device)
		data["devices"]=dev
		cherrypy.session['data']=json.dumps(data)
		data=json.dumps(data)
		if dev!=devices:
			f=open(path,'w')
			f.write(data)
			f.close()
		return cherrypy.session['data']
		


config = {
    'global': {
	'server.socket_host': '0.0.0.0',
	'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
	'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
	'tools.staticdir.on': True,
	'tools.staticdir.dir': 'assets',
    }
}

cherrypy.quickstart(CatalogWebService(), '/', conf)
