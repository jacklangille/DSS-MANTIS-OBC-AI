import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import json


class AnalyticsService:
    def __init__(self, bucket, org, token, url):
        self.__bucket = bucket
        self.__org = org
        self.__token = token
        self.__url = url
        self.__client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self.__write_api = self.__client.write_api(write_options=SYNCHRONOUS)
        self.__query_api = self.__client.query_api()

    def recordPoint(self, systemName: str, keyName: str, value: any):
        try:
            point = influxdb_client.Point(systemName).field(keyName, value)
            self.__write_api.write(bucket=self.__bucket, org=self.__org, record=point)
        except Exception as e:
            print(f"Error while recording point: {e}")

    def getPoint(self, systemName: str, keyName: str):
        try:
            query = f'from(bucket:"testing")\
        |> range(start: -10m)\
        |> filter(fn:(r) => r._measurement == "{systemName}")\
        |> filter(fn:(r) => r._field == "{keyName}")'

            result = self.__query_api.query(org=self.__org, query=query)

            results = []
            for table in result:
                for record in table.records:
                    results.append((record.get_field(), record.get_value()))

            return results
        except Exception as e:
            print(f"Error while getting point: {e}")
            return []

    def parseJson(self, filePath):
        try:
            with open("analyticsDashboard/testData.json", "r") as file:
                # Load the JSON data into a Python dictionary
                data = json.load(file)

            # Now you can work with the 'data' dictionary
            powerDraw = data.get("powerDraw")
            databaseInput = data.get("databaseInput")
            databaseOutput = data.get("databaseOutput")
            thermalTemp = data.get("thermalTemp")

            if powerDraw:
                self.recordPoint("powerDraw", "value", powerDraw)

            if databaseInput:
                self.recordPoint("databaseCapacity", "inputBuffer", databaseInput)

            if databaseOutput:
                self.recordPoint("databaseCapacity", "outputBuffer", databaseOutput)

            if thermalTemp:
                self.recordPoint("thermalStatus", "temperature", thermalTemp)
        except FileNotFoundError:
            print(f"Error: File '{filePath}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Unable to parse JSON file '{filePath}'.")
        except Exception as e:
            print(f"Error while parsing JSON and recording points: {e}")
