# VpnWebSelector

This is a simple web GUI that makes it easy to connect to openvpns. A main goal is,
to make it easy to handle a lot of vpn configurations. This is often the case
if you use a vpn provider like [Astrill](https://www.astrill.com/). If you have
hundrets of vpn configurations it gets annoying to create profiles for them
by hand. With this programm you can just copy all your configuration files in
one folder and your done.

## Installation

```bash
apt-get install openvpn python3
# Download the vpnwebselector
git clone https://github.com/JanoschDeurer/vpnwebselector
```

Now you have to put all the vpn configurations you want to use in the configs
folder and make shure they end with ```.ovpn```. After that you can start the
vpnwebseletor with

```bash
./vpnwebselector.py
```

Note that ```openvpn``` is executed by the script so the executing user must
have the rights to change the network configurations. You can enforce this by
starting the script as root or with sudo.






