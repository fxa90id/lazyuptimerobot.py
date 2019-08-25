# lazyuptimerobot.py 

UptimeRobot API Python integration with docs.

```python
from lazyuptimerobot import UptimeRobot
monitor = UptimeRobot(api_key="YOUR_API_KEY")
help(monitor)
...
print(monitor.getMonitors())
print(monitor.newAlertContact(type=2, value="email@email", friendly_name="John"))
...
```
