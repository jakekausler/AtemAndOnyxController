# Atem And Onyx Controller

## Requirements

- [Node.js](https://nodejs.org/en/)
- [Applest-Atem](https://github.com/applest/node-applest-atem)
- [Python 3](https://www.python.org/downloads/)
- [Naked](https://pypi.org/project/Naked/)
- [Mido](https://mido.readthedocs.io/en/latest/)
- [rtmidi](https://pypi.org/project/python-rtmidi/)
- [Flask](http://flask.pocoo.org/)
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
- Obsidian Control Systems [Onyx](http://support.obsidiancontrol.com/Content/Support/Downloads.htm)
- Blackmagic [Atem Software Control](https://www.obsidiancontrol.com/)
- A way to get midi to Onyx. I use [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)

## Setup

### Setting Up Cameras and Keys

On the Blackmagic switcher, plug the cameras into available slots. Note the slot you plugged it into for use in the config file later.

Upstream keys may also be set to use with the server. These are set in the right side panel in Atem Software Control.

### Setting Up Onyx Midi Cues

Lighting cues are triggered by sending MIDI events to Onyx. First, a Note-On event is sent, followed immediately by a Note-Off. Here are the steps to create the cues:

1. Create the cue normally in Onyx. The program will use the input from MIDI events to trigger this cue.

2. Create an empty cue that will serve as the MIDI listener. Note that if you already have one, you can use it for multiple MIDI cues. To create listeners with different fades or delays, however, you will need a separate MIDI listener cue for each set of fades and delays.

3. Click on the new listener cue and open the `Cuelist - Values` page on the left side of the screen. Click `Edit Mode` at the top. You can now click on any existing macros and edit them.

4. Click `Add Macro` at the top, and then click on the new macro. At the top in the dropdown, select `MIDIMACRO`. In the next dropdown, select the cue that should be triggered.

5. Edit the macro. The MIDI event should be `Note-On`. Choose a channel for the macro to listen on. For `Data 1` and `Data 2`, choose the same `From` and `To` values. These can be any values that are not overlapping with the any other MIDI Macros on the channel. `From` and `To` may be the same number. The lowest number in the range is what gets sent by the server.

6. Click `Apply` at the top. Run the MIDI listener scene to allow Onyx to actually start listening for data.

### Tweaking the Config File

The `config.yaml` contains the settings for the server. The file has four sections:

1. Server Information

    `ServerHost` and `ServerPort` contain the server location. The port tells Flask where to serve the program on the local machine. The host is put into the client side response to tell where to send the REST calls.

2. Midi Information

    `MidiPort` is the name of the port on which the MIDI calls should be made. To get a list of port names, run `mido.get_output_names()` in python. Note that a listener port should also be set up in Onyx.

3. ATEM Information

    `AtemIP` is the network location of the Blackmagic switcher.
    
    `AtemCameras` is a mapping of named cameras to the input in the switcher. The first input is 1. The names are used in `CueGroups` below.

4. Onyx Information

    `CueGroups` contains a list of categories. These are the groups on the returned webpage. Each category contains a list of cues in that category. These are the individual buttons on the page. Under each cue, there are the following fields:
    
     - `Channel` - The channel of a MIDI Macro that should be run in Onyx.
     - `NoteFrom` - The Note-From of a MIDI Macro that should be run  in Onyx.
     - `NoteTo` - The Note-To of a MIDI Macro that should be run  in Onyx.
     - `Live` - The Blackmagic input that should go live.
     - `Key` - The key number that should go live. If no key should be on, use `0`.

## Use

 - Run `python server.py`
 - Load the client on the host and port listed in the config file
