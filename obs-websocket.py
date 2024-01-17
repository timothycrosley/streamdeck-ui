#!/usr/bin/env python3

# TODO integrate this into streamdeck-ui for the best expirience

import argparse
import obsws_python as obs

parser = argparse.ArgumentParser()
parser.add_argument('--scene', type=str)
parser.add_argument('--recstop', action='store_true')
args = parser.parse_args()

cl = obs.ReqClient(host='localhost', port=4455, password='mystrongpass' , timeout=3)

def set_scene(scene_name):
    cl.set_current_program_scene(scene_name)

def toggle_recording():
    if cl.get_output_list().outputs[0]['outputActive']:
        cl.stop_output('simple_file_output')
    else:
        cl.start_output('simple_file_output')

if __name__ == "__main__":
    if args.scene is not None:
        set_scene(args.scene)
    if args.recstop:
        toggle_recording()
