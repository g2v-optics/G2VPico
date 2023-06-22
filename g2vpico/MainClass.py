'''
Copyright 2021 G2V Optics

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation 
     and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
'''

import traceback
import socket
import json

class G2VPico():
    '''
    A class used to represent a G2V Pico
    '''
    __DEFAULT_PORT_NUMBER = 50000

    def __init__(self, ip_address, pico_id):
        '''
        Parameters
        ----------
        ip_addres : str
            The IP address of the Pico on the network

        pico_id : str
            The 16 character ID of the Pico
        '''
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ip_address = ip_address
        self._id = str(pico_id)

        init_success = True
        try:
            self._socket.connect((self._ip_address, G2VPico.__DEFAULT_PORT_NUMBER))
        except ConnectionRefusedError:
            init_success = False

        if not init_success:
            raise ConnectionRefusedError(f"Connection to PICO at {ip_address} refused")

        self._channel_count = self.__get_channel_count()
        self._channel_list = self.__get_channel_list()

        if self._channel_count is None or self._channel_list is None:
            raise Exception("Instance can not be initialized")

    def __repr__(self):
        return f"PICO {self._id} at {self._ip_address}"   

    def __dir__(self):
        restricted_list = []
        restricted_list.append("id")
        restricted_list.append("channel_count")
        restricted_list.append("channel_list")

        restricted_list.append("get_channel_value")
        restricted_list.append("set_channel_value")
        restricted_list.append("clear_channels")
        restricted_list.append("get_channel_limit")
        restricted_list.append("get_spectrum")
        restricted_list.append("set_spectrum")
        restricted_list.append("get_channel_wavelength_range")
        restricted_list.append("get_global_intensity")
        restricted_list.append("set_global_intensity")
        restricted_list.append("turn_off")
        restricted_list.append("turn_on")
        restricted_list.append("is_fixture_on")

        return restricted_list

    @property
    def id(self):
        '''
        The ID of the Pico used to intialize the object
        '''
        return self._id
    
    @property
    def channel_count(self):
        '''
        The number of channels available in the Pico
        '''
        return self._channel_count
    
    @property
    def channel_list(self):
        '''
        A list of the available channels in the Pico
        '''
        return self._channel_list

    ### Private Internal Methods    

    def __error_handler(self, error, command):
        if "Pico ID invalid" in error:
            raise RuntimeError("Pico ID is invalid")
        if "Command type invalid" in error:
            raise NotImplementedError(f"Command {command} is not implemented")
        if "Pico is not Variable" in error:
            raise RuntimeError("Operation not allowed in Fixed Picos")
        if "Pico API not enabled" in error:
            raise RuntimeError("Pico API not enabled")
        
        raise Exception(f"Unknown error occurred: {error}")

    def __send_cmd(self, cmd):

        try:
            self._socket.sendall(json.dumps(cmd).encode('utf-8'))
        except Exception as e:
            print(f"Failed to send cmd {cmd} - {e} - {traceback.format_exc()}")
            return None

        data = self._socket.recv(1024)
        data = data.decode('utf-8')
        if data is not None:
            return json.loads(data)

        return None


    def __get_channel_count(self):
        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'get_channel_count'
        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            error = response.get('error', None)
            value = response.get('channel_count', None)

            if error is not None:
                self.__error_handler(error, new_cmd)
                
            if new_cmd == cmd['cmd']:
                return value

        return None

    def __get_channel_list(self):
        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'get_channel_list'
        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            error = response.get('error', None)
            value = response.get('channel_list', None)

            if error is not None:
                self.__error_handler(error, new_cmd)

            if new_cmd == cmd['cmd']:
                int_list = [int(x) for x in value]
                return int_list

        return None

    
    def __get_channel_check(self, channel):
        '''Internal method for verifying that a channel is valid and converting to int'''
        try:
            channel = int(channel)
        except Exception as exc:
            raise ValueError(f"Channel type of {channel} is invalid") from exc

        if channel not in self._channel_list:
            raise ValueError(f"A channel value of {channel} is invalid")

        return channel


    def get_channel_value(self, channel):
        '''
        Returns the current PWM value of the channel

        Parameters
        ----------
        channel : str, int
            The channel number in the range [1, channel_count]

        Returns
        -------
        int
            The current value of the channel in the range [0, 4096]

        Exceptions
        ----------
        ValueError
            Raised when the channel parameter is an invalid type
        '''
        channel = self.__get_channel_check(channel)

        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'get_channel_value'
        cmd['channel'] = channel

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            channel = response.get('channel')
            error = response.get('error', None)
            value = response.get('value', None)

            if error is not None:
                self.__error_handler(error, new_cmd)

            if new_cmd == cmd['cmd']:
                return value

        return None


    def set_channel_value(self, channel, value):
        '''
        Sets the chosen channel to the specified value.

        Parameters
        ----------
        channel : str, int
            The channel number in the range [1, channel_count]

        value : str, int, float
            The value to set the chosen channel to in the range [0, channel_limit]

        Returns
        -------
        bool
            True if the channel has been set to the new value
            False if the channel has not been changed

        Exceptions
        ----------
        ValueError
            Raised when the channel parameter is an invalid type
        
        ValueError
            Raised when the channel is not in the range [0, channel_count]

        ValueError
            Raised when the value parameter is an invalid type
        '''
        channel = self.__get_channel_check(channel)

        try:
            value = int(value)
        except Exception as exc:
            raise ValueError(f"Value type of {value} is invalid") from exc

        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'set_channel_value'
        cmd['channel'] = channel
        cmd['value'] = value

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            channel = response.get('channel')
            error = response.get('error', None)
            result = response.get('result', None)

            if error is not None:
                self.__error_handler(error, new_cmd)

            if new_cmd == cmd['cmd']:
                return result

        return None


    def clear_channels(self):
        '''
        Set all channels in the Pico to a value of 0

        Returns
        -------
        bool
            True when all channels have been set to 0
        '''
        result_array = {}
        for channel in self._channel_list:
            result_array[channel] = self.set_channel_value(channel,0)

        return True


    def get_channel_limit(self, channel):
        '''
        Returns the maximum limit [0-4096] of the channel.

        This limit is the maximum value that can be used when setting
        The channel value.

        Parameters
        ----------
        channel : str, int
            The channel number in the range [1, channel_count]

        Returns
        -------
        int
            The maximum limit of the channel in the range [0, 4096]

        Exceptions
        ----------
        ValueError
            Raised when the channel parameter is an invalid type
        
        ValueError
            Raised when the channel is not in the range [0, channel_count]
        '''
        channel = self.__get_channel_check(channel)

        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'get_channel_limit'
        cmd['channel'] = channel

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            channel = response.get('channel')
            error = response.get('error', None)
            limit = response.get('limit', None)

            if error is not None:
                self.__error_handler(error, new_cmd)

            if new_cmd == cmd['cmd']:
                return limit

        return None


    def get_spectrum(self):
        '''
        Get the current spectrum as a list of dict itmes

        Returns
        -------
        list
            A list of dict items channel and value keys forming
            the current spectrum in the Pico.
        '''
        spectrum_array = []

        for channel in self._channel_list:
            spectrum_dict = {}
            spectrum_dict['channel'] = str(channel)
            spectrum_dict['value'] = self.get_channel_value(channel=channel)

            spectrum_array.append(spectrum_dict)

        return spectrum_array


    def set_spectrum(self, channel_list):
        '''
        Load in a spectrum either as a json string or a dictionary

        Parameters
        ----------
        channel_list : str, list
            str - A JSON formatted string contain channels and their corresponding values
            list - A list of dict objects containing 'channel' and 'value' keys

        Returns
        -------
        bool
            True if the new spectrum has been loaded

        Exceptions
        ----------
        ValueError
            If the spectrum data in channel_list is invalid when of str type

        ValueError
            If the type of channel_list is invalid
            
        ValueError
            Raised when the channel value is an invalid type
        
        ValueError
            Raised when the channel is not in the range [0, channel_count]
        '''
        spectrum_list = []
        if isinstance(channel_list, str):
            load_good = True
            try:
                spectrum_list = json.loads(channel_list)
            except Exception:
                load_good = False

            if not load_good:
                raise ValueError("Spectrum data could not be loaded")

        elif isinstance(channel_list, list):
            spectrum_list = channel_list
        else:
            raise ValueError(f"Spectrum data of type {channel_list} is invalid")

        for item in spectrum_list:
            channel = item.get('channel', None)
            value = item.get('value', None)

            result_array = {}
            if channel and (value or value == 0):
                result_array[channel] = self.set_channel_value(channel=channel, value=value)

        return True


    def get_channel_wavelength_range(self, channel):
        '''
        Returns the minimum and maximum wavelength values for a channel in nm

        Parameters
        ----------
        channel : str, int
            The channel number in the range [1, channel_count]

        Returns
        -------
        list
            A list where index 0 is the minimum wavelength and index 1 is the maximum wavelength
            Units are nm

        Exceptions
        ----------
        ValueError
            Raised when the channel parameter is an invalid type
        
        ValueError
            Raised when the channel is not in the range [0, channel_count]

        '''
        channel = self.__get_channel_check(channel)

        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'get_channel_range'
        cmd['channel'] = channel

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            error = response.get('error', None)

            if error is not None:
                self.__error_handler(error, new_cmd)

            if new_cmd == cmd['cmd']:
                x_low = response.get('x_low', None)
                x_high = response.get('x_high', None)

                return [x_low, x_high]


        return None

    def get_global_intensity(self):
        '''
        Returns the global intensity that is applied to all channels

        Returns
        -------
        float
            A value between 0.0 and 100.0 where 100.0 means all channels are fully on
            and a value of 0.0 means all channels are 0.
        '''
        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'get_global_intensity'

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            error = response.get('error', None)

            if error is not None:
                raise Exception(error)

            if new_cmd == cmd['cmd']:
                return response.get('global_intensity', None)
        return None

    def set_global_intensity(self, value):
        '''
        Sets the global intensity that is applied to all channels.
        Note that the new global intensity will take effect immediately.

        Parameters
        ----------
        value : float
            The value of the new global intensity in the range [0.0, 100.0]

        Returns
        -------
        bool
            True if the global intensity has been set successfully
            False if the global intensity was not changed
        '''
        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'set_global_intensity'
        cmd['global_intensity'] = value

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            error = response.get('error', None)

            if error is not None:
                raise Exception(error)

            if new_cmd == cmd['cmd']:
                return response.get('result', None)
        return None


    def turn_off(self):
        '''
        Turns the fixture off while preserving channel values

        Returns
        -------
        bool
            True if the fixture was turned off
            False if the fixture failed to turn off
        '''
        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'set_fixture_on'
        cmd['fixture_on'] = False

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            error = response.get('error', None)

            if error is not None:
                raise Exception(error)

            if new_cmd == cmd['cmd']:
                return response.get('result', None)
        return None


    def turn_on(self):
        '''
        Turns the fixture on with previously stored spectrum

        Returns
        -------
        bool
            True if the fixture was turned on and channels set to their value
            False if the fixture failed to turn on
        '''
        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'set_fixture_on'
        cmd['fixture_on'] = True

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            error = response.get('error', None)

            if error is not None:
                raise Exception(error)

            if new_cmd == cmd['cmd']:
                return response.get('result', None)
        return None


    def is_fixture_on(self):
        '''
        Returns whether the fixture is on or off
    
        Returns
        -------
        bool :
            True if the fixture is on
            False if the fixture is off
        '''
        cmd = {}
        cmd['command'] = 'api'
        cmd['pico_id'] = self._id
        cmd['cmd'] = 'get_fixture_on'

        response = self.__send_cmd(cmd)

        if response is not None:
            new_cmd = response.get('cmd')
            error = response.get('error', None)

            if error is not None:
                raise Exception(error)

            if new_cmd == cmd['cmd']:
                return response.get('fixture_on', None)
        return None
