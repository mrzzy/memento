#
# Memento
# Pi
# Jack in a box
# 

import json
import asyncio
import argparse
import websockets

from dateutil.parser import parse as parse_datetime

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
    args = parser.parse_args()

    return {
        "api_host":  args.api_host,
        "channel_id": args.channel_id
    }

async def subscribe_channel(api_host, channel_id=None):
    # build subscribe url
    subscribe_url = f"ws://{api_host}/api/v0/notification/subscribe"
    if not channel_id is None:
        subscribe_url += f"?channel={channel_id}"
    # listen for notifications
    async with websockets.connect(subscribe_url) as socket:
        print(f"listening for notifications on channel {channel_id}")
        while socket.open:
            notify_json = await socket.recv()
            notify = json.loads(notify_json)
            print(f"recieved notification {notify['title']}")

async def main():
    options = parse_options()
    await subscribe_channel(options["api_host"], options["channel_id"])

# setup async event loop
event_loop = asyncio.get_event_loop().run_until_complete(main())
