# indigo-solaredge-plugin
## Installation:
1. Download and install Indigo
2. Download the .zip of this repository (green 'code' button)
3. Extract the 'indigo-solaredge-plugin' folder from the .zip in the folder with Indigo Plugins (/Library/Application Support/Perceptive Automation/Indigo/Plugins)
4. Rename the 'plugin' folder as 'indigo-solaredge-plugin.indigoPlugin' (add the '.indigoPlugin' termination)
5. Run the installation script in the command terminal using chmod +x ./install.sh && ./install.sh

## Features

- Connect to SolarEdge solar panels through an API
- Read site and inverter data
- Schedule site and inverter data retrieval
- Plot inverter technical data


## Indigo Actions shipped with the plugin:

1. Site Power Flow: _Retrieves the current power flow between all elements of the site including PV array, storage (battery), loads
(consumption) and grid._

    Parameters: 
        1. sites List (List): Choose the site Device whose data you want to see
2. Site Energy: _Return the site energy measurements_
    Parameters: 
        1. sites List (List): Choose the site Device whose data you want to see
3. Site Power: _Return the site power measurements in 15 minutes resolution_
    Parameters: 
        1. sites List (List): Choose the site Device whose data you want to see
        2. Time unit (List): 
            1. MINUTES: Return the data accrued in the last [time] minutes
            2. HOURS: Return the data accrued in the last [time] hours
            3. DAYS:  Return the data accrued in the last [time] days
        3. Time range for the selected time unit: Specify in numbers the [time] for the data to be retrieved
4. Get All Timeline Data on Site: _Display the site overview data_
    Parameters: 
        1. sites List (List): Choose the site Device whose data you want to see: `example: lastYearData (Energy and Revenue)`
5. Inverter Data: _Return specific inverter data for a given timeframe_
    Parameters: 
        1. Inverters List (List): Choose the Inverter Device whose data you want to see
        2. Time unit (List): 
            1. MINUTES: Return the data accrued in the last [time] minutes
            2. HOURS: Return the data accrued in the last [time] hours
            3. DAYS:  Return the data accrued in the last [time] days
        3. Time range for the selected time unit: Specify in numbers the [time] for the data to be retrieved

This Action plots the timeseries data of the specified inverter at: 
 `/Library/Application Support/Perceptive Automation/Indigo 2022.2/WebAssets/images/controls/static/power-INVERTER.png`
6. Get All Inverters Data by Site: _Execute Inverter Data Action for all existing inverters in Indigo Devices_
    Parameters: 
        1. sites List (List): Choose the site Device whose Inverter data you want to see
        2. Time unit (List): 
            1. MINUTES: Return the data accrued in the last [time] minutes
            2. HOURS: Return the data accrued in the last [time] hours
            3. DAYS:  Return the data accrued in the last [time] days
        3. Time range for the selected time unit: Specify in numbers the [time] for the data to be retrieved
