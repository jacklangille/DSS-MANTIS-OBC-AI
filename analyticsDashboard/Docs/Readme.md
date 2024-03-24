# Analytics Dashboard

Info here...

# Relevant Links
- [Grafana Dashboard](https://dsstesting.grafana.net/d/c56d74c9-74d1-4ce4-935c-6791fa3e3cad/dss-testing?orgId=1&from=now-7d&to=now&src=hg_notification_free)
- [InfluxDB Cloud Database](https://us-east-1-1.aws.cloud2.influxdata.com/orgs/3e8389e311b2b4b3/data-explorer?fluxScriptEditor)
  
## Data that we track

| DataName           | Parameters                                                         | Notes   |
| ------------------ | ------------------------------------------------------------------ | ------- |
| Logs               | {{timeStamp: number, logId: number}}                               |         |
| SDCardFillPercent  | {{timeStamp: number, percent: number}}                             |         |
| SBandTransmissions | {{timeStamp: number, statusId: number, gps-coordinates: string}}   |         |
| Power              | {{timeStamp: number, systemName: string, powerUse: number}}        | Volts   |
| Temperature        | {{timeStamp: number, systemName: string, powerUseInWatts: number}} | Celsius |

### Important Notes
- Strings must not have any special characters, including spaces. Use camelCase or underscores.
- Timestamps are in Unix time.

### Example JSON Structure

```json
{
	"Logs": [
		{
			"timeStamp": 1711289050,
			"logId": 1
		},
		{
			"timeStamp": 1711289049,
			"logId": 2
		}
	],
	"SDCardFillPercent": [
		{
			"timeStamp": 1711289050,
			"percent": 50
		},
		{
			"timeStamp": 1711289049,
			"percent": 51
		}
	],
	"SBandTransmissions": [
		{
			"timeStamp": 1711289050,
			"gps-coordinates": "41°24'12.2\"N 2°10'26.5\"E",
			"statusId": 1
		},
		{
			"timeStamp": 1711289049,
			"gps-coordinates": "41°24'12.2\"N 2°10'26.5\"E",
			"statusId": 2
		}
	],
	"Power": [
		{
			"timeStamp": 1711287050,
			"systemName": "System1",
			"powerUse": 50
		},
		{
			"timeStamp": 1711289049,
			"systemName": "System1",
			"powerUse": 60
		},
		{
			"timeStamp": 1711285050,
			"systemName": "System2",
			"powerUse": 50
		},
		{
			"timeStamp": 1711288049,
			"systemName": "System2",
			"powerUse": 60
		}
	],
	"Temperature": [
		{
			"timeStamp": 1711287050,
			"systemName": "System1",
			"temperature": 50
		},
		{
			"timeStamp": 1711289049,
			"systemName": "System1",
			"temperature": 60
		},
		{
			"timeStamp": 1711285050,
			"systemName": "System2",
			"temperature": 50
		},
		{
			"timeStamp": 1711288049,
			"systemName": "System2",
			"temperature": 60
		}
	]
}
```