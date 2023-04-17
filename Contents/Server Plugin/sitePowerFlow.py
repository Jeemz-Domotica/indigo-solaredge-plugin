import sys

import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os

import datetime
print(sys.argv)
endpoint = sys.argv[1]
inverter_serialNumber = sys.argv[2]
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
plt.savefig(os.path.join(os.getcwd(), "power-"+inverter_serialNumber+".png"))

