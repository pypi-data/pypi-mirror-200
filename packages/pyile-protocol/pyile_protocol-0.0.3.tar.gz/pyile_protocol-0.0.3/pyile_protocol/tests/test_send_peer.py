import threading

from pyile_protocol.lib.peers.JoinPeer import JoinPeer
from random import randint


def test_peer():
    # Add random int to auth port to avoid conflicts when testing
    peer = JoinPeer(address=("192.168.1.65", 4702 + randint(0, 20)))

    # Normal Instance
    # peer = JoinPeer(("172.20.100.99", 4702 + randint(0, 20)))

    '''
    get_authenticated() returns a boolean value, can be looped until peer is banned
    '''
    # authenticated = peer.get_authenticated(("172.20.100.39", 4702), "password")
    peer.get_authenticated(("192.168.1.66", 4702), "password")

    try:
        connect_thread = threading.Thread(target=peer.connect)
        connect_thread.start()
    except:
        print("threads terminated")

    while not peer.disconnected:
        data = input("~: ")
        if data == "exit":
            peer.leave()

        elif data == "peers":
            print(peer.peers)
        else:
            peer.broadcast(data)
