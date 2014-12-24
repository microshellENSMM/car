import socket
import threading
import select
import os

class ClientsCommanding:
    """ This class is a commanding clients and listeners list.
        Each client is listen in a separate thread.
        If a command is received, all listener are update by observer pattern
    """

    def __init__(self) :
        """ Clients and listener list are created
            Listing thread is launched
        """
        self.clients = []
        self.listeners = []
        self.resume = True
        thread = threading.Thread(None, self.loopClients, None, (), {})
        thread.start()

    def addListener(self, listener) :
        """ Add listener to catch new command """
        self.listeners.append(listener)

    def deleteListener(self, listener) :
        """ Delete listener to stop catching new command"""
        if listener in self.listeners :
            self.listeners.remove(listener)

    def update(self, tab) :
        """ call all listener with the new command"""
        print tab
        for listener in self.listeners :
            listener(tab)

    def str2tab(self, message, tab, i=0) :
        """ swap str command to tab number by a recursive method"""
        # if all message has been cut, return completed tab
        if message == "" :
            return tab
        # if cursor is on '-' char
        # tab is appended with the number from start to '-' char
        # message is cut to '-' char
        if message[i] == "-" :
            tab.append(int(message[:i]))
            message = message[i+1:]
            return self.str2tab(message, tab)
        # else cursor is moved to the next char
        else :
            return self.str2tab(message, tab, i+1)

    def loopClients(self) :
        """endless loop listening client connections """
        while self.resume :
            clients_update, wlist, xlist = select.select(self.clients, [], [], 0.05)
            for client in clients_update :
                message = client.recv(1024)
                self.update(self.str2tab(message, []))

        print "listing thread is stoped"


    def addClient(self, client, password) :
        """ Add client to the list only if the password is correct """
        if True :
            self.clients.append(client)

    def deleteClient(self, client) :
        """ Delete object client """
        if client in self.clients :
            self.clients.remove(client)

    def stop(self) :
        self.resume = False


class Server :
    """ This class manage new connection and send data to all client connected.
        It's build as a Singleton pattern.
    """

    class __impl :

        def __init__(self, port) :
            """ Begin server listening """
            self.clients = []
            self.resume = True
            self.clientsCommanding = ClientsCommanding()
            # setup connexion
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.bind(('', int(port) ))
            self.connection.listen(5)

            # launch new connection Thread listen
            thread = threading.Thread(None, self.__loopNewConnection, None, (), {})
            thread.start()

        def __loopNewConnection(self) :
            while self.resume :
                # wait for a new connection
                client, info = self.connection.accept()
                # add client like commanding client.
                self.clientsCommanding.addClient(client, "1234")
                # add client in the list
                self.clients.append(client)

        def tab2str(self, tab) :
            """ Swap tab to string message """
            mes = ""
            for i in tab :
                mes += str(i)
                mes += "-"
            return mes


        def send(self, param) :
            # else we swap it before send
            if type(param) == list :
                param = self.tab2str(param)
            # If the value is a string, we send it directly
            if type(param) == str :
                param = param.encode()
                for client in clients :
                    try :
                        client.send(param)
                    # If one exception rise client is deleted on all list
                    except :
                        self.clients.remove(client)
                        self.clientsCommanding.deleteClient(client)


        def addListener(self, listener) :
            self.clientsCommanding.addListener(listener)

        def deleteListener(self, listener) :
            self.clientsCommanding.deleteListener(listener)

        def close(self) :
            self.resume = False
            self.connection.close()
            self.clientsCommanding.stop()
            # This kill the thread, I don't find a softer way :(
            os.kill(os.getpid(), 9)

        def id(self) :
            return id(self)


    __instance = None

    def __init__(self, port) :
        if Server.__instance is None :
            Server.__instance = Server.__impl(port)
        self.__dict__['_Singleton__instance'] = Server.__instance

    def __getattr__(self, attr) :
        return getattr(self.__instance, attr)
    def __setattr__(self, attr, value) :
        return setattr(self.__instance, attr, value)
