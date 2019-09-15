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
from bpy.types import Panel


# Draw Socket panel in Toolbar
class BLENDZMQ_PT_zmqConnector(Panel):
    # bl_idname = "BLENDZMQ_PT_object_brush" # "BTRACE_PT_object_brush"
    bl_label = "BlenderZMQ"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category = "bZMQ"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        socket_settings = context.window_manager.socket_settings
        # Btrace = context.window_manager.curve_tracer
        # addon_prefs = context.preferences.addons[__package__].preferences
        # switch_expand = addon_prefs.expand_enum
        # obj = context.object

        row = layout.row()
        # layout.prop(socket_settings, "reload_module_name")
        # layout.operator("object.reload_module")
        # layout.operator("bpy.ops.script.reload()")
        row.prop(socket_settings, "socket_ip")
        row.prop(socket_settings, "socket_port", text="port")
        layout.prop(socket_settings, "dynamic_object")
        # if our socket hasn't connected yet
        if not socket_settings.socket_connected:
            layout.operator("socket.connect_subscriber")  # , text="Connect Socket"
        else:
            layout.operator("socket.connect_subscriber", text="Disconnect Socket")
            layout.prop(socket_settings, "msg_received")


def register():
    bpy.utils.register_class(BLENDZMQ_PT_zmqConnector)


def unregister():
    bpy.utils.unregister_class(BLENDZMQ_PT_zmqConnector)


#
if __name__ == "__main__":
    register()
