#!/usr/bin/python3
import http.server
import os
import re
import json
import subprocess


class VpnWebSelectorHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    """Docstring for VpnWebSelectorHTTPRequestHandler. """

    def do_GET(self):  # noqa
        if re.match("/getConfigs(\?.*|$)", self.path):
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

        if re.match("/setConfig(\?.*|$)", self.path):
            self.response()
            querry = re.findall("/setConfig\?q=(.*)", self.path)[0]
            self.server.selected_config = querry
            return

        super().do_GET()

    def response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def get_querry_results(self):
        querry = re.findall("/getConfigs\?q=(.*)", self.path)[0]
        files = self.server.get_configs()
        results = [f for f in files if querry.lower() in f.lower()]
        results.sort(key=len)
        results = json.dumps(results)
        self.wfile.write(bytes(results, "utf-8"))
        return


class VpnWebSelectorHTTPServer(http.server.HTTPServer):

    """Docstring for VpnWebSelectorHTTPServer. """

    def __init__(self, server_address, handler_class):
        """TODO: to be defined1. """
        self._selected_config = ""
        self._last_selected_config = ""
        self._openvpn_process = None
        self._output_file = None
        super().__init__(server_address, handler_class)

    def get_configs(self):
        path = os.path.join(os.path.pardir, "configs")
        return [conf for conf in os.listdir(path) if conf.endswith(".ovpn")]

    @property
    def selected_config(self):
        return self._selected_config

    @selected_config.setter
    def selected_config(self, val):
        if val in self.get_configs():
            self._last_selected_config = self._selected_config
            self._selected_config = val
            if self._last_selected_config != self._selected_config:
                self.connect_to_vpn_server()

    def connect_to_vpn_server(self):
        if self._selected_config is None:
            return
        self.terminate_vpn_connection()
        self._output_file = open('../output.txt', 'w')
        self._openvpn_process = subprocess.Popen(["openvpn", "--config",
                                                  "../configs/" +
                                                  self.selected_config],
                                                 stdout=self._output_file,
                                                 stderr=subprocess.STDOUT)

    def terminate_vpn_connection(self):
        if self._openvpn_process is None:
            return
        self._openvpn_process.terminate()
        self._openvpn_process.wait(timeout=5)
        self._openvpn_process = None

    def clear_selected_config(self):
        self._selected_config = ""


def main():
    os.chdir("www")

    server_class = VpnWebSelectorHTTPServer
    handler_class = VpnWebSelectorHTTPRequestHandler
    server_address = ('', 9000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
