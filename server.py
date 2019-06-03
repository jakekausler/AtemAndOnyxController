
from __future__ import print_function
import sys
import mido
import yaml
import re
import json
import time
from flask import Flask, send_file, Response, render_template
from Naked.toolshed.shell import execute_js


app = Flask(__name__)

def load_config(f="config.yaml"):
    with open(f, 'r', encoding='utf8') as stream:
        config = yaml.safe_load(stream)
        return config

outport = mido.open_output(load_config()['MidiPort'])

def format_url_name(s):
    return re.sub(r"[^\w']+", "", s.lower(), flags = re.UNICODE)

@app.route("/")
def Index():
    # return Response(create_html(load_config()).encode('ascii', 'xmlcharrefreplace'))
    config = load_config()
    return render_template('client.html', host=config['ServerHost'], port=config['ServerPort'], CueGroups=config['CueGroups'])

@app.route('/api/<string:category>/<string:scene>')
def Scene(category, scene):
    print(f"Loading Scene: {scene}")
    config = load_config()
    channel = config['CueGroups'][category][scene]["Channel"] - 1
    note = config['CueGroups'][category][scene]["NoteFrom"]
    trigger_lights(channel, note)
    atem_ip = config['AtemIP']
    camera = config["AtemCameras"][config['CueGroups'][category][scene]["Live"]]
    key = config['CueGroups'][category][scene]["Key"] - 1
    print(f"Triggering camera: {camera} with key:{key} @ ip: {atem_ip}")
    trigger_camera(atem_ip, camera, key)
    return success() #Not returning?


def success():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


def trigger_lights(channel, note):
    outport.send(mido.Message('note_on', note=note, channel=channel))
    outport.send(mido.Message('note_off', note=note, channel=channel))


def trigger_camera(atem_ip, camera, key):
    success = execute_js('atem.js', str(atem_ip) + " " + str(camera) + " " + str(key))


if __name__ == '__main__':
    app.run(port=load_config()['ServerPort'])