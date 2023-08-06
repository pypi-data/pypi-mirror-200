import threading

from pyile_protocol.lib.peers.AuthPeer import AuthPeer


def test_auth():
    auth_peer = AuthPeer(address=("192.168.1.66", 4702), password_attempts=1, password="password")
    # auth_peer = AuthPeer(("172.20.100.39", 4702), 1, "password")
    print(auth_peer)

    auth_thread = threading.Thread(target=auth_peer.authenticate_peers)
    peer_thread = threading.Thread(target=auth_peer.connect)
    auth_thread.start()
    peer_thread.start()

    while not auth_peer.disconnected:
        data = input("~: ")
        if data == "exit":
            auth_peer.leave()
        elif data == "peers":
            print(auth_peer.peers)
        else:
            auth_peer.broadcast(data)
