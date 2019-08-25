try:
    from urllib import urlencode


    def urljoin(*args):
        return "".join(args)
except ImportError:
    from urllib.parse import urlencode, urljoin

import requests


def api_call(method):
    def _dummy(self, **kwargs):
        api_endpoint_url = urljoin(self.api_url, method.__name__)
        f = self._gen_api_call(api_endpoint_url)
        return f(**kwargs)

    _dummy.__doc__ = method.__doc__
    _dummy.__name__ = method.__name__
    return _dummy


class UptimeRobot(object):
    class ResponseFormat(object):
        JSON = "json"
        XML = "xml"

    _DEFAULT_API_URL = "https://api.uptimerobot.com/v2/"

    def __init__(self, api_key, api_url=_DEFAULT_API_URL, format=ResponseFormat.JSON):
        self.api_url = api_url
        self.api_key = api_key
        self.payload = {'api_key': self.api_key,
                        'format': format}

    def _build_payload(self, params):
        payload = {} or params
        payload.update(self.payload)
        return urlencode(payload)

    def _gen_api_call(self, api_endpoint_url):
        def __inner(**kwargs):
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/x-www-form-urlencoded"
            }
            payload = self._build_payload(kwargs)
            print(api_endpoint_url, payload, headers)
            resp = requests.request("POST", api_endpoint_url, data=payload, headers=headers)
            return resp

        return __inner

    @api_call
    def getAccountDetails(self):
        """Account details (max number of monitors that can be added and number of up/down/paused monitors) can be grabbed using this method."""

    @api_call
    def getMonitors(self):
        """This is a Swiss-Army knife type of a method for getting any information on monitors.
        By default, it lists all the monitors in a user's account, their friendly names, types (http, keyword, port, etc.), statuses (up, down, etc.) and uptime ratios.
        There are optional parameters which lets the getMonitors method to output information on any given monitors rather than all of them.
        And also, parameters exist for getting the notification logs (alerts) for each monitor and even which alert contacts were alerted on each notification.

        Parameters:
            monitors - optional (if not used, will return all monitors in an account. Else, it is possible to define any number of monitors with their IDs like: monitors=15830-32696-83920)
            types - optional (if not used, will return all monitors types (HTTP, keyword, ping..) in an account. Else, it is possible to define any number of monitor types like: types=1-3-4)
            statuses - optional (if not used, will return all monitors statuses (up, down, paused) in an account. Else, it is possible to define any number of monitor statuses like: statuses=2-9)
            custom_uptime_ratios - optional (defines the number of days to calculate the uptime ratio(s) for. Ex: custom_uptime_ratios=7-30-45 to get the uptime ratios for those periods)
            custom_uptime_ranges - optional (defines the ranges to calculate the uptime ratio(s) for. Ex: custom_uptime_ranges=1465440758_1466304758 to get the uptime ratios for those periods. It is possible to send multiple ranges like 1465440758_1466304758-1434682358_1434855158)
            all_time_uptime_ratio - optional (returns the "all time uptime ratio". It will slow down the response a bit and, if not really necessary, suggest not using it. Default is 0)
            all_time_uptime_durations - optional (returns the "all time durations of up-down-paused events". It will slow down the response a bit and, if not really necessary, suggest not using it. Default is 0)
            logs - optional (defines if the logs of each monitor will be returned. Should be set to 1 for getting the logs. Default is 0)
            logs_start_date - optional (works only for the Pro Plan as 24 hour+ logs are kept only in the Pro Plan, formatted as Unix time and must be used with logs_end_date)
            logs_end_date - optional (works only for the Pro Plan as 24 hour+ logs are kept only in the Pro Plan, formatted as Unix time and must be used with logs_start_date)
            log_types - optional (the types of logs to be returned with a usage like: log_types=1-2-98). If empty, all log types are returned.
            logs_limit - optional (the number of logs to be returned in descending order). If empty, all logs are returned.
            response_times - optional (defines if the response time data of each monitor will be returned. Should be set to 1 for getting them. Default is 0)
            response_times_limit - optional (the number of response time logs to be returned (descending order). If empty, last 24 hours of logs are returned (if response_times_start_date and response_times_end_date are not used).
            response_times_average - optional (by default, response time value of each check is returned. The API can return average values in given minutes. Default is 0. For ex: the Uptime Robot dashboard displays the data averaged/grouped in 30 minutes)
            response_times_start_date - optional (formatted as Unix time and must be used with response_times_end_date) (response_times_end_date - response_times_start_date can't be more than 7 days)
            response_times_end_date - optional (formatted as Unix time and must be used with response_times_start_date) (response_times_end_date - response_times_start_date can't be more than 7 days)
            alert_contacts - optional (defines if the alert contacts set for the monitor to be returned. Default is 0)
            mwindows - optional (the maintenance windows for the monitor which can be mentioned with their IDs like 345-2986-71)
            ssl - optional (defines if SSL certificate info for each monitor will be returned)
            custom_http_headers - optional (defines if the custom HTTP headers of each monitor will be returned. Should be set to 1 for getting them. Default is 0)
            custom_http_statuses - optional (defines if the custom HTTP statuses of each monitor will be returned. Should be set to 1 for getting them. Default is 0)
            timezone - optional (defines if the user's timezone should be returned. Should be set to 1 for getting it. Default is 0)
            offset - optional (used for pagination. Defines the record to start paginating. Default is 0)
            limit - optional (used for pagination. Defines the max number of records to return for the response. Default and max. is 50)
            search - optional (a keyword of your choice to search within url and friendly_name and get filtered results)

        """

    @api_call
    def newMonitor(self):
        """New monitors of any type can be created using this method.

        Parameters:
            friendly_name - required
            url - required
            type - required
            sub_type - optional (required for port monitoring)
            port - optional (required for port monitoring)
            keyword_type - optional (required for keyword monitoring)
            keyword_value - optional (required for keyword monitoring)
            interval - optional (in seconds)
            http_username - optional
            http_word - optional
            alert_contacts - optional (the alert contacts to be notified when the monitor goes up/down.Multiple alert_contact>ids can be sent like alert_contacts=457_0_0-373_5_0-8956_2_3 where alert_contact>ids are seperated with - and threshold + recurrence are seperated with _. For ex: alert_contacts=457_5_0 refers to 457 being the alert_contact>id, 5 being the threshold and 0 being the recurrence. As the threshold and recurrence is only available in the Pro Plan, they are always 0 in the Free Plan)
            mwindows - optional (the maintenance windows for the monitor which can be mentioned with their IDs like 345-2986-71)
            custom_http_headers - optional (must be sent as a JSON object)
            custom_http_statuses - optional (must be sent as 404:0_200:1 to accept 404 as down and 200 as up)
            ignore_ssl_errors - optional (for ignoring SSL certificate related errors)

        """

    @api_call
    def editMonitor(self):
        """Monitors can be edited using this method.
        Important: The type of a monitor can not be edited (like changing a HTTP monitor into a Port monitor). For such cases, deleting the monitor and re-creating a new one is adviced.

        Parameters:
            id - required (the ID of the monitor to be edited)
            friendly_name - optional
            url - optional
            sub_type - optional
            port - optional
            keyword_type - optional
            keyword_value - optional
            interval - optional (in seconds)
            status - optional (0 for pause, 1 for resume)
            http_username - optional
            http_word - optional
            alert_contacts - optional (the alert contacts to be notified when the monitor goes up/down.Multiple alert_contact>ids can be sent like alert_contacts=457_0_0-373_5_0-8956_2_3 where alert_contact>ids are seperated with - and threshold + recurrence are seperated with _. For ex: alert_contacts=457_5_0 refers to 457 being the alert_contact>id, 0 being the threshold and 0 being the recurrence. As the threshold and recurrence is only available in the Pro Plan, they are always 0 in the Free Plan)
            mwindows - optional (the maintenance windows for the monitor which can be mentioned with their IDs like 345-2986-71)
            custom_http_headers - optional (must be sent as a JSON object)
            custom_http_statuses - optional (must be sent as 404:0_200:1 to accept 404 as down and 200 as up)
            ignore_ssl_errors - optional (for ignoring SSL certificate related errors)

        """

    @api_call
    def deleteMonitor(self):
        """Monitors can be deleted using this method.

        Parameters:
            id - required (the ID of the monitor to be deleted)

        """

    @api_call
    def resetMonitor(self):
        """Monitors can be reset (deleting all stats and response time data) using this method.

        Parameters:
            id - required (the ID of the monitor to be reset)

        """

    @api_call
    def getAlertContacts(self):
        """The list of alert contacts can be called with this method.

        Parameters:
            alert_contacts - optional (if not used, will return all alert contacts in an account. Else, it is possible to define any number of alert contacts with their IDs like: alert_contacts=236-1782-4790)
            offset - optional (used for pagination. Defines the record to start paginating. Default is 0)
            limit - optional (used for pagination. Defines the max number of records to return for the response. Default and max. is 50)

        """

    @api_call
    def newAlertContact(self):
        """New alert contacts of any type (mobile/SMS alert contacts are not supported yet) can be created using this method.
        The alert contacts created using the API are validated with the same way as they were created from uptimerobot.com (activation link for e-mails, etc.).

        Parameters:
            api_key - required
            type - required
            value - required
            friendly_name - optional

        """

    @api_call
    def editAlertContact(self):
        """Alert contacts can be edited using this method.

        Parameters:
            id - required
            friendly_name - optional
            value - optional (can only be used if it is a web-hook alert contact)

        """

    @api_call
    def editAlertContact(self):
        """Alert contacts can be deleted using this method.

        Parameters:
            id - required

        """

    @api_call
    def getMWindows(self):
        """The list of maintenance windows can be called with this method.

        Parameters:
            mwindows - optional (if not used, will return all mwindows in an account. Else, it is possible to define any number of mwindows with their IDs like: mwindows=236-1782-4790)
            offset - optional (used for pagination. Defines the record to start paginating. Default is 0)
            limit - optional (used for pagination. Defines the max number of records to return for the response. Default and max. is 50)

        """

    @api_call
    def newMWindow(self):
        """New maintenance windows can be created using this method.

        Parameters:
            friendly_name - required
            type - required
            value - required (only needed for weekly and monthly maintenance windows and must be sent like 2-4-5 for Tuesday-Thursday-Friday or 10-17-26 for the days of the month)
            start_time - required (the start datetime)
            duration - required (how many minutes the maintenance window will be active for)

        """

    @api_call
    def newMWindow(self):
        """Maintenance windows can be edited using this method.

        Parameters:
            id - required
            friendly_name - optional
            value - optional (only needed for weekly and monthly maintenance windows and must be sent like 2-4-5 for Tuesday-Thursday-Friday)
            start_time - optional (required the start datetime)
            duration - optional (required how many minutes the maintenance window will be active for)

        """

    @api_call
    def newMWindow(self):
        """Maintenance windows can be deleted using this method.

        Parameters:
            id - required

        """

    @api_call
    def getPSPs(self):
        """The list of public status pages can be called with this method.

        Parameters:
            psps - optional (if not used, will return all public status pages in an account. Else, it is possible to define any number of public status pages with their IDs like: psps=236-1782-4790)
            offset - optional (used for pagination. Defines the record to start paginating. Default is 0)
            limit - optional (used for pagination. Defines the max number of records to return for the response. Default and max. is 50)

        """

    @api_call
    def newPSP(self):
        """New public status pages can be created using this method.

        Parameters:
            type - required
            friendly_name - required
            monitors - required (The monitors to be displayed can be sent as 15830-32696-83920. Or 0 for displaying all monitors)
            custom_domain - optional
            word - optional
            sort - optional
            hide_url_links - optional (for hiding the Uptime Robot links and only available in the Pro Plan)
            status - optional
        """

    @api_call
    def editPSP(self):
        """Public status pages can be edited using this method.

        Parameters:
            id - required
            friendly_name - optional
            monitors - optional (The monitors to be displayed can be sent as 15830-32696-83920. Or 0 for displaying all monitors)
            custom_domain - optional
            word - optional
            sort - optional
            hide_url_links - optional (for hiding the Uptime Robot links and only available in the Pro Plan)
            status - optional

        """

    @api_call
    def deletePSP(self):
        """Public status pages can be deleted using this method.

        Parameters:
            id - required

        """


if __name__ == "__main__":
    help(UptimeRobot)
