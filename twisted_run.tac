from twisted.web.wsgi import WSGIResource
from twisted.internet import reactor
from twisted.web import server
from system_trading_django.wsgi import application as application
resource = WSGIResource(reactor, reactor.getThreadPool(), application)
site = server.Site(resource)
reactor.listenTCP(9000, site)
reactor.run()