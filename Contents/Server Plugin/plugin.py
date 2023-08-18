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

        if len(newData) > 0:
            last_telemetry = newData[-1]
            date = last_telemetry.get("date")
            inverter.updateStateOnServer(key="date", value=date)
            totalActivePower = format(last_telemetry.get("totalActivePower"), '.2f')
            inverter.updateStateOnServer(key="totalActivePower", value=totalActivePower)
            dcVoltage = last_telemetry.get("dcVoltage")
            inverter.updateStateOnServer(key="dcVoltage", value=dcVoltage)
            powerLimit = last_telemetry.get("powerLimit")
            inverter.updateStateOnServer(key="powerLimit", value=powerLimit)
            totalEnergy = format(last_telemetry.get("totalEnergy"), '.2f')
            inverter.updateStateOnServer(key="totalEnergy", value=totalEnergy)
            temperature = last_telemetry.get("temperature")
            inverter.updateStateOnServer(key="temperature", value=temperature)
            inverterMode = last_telemetry.get("inverterMode")
            inverter.updateStateOnServer(key="inverterMode", value=inverterMode)
            operationMode = last_telemetry.get("operationMode")
            inverter.updateStateOnServer(key="operationMode", value=operationMode)
        else:
            indigo.server.log(str(newData))
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
        # response = requests.get(MY_API_HOST + endpoint)
        arg = MY_API_HOST + endpoint
        cmd = ["python2", "sitePowerFlow.py", str(arg), str(inverter_serialNumber)]


        # send request for saving last timestep data to state
        response = requests.get(arg)
        data = response.json()
        print(data)
        newData = data["data"]["telemetries"]
        self.update_inverter(newData, inverter)


        # send request to script for plotting
        indigo.server.log("COMMAND")
        indigo.server.log(str(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
        out, err = p.communicate()
        result = out.split('\n')
        for lin in result:
            if not lin.startswith('#'):
                indigo.server.log(str(lin))
        indigo.server.log("Ran script")
        # indigo.server.log(str(response))
        # response = response.json()
        # indigo.server.log(str(response))
        # # update states of the inverter with new data
        # newData = response["data"]["telemetries"]
        # self.update_inverter(newData, inverter)

        # return response

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
        indigo.server.log(str(devId))
        indigo.server.log(str(action))
        # define timeunit and time
        # for each inverter device
        #  gets the new inverter timeseries data
        indigo.server.log(str(list(indigo.devices)))
        devices = indigo.devices
        inverters_devices = []
        for device in devices:
            indigo.server.log(str(device.deviceTypeId))
            if device.deviceTypeId == 'inverter':
                inverters_devices.append(device)

        for inverter in inverters_devices:
            #  get devId of the inverter device
            indigo.server.log(str(inverter))
            inverter_id = int(inverter.id)
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

        indigo.server.log(str(action))

        siteId = self.get_siteId(action.props.get('site'))
        timeUnit = action.props.get('timeUnit')[0]
        indigo.server.log('timeunit')
        indigo.server.log(str(timeUnit))
        time = action.props.get('time')[0]
        now = datetime.datetime.now()
        endTime = now.strftime("%Y-%m-%d%%20%H:%M:%S")
        if timeUnit or time == None:
            startTime = now - datetime.timedelta(weeks=1)
        else:
            if timeUnit == 'QUARTER_OF_AN_HOUR':
                startTime = now - datetime.timedelta(minutes=time*15)
            elif timeUnit == 'HOUR':
                startTime = now - datetime.timedelta(hours=time)
            elif timeUnit == 'DAY':
                if time <= 7:
                    startTime = now - datetime.timedelta(days=time)
                else:
                    startTime = now - datetime.timedelta(days=7)
            elif timeUnit == 'WEEK':
                startTime = now - datetime.timedelta(weeks=time)
            elif timeUnit == 'MONTH':
                startTime = now - datetime.timedelta(weeks=time*4)
            elif timeUnit == 'YEAR':
                startTime = now - datetime.timedelta(weeks=time*4*12)
        startTime = startTime.strftime("%Y-%m-%d%%20%H:%M:%S")
        indigo.server.log(str(time))
        endpoint = "site/" + str(siteId) + "/energyDetails?timeUnit=" + timeUnit + "&startTime=" + startTime + "&endTime=" + endTime + "&api_key=" + apikey
        indigo.server.log(str(MY_API_HOST + endpoint))
        # response = requests.get(MY_API_HOST + endpoint)
        arg = MY_API_HOST + endpoint
        cmd = ["python2", "siteEnergy.py", str(arg)]

        indigo.server.log("COMMAND")
        indigo.server.log(str(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
        out, err = p.communicate()
        result = out.split('\n')
        for lin in result:
            if not lin.startswith('#'):
                indigo.server.log(str(lin))
        indigo.server.log("Ran script")

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

