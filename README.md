# Blender-ZMQ-add-on (BlendZMQ)
Blender 2.8x add-on that allows streaming of data (from another computer) into Blender over ZeroMQ sockets,
**without** freezing the interface (publisher-subscriber pattern).

## Update
- v1.1 (2020-02-10) - **Blender 2.81+ pip support**: In Blender 2.81 pip is enabled by default.
This update takes that behavior into account. If the `Enable pip & install pyzmq` button fails, it still executes
`ensurepip.bootstrap()`. Restart Blender and try again, it will work this time
(on Windows make sure you run with admin rights).

## Overview
Blender is very powerful software, but if you run your own code that's a bit heavy, you quickly make the interface
unresponsive. I.e freezing the interface.
This could be solved with Threading/Async, however, this is difficult due Blender's internal loop (which is more like a game engine).
Also, in case of threading, you can't manipulate objects in the main loop of Blender without using e.g. a queue system.

Why not take the program logic and manipulation of data outside Blender, and possibly run heavy code on another PC?
Enter ZeroMQ.

ZeroMQ (`pyzmq` - Python wrapper of ZMQ) is a communication protocol library that allows the sending of data packages
between programs (even when written in different languages) by using sockets.
Therefore, the data can be send over the network (e.g. TCP), meaning you can even run the software on different machines.

This add-on works by setting a timer function (Blender 2.80+) that checks if a ZeroMQ socket has received
a message from outside (using `zmq.Poller()`). If so, process that data to move selected objects.
This timer keeps being invoked until the socket has been disconnected.
See for a demonstration:

[![BlendZMQ demo](https://img.youtube.com/vi/68zSpWZirtI/0.jpg)](https://youtu.be/68zSpWZirtI)]

You can take this add-on as an example on how to connect your own programs with Blender.


## Prerequisite
- Python (tested with 3.7, probably 2.7, 3.5+ works too) on your system with `pyzmq`
for programs outside Blender.
   - Anaconda (recommended to manage Python environments)
     1. Anaconda 3.7+: https://www.anaconda.com/distribution/
     2. `conda create --name bzmq python=3.7`  # create environment with Python 3.7
     3. `conda activate bzmq`  # activate newly created environment
     4. `conda install -c anaconda pyzmq`  # install pyzmq in this environment
   - System Python: `pip install pyzmq`

## How to use
1. Download this repository as a .zip by:
   - Go to https://github.com/NumesSanguis/Blender-ZMQ-add-on/releases and download the ZIP, or
   - Clicking the green "Clone or download" button and choose "Download ZIP"
1. Start Blender with Administrator right (at least on Windows) to allow enabling of `pip` and installing `pyzmq`
(does NOT work with a Snap package install of Blender on Linux, see troubleshooting)
1. In Blender, add this add-on by selecting Edit -> Preferences -> Add-ons ->
   1. Install... -> select downloaded ZIP from step 1 -> Install Add-on
   1. Search: `blendzmq` -> click checkbox to activate
1. Open side panel in 3D view by
   - Pressing `n` on your keyboard
   - Dragging `<` to the left
1. Click "bZMQ" -> "Enable pip & install pyzmq" button
1. Click "Connect socket" button. Now it's waiting for data message from outside.
1. Start outside script to send data into blender (Get the script by downloading from the GitHub repo / unzip previously downloaded ZIP):
   1. Get script by:
      * Unziping the .zip downloaded in step 1
      * In terminal: `git clone https://github.com/NumesSanguis/Blender-ZMQ-add-on`
   2. Open a terminal and navigate to `cd *path*/Blender-ZMQ-add-on`
   3. Make sure conda / virtual env is active (e.g. `conda activate bzmq`) with `pyzmq`
   4. Execute: `python zmq_pub_number_gen.py` (Change ip or port by adding `--ip 192.168.x.x` and/or `--port 8080`)
1. See objects moving!
   - "Dynamic objects" can be selected to update location of current selected objects
   - "Dynamic objects" can be deselected to keep updating only the objects that were active at deselection time.
    
    
## Troubleshooting
- If Step 5 (enable pip & install `pyzmq`) does not work (e.g. `Couldn't activate pip.`),
link Blender to e.g. your `bzmq` conda environment:
https://docs.blender.org/api/current/info_tips_and_tricks.html#bundled-python-extensions


# Notes
- Blender Artists: https://blenderartists.org/t/blendzmq-open-source-add-on-streaming-data-into-blender-2-8x-without-freezing-the-interface/
- Gumroad: https://gumroad.com/l/blendzmq
- Blender add-on file structure inspired by btrace: https://github.com/sobotka/blender-addons/tree/master/btrace
- More information about ZeroMQ: https://zeromq.org/
- Why not make your outside Blender software easy to deploy, independent of OS?
Take a look at ZeroMQ with Docker: https://github.com/NumesSanguis/pyzmq-docker
- When developing Blender Add-ons, reload all add-ons without restarting Blender by executing: `bpy.ops.script.reload()`


# Acknowledgement
- dr.sybren (bunch of small questions)
- joules (multi-selection of previously selected objects)
- Other people at blender.chat, blender.stackexchange.com and the documentation
