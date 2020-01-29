#
# Memento
# Pi
# Jack in a box
# 

import time
import json
import asyncio
import argparse
import websockets

from datetime import datetime,timedelta
from dateutil.parser import parse as parse_datetim
from display import displaymsg

FAILURE_THRESHOLD = 3

# parse command line arguments
# returns command line args as options dict
def parse_options():
    parser = argparse.ArgumentParser(
        description="Memento Raspberry Pi - Jack in the box client")
    parser.add_argument("--api-host", dest="api_host",
                        help="ip/dns name of the api endpoint host",
                        default="memento.mrzzy.co")
    parser.add_argument("--channel", dest="channel_id", type=int,
                        help="id of the channel to listen for notifications",
                        default=None)
    parser.add_argument("--secure",  dest="is_secure", type=bool, nargs="?",
                        const=True,
                        help="Whether to use secure websockets", default=False)
    args = parser.parse_args()

    return {
        "api_host":  args.api_host,
        "channel_id": args.channel_id,
        "is_secure": args.is_secure
    }

async def subscribe_channel(api_host, channel_id, is_secure):
    # build subscribe url
    protocol = "wss" if is_secure else "ws"
    subscribe_url = f"{protocol}://{api_host}/api/v1/notification/subscribe"
    if not channel_id is None:
        subscribe_url += f"?channel={channel_id}"

    # track failure times to determine if connection
    # dropping is due to inability connect or timeout
    n_failure = 0
    while n_failure < FAILURE_THRESHOLD:
        # try to connect to the backend
        try:
            socket = await websockets.client.connect(subscribe_url, ping_interval=None)

            # connected to backend - listening for notifications
            time_since_failure = timedelta(seconds=0)
            if channel_id  is None:
                print("listening for notifications on all channels")
            else:
                print(f"listening for notifications on channel {channel_id}")

            while socket.open:
                # read notifications from serve
                notify_json = await socket.recv()
                notify = json.loads(notify_json)
                print(f"recieved notification {notify['title']}")
                print(f"recieved notification {notify['title']}")
                displaymsg()

                # reset failure counter
                n_failure = 0

        except Exception as e:
            n_failure += 1
            print(f"failure {n_failure}: could not not connect.")
            time.sleep(1)

    if n_failure >= 3: print("could not connect: giving up.")

async def main():
    options = parse_options()
    await subscribe_channel(options["api_host"],
                            options["channel_id"],
                            options["is_secure"])

# setup async event loop
event_loop = asyncio.get_event_loop().run_until_complete(main())
