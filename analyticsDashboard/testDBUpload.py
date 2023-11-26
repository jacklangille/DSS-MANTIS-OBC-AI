import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import random

bucket = "testing"
org = "3e8389e311b2b4b3"
token = "3JT52YWz84HbwumkdttgvpjoDLPk9LdzN5WMuJ3S_fh29UUyg9KF-PXmKkBS-ZDU0FAhl_dzm5W0RKOLpBD50Q=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)


query_api = client.query_api()

def addNewPoint(systemName:str, keyName: str, value: any):
	point = influxdb_client.Point(systemName).field(keyName, value)
	write_api.write(bucket=bucket, org=org, record=point)

def getPoint(systemName:str, keyName: str):
	query = 'from(bucket:"testing")\
	|> range(start: -10m)\
	|> filter(fn:(r) => r._measurement == "' + systemName + '")\
	|> filter(fn:(r) => r._field == "' + keyName + '")'

	result = query_api.query(org=org, query=query)

	results = []
	for table in result:
		for record in table.records:
			results.append((record.get_field(), record.get_value()))

	return results

############################
## ADD NEW DATA EXAMPLES ##
############################

## Power Draw
addNewPoint("powerDraw", "value", random.randint(60, 80))

## Inference status (check the progress and success rate of image processing tasks)
addNewPoint("inferenceStatus", "progress", random.randint(40, 90))
addNewPoint("inferenceStatus", "successRate", random.randint(60, 80))

## Database capacity. We will have two databases (one is a buffer for input and one is a buffer for output)
addNewPoint("databaseCapacity", "inputBuffer", random.randint(0, 100))
addNewPoint("databaseCapacity", "outputBuffer", random.randint(0, 100))

## Thermal status
addNewPoint("thermalStatus", "temperature", random.randint(20, 60))

## CPU/GPU usage
addNewPoint("cpuUsage", "cpu", random.randint(20, 100))
addNewPoint("gpuUsage", "gpu", random.randint(20, 100))

## Memory usage
addNewPoint("memoryUsage", "memory", random.randint(10, 100))

## Network status - report status of comm. link
addNewPoint("networkStatus", "status", "OK")
addNewPoint("networkStatus", "status", "SOME_ERROR")

## Error log/alerts
addNewPoint("errorLog", "error", "SOME_ERROR")

## Task queue/workflow status
addNewPoint("taskQueue", "task_name", "task_value")
addNewPoint("taskQueue", "some_other_task_name", "task_value")

############################
## QUERY DATA EXAMPLES ##
############################

## Power Draw
print(getPoint("powerDraw", "value"))

## Inference status (check the progress and success rate of image processing tasks)
print(getPoint("inferenceStatus", "progress"))

## Database capacity. We will have two databases (one is a buffer for input and one is a buffer for output)
print(getPoint("databaseCapacity", "inputBuffer"))
print(getPoint("databaseCapacity", "outputBuffer"))

## Thermal status
print(getPoint("thermalStatus", "temperature"))

## CPU/GPU usage
print(getPoint("cpuUsage", "cpu"))
print(getPoint("gpuUsage", "gpu"))

## Memory usage
print(getPoint("memoryUsage", "memory"))

## Network status - report status of comm. link
print(getPoint("networkStatus", "status"))

## Error log/alerts
print(getPoint("errorLog", "error"))

## Task queue/workflow status
print(getPoint("taskQueue", "task_name"))
print(getPoint("taskQueue", "some_other_task_name"))