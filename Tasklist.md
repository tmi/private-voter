# Development plan

## 1. Single flask app in docker with in-memory SQL with `/create` and `/vote` without any reliability or queing or caching
* (/) Conda env
* (/) Flask app skeleton
* (/) Plain docker image
* (/) Proper logging and basic config file
* (/) Proper metrics
* (/) `Status` endpoint, or rather, readiness + liveness probe
* (/) `Create` endpoint dummily accepting parameters
* (/) `Vote` endpoint dummily accepting parameters
* (/) In-memory DB added to dependencies and initialised with a test write, as a part of readiness probe
* (/) DDL statements
* (/) `Create` endpoint to check if pollId is free and persist its input parameters
* (/) `Vote` endpoint to check first whether pollName exists and to persist its input parameters according to poll's settings
* (/) `Report` endpoint to return poll's results in an aggregated form
* (/) Externally specifiable config file
* (/) PyTest + Flask test suite
* () Minikube deployment (not supporting multi-instance deployment)

## 2. Docker replaced with docker-compose and external SQL is introduced
* () TBD
* () In-memory cache for the DB reads
* () Prometheus instance for local deployments and testing
* () Extend Minikube deployment accordingly

## 3. App separated into two plus queue is introduced
* () TBD
* () Extend Minikube deployment accordingly

## 4. AWS deployment is prepared via ECS, Kinesis, Aurora
* () TBD
* () Load ballancer with https allowed only

## 5. Rewritten to EKS
* () TBD

## 6. Generic Improvements / Bugs
* (/) Fix packaging and distribution
* () Introduce SQLAlchemy
* () Proper Type Hints
* () Solve the double stdout logging, and pre-logging outputs
* () Fix the pip freeze setuptools bug
* () Specifying the set of actors in advance
* () Throw differential privacy into the mix by allowing "switch of the true vote" to another option with certain probability
* () Decorators for simplified arg-parse and logging handling
* () extend `Report` endpoint with actuall stats analysis
* () separate runtime and test dependencies
