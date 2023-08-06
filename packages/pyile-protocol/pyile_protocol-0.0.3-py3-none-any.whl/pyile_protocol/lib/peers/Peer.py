import random
import socket


from pyile_protocol.lib import utils
from pyile_protocol.lib.error import *


class Peer:
    """
    A class to represent an authenticating peer.
    This class inherits from the Peer class.
    ...

    Attributes
    ----------

    ENCODE : str
        The encoding used to encode and decode messages
    BUFFER : int
        The buffer size used to send and receive messages
    disconnected : bool
        A boolean to represent if the peer is disconnected
    threads : list
        A list of threads that are running or have run
    address : tuple
        A tuple of the address and port of the peer
    auth_socket : socket
        The socket used to authenticate peers
    peer_address : tuple
        A tuple of the address and port of the communication socket
    peer_socket : socket
        The socket used to communicate with other non-initial peers
    peers : list
        A list of all the peers in the network


    Methods
    -------
    __init__(address)
        Constructor for the Peer class
    __str__()
        Returns a string representation of the peer
    handle_peer(addr)
        Helper function for connect() to handle peer connections
    connect()
        connect() is threaded method that lists for incoming peer connections
        that have already been authenticated
    broadcast(msg)
        Broadcasts a message to all peers in the network.
    send(address, msg)
        Sends a message to a specific peer
    leave()
        Leaves the network and closes all sockets along with joining all threads.



    """

    def __init__(self, address):
        if type(self) == Peer:
            raise TypeError("Peer cannot be directly instantiated")

        self.ENCODE = 'utf-8'
        self.BUFFER = 2048
        self.disconnected = False
        self.threads = []
        self.address = address
        self.auth_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.auth_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.auth_socket.settimeout(2)
        self.auth_socket.bind(self.address)
        self.peer_address =(self.address[0], 49000 + random.randint(0, 1000))
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.settimeout(2)
        self.peer_socket.bind(self.peer_address)
        self.peers = []

    def __str__(self):
        return f"Peer at {self.address}"

    def handle_peer(self, addr):
        """
        Helper function for connect() to handle peer connections

        Parameters
        ----------
        addr

        Returns
        -------

        """
        data = addr.recv(self.BUFFER).decode(self.ENCODE)
        print(data)
        addr.send(data.encode(self.ENCODE))

    def connect(self):
        """
        connect() is threaded method that lists for incoming peer connections
        that have already been authenticated

        Returns
        -------

        """
        try:
            self.peer_socket.listen()
        except:
            pass
        while not self.disconnected:
            try:
                addr, acc_connect = self.peer_socket.accept()
                self.handle_peer(addr)
            except:
                pass

    def broadcast(self, msg):
        """
        Broadcasts a message to all peers in the network.

        Parameters
        ----------
        msg

        Returns
        -------

        """
        for peer in self.peers:
            if peer != self.peer_address:
                self.send(peer, msg)

    def send(self, address, msg):
        if address == self.peer_address:
            print("Cannot send to self")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
            send_sock.settimeout(2)
            try:
                send_sock.connect(address)
                # print("sending: ", msg, "to", address)
                send_sock.send(msg.encode(self.ENCODE))
                data = send_sock.recv(self.BUFFER).decode(self.ENCODE)
            except Exception:
                send_sock.close()
                print("Peer at", address, "is not responding")



    def leave(self):
        """
        Leaves the network and closes all sockets along with joining all threads.

        Returns
        -------

        """
        self.auth_socket.close()
        self.peer_socket.close()
        self.disconnected = True
        utils.join_threads(self.threads)

