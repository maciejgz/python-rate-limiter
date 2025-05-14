# python-rate-limiter

## Description

Playground for analyzing the ways to limit the rate of API calls in Python. The main goal is to create a simple and efficient rate limiter that can be used in any Python project and to test different approaches to rate limiting.
For test purposes simple API writtern with fastapi ([FastAPI](https://fastapi.tiangolo.com/)).

## Algorithms

### Rate limiting
Rate limiting is a technique used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. Rate limiting can be used to prevent denial of service attacks, to prevent spam, and to ensure that the network is used in a fair way.

#### Token bucket algorithm
The token bucket algorithm is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The token bucket algorithm works by maintaining a bucket of tokens. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the bucket. If the bucket is empty, the packet is dropped or delayed until a token becomes available. The token bucket algorithm is a simple and efficient way to control the rate of traffic sent or received by a network. Token bucket algorithm is implemented in two ways:
- in_memory_token_bucket - [source code](/src/in_memory_token_bucket.py) - single instance of token bucket. Each user can make one request per 15 seconds. Rate limit is set to 100 requests per 15 seconds. Tokens are refilled every 15 seconds.
- redis_token_bucket - [source code](/src/redis_token_bucket.py) - distributed token bucket. Each user can make one request per 15 seconds. Rate limit is set to 100 requests per 15 seconds. Redis is used to store the state of the token bucket. Only one instance of the rate limiter instance is responsible for refilling the tokens. The other instances of the rate limiter instance are responsible for consuming the tokens. The token bucket algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.

Token bucket algorithm requires a single instance of the rate limiter to be responsible for refilling the tokens. This is done by setting the `MASTER_NODE` environment variable to `True`. The other instances of the rate limiter are responsible for consuming the tokens. The token bucket algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.

#### Sliding window algorithm
The sliding window algorithm ([source code](/src/sliding_window.py)) is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The sliding window algorithm works by maintaining a window of tokens. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the window. If the window is empty, the packet is dropped or delayed until a token becomes available. The sliding window algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.
##### Redis sliding window
- Redis sorted set is used to store the state of the sliding window. Rate limit is set to 5 requests per 5 seconds - [Redis sorted set](https://redis.io/docs/latest/develop/data-types/sorted-sets/)
- To add a new request to the sliding window, the timestamp of the request is added to the sorted set as a score. The score is the timestamp of the request. The value is a unique identifier of the request.
- Redis commands used in the sliding window algorithm:
    - ZADD - adds a new request to the sliding window
    - ZRANGEBYSCORE - gets all requests from the sliding window that are within the rate limit
    - ZCARD - gets the number of requests in the sliding window

#### Leaking bucket algorithm - #TODO - implement leaking bucket algorithm with some queue
The leaking bucket algorithm is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The leaking bucket algorithm works by maintaining a bucket of tokens represented by the queue. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the queue. If the queue is full, the packet is dropped or delayed until a token becomes available. The leaking bucket algorithm is a simple and efficient way to control the rate of traffic sent or received by a network. The leaking bucket algorithm is implemented in two ways:
- leaking_bucket_queue - [source code](/src/leaking_bucket_queue.py) - single instance of leaking bucket. Each user can make one request per 15 seconds. Rate limit is set to 100 requests per 15 seconds. Tokens are refilled every 15 seconds.

## Configuration

The rate limiter can be configured by setting the following environment variables:
- `RATE_LIMITER_ALGORITHM` - the rate limiting algorithm to use. Available options are:
    - in_memory_token_bucket
    - redis_token_bucket
    - sliding_window
    - leaking_bucket_queue

## Installation

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

## Pre-requisites
###  Run Redis

```bash
docker-compose -f docker/redis.yml up -d 
```
This command will start a Redis container and create a network called `docker_python-rate-limiter-network` which will be used by the rate limiter container to connect to Redis.

Then you can connect to Redis using the following command:
```bash
 docker exec -it python-rate-limiter-redis redis-cli
```

### Run ActiveMQ
```bash
docker-compose -f docker/activemq.yml up -d 
```


## Run rate limiter locally
To run rate-limiter locally. Params:
- `MASTER_NODE` - if set to `True` the instance will be responsible for refilling the tokens. Default is `False`. Required for `redis_token_bucket` algorithm.
- `RATE_LIMITER_ALGORITHM` - the rate limiting algorithm to use. Default is `in_memory_token_bucket`. Allowed values are `in_memory_token_bucket`, `redis_token_bucket`, `sliding_window`
- `--port` - port on which the API will be available. Default is `8000`

### in_memory_token_bucket
Single instance of token bucket. Each user can make one request per 15 seconds. Tokens are refilled every 15 seconds.
```bash
$env:RATE_LIMITER_ALGORITHM="in_memory_token_bucket"; $env:MASTER_NODE="True"; fastapi run main.py --port 8000
```

### redis_token_bucket
Distributed token bucket which requires a Redis instance to be running. Each user can make one request per 15 seconds. Rate limit is set to 100 requests per 15 seconds. Only one instance of the rate limiter instance is responsible for refilling the tokens. The other instances of the rate limiter instance are responsible for consuming the tokens.
To run the rate limiter as a master node, run the following command:
```bash
$env:RATE_LIMITER_ALGORITHM="redis_token_bucket"; $env:MASTER_NODE="True"; $env:REDIS_HOST="localhost"; fastapi run main.py --port 8000
```

To run the rate limiter as a slave node, run the following command:
```bash
$env:RATE_LIMITER_ALGORITHM="redis_token_bucket"; $env:MASTER_NODE="False"; $env:REDIS_HOST="localhost"; fastapi run main.py --port 8001
```

### sliding_window
Distributed sliding window algorithm which requires a Redis instance to be running. Each user can make one request per 5 seconds. Rate limit is set to 5 requests per 5 seconds for all users.
You can run mulltiple instances of the rate limiter. There is no need to set the `MASTER_NODE` environment variable. The rate limiter will automatically use the Redis instance to store the state of the sliding window.
```bash
$env:RATE_LIMITER_ALGORITHM="sliding_window"; $env:REDIS_HOST="localhost"; fastapi run main.py --port 8000
```

### leaking_bucket_queue
Distributed leaking bucket algorithm which requires a queue to be running. Each user can make one request per 15 seconds. Rate limit is set to 5 requests and one request is consumed every 5 seconds.
```bash
$env:RATE_LIMITER_ALGORITHM="leaking_bucket_queue"; $env:ACTIVEMQ_HOST="localhost"; fastapi run main.py --port 8000
```


### Limitations and Additional Notes

- The `in_memory_token_bucket` algorithm is **not distributed**. It only works within a single application instance. For distributed rate limiting, use the `redis_token_bucket`, `sliding_window` or `leaking_bucket_queue` algorithms.
- The `redis_token_bucket` and `sliding_window` algorithm requires a Redis instance to be running. Make sure to set the `REDIS_HOST` environment variable to the hostname of the Redis instance.
- Make sure to set `MASTER_NODE=True` only for one instance when using the `redis_token_bucket` algorithm to avoid race conditions during token refilling.
- `MASTER_NODE` is not required for `sliding_window`, `in_memory_token_bucket` and 'leaking_bucket_queue' algorithms.
- The `leaking_bucket_queue` algorithm requires a queue to be running. Make sure to set the `ACTIVEMQ_HOST` and `ACTIVEMQ_PORT` environment variables to the hostname of the queue instance.

## Docker
You can build and run the rate limiter in a Docker container or deploy it to Kubernetes.

### Build the image
Build the image used to run the rate limiter:
```bash
docker build -t python-rate-limiter:latest .
```

### Run single container
Run the rate limiter in a single container:
```bash
docker run --network docker_python-rate-limiter-network -p 8000:8000 -e "REDIS_HOST=python-rate-limiter-redis" -e "MASTER_NODE=True" -e "RATE_LIMITER_ALGORITHM=redis_token_bucket" python-rate-limiter:latest
```

### Kubernetes
Predefined Kubernetes deployment files are available in the `k8s` directory. It contains configuration with predefined algorithm and master/slave instances. 
To deploy the rate limiter to Kubernetes, run the following command:
```bash
kubectl apply -f k8s/python-rate-limiter.yml
```
API will be available on port 80: http://localhost:80/

## Testing
There is no API Gateway or load balancer in front of the API. The API is exposed directly to the internet. This is not recommended for production use. To test the API, you should call the service/services directly. The main goal is to test the rate limiting algorithms in a distributed environment.
To test the API, you can use the following command:
```bash
curl -X GET http://localhost:8000
```