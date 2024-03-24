import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import datetime


class AnalyticsService:
    def __init__(self, bucket, org, token, url):
        self.__bucket = bucket
        self.__org = org
        self.__client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self.__write_api = self.__client.write_api(write_options=SYNCHRONOUS)
        self.__query_api = self.__client.query_api()

    def recordPoint(self, systemName: str, keyName: str, value: any, time: int = None):
        try:
            point = influxdb_client.Point(systemName).field(keyName, value)

            if time:
                dt_object = datetime.datetime.fromtimestamp(time)
                formatted_datetime = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                point = point.time(time=formatted_datetime)

            self.__write_api.write(bucket=self.__bucket, org=self.__org, record=point)
        except Exception as e:
            print(f"Error while recording point: {e}")

    def getPoint(self, systemName: str, keyName: str, timeRange: str = "-10m"):
        try:
            query = f'from(bucket:"testing")\
        |> range(start: {timeRange})\
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

    def parseJson(self, filePath: str):
        try:
            with open(filePath, "r") as file:
                # Load the JSON data into a Python dictionary
                data = json.load(file)

            logs = data.get("Logs")
            SDCardFillPercent = data.get("SDCardFillPercent")
            sBandTransmissions = data.get("SBandTransmissions")
            power = data.get("Power")
            temperature = data.get("Temperature")

            if logs:
                print("Logging logs " + str(logs))
                for log in logs:
                    timeStamp = log.get("timeStamp")
                    logId = log.get("logId")

                    self.recordPoint("logs", "log", logId, timeStamp)

            if SDCardFillPercent:
                print("Logging SDCardFillPercent " + str(SDCardFillPercent))
                for percent in SDCardFillPercent:
                    timeStamp = percent.get("timeStamp")
                    percentValue = percent.get("percent")

                    self.recordPoint(
                        "SDCardFillPercent", "percent", percentValue, timeStamp
                    )

            if sBandTransmissions:
                print("Logging sBandTransmissions " + str(sBandTransmissions))
                for transmission in sBandTransmissions:
                    timeStamp = transmission.get("timeStamp")
                    statusId = transmission.get("statusId")

                    self.recordPoint(
                        "sBandTransmissions", "status", statusId, timeStamp
                    )

            if power:
                print("Logging power " + str(power))
                for info in power:
                    timeStamp = info.get("timeStamp")
                    systemName = info.get("systemName")
                    powerUse = info.get("powerUse")

                    self.recordPoint("power", systemName, powerUse, timeStamp)

            if temperature:
                print("Logging temperature " + str(temperature))
                for temp in temperature:
                    timeStamp = temp.get("timeStamp")
                    systemName = temp.get("systemName")
                    tempValue = temp.get("temperature")

                    self.recordPoint(
                        "systemTemperature", systemName, tempValue, timeStamp
                    )

        except FileNotFoundError:
            print(f"Error: File '{filePath}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Unable to parse JSON file '{filePath}'.")
        except Exception as e:
            print(f"Error while parsing JSON and recording points: {e}")
