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


bl_info = {
    "name": "blendzmq",
    "author": "Stef van der Struijk",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Create Tab",
    "description": "Connects Blender with outside programs through ZeroMQ without freezing the interface",
    "warning": "",
    "wiki_url": "https://github.com/NumesSanguis/Blender-ZMQ-add-on",
    "category": "Development"}

#--------------------------
# import exporter modules
#--------------------------
# if "bpy" in locals():
#     import importlib as imp
#     if "blendzmq_props" in locals:
#         imp.reload(blendzmq_props)
#     if "blendzmq_panel" in locals:
#         imp.reload(blendzmq_panel)
#     if "blendzmq" in locals:
#         imp.reload(blendzmq)
#     # if "ot" in locals:
#     #     imp.reload(ot)
# else:
#     #
#     import bpy
#     from . import prop
#     from . import io
#     from . import ui
#     from . import ot

if "bpy" in locals():
    print("reloading .py files")
    import importlib
    # from . blendzmq_props import ZMQSocketProperties
    # importlib.reload(ZMQSocketProperties)
    # from . blendzmq_panel import BLENDZMQ_PT_zmqConnector
    # importlib.reload(BLENDZMQ_PT_zmqConnector)

    from . import blendzmq_props
    importlib.reload(blendzmq_props)
    from . import blendzmq_panel
    importlib.reload(blendzmq_panel)
    from . import blendzmq_ops
    importlib.reload(blendzmq_ops)
    # importlib.reload(ZMQSocketProperties)
else:
    print("importing .py files")
    import bpy
    from . import blendzmq_props
    from . import blendzmq_panel
    from . import blendzmq_ops

from bpy.types import AddonPreferences
from bpy.props import (
    EnumProperty,
    PointerProperty,
)
# print("hello")
# classes_register = []
# from . blendzmq_props import TracerProperties
from . blendzmq_props import PIPZMQProperties, ZMQSocketProperties, MyCollections, TrackSelectionProperties  # MyPropertyGroup
from . blendzmq_panel import BLENDZMQ_PT_zmqConnector
# classes_register.append(BLENDZMQ_PT_zmqConnector)

# classes_operators = SOCKET_OT_connect_subscriber
from . blendzmq_ops import (
    SOCKET_OT_connect_subscriber,
    PIPZMQ_OT_pip_pyzmq,
)


# Add-on Preferences
class blendzmq_preferences(AddonPreferences):
    bl_idname = "blendzmq"

    expand_enum: EnumProperty(
            name="UI Options",
            items=[
                 ('list', "Drop down list",
                  "Show all the items as dropdown list in the Tools Region"),
                 ('col', "Enable Expanded UI Panel",
                  "Show all the items expanded in the Tools Region in a column"),
                 ('row', "Icons only in a row",
                  "Show all the items as icons expanded in a row in the Tools Region")
                  ],
            description="",
            default='list'
            )

    def draw(self, context):
        layout = self.layout
        layout.label(text="UI Options:")

        row = layout.row(align=True)
        row.prop(self, "expand_enum", text="UI Options", expand=True)


# Define Classes to register
classes = (
    PIPZMQProperties,
    ZMQSocketProperties,
    MyCollections,
    TrackSelectionProperties,
    # MyPropertyGroup,
    BLENDZMQ_PT_zmqConnector,
    PIPZMQ_OT_pip_pyzmq,
    SOCKET_OT_connect_subscriber,
    blendzmq_preferences,
    )

# register, unregister = bpy.utils.register_classes_factory(classes)
def register():
    # development purposes to prevent "already registered error"
    # try:
    #     unregister()
    # except:
    #     pass
    #
    # # development purposes to prevent not detecting changes
    # try:
    #     print("reloading .py files")
    #     import importlib
    #     importlib.reload(blendzmq_props)
    #     importlib.reload(blendzmq_panel)
    #     importlib.reload(blendzmq_ops)
    # except:
    #     pass
    # print("nothing4")

    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.types.WindowManager.curve_tracer = PointerProperty(type=TracerProperties)
    bpy.types.WindowManager.install_props = PointerProperty(type=PIPZMQProperties)
    bpy.types.WindowManager.socket_settings = PointerProperty(type=ZMQSocketProperties)
    bpy.types.WindowManager.track_selection = PointerProperty(type=TrackSelectionProperties)  #  MyPropertyGroup

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # del bpy.types.WindowManager.curve_tracer
    del bpy.types.WindowManager.track_selection
    del bpy.types.WindowManager.socket_settings
    del bpy.types.WindowManager.install_props


if __name__ == "__main__":
    register()
