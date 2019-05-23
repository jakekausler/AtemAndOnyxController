
from __future__ import print_function
import sys
import mido
import yaml
import re
import json
import time
from flask import Flask, send_file, Response
from Naked.toolshed.shell import execute_js


app = Flask(__name__)

outport = mido.open_output('loopMIDI Port 1')

def load_config(f="config.yaml"):
    with open(f, 'r', encoding='utf8') as stream:
        config = yaml.safe_load(stream)
        return config

def format_url_name(s):
    return re.sub(r"[^\w']+", "", s.lower(), flags = re.UNICODE)

def create_html(config):
    s = '''<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>
<body>
    <h1>Video and Lighting Switcher</h1>
    <div id="header" class="hide-on-mobile">
        <p>Before using, ensure that Node Red, Onyx, and LoopMidi are running. Also ensure that Onyx recognizes LoopMidi as a Midi device and that CL10 on Bank 11 is on. Finally, make sure that Atem is connected in Node Red. All hotkeys in parenthesis use the ALT key.</p>
        <p>Always run "House On" before leaving.</p>
    </div>
    <div id="buttons">'''
    for category in config['CueGroups']:
        s += '''
        <div class="buttongroup">
            <h2>{0}</h2>'''.format(category)
        for scene in config['CueGroups'][category]:
            s += '''
            <div class="button" onclick="call('{0}', '{1}')">{2}</div>'''.format(category, scene, scene)
        s += '''
        </div>'''
    s += '''
    </div>
</body>
<script>
    function call(category, scene) {
        $.ajax({
            type: "GET",
            '''
    s += 'url: "http://{}:{}/api/"+category+"/"+scene,'.format(config['ServerIP'], config['ServerPort'])
    s += '''
            crossDomain: true
        });
    }
</script>
<style>
    body {
        background: #333333;
        color: #FFFFFF;
        font-size: medium;
        font-family: sans-serif;
    }

    #header {
        margin: 8px .25%;
        padding: 5px;
        border: 2px solid rgba(0,0,0,.5);
        border-radius: .5em;
        border-sizing: border-box;
        text-decoration: none;
        font-family: sans-serif;
        font-weight: 300;
        color: #000000;
        background: #FFFFFF;
    }

    #header > p {
        margin: 5px;
    }

    .button {
        display: block;
        margin: 8px .25%;
        padding: 20px;
        border: 2px solid rgba(255,255,255,.5);
        border-radius: .5em;
        border-sizing: border-box;
        text-decoration: none;
        font-family: sans-serif;
        font-weight: 300;
        color: #FFFFFF;
        background: rgba(0,0,0,.5);
        transition: all 0.2s;
        text-align: center;
    }

    .button:hover {
        color: #000000;
        background-color: #FFFFFF;
        cursor: pointer;
    }

    .hide-on-mobile {
        display: none;
    }

    @media only screen and (min-width:769px) {
        body {
            font-size: large;
        }

        .button {
            display: inline-block;
            width: 21%;
            padding-top: 10px;
            padding-bottom: 10px;
            margin: 2px .25%;
        }

        .hide-on-mobile {
            /*display: inline-block;*/
            display: none;
        }
    }
</style>
</html>'''
    return s

# msg = mido.Message('note_off', note=60, channel=1)
# msg = mido.Message('note_off', note=60, channel=0)
# msg = mido.Message('note_off', note=60, channel=2)
# outport.send(msg)

@app.route("/")
def Index():
    load_config()
    return Response(create_html(load_config()).encode('ascii', 'xmlcharrefreplace'))

@app.route('/api/<string:category>/<string:scene>')
def Scene(category, scene):
    config = load_config()
    channel = config['CueGroups'][category][scene]["Channel"] - 1
    note = config['CueGroups'][category][scene]["NoteFrom"]
    trigger_lights(channel, note)
    atem_ip = config['AtemIP']
    camera = config["ATEMCameras"][config['CueGroups'][category][scene]["Live"]]
    key = config['CueGroups'][category][scene]["Key"] - 1
    trigger_camera(atem_ip, camera, key)
    return success()


def success():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


def trigger_lights(channel, note):
    outport.send(mido.Message('note_on', note=note, channel=channel))
    outport.send(mido.Message('note_off', note=note, channel=channel))


def trigger_camera(atem_ip, camera, key):
    success = execute_js('atem.js', str(atem_ip) + " " + str(camera) + " " + str(key))


if __name__ == '__main__':
    app.run()