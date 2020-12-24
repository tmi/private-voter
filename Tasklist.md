# Development plan

## 1. Single flask app in docker with in-memory SQL with `/create` and `/vote` without any reliability or queing or caching
* (/) Conda env
* (/) Flask app skeleton
* (/) Plain docker image
* () Proper logging and basic config file
* () Proper metrics
* () `Status` endpoint, or rather, readiness + liveness probe
* () `Create` endpoint dummily accepting parameters
* () `Vote` endpoint dummily accepting parameters
* () Externally specifiable config file
* () In-memory DB added to dependencies and initialised with a test write, as a part of readiness probe
* () DDL statements
* () `Vote` endpoint to check first whether the voter is elligible
* () `Create` endpoint to persist its input parameters
* () `Vote` endpoint to persist its input parameters according to poll's settings
* () PyTest + Flask test suite
* () Switch from development to production server

## 2. Docker replaced with docker-compose and external SQL is introduced
* () TBD
* () In-memory cache for the DB reads

## 3. App separated into two plus queue is introduced
* () TBD

## 4. AWS deployment is prepared via ECS, Kinesis, Aurora
* () TBD
* () Load ballancer with https allowed only

## 5. Rewritten to EKS
* () TBD
