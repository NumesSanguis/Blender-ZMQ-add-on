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

# Copyright (c) Stef van der Struijk


import bpy
import sys
import subprocess
from pathlib import Path  # Object-oriented filesystem paths since Python 3.4
from copy import deepcopy
# import zmq
import functools
# import selection_utils
from bpy.types import Operator
from random import (
        choice as rand_choice,
        random as rand_random,
        randint as rand_randint,
        uniform as rand_uniform,
        )
from functools import partial
import copy


# class StartZMQSub(bpy.types.Operator):
class SOCKET_OT_connect_subscriber(bpy.types.Operator):
    """Connects ZeroMQ socket: Subscriber"""  # Use this as a tooltip for menu items and buttons.
    # bl_idname = "object.move_x"  # Unique identifier for buttons and menu items to reference.
    bl_idname = "socket.connect_subscriber"
    bl_label = "Connect socket"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    statetest = "Nothing yet..."

    # def get_default_context(self):
    #     window = bpy.context.window_manager.windows[0]
    #     return {'window': window, 'screen': window.screen}
    #
    #
    # def execute(self, context):
    #     #self.blend_ctx = copy.deepcopy(context)
    #     print("execute function...")
    #     # print(dir(self.blend_ctx))
    #
    #     # print(self.statetest)
    #
    #     self.selected_objs = context.selected_objects
    #     self.socket_settings = context.window_manager.socket_settings
    #
    #     # connect to a ZMQ socket and set a timer for ZMQ poller
    #     if not self.socket_settings.socket_connected:
    #         bpy.types.WindowManager.test_dict = {"helo": -1}
    #     #     self.statetest = "Socket on"
    #         self.socket_settings.socket_connected = True
    #     else:
    #         bpy.types.WindowManager.test_dict = {"helo": 1}
    #     #     self.statetest = "Socket off"
    #         self.socket_settings.socket_connected = False
    #
    #     # print(self.statetest)
    #
    #     bpy.app.timers.register(self.timed_test)
    #
    #     return {'FINISHED'}
    #
    # def timed_test(self):
    #     # print(self.statetest)
    #
    #     print("timer function...")
    #     # print(dir(self.blend_ctx))
    #     # print(dir(context))
    #
    #     move_val = bpy.types.WindowManager.test_dict["helo"]
    #     print(move_val)
    #     # blend_ctx = self.get_default_context()
    #     # for obj in self.selected_objs:
    #     # for obj in blend_ctx['selected_objects']:
    #     # for obj in bpy.context.scene.view_layers[0].objects.active:
    #     #for obj in bpy.context.scene.view_layers[0].selected_objects:
    #     # for obj in bpy.context.selected_objects:
    #     for obj in bpy.context.window_manager.windows[0].objects.active:
    #         obj.location.x = move_val
    #     # bpy.context.scene.view_layers[0].objects.active.location.x = move_val
    #
    #     return 0.2

    def execute(self, context):  # execute() is called when running the operator.
        # if this operator can be triggered thought an interface button, pyzmq has been installed
        import zmq

        # self.blend_ctx = context
        #print(dir(self.blend_ctx))
        self.socket_settings = context.window_manager.socket_settings
        self.track_selection = context.window_manager.track_selection
        print("track_selection")
        print(self.track_selection.multiple_objects)

        if not self.socket_settings.socket_connected:
            self.zmq_ctx = zmq.Context().instance()  # zmq.Context().instance()  # Context
            self.url = f"tcp://{self.socket_settings.socket_ip}:{self.socket_settings.socket_port}"
            bpy.types.WindowManager.socket_sub = self.zmq_ctx.socket(zmq.SUB)
            bpy.types.WindowManager.socket_sub.bind(self.url)  # publisher connects to this (subscriber)
            bpy.types.WindowManager.socket_sub.setsockopt(zmq.SUBSCRIBE, ''.encode('ascii'))
            print("Sub bound to: {}\nWaiting for data...".format(self.url))

            # poller socket for checking server replies (synchronous)
            self.poller = zmq.Poller()
            self.poller.register(bpy.types.WindowManager.socket_sub, zmq.POLLIN)

            # let Blender know our socket is connected
            self.socket_settings.socket_connected = True

            # reference to active object at start of data stream
            print(bpy.context.scene.view_layers[0].objects.selected)
            print(type(bpy.context.scene.view_layers[0].objects.selected))

            # self.socket_settings.selected_objects = bpy.context.scene.view_layers[0].objects.selected
            # self.selected_obj = bpy.context.scene.view_layers[0].objects.active
            # self.selected_objs = bpy.context.scene.view_layers[0].objects.selected  # .active
            # self.selected_objs = bpy.context.scene.view_layers[0].selected_objects
            self.track_selection.multiple_objects = bpy.context.scene.view_layers[0].objects.selected

            bpy.app.timers.register(self.timed_msg_poller)
            # bpy.app.timers.register(partial(self.timed_msg_poller, context))

        # stop ZMQ poller timer and disconnect ZMQ socket
        else:
            print(self.statetest)
            # cancel timer function with poller if active
            if bpy.app.timers.is_registered(self.timed_msg_poller):
                bpy.app.timers.unregister(self.timed_msg_poller())

            try:
                # close connection
                bpy.types.WindowManager.socket_sub.close()
                print("Subscriber socket closed")
                # remove reference
            except AttributeError:
                print("Subscriber was socket not active")

            # let Blender know our socket is disconnected
            bpy.types.WindowManager.socket_sub = None
            self.socket_settings.socket_connected = False

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.

    def timed_msg_poller(self):  # context
        socket_sub = bpy.types.WindowManager.socket_sub
        # track_selection = bpy.types.WindowManager.track_selection
        # print("track_selection")
        # print(track_selection.multiple_objects)

        # socket_settings = bpy.types.WindowManager.socket_settings
        # only keep running if socket reference exist (not None)
        if socket_sub:
            # get sockets with messages (0: don't wait for msgs)
            sockets = dict(self.poller.poll(0))
            # check if our sub socket has a message
            if socket_sub in sockets:
                # get the message
                topic, msg = socket_sub.recv_multipart()
                print("On topic {}, received data: {}".format(topic, msg))
                # context stays the same as when started?
                self.socket_settings.msg_received = msg.decode('utf-8')

                # update selected obj as long as Dynamic object is on
                if self.socket_settings.dynamic_object:
                    print("\nobj selection info:")
                    # self.socket_settings.selected_objects = bpy.context.scene.view_layers[0].objects.selected
                    print(bpy.context.scene.view_layers[0].objects.selected)
                    print(type(bpy.context.scene.view_layers[0].objects.selected))
                    # print(bpy.context.scene.view_layers[0].objects.active)
                    # print(type(bpy.context.scene.view_layers[0].objects.active))
                    # self.selected_obj = bpy.context.scene.view_layers[0].objects.active
                    self.track_selection.multiple_objects = bpy.context.scene.view_layers[0].objects.selected
                    # dict works with pointers, therefore "Dynamic object" selection doesn't keep the old reference
                    # self.selected_objs = deepcopy(bpy.context.scene.view_layers[0].objects.selected)  # .active
                    # self.selected_objs = bpy.context.scene.view_layers[0].selected_objects

                # move all objects
                # for obj in self.blend_ctx.scene.objects:
                #     obj.location.x = int(msg.decode('utf-8')) * .1
                #   move active object
                move_val = int(msg.decode('utf-8')) * .1
                # collections work with pointers, therefore "Dynamic object" selection doesn't keep the old reference
                # for obj in self.selected_objs:
                print(self.track_selection.multiple_objects)
                for obj in self.track_selection.multiple_objects:
                    obj.location.x = move_val
                # self.selected_obj.location.x = int(msg.decode('utf-8')) * .1

            # keep running
            return 0.001

    # def timed_msg_poller(self):  # context
    #     # get sockets with messages (0: don't wait for msgs)
    #     sockets = dict(bpy.types.WindowManager.poller.poll(0))
    #     # check if our sub socket has a message
    #     if bpy.types.WindowManager.socket_sub in sockets:
    #         # get the message
    #         topic, msg = bpy.types.WindowManager.socket_sub.recv_multipart()
    #         print("On topic {}, received data: {}".format(topic, msg))
    #         # context stays the same as when started?
    #         # self.socket_sub_settings.msg_received = msg.decode('utf-8')
    #
    #         # move cube
    #         # for obj in self.blend_ctx.scene.objects:
    #         #     obj.location.x = int(msg.decode('utf-8')) * .1
    #         bpy.context.scene.view_layers[0].objects.active.location.x = int(msg.decode('utf-8')) * .1
    #
    #         # move only selected object
    #         # self.blend_ctx.selected_objects.location.x = int(msg.decode('utf-8')) * .1
    #
    #     # keep running
    #     return 0.001

    # def execute(self, context):        # execute() is called when running the operator.
    #     self.blend_ctx = context
    #     print(dir(self.blend_ctx))
    #     self.socket_settings = context.window_manager.socket_settings
    #
    #     if not self.socket_settings.socket_connected:
    #         self.zmq_ctx = zmq.Context().instance()  # zmq.Context().instance()  # Context
    #         self.url = f"tcp://{self.socket_settings.socket_ip}:{self.socket_settings.socket_port}"
    #         self.socket_sub = self.zmq_ctx.socket(zmq.SUB)
    #         self.socket_sub.connect(self.url)  # subscriber connects to publisher
    #         self.socket_sub.setsockopt(zmq.SUBSCRIBE, ''.encode('ascii'))
    #         print("Sub bound to: {}\nWaiting for data...".format(self.url))
    #
    #         # poller socket for checking server replies (synchronous)
    #         self.poller = zmq.Poller()
    #         self.poller.register(self.socket_sub, zmq.POLLIN)
    #
    #         # let Blender know our socket is connected
    #         self.socket_settings.socket_connected = True
    #
    #         bpy.app.timers.register(self.timed_msg_poller)
    #         # bpy.app.timers.register(partial(self.timed_msg_poller, context))
    #
    #     # stop ZMQ poller timer and disconnect ZMQ socket
    #     else:
    #         print(self.statetest)
    #         # cancel timer function with poller if active
    #         if bpy.app.timers.is_registered(self.timed_msg_poller):
    #             bpy.app.timers.unregister(self.timed_msg_poller())
    #
    #         # try:
    #         self.socket_sub.close()
    #         #     print("Subscriber socket closed")
    #         # except AttributeError:
    #         #     print("Subscriber socket not active")
    #
    #         # let Blender know our socket is disconnected
    #         self.socket_settings.socket_connected = False
    #
    #     return {'FINISHED'}            # Lets Blender know the operator finished successfully.
    #
    # def timed_msg_poller(self):  # context
    #     # get sockets with messages (0: don't wait for msgs)
    #     sockets = dict(self.poller.poll(0))
    #     # check if our sub socket has a message
    #     if self.socket_sub in sockets:
    #         # get the message
    #         topic, msg = self.socket_sub.recv_multipart()
    #         print("On topic {}, received data: {}".format(topic, msg))
    #         # context stays the same as when started?
    #         # self.socket_sub_settings.msg_received = msg.decode('utf-8')
    #
    #         # move cube
    #         for obj in self.blend_ctx.scene.objects:
    #             obj.location.x = int(msg.decode('utf-8')) * .1
    #
    #         # move only selected object
    #         # self.blend_ctx.selected_objects.location.x = int(msg.decode('utf-8')) * .1
    #
    #     # keep running
    #     return 0.001


class PIPZMQ_OT_pip_pyzmq(bpy.types.Operator):
    """Enables and updates pip, and installs pyzmq"""  # Use this as a tooltip for menu items and buttons.
    # bl_idname = "object.move_x"  # Unique identifier for buttons and menu items to reference.
    bl_idname = "pipzmq.pip_pyzmq"
    bl_label = "Enable pip & install pyzmq"  # Display name in the interface.
    bl_options = {'REGISTER'}  # Enable undo for the operator.
    # statetest = "Nothing yet..."

    def execute(self, context):  # execute() is called when running the operator.
        install_props = context.window_manager.install_props
        install_props.install_status = "Preparing to enable pip..."

        # OS independent (Windows: bin\python.exe; Linux: bin/python3.7m)
        py_path = Path(sys.prefix) / "bin"
        py_exec = str(next(py_path.glob("python*")))  # first file that starts with "python" in "bin" dir
        # TODO check permission rights
        if subprocess.call([py_exec, "-m", "ensurepip"]) != 0:
            install_props.install_status += "\nCouldn't activate pip."
            self.report({'ERROR'}, "Couldn't activate pip.")
            return {'CANCELLED'}
        install_props.install_status += "\nPip activated! Updating pip..."
        self.report({'INFO'}, "Pip activated! Updating pip...")
        if subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip"]) != 0:
            install_props.install_status += "\nCouldn't update pip."
            self.report({'ERROR'}, "Couldn't update pip.")
            return {'CANCELLED'}
        install_props.install_status += "\nPip updated! Installing pyzmq..."
        self.report({'INFO'}, "Pip updated! Installing pyzmq...")

        if subprocess.call([py_exec, "-m", "pip", "install", "pyzmq"]) != 0:
            install_props.install_status += "\nCouldn't install pyzmq."
            self.report({'ERROR'}, "Couldn't install pyzmq.")
            return {'CANCELLED'}
        install_props.install_status += "\npyzmq installed! READY!"
        self.report({'INFO'}, "pyzmq installed! READY!")

        return {'FINISHED'}  # Lets Blender know the operator finished successfully


def register():
    bpy.utils.register_class(PIPZMQ_OT_pip_pyzmq)
    bpy.utils.register_class(SOCKET_OT_connect_subscriber)


def unregister():
    bpy.utils.unregister_class(SOCKET_OT_connect_subscriber)
    bpy.utils.register_class(PIPZMQ_OT_pip_pyzmq)


#
if __name__ == "__main__":
    register()
