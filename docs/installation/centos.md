# Installing on CentOS

This has been tested on CentOS 7, 8.

## Install hidapi

``` bash
sudo yum install epel-release
sudo yum update
sudo yum install hidapi
```

> ### Note for CentOS7
>
> If you're having trouble installing hdapi, try installing the epel from the Fedora site as follows:
>
```bash
sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
```

> and try the hdapi install again.

## Install python 3.8

CentOS 7/8 ships with Python 3.6. We need to build version 3.8 (or later if you prefer).

```bash
sudo yum -y groupinstall "Development Tools"
sudo yum -y install openssl-devel bzip2-devel libffi-devel
wget https://www.python.org/ftp/python/3.8.9/Python-3.8.9.tgz
tar xvf Python-3.8.9.tgz 
cd Python-3.8.9/
./configure --enable-optimizations
sudo make altinstall
```

## Upgrade pip

You need to upgrade pip, using pip. In my experience, old versions of pip may fail to properly install some of the required Python dependencies.

```bash
python3.8 -m pip install --upgrade pip
```

## Configure access to Elgato devices

The following will create a file called `/etc/udev/rules.d/70-streamdeck.rules` and add the following text to it: `SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"`. Creating this file adds a udev rule that provides your user with access to USB devices created by Elgato.

```bash
sudo sh -c 'echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0fd9\", TAG+=\"uaccess\"" > /etc/udev/rules.d/70-streamdeck.rules'
```

For the rule to take immediate effect, run the following command:

```bash
sudo udevadm trigger
```

If the software is having problems later to detect the Stream Deck, you can try unplugging/plugging it back in.

## Install Stream Deck UI

### From Pypi with pip

```bash
python3.8 -m pip install streamdeck-linux-gui --user
```

### From Surce

Please make sure you have followed the steps below untill the **Install Stream Deck UI section** before continuing.

The steps to install from source can be found [here](source.md)

### Launch the Streamdeck UI

```bash
streamdeck
```

See [troubleshooting](../troubleshooting.md) for tips if you're stuck.
