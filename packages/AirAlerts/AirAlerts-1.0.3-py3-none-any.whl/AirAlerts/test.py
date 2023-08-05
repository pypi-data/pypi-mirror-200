import asyncio
from AirAlerts.Async import AsyncAlertClass

async def main():
	alerts = AirAlerts.AsyncAlertClass()
	real_time_alerts = alerts.get_alerts()
	print(real_time_alerts)
asyncio.run(main())