
# Air Alerts

Air Alerts is a module for monitorining Air Raid Alerts in Ukraine.
The module uses a complete map of alerts that provides incredibly accurate information.

# WARNING
Module was tested only on Python 3.9 with Windows 10. With other versions of python or on other operating system module may be broken.

# Requirements

This module is lightweight and not need many libraries. You need only 2!

- Requests
- Pillow

All of needed libraries will be automaticly installed on your computer
while you installing Air Alerts

# Updates in new version
- Added two versions: Async and Sync

# Usage

## Sync

#### Getting real-time information dictionary
```python
import AirAlerts

alerts = AirAlerts.AlertClass()
real_time_alerts = alerts.get_alerts()

print(real_time_alerts)
```
This code will return an dictionary of alerts. It will look like this:
```json
{
    "kyiv": False,
    "chernivtsi_region": False,
    "ivano-frankivsk_region": False,
    "volyn_region": False,
    "zakarpattia_region": False,
    "zaporizhia_region": False,
    "zhytomyr_region": False,
    "kirovohrad_region": False,
    "kyiv_region": False,
    "luhansk_region": False,
    "lviv_region": False,
    "mykolaiv_region": False,
    "odesa_region": False,
    "poltava_region": False,
    "rivne_region": False,
    "sumy_region": False,
    "ternopil_region": False,
    "kharkiv_region": False,
    "kherson_region": False,
    "khmelnytskyi_region": False,
    "chernihiv_region": False,
    "cherkasy_region" : False,
    "donetsk_region" : False
    "vinnytsia_region" : False
    "dnipropetrovsk_region" : False
}
```

#### Getting air alerts in list
```python
import AirAlerts

alerts = AirAlerts.AlertClass()
alerts_list = alerts.alerts_list()

print(alerts_list)
```
This code will return a list of alerts that will look like this:
['kyiv','kyiv_region','luhansk_region']

##Async

#### Getting real-time information dictionary
```python
import asyncio
from AirAlerts.Async import AsyncAlertClass

async def main():
    alerts = AsyncAlertClass()
    real_time_alerts = await alerts.get_alerts()
    print(real_time_alerts)
await main()
```
This code will return a dictionary of alerts as i mentioned in Sync version

#### Getting air alerts in list

```python
import asyncio
from AirAlerts.Async import AsyncAlertClass

async def main():
    alerts = AsyncAlertClass()
    alerts_list = await alerts.alerts_list()
    print(alerts_list)
await main()
```
### Thanks everybody who is supporting this project. I appreciate it! Thanks to Ukrainian Army and all Ukrainian, Polish, Romanian, American, Israel and much much more people for helping Ukraine
### Ukraine is very grateful for your help. And we wish one day that all ends

### If you have any questions don't be shy, contact me on Discord Romikan#5428

# License

MIT License

Copyright (c)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

