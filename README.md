# Script to generate an export file containing kaltura fields for an LMS integration


## Dependency
```sh
$ pip install KalturaApiClient
```
Or download from [Kaltura Python Native Client Library](https://developer.kaltura.com/api-docs/Client_Libraries)


## Configuration
Create a **.cfg** file with the relevant Kaltura information.  
_Example:_  
```
[KALTURA]
PARTNER_ID=1234567890
ADMIN_SECRET=copy_from_kmc
USER_ID=ron.raz@kaltura.com
```


## Execution
Run the script:  
```sh
$ python my.cfg output.csv
```