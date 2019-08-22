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
from bpy.types import (
        PropertyGroup,
        )
from bpy.props import (
        StringProperty,
        FloatProperty,
        EnumProperty,
        IntProperty,
        BoolProperty,
        FloatVectorProperty,
        )


class ZMQSocketProperties(PropertyGroup):
    """ZeroMQ socket Properties"""
    socket_ip: StringProperty(name="Socket ip",
                              description="IP of ZMQ publisher socket",
                              default="127.0.0.1",
                              )
    socket_port: StringProperty(name="Socket port",
                                description="Port of ZMQ publisher socket",
                                default="5550",
                                )
    socket_connected: BoolProperty(name="Connect status",
                                   description="Boolean whether the Socket's connection is active or not",
                                   default=False
                                   )
    msg_received: StringProperty(name="Received msg",
                                 description="Message received from ZMQ subscriber socket",
                                 default="Awaiting msg...",
                                 )
    # reload_module_name: StringProperty(name="Name",
    #                                    description="Reload this module",
    #                                    default="blendzmq",
    #                                    )


def register():
    bpy.utils.register_class(ZMQSocketProperties)


def unregister():
    bpy.utils.unregister_class(ZMQSocketProperties)


#
if __name__ == "__main__":
    register()
