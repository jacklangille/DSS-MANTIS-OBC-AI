from AnalyticsService import AnalyticsService

bucket = "testing"
org = "3e8389e311b2b4b3"
token = "3JT52YWz84HbwumkdttgvpjoDLPk9LdzN5WMuJ3S_fh29UUyg9KF-PXmKkBS-ZDU0FAhl_dzm5W0RKOLpBD50Q=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

TEST_JSON_PATH = "analyticsDashboard/SampleJSONPayloads/Payload1.json"

analyticsService = AnalyticsService(bucket, org, token, url)

analyticsService.parseJson(TEST_JSON_PATH)