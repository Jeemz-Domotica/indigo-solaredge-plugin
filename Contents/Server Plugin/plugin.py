import indigo
from Queue import Queue
import requests
# import validation later

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

    def runConcurrentThread(self):
        try:
            while True:
                # Do your stuff here
                indigo.server.log('SOLAREDGE PLUGIN RUNNING')
                self.sleep(4) # in seconds
        except self.StopThread:
            # do any cleanup here
            pass

    
    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        indigo.server.log(str(valuesDict.get("apikey", "")))
    #     automatically init the sites on the account

    def closedDeviceConfigUi(self, valuesDict, userCancelled, typeId, devId):
        """
        Called when device config is closed, used for saving states.
        :param valuesDict: indigo.Dict containing the key-value pairs of the menu items, as specified in Devices.xml
        :param userCancelled: Boolean telling if the menu was saved by user or not.
        :param typeId: device type identifier, as specified in Devices.xml
        :param devId: device id, unique per device.
        :return: True
        """
        indigo.server.log(str(valuesDict.get('deviceId', "")))
        device = indigo.devices[devId]
        indigo.server.log("VERIFY STATE IN CONFIG UI CLOSED %s" % valuesDict)
        if not userCancelled and typeId == 'myThermostat':
            device = indigo.devices[devId]
            thermostat_id = safe_dict_retrieval(valuesDict, 'deviceId')
            indigo.server.log("thermostat id %s" % thermostat_id )

            # Update device in the environment
            props_copy = device.pluginProps
            indigo.server.log("PROPS COPY")
            indigo.server.log(str(props_copy))
            indigo.server.log("props copy before deviceId %s" % props_copy['deviceId'] )
            props_copy['deviceId'] = thermostat_id
            indigo.server.log("props copy after deviceId %s" % props_copy['deviceId'] )
            device.replacePluginPropsOnServer(props_copy)

            # Update device states on Server - triggers deviceUpdated() method
            # device.updateStateOnServer(states_copy)


        return True


    def get_device_fan(self, valuesDict, typeId, devId):
        """
        Callback command for the httpRequest Indigo Action
        Calls the Request for the user input action
        :param action: indigo.Dict object containing action params
        """
        indigo.server.log("GET DEVICE FAN   ")
        # do whatever you need to here
    #   typeId is the device type specified in the Devices.xml
    #   devId is the device ID - 0 if it's a new device
        indigo.server.log( "valuesDict thermostatList selected%s" % valuesDict['thermostatList'])
        indigo.server.log("typeId %s" % typeId)
        indigo.server.log("devId %s" % devId)
        selected_device = indigo.devices[int(valuesDict['thermostatList'])]

    def validateActionConfigUi(self, valuesDict, typeId, deviceId):
        """
        Callback for validating the saved preferences in Action dialog
        :param typeId - action type specified in the type attribute
        :param deviceId - the unique device ID for the device the user selected for the action if you specify a deviceFilter
        :param valuesDict - the dictionary of values currently specified in the dialog
        """
        if typeId == 'httpRequest':  # Validation for httpRequest custom action
            try:
                indigo.server.log(valuesDict.get('thermostatList'))
                indigo.server.log("temptCool is %s" % valuesDict.get('temperatureCool'))
                indigo.server.log("temptHeat is %s" % valuesDict.get('temperatureHeat'))
                assert int(valuesDict['temperatureCool']) in range(int(valuesDict.get('temperatureHeat')), 40)
                assert int(valuesDict['temperatureHeat']) in range(0, int(valuesDict.get('temperatureCool')))

            except (ValueError, AssertionError) as e:
                errors = indigo.Dict()
                errors['httpRequest'] = "Action for request must be one of the two options"

                indigo.server.log(errors)

                return False, valuesDict, errors

        return True

    def closedActionConfigUi(self, valuesDict, userCancelled, typeId, actionId):
        """
        Callback for updating the stat eof Aciton after validating the data and closing the dialog
        """
        indigo.server.log(str("closedAction valuesDict %s" % valuesDict))
        indigo.server.log(str("closedAction actionID %s" % actionId))
        indigo.server.log(str("closedAction typeId %s" % typeId))
        device = indigo.devices[int(valuesDict['thermostatList'])]
        indigo.server.log("SELECTED DEVICE %s " % device)

        indigo.server.log('Dict length: ' + str(len(device.pluginProps.keys())))
        for key in device.pluginProps.keys():
            indigo.server.log(key + " - " + str(device.pluginProps[key]))
        for key in device.states.keys():
            indigo.server.log(key + " - " + str(device.states[key]))

        if not userCancelled and typeId == 'httpRequest' and str(valuesDict['httpMethod'][0]) == 'crudFan':
            POSTdevicefan = valuesDict['POSTdevicefan']
            indigo.server.log("Fan Settings Mode%s" % POSTdevicefan )

            # Update device in the environment
            states_copy = device.states
            indigo.server.log("STATES COPY")
            indigo.server.log(str(states_copy))
            indigo.server.log("states copy before change %s" % states_copy['mode.off'] )
            states_copy['mode.off'] = POSTdevicefan
            indigo.server.log("states copy after deviceId %s" % states_copy['mode.off'] )

            device.updateStateOnServer('mode.off', states_copy['mode.off'])
        
        if not userCancelled and typeId == 'httpRequest' and str(valuesDict['httpMethod'][0]) == 'crudThermostat':
            POSTtempCool = valuesDict['POSTtemperatureCool']
            indigo.server.log("Post temp cool  to change to %s " % POSTtempCool)
            POSTtempHeat = valuesDict['POSTtemperatureHeat']

            # Update device in the environment
            states_copy = device.states
            indigo.server.log("Post temp cool  nefore change in device %s " % states_copy['coolSetPoint'])

            indigo.server.log(str(states_copy))
            states_copy['coolSetPoint'] = POSTtempCool

            states_copy['heatSetPoint'] = POSTtempHeat

            device.updateStateOnServer('coolSetPoint', states_copy['coolSetPoint'])
            device.updateStateOnServer('heatSetPoint', states_copy['heatSetPoint'])
            indigo.server.log("now state cool temp poitn is %s " % device.states['coolSetPoint'])
        
   
        return (True, valuesDict)
        


        
    def send_http_request(self, action, typeId, devId):
        """
        Callback command for the httpRequest Indigo Action
        Calls the Request for the user input action
        :param action: indigo.Dict object containing action params
        """
        indigo.server.log("ACTION PROPS")
        indigo.server.log(str(action))
        indigo.server.log(str(typeId))
        indigo.server.log(str(devId))

    def site_power_flow(self, siteId):
        endpoint = 'site/'+siteId+'currentPowerFlow?api_key=' + apikey
        indigo.server.log(str(MY_API_HOST + endpoint))
        response = requests.get(MY_API_HOST + endpoint)
        indigo.server.log(str(response.json()))
        return response

    # initializes one node which is registered in Velux
    # runs only when indigo plugin is configured
    def init_site(self, node):
        indigo.server.log(str(node))
        device = {}
        device['device'] = {}
        device['device']['name'] = node['name']
        device['device']['location'] = node['location']
        device['device']['siteId'] = node['id']
        device['device']['installationDate'] = node['installationDate']

        return device

    def create_site_device(self, site):
        try:
            created_device = indigo.device.create(
                protocol=indigo.kProtocol.Plugin,
                pluginId='jeemzsolaredge',
                name=site['name'],
                deviceTypeId='site',
                props={'deviceId': site['deviceId']},
            )
            created_device.updateStateOnServer(site)
        except:
            indigo.server.log("Device already exist. Continue.")

    def init_inverter(self, node):
        indigo.server.log(str(node))
        device = {}
        device['device'] = {}
        device['device']['name'] = node['name']
        device['device']['manufacturer'] = node['manufacturer']
        device['device']['serialNumber'] = node['serialNumber']
        device['device']['model'] = node['model']

        return device

    def create_inverter_device(self, inverter):
        try:
            created_device = indigo.device.create(
                protocol=indigo.kProtocol.Plugin,
                pluginId='jeemzsolaredge',
                name=inverter['name'],
                deviceTypeId='inverter',
                props={'deviceId': inverter['deviceId']},
            )
            created_device.updateStateOnServer(inverter)
        except:
            indigo.server.log("Device already exist. Continue.")

    def init_battery(self, node):
        indigo.server.log(str(node))
        device = {}
        device['device'] = {}
        device['device']['nameplate'] = node['nameplate']
        device['device']['modelNumber'] = node['modelNumber']
        device['device']['serialNumber'] = node['serialNumber']
        device['device']['telemetries'] = node['telemetries']

        return device

    def create_battery_device(self, battery):
        try:
            created_device = indigo.device.create(
                protocol=indigo.kProtocol.Plugin,
                pluginId='jeemzsolaredge',
                name=battery['nameplate'],
                deviceTypeId='battery',
                props={'deviceId': battery['deviceId']},
            )
            created_device.updateStateOnServer(battery)
        except:
            indigo.server.log("Device already exist. Continue.")


    def req_all_sites(self):
        endpoint = 'sites/list?api_key=' + apikey
        indigo.server.log(str(MY_API_HOST + endpoint))
        response = requests.get(MY_API_HOST + endpoint)
        return response

    def req_all_inverters(self, siteId):
        endpoint = '/site/'+siteId+'/storageData?api_key='+apikey
        response = requests.get(MY_API_HOST + endpoint)
        print(response.json)
        return response

    def req_all_batteries(self, siteId):
        endpoint = '/equipment/'+siteId+'/list?api_key='+apikey
        response = requests.get(MY_API_HOST + endpoint)
        print(response.json)
        return response



    # initialize all nodes (blinders) registered with Velux on indigo config of password and ip of Velux
    def initialize_devices(self, apikey):

        sites = []
        try:
            response = self.req_all_sites()
            sites_json = response.json()
            indigo.server.log(str(sites_json))
            sites.append(sites_json["Sites"]["list"])
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
                inverters_json = response.json()["list"]
                inverters = inverters_json["Sites"]["list"]
                indigo.server.log(str(inverters))
                for inverter in inverters:
                    inverter_device = self.init_inverter(inverter)
                    self.create_inverter_device(inverter_device)

                # create batteries of the site
                response = self.req_all_batteries(siteId)
                batteries_json = response.json()
                batteries = batteries_json["storageData"]["batteries"]
                indigo.server.log(str(batteries))
                for battery in batteries:
                    battery_device = self.init_battery(battery)
                    self.create_battery_device(battery_device)

        elif len(sites) == 0:
            indigo.server.log("Could not find any device to connect to Velux")

