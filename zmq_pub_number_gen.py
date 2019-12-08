# The Unlicense: https://choosealicense.com/licenses/unlicense/
# Author: Stef van der Struijk <stefstruijk@protonmail.ch>

"""Generates numbers between 0-100 and publishes it to subscriber sockets (e.g. Blender) at 30fps

With default values, connects to a socket at 127.0.0.1:5550.
Change ip with e.g. `--ip 192.168.x.x` and change port with e.g. `--port 8080`
E.g. `python zmq_pub_number_gen.py --ip 192.168.10.50 --port 8080`"""

import argparse
import zmq
import time


def main(ip="127.0.0.1", port="5550"):
    # ZMQ connection
    url = "tcp://{}:{}".format(ip, port)
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUB)
    socket.connect(url)  # publisher connects to subscriber
    print("Pub connected to: {}\nSending data...".format(url))

    i = 0
    topic = 'foo'.encode('ascii')

    # keep sending messages until program interruption
    while True:
        # user_msg = input("Please type a message to send: ")
        msg = str(i).encode('utf-8')
        # publish data
        socket.send_multipart([topic, msg])  # 'test'.format(i)
        print("On topic {}, send data: {}".format(topic, msg))
        # 30 fps
        time.sleep(1/30)

        i += 2
        if i > 100:
            i = 0


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser()

    # publisher setup commandline arguments
    parser.add_argument("--ip", default="127.0.0.1",
                        help="IP (e.g. 192.168.x.x) of where to pub to; Default: 127.0.0.1 (local)")
    parser.add_argument("--port", default="5550",
                        help="Port of where to pub to; Default: 5550")

    args, leftovers = parser.parse_known_args()
    print("The following arguments are used: {}".format(args))
    print("The following arguments are ignored: {}\n".format(leftovers))

    main(**vars(args))
