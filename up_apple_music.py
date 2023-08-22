#!/usr/bin/env python3

'''
up_spotify

Unofficial input and output plugin for Apple Music. Can access a user's public or private playlists, and read songs from, or save songs to them.
Will not overwrite songs already in a playlist, so stuff like date added are kept accurate.

Gavin Edens, Luke Simmons, 2023
'''

from app import _ultrasonics
from ultrasonics import logs
from ultrasonics.tools import api_key, fuzzymatch, name_filter

log = logs.create_log(__name__)

handshake = {
    "name": "apple_music",
    "description": "Sync your playlists to and from Apple Music",
    "type": ["inputs", "outputs"],
    "mode": ["playlists"],
    "version": "0.1.0",
    "settings": [
        {"type": "auth", "label": "Authorize Apple Music",
            "path": "/spotify/auth/request"},
        {
            "type": "string",
            "value": "Songs will always attempt to be matched using fixed values like ISRC or Apple Music URI, however if you're trying to sync music without these tags, fuzzy matching will be used instead.",  # TODO: Check
        },
        {
            "type": "string",
            "value": "This means that the titles 'You & Me - Flume Remix', and 'You & Me (Flume Remix)' will probably qualify as the same song [with a fuzzy score of 96.85 if all other fields are identical]. However, 'You, Me, & the Log Flume Ride' probably won't 🎢 [the score was 88.45 assuming *all* other fields are identical]. The fuzzyness of this matching is determined with the below setting. A value of 100 means all song fields must be identical to pass as duplicates. A value of 0 means any song will quality as a match, even if they are completely different. 👽",
        },
        {
            "type": "text",
            "label": "Default Global Fuzzy Ratio",
            "name": "fuzzy_ratio",
            "value": "Recommended: 90",
        },
        {
            "type": "string",
            "value": "If you sync a playlist to Apple Music which doesn't already exist, ultrasonics will create a new playlist for you automatically ✨. Would you like any new playlists to be public or private?",
        },
        {
            "type": "radio",
            "label": "Created Playlists",
            "name": "created_playlists",
            "id": "created_playlists",
            "options": ["Public", "Private"],
        },
    ],
}


def run(settings_dict, **kwargs):
    '''
    Runs the up_apple_music plugin.
    '''

    database = kwargs["database"]
    global_settings = kwargs["global_settings"]
    component = kwargs["component"]
    applet_id = kwargs["applet_id"]
    songs_dict = kwargs["songs_dict"]


def builder(**kwargs):
    '''
    Builds the settings page for the up_apple_music plugin.
    '''
    component = kwargs["component"]

    if component == "inputs":
        settings_dict = [
            '''
            <div class="field">
                <label class="label">Input</label>
                <div class="control">
                    <input class="is-checkradio" type="radio" name="mode" id="playlists" value="playlists" checked=true>
                    <label for="playlists">Playlists</label>

                    <input class="is-checkradio" type="radio" name="mode" id="saved" value="saved">
                    <label for="saved">Saved Songs</label>
                </div>
            </div>

            <div class="shy-elements field">
                <div class="field shy playlists-only">
                    <label class="label">You can use regex style filters to only select certain playlists. For example,
                        'disco' would sync playlists 'Disco 2010' and 'nu_disco', or '2020$' would only sync playlists which
                        ended with the value '2020'.</label>
                </div>

                <div class="field shy playlists-only">
                    <label class="label">Leave it blank to sync everything 🤓.</label>
                </div>

                <div class="field shy playlists-only">
                    <label class="label">Filter</label>
                    <div class="control">
                        <input class="input" type="text" name="filter" placeholder="">
                    </div>
                </div>

                <div class="field shy saved-only">
                    <label class="label">Saved Songs mode will only save newly added songs. This is designed for output
                        plugins which append tracks, as opposed to overwrite existing playlist songs.</label>
                </div>

                <div class="field shy saved-only">
                    <label class="label">
                        ⚠️ The playlist will only contain songs you've saved since the last run of this applet.
                    </label>
                </div>

                <div class="field shy saved-only">
                    <label class="label">
                        This plugin will pass the songs in playlist form. What would you like this playlist to be
                        called?</label>
                </div>

                <div class="field shy saved-only">
                    <label class="label">Playlist Title</label>
                    <div class="control">
                        <input class="input" type="text" name="playlist_title" placeholder="Spotify Saved Songs">
                    </div>
                </div>

            </div>

            <script type="text/javascript">

                radios = document.querySelectorAll(".control input.is-checkradio")

                for (i = 0; i < radios.length; i++) {
                    radios[i].addEventListener("change", updateInputs)
                }

                updateInputs()

                function updateInputs() {
                    shyElements = document.querySelectorAll(".shy-elements .shy")
                    for (i = 0; i < radios.length; i++) {
                        if (radios[i].checked) {
                            selected = radios[i].value;
                        }
                    }

                    var unhide

                    switch (selected) {
                        case "playlists":
                            unhide = document.querySelectorAll(
                                ".shy-elements .shy.playlists-only")
                            break
                        case "saved":
                            unhide = document.querySelectorAll(
                                ".shy-elements .shy.saved-only")
                            break
                    }

                    for (j = 0; j < shyElements.length; j++) {
                        shyElements[j].style.display = "none"
                    }
                    for (k = 0; k < unhide.length; k++) {
                        unhide[k].style.display = "block"
                    }
                }

            </script>
            '''
        ]

        return settings_dict

    else:
        settings_dict = [
            {
                "type": "string",
                "value": "Do you want to update any existing playlists with the same name (replace any songs already in the playlist), or append to them?",
            },
            {
                "type": "radio",
                "label": "Existing Playlists",
                "name": "existing_playlists",
                "id": "existing_playlists",
                "options": ["Append", "Update"],
                "required": True,
            },
        ]

        return settings_dict


def test(database, **kwargs):
    '''
    Tests the up_apple_music settings when entered by the user.
    '''
    pass
