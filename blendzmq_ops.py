# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import zmq
import functools
# import selection_utils
from bpy.types import Operator
from random import (
        choice as rand_choice,
        random as rand_random,
        randint as rand_randint,
        uniform as rand_uniform,
        )


# class StartZMQSub(bpy.types.Operator):
class SOCKET_OT_connect_subscriber(bpy.types.Operator):
    """Connects ZeroMQ socket: Subscriber"""  # Use this as a tooltip for menu items and buttons.
    # bl_idname = "object.move_x"  # Unique identifier for buttons and menu items to reference.
    bl_idname = "socket.connect_subscriber"
    bl_label = "Connect socket"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        self.blend_ctx = context
        self.socket_settings = context.window_manager.socket_settings

        # connect to a ZMQ socket and set a timer for ZMQ poller
        if not self.socket_settings.socket_connected:
            self.zmq_ctx = zmq.Context().instance()  # zmq.Context().instance()  # Context
            self.url = f"tcp://{self.socket_settings.socket_ip}:{self.socket_settings.socket_port}"
            self.socket_sub = self.zmq_ctx.socket(zmq.SUB)
            self.socket_sub.connect(self.url)  # subscriber connects to publisher
            self.socket_sub.setsockopt(zmq.SUBSCRIBE, ''.encode('ascii'))
            print("Sub bound to: {}\nWaiting for data...".format(self.url))

            # poller socket for checking server replies (synchronous)
            self.poller = zmq.Poller()
            self.poller.register(self.socket_sub, zmq.POLLIN)

            # let Blender know our socket is connected
            self.socket_settings.socket_connected = True

            bpy.app.timers.register(self.timed_msg_poller)

        # stop ZMQ poller timer and disconnect ZMQ socket
        else:
            # cancel timer function with poller if active
            if bpy.app.timers.is_registered(self.timed_msg_poller):
                bpy.app.timers.unregister(self.timed_msg_poller())

            # try:
            self.socket_sub.close()
            #     print("Subscriber socket closed")
            # except AttributeError:
            #     print("Subscriber socket not active")

            # let Blender know our socket is disconnected
            self.socket_settings.socket_connected = False

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

    def timed_msg_poller(self):
        # get sockets with messages (0: don't wait for msgs)
        sockets = dict(self.poller.poll(0))
        # check if our sub socket has a message
        if self.socket_sub in sockets:
            # get the message
            topic, msg = self.socket_sub.recv_multipart()
            print("On topic {}, received data: {}".format(topic, msg))
            # context stays the same as when started?
            # self.socket_sub_settings.msg_received = msg.decode('utf-8')

            # move cube
            for obj in self.blend_ctx.scene.objects:
                obj.location.x = int(msg.decode('utf-8')) * .1

        # keep running
        return 0.001


def register():
    bpy.utils.register_class(SOCKET_OT_connect_subscriber)


def unregister():
    bpy.utils.unregister_class(SOCKET_OT_connect_subscriber)


#
if __name__ == "__main__":
    register()
