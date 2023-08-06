# Introduction

A library that makes development of Python Minecraft Bedrock Edition websocket applications easier.

# Install

```bash
pip install fcwslib
```

# Demo

```python
import fcwslib


class Plugin(fcwslib.Plugin):
    async def on_connect(self):
        print('Connected')
        await self.send_command('list', callback=self.list)
        await self.subscribe('PlayerMessage', callback=self.player_message)

    async def on_disconnect(self):
        print('Disconnected')

    async def on_receive(self, response):
        print('Receive other response {}'.format(response))

    async def list(self, response):
        print('Receive command response {}'.format(response))

    async def player_message(self, response):
        print('Receive event response {}'.format(response))


server = fcwslib.Server()
server.add_plugin(Plugin)
server.run_forever()
```