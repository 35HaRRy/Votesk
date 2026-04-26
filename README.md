# Votesk

## Overview
A Python-based voice-command and Kodi control utility.
It combines speech-to-text input with a dispatcher layer that sends commands to Kodi and related helpers.

## Dependencies
- Python 2.x or a compatible legacy Python runtime
- Modules referenced by the project files such as `SpeechToText`, `Dispatcher`, and `Kodi`
- A Kodi instance reachable from the configured endpoint

## Setup
1. Review `Config.py` and update the Kodi endpoint and command settings.
2. Make sure the companion Python modules are available in the same project directory.
3. Prepare your speech-to-text backend or microphone input setup.

## Run
- Start the tool with `python Votesk.py`.
- Pass `-t` and `-m` arguments if you want to trigger a specific task directly.

## Notes
This is a legacy script-style project, so it is best run in the environment it was originally developed for.