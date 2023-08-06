import pickle
import threading

from pyile_protocol.lib.peers.Peer import Peer
from pyile_protocol.lib.error import *


class AuthPeer(Peer):
    """
    A class to represent an authenticating peer.
    This class inherits from the Peer class.
    ...

    Attributes
    ----------

    address : tuple of (ip, port)
        address of the authentication peer
    password_attempts : int
        Allowed attempts that a joining peer is allowed
    password : str
        Password that joining peers must authenticate with
    blocked_peers : set
        Set of peers that are banned from joining the network
    changes_made : bool
        Boolean to check if changes have been made to the network


    Methods
    -------
    __init__(address, password_attempts, password)
        Constructor for the AuthPeer class
    authenticate_peers()
        The first method that should be called when an authentication peer is created
    """

    def __init__(self, address, password_attempts, password):
        Peer.__init__(self, address=address)
        self.password_attempts = password_attempts
        self.peers.append(self.peer_address)
        self.blocked_peers = set()
        self.changes_made = False
        self.password = password

    def authenticate_peers(self):
        """
        The first method that should be called when an authentication peer is created.
        Starts a thread to listen for incoming connections, Authenticates peers and calls the
        heartbeat method.
        """

        def auth_password_check():
            """
                Auxiliary function to help authenticate
            :return: peer address if authenticated, None if not
            """
            try:
                password = addr.recv(self.BUFFER).decode(self.ENCODE)
                print(addr.getpeername(), "Trying to login with password:", password)
                if password == self.password:
                    # Sends authenticated status to peer
                    addr.send("authenticated".encode(self.ENCODE))
                    # Receives peer address from peer
                    peer_recv = addr.recv(self.BUFFER)
                    pickled_peer = pickle.loads(peer_recv)
                    self.peers.append(pickled_peer)
                    # Sends new set to peer
                    addr.send(pickle.dumps(self.peers))
                    print(self.peers)
                    return pickled_peer
                else:
                    addr.send("notauthenticated".encode(self.ENCODE))
                    raise AuthenticationException("Incorrect password.")
            except AuthenticationException as e:
                print(e)
                return None

        self.auth_socket.listen()

        while not self.disconnected:
            self.auth_socket.settimeout(2)
            try:
                addr, acc_connect = self.auth_socket.accept()
                print("Got connection from: ", addr.getpeername())

            # self.blocked_peers.add(addr.getpeername())  # Uncomment to test ban.
            # Checks if joining peer in banned
                if addr.getpeername() not in self.blocked_peers:
                    # Sends not banned status to peer
                    try:
                        addr.send("notbanned".encode(self.ENCODE))
                    except AuthenticationException:
                        print("Could not send banned status to peer.")
                    # Performs authentication
                    peer_address = auth_password_check()
                    if peer_address is not None:
                        self.auth_beat(addr, peer_address)
                        self.changes_made = True

                else:
                    print(addr.getpeername(), "is banned")
                    addr.send("banned".encode(self.ENCODE))
                    addr.close()
            except:
                pass

    def auth_beat(self, addr, peer_address):
        """
        Sends a heartbeat to the peer to check if it is still connected
        :return:
        """
        if self.disconnected:
            return
        try:
            if self.changes_made:
                addr.send(pickle.dumps({"type": "set", "data": self.peers}))
                self.changes_made = False
            else:
                addr.send(pickle.dumps({"type": "<3", "data": "<3"}))
            beat = addr.recv(self.BUFFER)
            if not beat:
                raise ConnectionResetError
        except ConnectionResetError:
            print("Peer disconnected")
            self.peers.remove(peer_address)
            print(self.peers)
            self.changes_made = True
            return

        beat_thread = threading.Timer(2, self.auth_beat, args=(addr, peer_address))
        self.threads.append(beat_thread)
        beat_thread.start()


