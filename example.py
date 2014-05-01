from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory, Protocol
 
class EchoSession(LineReceiver):
    delimiter = "\n"
 
    def __init__(self):
        self.username = None
 
    def connectionMade(self):
        self.sendLine("Welcome! Please enter a nick:")
        self.factory.sessions.append(self)
 
    def connectionLost(self, reason):
        self.factory.sessions.remove(self)
        self.broadcast("%s quit" % self.username)
 
    def lineReceived(self, data):
        if self.username is None:
            self.username = data.strip()
            self.sendLine("Welcome, %s" % self.username)
            self.broadcast("%s joined" % self.username)
        else:
            self.broadcast("<%s> %s" % (self.username, data))
 
 
    def broadcast(self, message):
        for session in self.factory.sessions:
            session.sendLine(message)
 
 
class EchoServer(Factory):
    protocol = EchoSession
 
    def __init__(self):
        self.sessions = []
 
 
server = EchoServer()
reactor.listenTCP(4000, server)
 
print "running!"
reactor.run()
