Temperature Monitoring Application
=======================

## About this
This is a tutoril application to learn how to develop a client application of ServiceSync.
This application measures temperature in Armadillo-IoT and upload it to the ServiceSync server.


## System Requirements
### Supported device and OS
* Armadillo-IoT, AtmarkTechno Inc.
    * Atmark Dist
* Raspberry Pi
    * Rasbian

### ServiceSync
* ServiceSync 2.0 or later

### ServiceSync Clinet
* 1.0.6 or later

### Moat-C SDK
* 1.0.5 or later

## Preparatetion

### Installing development environment

#### Armadillo-IoT

Please install ATDE5 which is development environment for Armadillo-IoT ou your computer. Please refer to the followin URL for more details.

* http://armadillo.atmark-techno.com/armadillo-iot/downloads

#### Raspberry Pi

Please build an application on Respberry Pi itself.

### Adding the packages

#### Armadillo-IoT

Please execute the followng commands to add packages required by ServiceSync Client development.

```
$ sudo apt-get update
$ sudo apt-get install -y --force-yes \
	git \
	mercurial\ 
	build-essential \
	gyp \
	zip \
	libssl-dev \
	libz-dev \
	libxml2-dev \
	libev-dev \
	uuid \
	uuid-dev \
	gcc-multilib \
	libreadline-dev \
	libudev-dev \
	openjdk-7-jdk
$ curl -O http://ftp.jp.debian.org/debian/pool/main/libe/libev/libev4_4.11-1_armel.deb
$ curl -O http://ftp.jp.debian.org/debian/pool/main/libe/libev/libev-dev_4.11-1_armel.deb
$ sudo dpkg-cross --build  --arch armel libev4_4.11-1_armel.deb
$ sudo dpkg-cross --build  --arch armel libev-dev_4.11-1_armel.deb
$ sudo dpkg -i libev4-armel-cross_4.11-1_all.deb libev-dev-armel-cross_4.11-1_all.deb
```

#### Raspberry Pi

```
$ sudo apt-get update
$ sudo apt-get install -y --force-yes \
	git \
	mercurial\ 
	build-essential \
	gyp \
	zip \
	libssl-dev \
	libz-dev \
	libxml2-dev \
	libev-dev \
	uuid \
	uuid-dev \
	libreadline-dev \
	libudev-dev \
	openjdk-7-jdk
```

## Making package

### Getting the source code.

Clone the source code from GitHub.
```
$ git clone https://github.com/inventit/ssegw-temperature-monitoring.git
Cloning into 'ssegw-temperature-monitoring'...
remote: Counting objects: 71, done.
remote: Compressing objects: 100% (57/57), done.
remote: Total 71 (delta 8), reused 71 (delta 8), pack-reused 0
Unpacking objects: 100% (71/71), done.
Checking connectivity... done.
```

`ssegw-temperature-monitoring` will be created. Thereafter it is described as ${APP_ROOT}.

### Platform certificate

Copy your platform certificate, `moat.pem` into `{$APP_ROOT}/certs`.
If you don't have a platform certificate, please contact to the administrator of ServiceSync server.

### Getting the token

Please execute the following commands to get the token to sign your application package.
```
$ cd ${APP_ROOT}
$ export SSDMS_PREFIX="YOUR SERVICESYNC DMS URL"
$ export APP_ID="YOUR APPLICATION ID"
$ export CLIENT_ID="YOUR CLIENT ID"
$ export CLIENT_SECRET="YOUR PASSWORD"
$ export TOKEN=`curl -v "${SSDMS_PREFIX}/moat/v1/sys/auth?a=${APP_ID}&u=${CLIENT_ID}&c=${CLIENT_SECRET}" | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' | grep -w 'accessToken' | cut -d"|" -f2 | sed -e 's/^ *//g' -e 's/ *$//g'`
$ curl -v -o token.bin -L "${SSDMS_PREFIX}/moat/v1/sys/package/temperature-monitoring?token=${TOKEN}&secureToken=true"
```

### Build

#### Armadillo-IoT

```
$ cd ${APP_ROOT}
$ export CROSS=arm-linux-gnueabi-
$ export CC=${CROSS}gcc
$ export CXX=${CROSS}g++
$ export AR=${CROSS}ar
$ export LD=${CROSS}ld
$ export RANLIB=${CROSS}ranlib
$ export STRIP=${CROSS}strip
$ ./configure --dest-cpu=arm
$ make
$ make package
```
Geteway package `temperature-monitoring_${VERSION]_arm.zip` for Armadillo-IoT will be created.

#### Raspberry Pi

```
$ cd ${APP_ROOT}
$ ./configure --dest-cpu=arm --product=RaspberryPi
$ make
$ make package
```
Geteway package `temperature-monitoring_${VERSION]_arm.zip` for Armadillo-IoT will be created.

## Deploy

Please deploy the package with ServiceSync WebConsole. After that, install it into your gateway device.
Also, Server Package must be deployed in advance.


## How to use

__CAUTION__

* In case of using Raspberry Pi, make sure to connect a USB keyboard to Raspberry Pi and never connect other input devices (e.g. USB mouse).

Press SW1 on the Armadillo-IoT to start monitoring. If you are using Raspberry Pi, plase press "1" key instead of SW1.


Scripts for remote control and reporting are provided. You are able to find them in ${APP_ROOT}/REST-cli

First of all, rename `dot.env` to `.env` and fill in your application authentication information. Then run the following command to apply configuration.

```
$ . .env
```

__TIPS__

* If Server Package and Gateway Package were deployed by PP (Platform Provider), please input PP's Application-Id instead of your Application-Id i.e. PU's ID.

To start monitoring, please exexute the followng command.
```
$ ./monitoring.py stop
{
  "activatedAt": "Fri, 25 Sep 2015 05:55:10 +0000",
  "arguments": {
    "command": "stop",
    "uid": "2c9f8e444fa55d25014facc36c040b67"
  },
  "expiredAt": "Mon, 21 Jan 2100 13:05:55 +0000",
  "jobServiceId": "urn:moat:f90366b0-a8e0-4f37-a099-f0050bb85c7b:temperature-monitoring:startstop-monitoring:1.0.0",
  "name": "RSP:SN:00000000a4c1a9a3",
  "uid": "2c9f8e444ffedd3301500311d1c73a58"
}
```

Also, you are able to start monitoring with the followng command.
```
$ ./monitoring.py start
{
  "activatedAt": "Fri, 25 Sep 2015 05:58:02 +0000",
  "arguments": {
    "command": "start",
    "uid": "2c9f8e444fa55d25014facc36c040b67"
  },
  "expiredAt": "Mon, 21 Jan 2100 13:05:55 +0000",
  "jobServiceId": "urn:moat:f90366b0-a8e0-4f37-a099-f0050bb85c7b:temperature-monitoring:startstop-monitoring:1.0.0",
  "name": "RSP:SN:00000000a4c1a9a3",
  "uid": "2c9f8e444ffedd33015003146ff83a63"
}
```

To report the captured data, please execute the following command.
```
$ ./report.py
"timestampe", "temperature"
"2015-09-25 13:17:44.078", 46.54
"2015-09-25 13:17:54.087", 46.002
"2015-09-25 13:18:04.090", 46.002
"2015-09-25 13:18:14.100", 45.464
"2015-09-25 13:18:24.110", 46.002
"2015-09-25 13:18:34.120", 46.54

... (snip) ...
```



## Version
* 1.0.3
 
## Change History

#### Changes in `1.0.3` (September 25, 2015)

* Raspberry Pi support

#### Changes in `1.0.2` (August 3, 2015)

* Migrate the repository from private Bitbucket to public GitHub.
* Change the loggin API (SSE_LOG to MOAT_LOG).

#### Changes in `1.0.1` (April 23, 2015)

* ATDE5 (32bit) support

#### Changes in `1.0.0` (March 16, 2015)

* Initial Release
