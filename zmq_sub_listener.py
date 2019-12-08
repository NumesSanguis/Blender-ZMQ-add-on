# The Unlicense: https://choosealicense.com/licenses/unlicense/
# Author: Stef van der Struijk <stefstruijk@protonmail.ch>

"""Listens to messages from publisher sockets, e.g. from `python zmq_pub_number_gen.py` or `python zmq_pub_command.py`

WARNING: Don't run this in combination with Blender add-on `blendzmq` active; Only 1 port can be `bind` to.
With default values, binds as a socket to 127.0.0.1:5550.
Change ip with e.g. `--ip 192.168.x.x` and change port with e.g. `--port 8080`
E.g. `python zmq_sub_listener.py --ip 192.168.10.50 --port 8080`"""

import argparse
import zmq


def main(ip="127.0.0.1", port="5550"):
    # ZMQ connection
    url = "tcp://{}:{}".format(ip, port)
    ctx = zmq.Context()
    socket = ctx.socket(zmq.SUB)
    socket.bind(url)  # subscriber creates ZeroMQ socket
    socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))  # any topic
    print("Sub bound to: {}\nWaiting for data...".format(url))

    while True:
        # wait for publisher data
        topic, msg = socket.recv_multipart()
        print("On topic {}, received data: {}".format(topic, msg))


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser()

    # publisher setup commandline arguments
    parser.add_argument("--ip", default="127.0.0.1",
                        help="IP (e.g. 192.168.x.x) of where to sub to; Default: 127.0.0.1 (local)")
    parser.add_argument("--port", default="5550",
                        help="Port of where to sub to; Default: 5550")

    args, leftovers = parser.parse_known_args()
    print("The following arguments are used: {}".format(args))
    print("The following arguments are ignored: {}\n".format(leftovers))

    main(**vars(args))
