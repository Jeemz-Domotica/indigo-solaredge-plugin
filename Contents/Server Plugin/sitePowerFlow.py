import sys

import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import numpy as np


import datetime
# MY_API_HOST = 'https://monitoringapi.solaredge.com/'
# apikey = "MGB6NFG5T080XM7UFKK6VMEJLH9VGYOF"

# endpoint = 'site/149132/currentPowerFlow?api_key=' + apikey
# response = requests.get(MY_API_HOST + endpoint)
# print(MY_API_HOST + endpoint)
# print(response)
# print(response.content)

# siteId = '149132'
# endpoint = 'equipment/' + str(siteId) + '/list?api_key=' + apikey
# endpoint = 'https://monitoringapi.solaredge.com/equipment/149132/7E19C580-DC/data?startTime=2023-04-06%2015:09:18&endTime=2023-04-07%2015:09:18&api_key=MGB6NFG5T080XM7UFKK6VMEJLH9VGYOF'
print(sys.argv)
endpoint = sys.argv[1]
response = requests.get(endpoint)
data = response.json()
print(data)
newData = data["data"]["telemetries"]
powers = []
dates = []
voltages = []
temperatures = []
energies = []
for telemetry in newData:
    date = telemetry.get("date")

    totalActivePower = telemetry.get("totalActivePower")
    powers.append(float(totalActivePower))
    dates.append(date)

    dcVoltage = telemetry.get("dcVoltage")
    voltages.append(dcVoltage)

    totalEnergy = format(telemetry.get("totalEnergy"), '.2f')
    energies.append(totalEnergy)
    temperature = telemetry.get("temperature")
    temperatures.append(temperature)

fig, ax = plt.subplots(4)
ax[0].plot(dates, powers)
ax[0].set_xticks([ax[0].get_xticks()[0], ax[0].get_xticks()[-1]])
ax[0].set_ylabel('totalActivePower')
ax[1].plot(dates, voltages)
ax[1].set_xticks([ax[1].get_xticks()[0], ax[1].get_xticks()[-1]])
ax[1].set_ylabel('dcVoltage')
ax[2].plot(dates, energies)
ax[2].set_xticks([ax[2].get_xticks()[0], ax[2].get_xticks()[-1]])
ax[2].set_yticks([ax[2].get_yticks()[0], ax[2].get_yticks()[-1]])
ax[2].set_ylabel('totalEnergy')
ax[3].plot(dates, temperatures)
ax[3].set_ylabel('Temperature')
ax[3].set_xticks([ax[3].get_xticks()[0], ax[3].get_xticks()[-1]])
fig.tight_layout()
pwd = os.path.join("Library", "Application Support", "Perceptive Automation", "Indigo 2022.2", "Web Assets", "images")
print(os.getcwd())
os.chdir('..')
os.chdir('..')
os.chdir('..')
os.chdir('..')
print(os.getcwd())
os.chdir('Web Assets')
print(os.getcwd())
os.chdir('images')
print(os.getcwd())
os.chdir('controls')
os.chdir('static')
print(os.getcwd())
plt.savefig(os.path.join(os.getcwd(), "power.png"))

# apikey = 'L4MS1MBRYS04PRSC8VI75R3MRT4E4XQX'
# inverter = self.get_device(int(inverter_serialNumber))
# siteId = '548411'
# timeUnit = action.props.get('timeUnit')
# time = action.props.get('time')
# now = datetime.datetime.now()
# endTime = now.strftime("%Y-%m-%d%%20%H:%M:%S")
# if timeUnit or time == None:
#     startTime = now - datetime.timedelta(weeks=1)
# else:
#     if timeUnit == 'MINUTES':
#         startTime = now - datetime.timedelta(minutes=time)
#     elif timeUnit == 'HOUR':
#         startTime = now - datetime.timedelta(hours=time)
#     elif timeUnit == 'DAY':
#         if time <= 7:
#             startTime = now - datetime.timedelta(days=time)
#         else:
#             startTime = now - datetime.timedelta(days=7)
# startTime = startTime.strftime("%Y-%m-%d%%20%H:%M:%S")
# endpoint = 'equipment/' + siteId + '/' + inverter_serialNumber + '/data?startTime=' + startTime + '&endTime=' + endTime + '&api_key=' + apikey
# indigo.server.log(str(MY_API_HOST + endpoint))
# response = requests.get(MY_API_HOST + endpoint)
# indigo.server.log(str(response))
# response = response.json()
# indigo.server.log(str(response))
# # update states of the inverter with new data
# newData = response["data"]["telemetries"]
# self.update_inverter(newData, inverter)