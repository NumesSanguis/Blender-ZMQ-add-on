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

# Copyright (c) Stef van der Struijk <stefstruijk@protonmail.ch>

import bpy
from bpy.types import (
        PropertyGroup,
        )
from bpy.props import (
        StringProperty,
        BoolProperty,
        )


class ZMQSocketProperties(PropertyGroup):
    """ZeroMQ socket Properties"""

    #   moved to __init__.py -> BlendzmqPreferences()
    # socket_ip: StringProperty(name="Socket ip",
    #                           description="IP of ZMQ publisher socket",
    #                           default="127.0.0.1",
    #                           )
    # socket_port: StringProperty(name="Socket port",
    #                             description="Port of ZMQ publisher socket",
    #                             default="5550",
    #                             )

    socket_connected: BoolProperty(name="Connect status",
                                   description="Boolean whether the Socket's connection is active or not",
                                   default=False
                                   )
    msg_received: StringProperty(name="Received msg",
                                 description="Message received from ZMQ subscriber socket",
                                 default="Awaiting msg...",
                                 )
    dynamic_object: BoolProperty(name="Dynamic objects",
                                 description="Stream data to selected objects (False: stream to same objects)",
                                 default=True
                                 )
    # selected_objects: CollectionProperty(type=bpy.types.Object)


class PIPZMQProperties(PropertyGroup):
    """pip install and pyzmq install Properties"""
    install_status: StringProperty(name="Install status",
                                   description="Install status messages",
                                   default="pyzmq not found in Python distribution",
                                   )


# failed attempt at storing reference to selected objects
# class MyCollections(bpy.types.PropertyGroup):
#     object: bpy.props.PointerProperty(type=bpy.types.Object)
# class TrackSelectionProperties(bpy.types.PropertyGroup):
#     selected_objects: bpy.props.CollectionProperty(type=MyCollections)  # bpy.types.Object


def register():
    bpy.utils.register_class(PIPZMQProperties)
    bpy.utils.register_class(ZMQSocketProperties)


def unregister():
    bpy.utils.unregister_class(ZMQSocketProperties)
    bpy.utils.unregister_class(PIPZMQProperties)


if __name__ == "__main__":
    register()
