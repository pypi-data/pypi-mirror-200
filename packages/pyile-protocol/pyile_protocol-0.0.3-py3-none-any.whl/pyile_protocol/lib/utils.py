def join_threads(threads):
    for t in threads:
        t.join(timeout=2)
