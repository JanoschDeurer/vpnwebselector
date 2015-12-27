# vpnwebselector

This is a simple web UI that makes it easy to connect to openvpns. A main goal is,
to make it easy to handle a lot of vpn configurations. This is often the case
if you use a vpn provider like [Astrill](https://www.astrill.com/).

## Installation

```bash
apt-get install openvpn
# Download the vpnwebselector
git clone https://github.com/JanoschDeurer/vpnwebselector
cd vpnwebselector
# make a directory for the vpn configurations
mkdir configs
```

Now you have to put all the vpn configurations you want to use in the configs
folder. After that you can start the vpnwebseletor with

```bash
./vpnwebselector.py
```

Note that openvpn is executed by the script so the executing user must have the
rights to change the network configurations. You can enforce this by starting
the script as root or with sudo.






