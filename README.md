# Blender-ZMQ-add-on
Blender 2.8x add-on that allows streaming of data into Blender over ZeroMQ sockets, **without** freezing the interface.

**WARNING: CODE STILL IN PROGRESS and INSTRUCTIONS NOT COMPLETE**

## Overview
Blender is very powerful software, but if you run your own code that's a bit heavy, you quickly make the interface
unresponsive, if you don't employ Threading or Async.
Threading/Async is difficult in Blender, however, due it's internal loop (which is more like a game engine).
Also, in case of threading, you can't manipulate objects in the main loop of Blender without using e.g. a queue system.

Why not take the program logic and manipulation of data outside Blender? Enter ZeroMQ.

ZeroMQ (pyzmq - Python wrapper of ZMQ) is a communication protocol library that allows the sending of data packages
between programs (even when written in different languages) by using sockets.
Therefore, the data can be send over the network (e.g. TCP), meaning you can even run the software on different devices.

This add-on works by setting a timer function (Blender 2.80+) that checks if a ZeroMQ socket has received
a message from outside (using `zmq.Poller()`). If so, process that data to move a selected object.
This timer keeps being triggered until the socket has been disconnected.
See for a demonstration:

YOUTUBE link

You can take this add-on as an example on how to connect your own programs with Blender.


## Prerequisite
- Python (tested with 3.7, probably 2.7, 3.5+ works too) on your system with `pyzmq`
for programs outside Blender.
    - Anaconda (recommended to manage Python environments)
        0. Anaconda 3.7+: https://www.anaconda.com/distribution/
        0. `conda create --name bzmq python=3.7`  # create environment with Python 3.7
        0. `conda activate bzmq`  # activate newly created environment
        0. `conda install -c anaconda pyzmq`  # install pyzmq in this environment
    - System Python: `pip install pyzmq`

## How to use
0. Download this repository as a .zip by:
    - Go to https://github.com/NumesSanguis/Blender-ZMQ-add-on/releases and download the ZIP, or
    - Clicking the green "Clone or download" button and choose "Download ZIP"
0. Start Blender with Administrator right (at least on Windows) to allow enabling of `pip` and installing `pyzmq`
0. In Blender, add this add-on by selecting Edit -> Preferences -> Add-ons ->
    0. Install... -> select downloaded ZIP from previous step -> Install Add-on from File...
    0. Search: `Development: blendzmq` -> click checkbox to activate
0. Open side panel in 3D view by
    - Pressing `n` on your keyboard
    - Dragging `<` to the left
0. Click "bZMQ" -> "Enable pip and update" button -> "Install pyzmq" button
0. Click "Connect socket" button. Now it's waiting for data message from outside.
0. Start outside script to send data into blender (Get the script by downloading from the GitHub repo / unzip previously downloaded ZIP):
    0. Open a terminal and navigate to `cd *path*/Blender-ZMQ-add-on`
    0. Make sure conda / virtual env is active (e.g. `conda activate bzmq`) with `pyzmq`
    0. Execute: `python zmq_pub_number_gen.py`
0. See objects moving!
    - Dynamic object can be selected to update location of current active object
    - Dynamic object can be deselected to keep updating only the object that was active at deselection time.
    
    
# TODO
- Enable pip and install `pyzmq` in Blender with buttons (step 5)


# Notes
Blender add-on file structure inspired by btrace: https://github.com/sobotka/blender-addons/tree/master/btrace

More information about ZeroMQ: https://zeromq.org/

Why not make your outside Blender software easy to deploy, independent of OS?
Take a look at ZeroMQ with Docker: https://github.com/NumesSanguis/pyzmq-docker
