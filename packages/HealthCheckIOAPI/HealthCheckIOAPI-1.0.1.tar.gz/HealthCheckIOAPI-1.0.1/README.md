# healthcheckioapi
# Description
Simple API binding to assist with using the HealthCheck.IO Ping functionality.
The whole purpose of this project is to simplify the and minimize the amount of code necessary
to perform all the ping functionality available from HealthCheck.IO
# Installation
```
pip install healthcheckioapi
```
# Usage
## Send Normal Ping:
```
import healthcheckio.hc_ping as hc
PING_UUID="THE-UUID-GIVEN-FROM-THE-LINK"
ping = hc.ping(PING_UUID)
ping.ping_send()
```
## Send Fail Ping:
```
import healthcheckio.hc_ping as hc
PING_UUID="THE-UUID-GIVEN-FROM-THE-LINK"
ping = hc.ping(PING_UUID)
ping.ping_error()
```
## Send Start Ping:
```
import healthcheckio.hc_ping as hc
PING_UUID="THE-UUID-GIVEN-FROM-THE-LINK"
ping = hc.ping(PING_UUID)
ping.ping_start()
```
## Send Log Ping:
```
import healthcheckio.hc_ping as hc
PING_UUID="THE-UUID-GIVEN-FROM-THE-LINK"
ping = hc.ping(PING_UUID)
ping.ping_log("THIS IS DATA YOU WANT TO LOG")
```