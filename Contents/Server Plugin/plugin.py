import indigo
import requests
import json
import datetime
# import pandas as pd
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import runpy
import subprocess
# import validation later

apikey = None

MY_API_HOST = 'https://monitoringapi.solaredge.com/'


# Here define any functionalities
def safe_dict_retrieval(struct, field):
    return struct[field][0] if len(struct[field]) == 1 else struct[field]


class Plugin(indigo.PluginBase):

    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        indigo.PluginBase.__init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs)

        # Create settings map
        self.settings = {
            "host": None,
        }

    def __del__(self):
        indigo.PluginBase.__del__(self)

    def startup(self):
        indigo.server.log(u"Startup called")

    '''def runConcurrentThread(self):
        try:
            while True:
                # Do your stuff here
        except self.StopThread:
            # do any cleanup here
            pass
            '''

    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        apikey = valuesDict.get('apikey')
        try:
            indigo.variable.delete("apikey")
        except:
            indigo.server.log("No apikey created yet. Proceeding with creation of apikey.")

        indigo.variable.create("apikey", value=apikey)
        indigo.server.log(str(apikey))
        # device.ownerProps
        self.initialize_devices()

    #     automatically init the sites on the account

    # def closedDeviceConfigUi(self, valuesDict, userCancelled, typeId, devId):
    #     """
    #     Called when device config is closed, used for saving states.
    #     :param valuesDict: indigo.Dict containing the key-value pairs of the menu items, as specified in Devices.xml
    #     :param userCancelled: Boolean telling if the menu was saved by user or not.
    #     :param typeId: device type identifier, as specified in Devices.xml
    #     :param devId: device id, unique per device.
    #     :return: True
    #     """
    #     indigo.server.log(str(valuesDict.get('deviceId', "")))
    #     device = indigo.devices[devId]
    #     indigo.server.log("VERIFY STATE IN CONFIG UI CLOSED %s" % valuesDict)
    #     if not userCancelled and typeId == 'myThermostat':
    #         device = indigo.devices[devId]
    #         thermostat_id = safe_dict_retrieval(valuesDict, 'deviceId')
    #         indigo.server.log("thermostat id %s" % thermostat_id )
    #
    #         # Update device in the environment
    #         props_copy = device.pluginProps
    #         indigo.server.log("PROPS COPY")
    #         indigo.server.log(str(props_copy))
    #         indigo.server.log("props copy before deviceId %s" % props_copy['deviceId'] )
    #         props_copy['deviceId'] = thermostat_id
    #         indigo.server.log("props copy after deviceId %s" % props_copy['deviceId'] )
    #         device.replacePluginPropsOnServer(props_copy)
    #
    #         # Update device states on Server - triggers deviceUpdated() method
    #         # device.updateStateOnServer(states_copy)
    #
    #
    #     return True

    # def validateActionConfigUi(self, valuesDict, typeId, deviceId):
    #     """
    #     Callback for validating the saved preferences in Action dialog
    #     :param typeId - action type specified in the type attribute
    #     :param deviceId - the unique device ID for the device the user selected for the action if you specify a deviceFilter
    #     :param valuesDict - the dictionary of values currently specified in the dialog
    #     """
    #     if typeId == 'httpRequest':  # Validation for httpRequest custom action
    #         try:
    #             indigo.server.log(valuesDict.get('thermostatList'))
    #             indigo.server.log("temptCool is %s" % valuesDict.get('temperatureCool'))
    #             indigo.server.log("temptHeat is %s" % valuesDict.get('temperatureHeat'))
    #             assert int(valuesDict['temperatureCool']) in range(int(valuesDict.get('temperatureHeat')), 40)
    #             assert int(valuesDict['temperatureHeat']) in range(0, int(valuesDict.get('temperatureCool')))
    #
    #         except (ValueError, AssertionError) as e:
    #             errors = indigo.Dict()
    #             errors['httpRequest'] = "Action for request must be one of the two options"
    #
    #             indigo.server.log(errors)
    #
    #             return False, valuesDict, errors
    #
    #     return True

    # def closedActionConfigUi(self, valuesDict, userCancelled, typeId, actionId):
    #     """
    #     Callback for updating the stat eof Aciton after validating the data and closing the dialog
    #     """
    #     indigo.server.log(str("closedAction valuesDict %s" % valuesDict))
    #     indigo.server.log(str("closedAction actionID %s" % actionId))
    #     indigo.server.log(str("closedAction typeId %s" % typeId))
    #     device = indigo.devices[int(valuesDict['thermostatList'])]
    #     indigo.server.log("SELECTED DEVICE %s " % device)
    #
    #     indigo.server.log('Dict length: ' + str(len(device.pluginProps.keys())))
    #     for key in device.pluginProps.keys():
    #         indigo.server.log(key + " - " + str(device.pluginProps[key]))
    #     for key in device.states.keys():
    #         indigo.server.log(key + " - " + str(device.states[key]))
    #
    #     if not userCancelled and typeId == 'httpRequest' and str(valuesDict['httpMethod'][0]) == 'crudFan':
    #         POSTdevicefan = valuesDict['POSTdevicefan']
    #         indigo.server.log("Fan Settings Mode%s" % POSTdevicefan )
    #
    #         # Update device in the environment
    #         states_copy = device.states
    #         indigo.server.log("STATES COPY")
    #         indigo.server.log(str(states_copy))
    #         indigo.server.log("states copy before change %s" % states_copy['mode.off'] )
    #         states_copy['mode.off'] = POSTdevicefan
    #         indigo.server.log("states copy after deviceId %s" % states_copy['mode.off'] )
    #
    #         device.updateStateOnServer('mode.off', states_copy['mode.off'])
    #
    #     if not userCancelled and typeId == 'httpRequest' and str(valuesDict['httpMethod'][0]) == 'crudThermostat':
    #         POSTtempCool = valuesDict['POSTtemperatureCool']
    #         indigo.server.log("Post temp cool  to change to %s " % POSTtempCool)
    #         POSTtempHeat = valuesDict['POSTtemperatureHeat']
    #
    #         # Update device in the environment
    #         states_copy = device.states
    #         indigo.server.log("Post temp cool  nefore change in device %s " % states_copy['coolSetPoint'])
    #
    #         indigo.server.log(str(states_copy))
    #         states_copy['coolSetPoint'] = POSTtempCool
    #
    #         states_copy['heatSetPoint'] = POSTtempHeat
    #
    #         device.updateStateOnServer('coolSetPoint', states_copy['coolSetPoint'])
    #         device.updateStateOnServer('heatSetPoint', states_copy['heatSetPoint'])
    #         indigo.server.log("now state cool temp poitn is %s " % device.states['coolSetPoint'])
    #
    #
    #     return (True, valuesDict)

    # getter for the device id

    def get_serialNumber(self, devId):
        device = indigo.devices[int(devId)]

        device_id = device.states.get("serialNumber")
        return device_id

    def get_device(self, devId):
        device = indigo.devices[int(devId)]
        return device

    def get_siteId(self, devId):
        device = indigo.devices[int(devId)]
        indigo.server.log("device: ")
        indigo.server.log(str(device))
        indigo.server.log("states:")
        indigo.server.log(str(device.states))
        siteId = device.pluginProps.get("id")
        return siteId

    def get_siteId_from_inverter(self, devId):
        device = indigo.devices[int(devId)]
        indigo.server.log("device: ")
        indigo.server.log(str(device))
        siteId = device.states.get("siteId")
        indigo.server.log("site id is : ")
        indigo.server.log(str(siteId))
        return siteId

    def get_apikey(self):
        # apikey = indigo.pluginProps.get("apikey")
        indigo.server.log(str(indigo.variables.__dict__))
        # Get a variable
        var = indigo.variables["apikey"]
        apikey = var.value
        return apikey

    def update_inverter(self, newData, inverter):
        indigo.server.log(str(newData))
        indigo.server.log(str(type(newData)))
        states = inverter.states
        '''
        powers = []
        dates = []
        voltages = []
        temperatures = []
        energies = []
        for telemetry in newData:
            date = telemetry.get("date")
            print(date)
            totalActivePower = telemetry.get("totalActivePower")
            powers.append(float(totalActivePower))
            dates.append(date)
            print(str(totalActivePower))
            dcVoltage = telemetry.get("dcVoltage")
            voltages.append(dcVoltage)
            print(str(dcVoltage))
            totalEnergy = format(telemetry.get("totalEnergy"), '.2f')
            energies.append(totalEnergy)
            temperature = telemetry.get("temperature")
            temperatures.append(temperature)
        '''

        #runpy.run_path(path_name='sitePowerFlow.py')
        indigo.server.log("BEFORE PLOTTING")
       # indigo.server.log(str(os.system("sitePowerFlow.py")))
        import subprocess
        cmd = 'python2 sitePowerFlow.py'

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.split('\n')
        for lin in result:
            if not lin.startswith('#'):
                indigo.server.log(str(lin))
        indigo.server.log("Ran script")
        '''
        try:
            fig, ax = plt.subplots(4)
            indigo.server.log("started plotting")
            ax[0].plot(dates, powers)
            ax[0].set_xticks(ax[0].get_xticks()[::100])
            ax[0].set_ylabel('totalActivePower')
            ax[1].plot(dates, voltages)
            ax[1].set_xticks(ax[1].get_xticks()[::100])
            ax[1].set_ylabel('dcVoltage')
            ax[2].plot(dates, energies)
            ax[2].set_xticks(ax[2].get_xticks()[::100])
            ax[2].set_yticks([ax[2].get_yticks()[0], ax[2].get_yticks()[-1]])
            ax[2].set_ylabel('totalEnergy')
            ax[3].plot(dates, temperatures)
            ax[3].set_ylabel('Temperature')
            ax[3].set_xticks(ax[3].get_xticks()[::100])
            fig.tight_layout()
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
        except Exception as e:
            indigo.server.log(str(e))
            # inverter.updateStateOnServer(key=key, value=value)
        # site.replacePluginPropsOnServer(pluginProps)
        # os.path.join(os.getcwd(),
        '''
        indigo.server.log(str(inverter))

    def update_site(self, newData, site):
        indigo.server.log(str(newData))
        indigo.server.log(str(type(newData)))
        pluginProps = site.pluginProps
        pluginProps.update(newData)
        indigo.server.log(str(pluginProps))
        if newData.get('currentPower'):
            indigo.server.log(str(type(newData.get('currentPower'))))
            indigo.server.log(str(newData.get('currentPower')))

            site.updateStateOnServer(key='currentPower', value=float(newData.get('currentPower').get('power')))
        if newData.get('lastDayData'):
            site.updateStateOnServer(key='lastDayEnergy', value=float(newData.get('lastDayData').get('energy')))
        if newData.get('lastMonthData'):
            site.updateStateOnServer(key='lastMonthEnergy', value=float(newData.get('lastMonthData').get('energy')))
        if newData.get('lastYearData'):
            site.updateStateOnServer(key='lastYearEnergy', value=float(newData.get('lastYearData').get('energy')))
        if newData.get('lifeTimeData'):
            site.updateStateOnServer(key='lifeTimeEnergy', value=float(newData.get('lifeTimeData').get('energy')))
        if newData.get('lastUpdateTime'):
            site.updateStateOnServer(key='lastUpdateTime', value=str(newData.get('lastUpdateTime')))
            indigo.server.log("updated the state with new data")
        # for key, value in pluginProps.items():
        #     indigo.server.log(str(key))
        #     indigo.server.log(str(value))
        #     energy_value = value.values()[0]
        #     indigo.server.log(str(energy_value))
            # if type(value) == dict:
            #     indigo.server.log(str(value.values()[0]))
            #     site.updateStateOnServer(key=key, value=value.values()[0])
            # site.updateStateOnServer(key=key, value=value)

        # site.replacePluginPropsOnServer(pluginProps)
        indigo.server.log(str(site))

    def update_battery(self, newData, battery):
        battery.updateStateOnServer(newData)

    def req_site_power_flow(self, action):
        '''
        API request. Retrieves the power flow
        :param siteId:
        :return:
        '''
        apikey = self.get_apikey()
        indigo.server.log(str(action))
        site = action.props['site']
        siteId= self.get_siteId(site)
        endpoint = 'site/' + str(siteId) + '/currentPowerFlow?api_key=' + apikey
        indigo.server.log(str(MY_API_HOST + endpoint))
        response = requests.get(MY_API_HOST + endpoint)
        indigo.server.log(str(response))
        response = response.json()
        indigo.server.log(str(response))
        return response

    def update_inverter_data_by_serialNumber(self, action, inverter_serialNumber, inverter, devId):
        '''
        Helpter function. Updates the inverter device with new data by serialNumber
        :param action:
        :param inverter_serialNumber:
        :return:
        '''
        #  Inverter Technical Data: Description: Return specific inverter data for a given timeframe
        # URL: /equipment/{siteId} /{serialNumber}/data
        apikey = self.get_apikey()
        indigo.server.log("REQ INVERTER DATA")
        siteId = self.get_siteId_from_inverter(int(devId))
        timeUnit = action.props.get('timeUnit')[0]
        indigo.server.log('timeunit')
        indigo.server.log(str(timeUnit))
        time = action.props.get('time')
        now = datetime.datetime.now()
        endTime = now.strftime("%Y-%m-%d%%20%H:%M:%S")
        if timeUnit or time == None:
            startTime = now - datetime.timedelta(weeks=1)
        else:
            if timeUnit == 'MINUTES':
                startTime = now - datetime.timedelta(minutes=time)
            elif timeUnit == 'HOUR':
                startTime = now - datetime.timedelta(hours=time)
            elif timeUnit == 'DAY':
                if time <= 7:
                    startTime = now - datetime.timedelta(days=time)
                else:
                    startTime = now - datetime.timedelta(days=7)
        startTime = startTime.strftime("%Y-%m-%d%%20%H:%M:%S")
        endpoint = 'equipment/' + str(siteId) + '/' + inverter_serialNumber + '/data?startTime=' + startTime + '&endTime=' + endTime + '&api_key=' + apikey
        indigo.server.log(str(MY_API_HOST + endpoint))
        response = requests.get(MY_API_HOST + endpoint)
        indigo.server.log(str(response))
        response = response.json()
        indigo.server.log(str(response))
        # update states of the inverter with new data
        newData = response["data"]["telemetries"]
        self.update_inverter(newData, inverter)

        return response

    def req_inverter_data_by_serialNumber(self, action, typeId, devId):
        '''
        Indigo Action. Updates the inverter object with the serialNumber with new data
        :param action:
        :param typeId:
        :param devId:
        :return:
        '''
        indigo.server.log(str(action))
        devId = action.props.get('inverter')
        indigo.server.log(devId)
        inverter_serialNumber = self.get_serialNumber(devId)
        inverter = self.get_device(devId)
        self.update_inverter_data_by_serialNumber(action, inverter_serialNumber, inverter, devId)

    def req_update_all_inverters(self, action, typeId, devId):
        '''
        Calls the request to get all inverters and updates with the new data the
        state of the already created inverter devices
        :param action:
        :param typeId:
        :param devId:
        :return:
        '''
        siteId = self.get_siteId(int(devId))
        # define timeunit and time
        # for each inverter device
        #  gets the new inverter timeseries data
        inverters_devices = indigo.devices.deviceTypeId['inverter']
        for inverter in inverters_devices:
            #  get devId of the inverter device
            indigo.server.log(str(inverter))
            inverter_id = inverter.props.get('id')
            inverter_serialNumber = self.get_serialNumber(inverter_id)
            self.update_inverter_data_by_serialNumber(action, inverter_serialNumber, inverter, inverter_id)

    def req_update_all_batteries(self, action, typeId, devId):
        '''
        Calls the request to get all the batteries and updates with the new data the
        existing battery devices
        :param action:
        :param typeId:
        :param devId:
        :return:
        '''

        siteId = self.get_siteId(int(devId))
        # define timeunit and time
        timeUnit = action.props.get('timeUnit')
        time = action.props.get('time')
        #  gets the new battery timeseries data
        response = self.req_all_batteries(siteId, timeUnit, time)
        batteries_json = response.json()
        batteries = batteries_json["storageData"]["batteries"]
        indigo.server.log(str(batteries))
        # now get all the battery devices and their serialNumber
        batteries_devices = indigo.devices.deviceTypeId['battery']
        # correlate the battery data with the serial number of the battery devices
        # and update the state of the battery device with the new data correlated with its id
        for battery_device in batteries_devices:
            for battery_data in batteries:
                if battery_data["serialNumber"] == battery_device.props.get("serialNumber"):
                    self.update_battery(battery_data, battery_device)

    def req_site_energy(self, action, typeId, devId):
        '''
        Site Energy - Detailed:
        Description: Detailed site energy measurements from meters such as consumption, export (feed-in), import (purchase), etc.
        Note: Calculated meter readings (also referred to as "virtual meters"), such as self-consumption, are calculated
        using the data measured by the meter and the inverters.
        URL:/site/{siteId}/energyDetails
        # &timeUnit=DAY
        '''
        indigo.server.log("REQ SITE ENERGY DATA")
        apikey = self.get_apikey()
        siteId = self.get_siteId(devId)
        time = action.props.get('time')
        indigo.server.log(str(time))
        endpoint = 'site/' + siteId + '/energyDetails?timeUnit=' + time + '&api_key=' + apikey
        indigo.server.log(str(MY_API_HOST + endpoint))
        response = requests.get(MY_API_HOST + endpoint)
        indigo.server.log(str(response))
        response = response.json()
        indigo.server.log(str(response))
        return response

    def req_site_power(self, action, typeId, devId):
        '''
        Description: Detailed site power measurements from meters such as consumption, export (feed-in), import (purchase),
        Note: Calculated meter readings (also referred to as "virtual meters"), such as self-consumption, are calculated
        using the data measured by the meter and the inverters.
        URL: /site/{siteId}/powerDetails
        :param action:
        :param typeId:
        :param devId:
        :return:
        '''
        apikey = self.get_apikey()
        indigo.server.log("REQ SITE POWER DATA")
        siteId = self.get_siteId(devId)
        # time in hours
        timeUnit = action.props.get('timeUnit')
        time = action.props.get('time')
        now = datetime.datetime.now()
        endTime = now.strftime("%Y-%m-%d%%20%H:%M:%S")
        if timeUnit == 'MINUTES':
            startTime = now - datetime.timedelta(minutes=time)
        elif timeUnit == 'HOUR':
            startTime = now - datetime.timedelta(hours=time)
        elif timeUnit == 'DAY':
            startTime = now - datetime.timedelta(days=time)
        elif timeUnit == 'WEEK':
            startTime = now - datetime.timedelta(weeks=time)
        startTime = startTime.strftime("%Y-%m-%d%%20%H:%M:%S")
        endpoint = 'site/' + siteId + '/powerDetails' + '?startTime=' + startTime + '&endTime=' + endTime + '&api_key=' + apikey
        indigo.server.log(str(MY_API_HOST + endpoint))
        response = requests.get(MY_API_HOST + endpoint)
        indigo.server.log(str(response))
        data = response.json()
        indigo.server.log(str(response))
        # df = pd.json_normalize(data["powerDetails"], record_path=['meters'])
        # print(df.head())
        # df.to_csv()
        return response

    def req_site_data(self, action, typeId, devId):
        '''
        Site Overview
        Description: Display the site overview data.
        URL: /site/{siteId}/ overview
        :return:
        '''
        apikey = self.get_apikey()
        indigo.server.log(str(action))
        id = action.props.get('site')
        site = self.get_device(id)
        siteId = self.get_siteId(id)
        indigo.server.log("siteId:")
        indigo.server.log(str(siteId))
        endpoint = 'site/' + str(siteId) + '/overview?api_key=' + apikey
        indigo.server.log(MY_API_HOST + endpoint)
        response = requests.get(MY_API_HOST + endpoint)
        indigo.server.log(str(response))
        data = response.json()
        indigo.server.log(str(data))
        self.update_site(data["overview"], site)

    # initializes one node which is registered in Velux
    # runs only when indigo plugin is configured
    def init_site(self, node):
        '''
        Initialize a dictionary for the site device object
        :param node:
        :return:
        '''
        indigo.server.log(str(node))
        device = {}
        device['name'] = node['name']
        device['location'] = node['location']
        device['siteId'] = node['id']
        device['installationDate'] = node['installationDate']
        indigo.server.log(str(device))
        return device

    def create_site_device(self, site):
        '''
        Create the device site object in indigo with the initialized data
        :param site:
        :return:
        '''
        indigo.server.log(str(site))
        indigo.server.log(str(site['name']).split(' ')[-1])
        try:
            created_device = indigo.device.create(
                protocol=indigo.kProtocol.Plugin,
                pluginId='jeemzsolaredge',
                name=site['name'],
                deviceTypeId='site',
                props={'id': site['siteId']},
            )
            created_device.updateStatesOnServer(site)
        except Exception as e:
            indigo.server.log("Device already exist. Continue.")
            indigo.server.log(str(e))

    def init_inverter(self, node, siteId):
        '''
        Initialize the inverter object device with the data retrieved from the api
        :param node:
        :param siteId:
        :return:
        '''
        indigo.server.log(str(node))
        device = {}
        device['name'] = node['name']
        device['manufacturer'] = node['manufacturer']
        device['serialNumber'] = node['serialNumber']
        device['model'] = node['model']
        device['siteId'] = siteId
        indigo.server.log('siteId will be created as: ')
        indigo.server.log(str(device['siteId']))

        return device

    def create_inverter_device(self, inverter):
        '''
        Create the initialized inverter device
        :param inverter:
        :return:
        '''
        try:
            created_device = indigo.device.create(
                protocol=indigo.kProtocol.Plugin,
                pluginId='jeemzsolaredge',
                name=inverter['name'],
                deviceTypeId='inverter',
                props={'id': inverter['serialNumber']},
            )
            indigo.server.log("created inverter with id , now creating states")
            for key, value in inverter.items():
                created_device.updateStateOnServer(key=key, value=value)
            indigo.server.log('created inverter: ')
            indigo.server.log(str(created_device))
        except Exception as e:
            indigo.server.log("Device already exist. Continue.")
            indigo.server.log(str(e))

    def init_battery(self, node, siteId):
        '''
        Initialize the battery device object with the new data
        :param node:
        :param siteId:
        :return:
        '''
        indigo.server.log(str(node))
        device = {}
        device['nameplate'] = node['nameplate']
        device['modelNumber'] = node['modelNumber']
        device['serialNumber'] = node['serialNumber']
        device['telemetries'] = node['telemetries']
        device['siteId'] = siteId
        return device

    def create_battery_device(self, battery):
        '''
        Create the battery device in indigo
        :param battery:
        :return:
        '''
        try:
            created_device = indigo.device.create(
                protocol=indigo.kProtocol.Plugin,
                pluginId='jeemzsolaredge',
                name=battery['nameplate'],
                deviceTypeId='battery',
                props={'id': battery['serialNumber']},
            )
            indigo.server.log("created inverter with id , now creating states")
            for key, value in battery.items():
                created_device.updateStateOnServer(key=key, value=value)
            indigo.server.log('created battery: ')
            indigo.server.log(str(created_device))
        except Exception as e:
            indigo.server.log("Device already exist. Continue.")
            indigo.server.log(str(e))

    def req_all_sites(self):
        '''
        Retrieve all the sites from the api
        :return:
        '''
        apikey = self.get_apikey()
        endpoint = 'sites/list?api_key=' + apikey
        indigo.server.log(str(MY_API_HOST + endpoint))
        response = requests.get(MY_API_HOST + endpoint)
        return response

    def req_all_inverters(self, siteId):
        '''
        Retrieve all the inverters from the api
        :param siteId:
        :return:
        '''
        apikey = self.get_apikey()
        endpoint = '/equipment/' + str(siteId) + '/list?api_key=' + apikey
        response = requests.get(MY_API_HOST + endpoint)
        print(response.json)
        return response

    def req_all_batteries(self, siteId, timeUnit=None, time=None):
        '''
        Retrieve all the batteries from the api
        :param siteId:
        :param timeUnit:
        :param time:
        :return:
        '''
        apikey = self.get_apikey()
        now = datetime.datetime.now()
        endTime = now.strftime("%Y-%m-%d%%20%H:%M:%S")
        if timeUnit or time == None:
            startTime = now - datetime.timedelta(weeks=1)
        else:
            if timeUnit == 'MINUTES':
                startTime = now - datetime.timedelta(minutes=time)
            elif timeUnit == 'HOUR':
                startTime = now - datetime.timedelta(hours=time)
            elif timeUnit == 'DAY':
                if time <= 7:
                    startTime = now - datetime.timedelta(days=time)
                else:
                    startTime = now - datetime.timedelta(days=7)
        startTime = startTime.strftime("%Y-%m-%d%%20%H:%M:%S")
        query = {'startTime': startTime, 'endTime': endTime, 'api_key': apikey}

        endpoint = 'site/' + str(siteId) + '/storageData'
        url = MY_API_HOST + endpoint + '?' + 'startTime=' + startTime + '&endTime=' + endTime + '&api_key=' + apikey
        response = requests.get(url)
        indigo.server.log("url: ")
        indigo.server.log(str(response.url))
        indigo.server.log(str(response.headers))
        print(response.json)
        return response

    # initialize all nodes (blinders) registered with Velux on indigo config of password and ip of Velux
    def initialize_devices(self):
        '''
        This function is only called to automatically create new devices with a Solaredge account
        :return:
        '''
        sites = []
        try:
            response = self.req_all_sites()
            sites_json = response.json()
            indigo.server.log(str(sites_json))
            sites = sites_json["sites"]["site"]
            indigo.server.log(str(sites))
        except:
            indigo.server.log("Could not reach the SolarEdge server or wrong API key.")

        if len(sites) > 0:
            for site in sites:
                indigo.server.log("inside the loop of init devices")
                indigo.server.log(str(site))
                # create site
                device_site = self.init_site(site)
                self.create_site_device(device_site)

                # create inverters of the site
                siteId = device_site['siteId']
                response = self.req_all_inverters(siteId)
                indigo.server.log(str(response))
                inverters_json = response.json()
                indigo.server.log(str(inverters_json))
                inverters = inverters_json["reporters"]["list"]
                indigo.server.log(str(inverters))
                for inverter in inverters:
                    inverter_device = self.init_inverter(inverter, siteId)
                    self.create_inverter_device(inverter_device)

                # create batteries of the site
                response = self.req_all_batteries(siteId)
                indigo.server.log(str(response))
                batteries_json = response.json()
                indigo.server.log(str(batteries_json))
                batteries = batteries_json["storageData"]["batteries"]
                indigo.server.log(str(batteries))
                if len(batteries) > 0:
                    for battery in batteries:
                        battery_device = self.init_battery(battery, siteId)
                        self.create_battery_device(battery_device)
                else:
                    indigo.server.log("There are no batteries on your account on this site.")

        elif len(sites) == 0:
            indigo.server.log("Could not find any device to connect to SolarEdge")

