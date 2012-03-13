'''
Created on Mar 6, 2012

@author: ayoung
'''


"""
At the start of an application,  the
factories used to create instances of the various types of classes get
registered with an associated scope.  Scope and Resolvers are tightly coupled
objects.  The clients of the resolver code should request an instance from the
shortest lived resolver:  Request scoped.  When the client  requests an
instance of a registered object, the scopes are searched from shortest lived to
longest lived.  In the enumeration below,  that is from Request to Session to
Global.

The application will only have a single Resolver of a Global scope.

Session support is optional.  If session support is required,  set the Global
Variable RESOLVER_SESSION_SUPPORT=True.
When a new request comes in, it either has enough information to link it up
with an existing Session scoped Resolver,  or it will create a new one.

Since sessions are often timed controlled,  the sessions associated with the
request will often turn out to be stale. In this case, a new session scoped
resolver is instantiated.

"""


scope_map = dict()


class Scope(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        proxy_map = dict()
        scope_map[self.name] = proxy_map

scope_map = {}
GLOBAL_SCOPE = Scope("Global")

SESSION_SCOPE = Scope("Session", GLOBAL_SCOPE)

REQUEST_SCOPE = Scope("Request", SESSION_SCOPE)


def register(classname, proxy, scope=GLOBAL_SCOPE):
    proxy_map = scope_map[scope.name]
    proxy_map[classname] = proxy


class Resolver(object):
    '''
    classdocs
    '''
    instances = dict()

    def __init__(self, scope=GLOBAL_SCOPE, parent=None):
        self.factories = scope_map[scope.name]
        self.parent = parent

    def resolve(self, classname):
        if (classname in self.instances):
            return  self.instances[classname]
        if classname in self.factories:
            inst = self.factories[classname](self)
            self.instances[classname] = inst
            return inst
        if self.parent is not None:
            return self.parent.resolve(classname)
        else:
            raise KeyError(classname)


global_resolver = Resolver(GLOBAL_SCOPE)


class SessionResolver(Resolver):
    def __init__(self, params):
        super(SessionResolver, self).__init__(SESSION_SCOPE, global_resolver)


def fetch_session_resolver(global_resolver, headers):
    #TODO expand the logic here to deduce the session Identifier
    #and find the correct session in the global scope
    return SessionResolver(headers)


class RequestResolver(Resolver):
    def __init__(self, params, headers, with_session=False):
        if with_session:
            parent_resolver = fetch_session_resolver(global_resolver, headers)
        else:
            parent_resolver = global_resolver
        super(RequestResolver, self).__init__(REQUEST_SCOPE, parent_resolver)
        self.params = params
        self.headers = headers
