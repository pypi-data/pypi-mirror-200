import pickle
import threading

from pyile_protocol.lib.peers.Peer import Peer
from pyile_protocol.lib.error import *


class JoinPeer(Peer):
    """
    Child class of Peer Class. Used to join a network and get authentication from an initial peer.
    ...

    Attributes
    ----------

    auth_peer : tuple of (ip, port)

    Methods
    -------
    __init__(address)
        Constructor for JoinPeer class.
    get_authenticated(starting_address, password)
        The first method that should be called when a JoinPeer is created.
    recv_status()
        Establishes and maintains a heart beat from the auth peer.
    """

    def __init__(self, address):
        Peer.__init__(self, address=address)
        self.auth_peer = None

    def get_authenticated(self, starting_address, password):
        """
        The first method that should be called when a peer is created.
        connects to initial peer and authenticates with password.
        :param starting_address: tuple of (ip, port)
        :param password: string
        :return: True if authenticated, False if not
        """

        def password_check():
            """
            Helper function that checks the password.

            :return: True if authenticated, False if not

            """
            try:
                self.auth_socket.send(password.encode(self.ENCODE))
                pw_status = self.auth_socket.recv(self.BUFFER).decode(self.ENCODE)
                if pw_status == "authenticated":
                    print(str(password) + " is correct")
                    # adding auth peer
                    self.auth_peer = starting_address
                    # sends new socket to auth peer
                    pickled_socket = pickle.dumps(self.peer_address)
                    self.auth_socket.send(pickled_socket)
                    # receives peers from auth peer
                    recv_peers = self.auth_socket.recv(self.BUFFER)
                    self.peers = pickle.loads(recv_peers)
                    # print("Received peers from auth: ", self.peers)
                    return True
                elif pw_status == "notauthenticated":
                    raise AuthenticationException("Password is incorrect")
            except AuthenticationException as e:
                print(e)
                self.auth_socket.close()
                self.peer_socket.close()
                return False

        # Connect to initial peer
        try:
            self.auth_socket.connect(starting_address)
        except ConnectionRefusedError:
            self.auth_socket.close()

        # Receive banned status from initial peer
        try:
            banned = self.auth_socket.recv(self.BUFFER).decode(self.ENCODE)
            print(banned)
            if banned == "banned":
                raise AuthenticationException("You are banned from this network")
        except AuthenticationException as e:
            print(e)
            self.auth_socket.close()
            return

        # Performs password check
        authenticated = password_check()
        if authenticated:
            self.recv_status()
        return authenticated


    def recv_status(self):
        """
        Establishes and maintains a heart beat from the auth peer.

        :return:

        """

        try:
            beat = self.auth_socket.recv(self.BUFFER)
            pickled_beat = pickle.loads(beat)
            if not beat:
                raise StatusException("Did not receive a heartbeat, Disconnecting")
            if pickled_beat['type'] == "set":
                self.peers = pickled_beat["data"]
                print("Auth peer sent a new set", self.peers)
            try:
                self.auth_socket.send("<3>".encode(self.ENCODE))
            except SendException:
                print("Could not send heartbeat to auth peer")
                self.auth_socket.close()
                self.disconnected = True
                return

        except Exception:
            print("Disconnected from Auth Peer...")
            self.auth_socket.close()
            self.disconnected = True
            return
        try:
            beat_thread = threading.Timer(2, self.recv_status)
            self.threads.append(beat_thread)
            beat_thread.start()
        except threading.ThreadError:
            print("Could not start heartbeat thread")
