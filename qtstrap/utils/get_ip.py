import socket


def get_ip():
    """
    Get the current machine's IPv4 address.

    This process is more complicated than it appears because of the possiblity of multiple arbitrary network interfaces.
    """

    # possible alternate implementation
    # it's cleaner but partially broken
    # hostname = socket.gethostname()
    # print(hostname)
    # ip = socket.gethostbyname(hostname)
    # return ip

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    print(get_ip())