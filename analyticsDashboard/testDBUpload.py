import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "testing"
org = "3e8389e311b2b4b3"
token = "3JT52YWz84HbwumkdttgvpjoDLPk9LdzN5WMuJ3S_fh29UUyg9KF-PXmKkBS-ZDU0FAhl_dzm5W0RKOLpBD50Q=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)

point = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 26.3)
write_api.write(bucket=bucket, org=org, record=point)

# query_api = client.query_api()

query = 'from(bucket:"testing")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == "my_measurement")\
|> filter(fn:(r) => r.location == "Prague")\
|> filter(fn:(r) => r._field == "temperature")'

# result = query_api.query(org=org, query=query)

# results = []
# for table in result:
#     for record in table.records:
#         results.append((record.get_field(), record.get_value()))

# print(results)
