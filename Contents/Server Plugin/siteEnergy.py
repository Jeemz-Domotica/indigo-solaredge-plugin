
import sys

import requests
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os


print(sys.argv)
endpoint = sys.argv[1]
inverter_serialNumber = sys.argv[2]
response = requests.get(endpoint)
data = response.json()
print(data)
newData = data["energyDetails"]["meters"]
consumption = []
production = []
#fig, ax = plt.subplots(len(newData))
types={}
for idx, telemetry in enumerate(newData):
    type = telemetry.get("type").encode('utf-8')
    print("type : ", type)
    types[type] = {}
    types[type]['dates'] = []
    types[type]['values'] = []
    for meterTelemetry in telemetry.get("values"):
        if type == "FeedIn":
            print("meterTelemetry: ", meterTelemetry)
        date = meterTelemetry.get("date")

        value = meterTelemetry.get("value")
        if value != None and date != None:
            types[type]['dates'].append(date)
            types[type]['values'].append(value)


            #ax[idx].plot(date, value)
# print(types)
print(types['FeedIn'])
print(len(types.keys()))
print(types.keys())

fig, ax = plt.subplots(len(types.keys()))
idx = 0
for type in types.keys():
    print("key: " + type)
    ax[idx].plot(types[type].get('dates'), types[type].get('values'))
    ax[idx].set_xticks([ax[idx].get_xticks()[0], ax[idx].get_xticks()[-1]])
    ax[idx].set_yticks([ax[idx].get_yticks()[0], ax[idx].get_yticks()[-1]])
    ax[idx].set_ylabel(type)
    idx = idx + 1

    # ax[idx].set_xticks([ax[idx].get_xticks()[0], ax[idx].get_xticks()[-1]])
    # ax[idx].set_yticks([ax[idx].get_yticks()[0], ax[idx].get_yticks()[-1]])
    # ax[idx].set_ylabel(type)
    # plt.show()


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
plt.savefig(os.path.join(os.getcwd(), "energy-"+inverter_serialNumber+".png"))

