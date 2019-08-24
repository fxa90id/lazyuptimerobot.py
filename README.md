# lazyuptimerobot.py 
Super lazy python integration with uptimerobot.com 

```python
from lazyuptimerobot import LazyUptimeRobot
monitor = LazyUptimeRobot(api_key="YOUR_API_KEY")
print(monitor.getMonitors())
print(monitor.newAlertContact(type=2, value="email@email", friendly_name="John"))
```