# Buffered Queue

This library basically accepts messages via Post request and stores them in buffered queues in redis unless buffer threshold is achieved. Once achieved all the messages will be pushed to kafka topic that you have set

# Pre Requisite

You need the following to be setup on your machines :-

1) Redis - https://redis.io/download

2) Kakfka - https://kafka.apache.org/quickstart

3) Python >= 1.7.3 https://www.python.org/downloads/

**Note:** Make sure auto-creation of topic is enabled in kafka. It is so by default

# Setting up Buffered Queue

1) `cd /path/to/cloned/directory`

2) `python setup.py install`

**Note:-** Make sure you get a successful install or else report to sahilbathla1@gmail.com

3) `cp config/conf.yaml.example config/conf.yaml`

4) Edit the above config as per your requirement

5) python buffered_queue.py


# Quick Start

1) Add group info for group_id g1 :-

```
redis-cli

set g1:limit 10 # The maximum length of this group

set g1:topic buffer # Kafka Topic to push this message to.

```

2) Send Post Request With Json Data :-

`curl -H "Content-Type: application/json" -X POST -d '{"username":"xyz","group_id":"g1"}'  http://localhost:8082`

3) Once you reach the limit 10 the data will be pushed to kafka


# Contribute

To contribute just fork the repository and open a pull request against master. Few issues you can work at :-

1) Currently there is no security checks on post requests received. Exposes this service to DOS attacks. Add security.

2) Currently there are no logs but just print statement. Add proper logging with stacktrace.

3) Identify and handle further cases which can break this app.

