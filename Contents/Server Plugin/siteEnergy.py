
import sys

import requests
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
from datetime import datetime

print(sys.argv)
endpoint = sys.argv[1]
response = requests.get(endpoint)
data = response.json()
print(data)
newData = data["energyDetails"]["meters"]
consumption = []
production = []
#fig, ax = plt.subplots(len(newData))
types={}
try :
    for idx, telemetry in enumerate(newData):
        type = telemetry.get("type").encode('utf-8')

        types[type] = {}
        types[type]['dates'] = []
        types[type]['values'] = []
        for meterTelemetry in telemetry.get("values"):

            date = meterTelemetry.get("date")
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            value = meterTelemetry.get("value")
            if value != None and date != None:
                types[type]['dates'].append(date)
                types[type]['values'].append(value)


                #ax[idx].plot(date, value)
    # print(types)

    fig, ax = plt.subplots(len(types.keys()), squeeze=False )
    idx = 0
    for type in types.keys():

        ax[idx, idx].plot(types[type].get('dates'), types[type].get('values'))
        ax[idx, idx].set_xticks([ax[idx, idx].get_xticks()[0], ax[idx, idx].get_xticks()[-1]])
        ax[idx, idx].set_yticks([ax[idx, idx].get_yticks()[0], ax[idx, idx].get_yticks()[-1]])
        ax[idx, idx].set_ylabel(type)
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
    plt.savefig(os.path.join(os.getcwd(), "energy.png"))

except Exception as e:
    print(e)