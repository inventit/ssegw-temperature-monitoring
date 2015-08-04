Temperature Monitoring Application
=======================

## About this
This is a tutoril application to learn how to develop a client application of ServiceSync.
This application measures temperature in Armadillo-IoT and upload it to the ServiceSync server.


## System Requirements
### Supported device and OS
* Armadillo-IoT, AtmarkTechno Inc.
    * Atmark Dist

### ServiceSync
* ServiceSync 2.0 or later

### ServiceSync Clinet
* 1.0.6 or later

### Moat-C SDK
* 1.0.5 or later

## Preparatetion

### Installing Debian

Please install ATDE5 which is development environment for Armadillo-IoT ou your computer. Please refer to the followin URL for more details.

* http://armadillo.atmark-techno.com/armadillo-iot/downloads

### Adding the packages

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

## Build

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

### Deploy

Please deploy the package with ServiceSync WebConsole.

## Version
* 1.0.2
 
## Change History

#### Changes in `1.0.2` (August 3, 2015)

* Migrate the repository from private Bitbucket to public GitHub.
* Change the loggin API (SSE_LOG to MOAT_LOG).

#### Changes in `1.0.1` (April 23, 2015)

* ATDE5 (32bit) support

#### Changes in `1.0.0` (March 16, 2015)

* Initial Release
