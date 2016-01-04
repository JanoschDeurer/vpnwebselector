#!/usr/bin/python3
"""
The VpnWebSelector is a program to easily setup vpn connections via a web gui.
Copyright © 2016 Janosch Deurer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

This program searches for vpn configuration files in the configs folder. It
starts a webserver and provides a web gui to select one of these configs
connect to the corresponding server or reset the connection.

Author: Janosch Deurer
E-Mail: janosch.deurer@geonautik.de

When executing the script, you have to make shure that the executing user hase
the previleges to create openvpn connections, this can for example be reached
by using sudo. The script can be executed by:
    ./vpnwebselector.py


Dependencies:
    The script is witten in python 3 it was tested with python 3.4.3.
    It furthermore uses openvpn it was tested wit openvpn version 2.3.7
"""


import http.server
import os
import re
import json
import subprocess


class VpnWebSelectorHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Handles http requests for the vpnwebselector
    """

    # Disable [too-many-public-methods] error as this is caused by inheritance.
    # pylint: disable=R0904

    def do_GET(self):  # noqa
        if re.match(r"/getConfigs(\?.*|$)", self.path):
            self.response()
            self.get_querry_results()
            return

        if self.path == "/getSelectedConfig":
            self.response()
            if self.server.selected_config:
                self.wfile.write(bytes(self.server.selected_config, "utf-8"))
            else:
                self.wfile.write(bytes("No config selected", "utf-8"))
            return

        if self.path == "/reconnect":
            self.response()
            self.server.connect_to_vpn_server()
            return

        if self.path == "/closeConnection":
            self.response()
            self.server.terminate_vpn_connection()
            self.server.clear_selected_config()
            return

        if re.match(r"/setConfig(\?.*|$)", self.path):
            self.response()
            querry = re.findall(r"/setConfig\?q=(.*)", self.path)[0]
            self.server.selected_config = querry
            return

        super().do_GET()

    def end_headers(self):
        if self.path == "/output.txt":
            self.send_header("Cache-Control",
                             "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        super().end_headers()

    def response(self):
        """
        Makes a standard 200 Response with
        content-type text/html
        :returns: None
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def get_querry_results(self):
        """
        Find all vpn confings in the configs folder that match the description
        given in the get request. The matching is done case insensitive and
        with no typos allowed. The result is returned directly to the client.
        :returns: None
        """
        querry = re.findall(r"/getConfigs\?q=(.*)", self.path)[0]
        files = get_configs()
        results = [f for f in files if querry.lower() in f.lower()]
        results.sort(key=len)
        results = json.dumps(results)
        self.wfile.write(bytes(results, "utf-8"))
        return


class VpnWebSelectorHTTPServer(http.server.HTTPServer):
    """
    HTTPServer for the vpnwebselector
    """
    def __init__(self, server_address, handler_class):
        self._selected_config = ""
        self._last_selected_config = ""
        self._openvpn_process = None
        self._output_file = None
        super().__init__(server_address, handler_class)

    @property
    def selected_config(self):
        """
        Getter for _selected_config
        :returns: _selected_config
        """
        return self._selected_config

    @selected_config.setter
    def selected_config(self, val):
        """
        Setter for _selected_config. This first checks if val is a valid value
        for _selected_config, if so it sets the config and changes the
        connection to the new _selected_config.
        :returns: None
        """
        if val in get_configs():
            self._last_selected_config = self._selected_config
            self._selected_config = val
            if self._last_selected_config != self._selected_config:
                self.connect_to_vpn_server()

    def connect_to_vpn_server(self):
        """
        Starts an openvpn process with _selected_config as config and saves the
        process in _openvpn_process.
        :returns: None
        """
        if self._selected_config is None:
            return
        self.terminate_vpn_connection()
        if self._output_file is not None:
            self._output_file.close()
        self._output_file = open('output.txt', 'w')
        self._openvpn_process = subprocess.Popen(["openvpn", "--config",
                                                  "../configs/" +
                                                  self.selected_config],
                                                 stdout=self._output_file,
                                                 stderr=subprocess.STDOUT)

    def terminate_vpn_connection(self):
        """
        Exits the _openvpn_process if one exists.
        :returns: None
        """
        if self._openvpn_process is None:
            return
        if self._output_file is not None:
            self._output_file.close()
        self._output_file = open('output.txt', 'w')
        self._openvpn_process.terminate()
        self._openvpn_process.wait(timeout=5)
        self._openvpn_process = None

    def clear_selected_config(self):
        """
        Reset the _selected_config to None
        :returns: None
        """
        self._selected_config = None


def get_configs():
    """
    Get a list of all configs in the configs directory ending with .ovpn
    :returns: List with configs
    """
    path = os.path.join(os.path.pardir, "configs")
    return [conf for conf in os.listdir(path) if conf.endswith(".ovpn")]


def main():
    """
    Entrypoint when called as executable
    """
    # Serve only files from www
    os.chdir("www")

    server_class = VpnWebSelectorHTTPServer
    handler_class = VpnWebSelectorHTTPRequestHandler
    server_address = ('', 9000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
