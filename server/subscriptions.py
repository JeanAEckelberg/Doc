import os
import json
import random

import youtube_utils as yt
import amixer_control as mixer


def search(client, req):
    params = [ "query" ]
    if not valid_params(params, req, client):
        return False

    yt_response = yt.search(req["details"]["query"])

    client.sendTarget(req["id"]["query"], {"key":"get.search", "payload": yt_response})

    return True


def toggle_play_pause(client, req):
    client.setState("playing", not client.getState("playing"))

    if client.getState("playing"):
        print("Resumed playback")
    else:
        print("Paused playback")

    return True


def get_play_pause(client, req):
    client.sendTarget(req["id"], payload={
        "key": "get.play_pause",
        "payload": {"playing": client.getState("playing") }
    })

    return True

def add_queue(client, req):

    params = [
        "id"
        "query"
    ]

    if not valid_params(params, req, client):
        return False

    # validate we don't already have this video
    q = client.getState("queue")

    for v in q:
        if req["details"]["id"] == v["id"]:
            return False

    # get full video details
    video = yt.get_video(req["details"]["id"]["query"])

    if not video:
        pass # TODO implement exception

    # flag video as not autoqueued
    video["auto_queued"] = False

    q.append(video)
    client.setState("queue", q)

    #client.send(key="get.queue", type="broadcast", payload={"payload": q})

    return True

def get_queue(client, req):
    client.sendTarget(req["id"], {"key":"get.queue", "payload": client.getState("queue")})

    return True

def remove_queue(client, req):
    client.setState("queue", [])
    print("Clearning Queue")
    return True

def shuffle_queue(client, req):
    print("Hello!")
    queue = client.getState("queue")
    random.shuffle(queue)
    if len(queue) > 0:
        client.setState("queue", queue)
    client.factory.sendAll({
        "key":"get.queue", 
        "payload": queue
    })
    print("Shuffling Queue")
    return True

def get_current_song(client, req):
    client.sendTarget(req["id"], {"key": "get.current_song", "payload": client.getState("current_song")})

    return True

def set_skip(client, req):
    print("Skipping Song")
    client.setState("current_song", None)
    client.setState("playback_timer", None)

    return True

def toggle_magic_mode(client, req):
    client.setState("magic_mode", not client.getState("magic_mode"))

    if client.getState("magic_mode"):
        print("Enabled Magic Mode")
    else:
        print("Disabled Magic Mode")

    return True


def get_magic_mode(client, req):
    client.sendTarget(req["id"],  payload={
        "key": "get.magic_mode",
        "payload": {"magic_mode": client.getState("magic_mode") }
    })

    return True

def remove_history(client, req):

    client.setState("history", [])
    client.setState("magic_mode_history", [])

    print("Clearing History")

    return True

def get_duration_limit(client, req):
    client.sendTarget(req["id"], payload={
        "key": "get.duration_limit",
        "payload": {"duration_limit": client.getState("duration_limit") }
    })

    return True

def toggle_duration_limit(client, req):
    client.setState("duration_limit", not client.getState("duration_limit"))

    if client.getState("duration_limit"):
        print("Enabled Duration Limit")
    else:
        print("Disabled Duration Limit")

    return True

def get_volume(client, req):
    volume = mixer.get_volume()
    client.sendTarget(req["id"], payload={
        "key": "get.volume",
        "payload": {"volume": volume }
    })

    return True

def set_volume(client, req):
    params = [ "volume" ]
    if not valid_params(params, req, client):
        return False

    mixer.set_volume(req["details"]["volume"])

    return True

def get_history(client,req):
    client.sendTarget(req["id"],  payload={
        "key": "get.history",
        "payload": client.getState("history")
    })


def get_listener_count(client, req):
    client.sendTarget(req["id"],  payload={
        "key": "get.listener_count",
        "payload": client.getState("clients")
    })




## Helpers

def valid_params(params, req, client):
    for p in params:
        if p not in req["details"]:
            client.sendTarget(
                req["id"],
                {"key": req["key"], "msg": "Request details missing \"%s\"" % p})
            return False
    return True


##########################
# Handlers               #
##########################

handlers = {
    "get.search": [search],

    "toggle.play_pause": [toggle_play_pause],
    "get.play_pause": [get_play_pause],

    "add.queue": [add_queue],
    "get.queue": [get_queue],
    "remove.queue": [remove_queue],
    "shuffle.queue": [shuffle_queue],

    "get.current_song": [get_current_song],

    "set.skip": [set_skip],

    "toggle.magic_mode": [toggle_magic_mode],
    "get.magic_mode": [get_magic_mode],

    "remove.history": [remove_history],

    "get.duration_limit": [get_duration_limit],
    "toggle.duration_limit": [toggle_duration_limit],

    "set.volume": [set_volume],
    "get.volume": [get_volume],

    "get.history": [get_history],

    "get.listener_count": [get_listener_count],

}
