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

#### Sliding window algorithm
The sliding window algorithm is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The sliding window algorithm works by maintaining a window of tokens. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the window. If the window is empty, the packet is dropped or delayed until a token becomes available. The sliding window algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.
##### Redis sliding window
- Redis sorted set is used to store the state of the sliding window. Rate limit is set to 5 requests per 5 seconds - [Redis sorted set](https://redis.io/docs/latest/develop/data-types/sorted-sets/)
- To add a new request to the sliding window, the timestamp of the request is added to the sorted set as a score. The score is the timestamp of the request. The value is a unique identifier of the request.
- Redis commands used in the sliding window algorithm:
    - ZADD - adds a new request to the sliding window
    - ZRANGEBYSCORE - gets all requests from the sliding window that are within the rate limit
    - ZCARD - gets the number of requests in the sliding window

## Configuration

The rate limiter can be configured by setting the following environment variables:
- `RATE_LIMITER_ALGORITHM` - the rate limiting algorithm to use. Available options are:
    - in_memory_token_bucket
    - redis_token_bucket
    - sliding_window

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


## Run rate limiter locally
To run rate-limiter locally, run the following command:

```bash
$env:RATE_LIMITER_ALGORITHM="redis_token_bucket"; $env:MASTER_NODE="True"; fastapi run main.py --port 8000
```

Params:
- `MASTER_NODE` - if set to `True` the instance will be responsible for refilling the tokens. Default is `False`
- `RATE_LIMITER_ALGORITHM` - the rate limiting algorithm to use. Default is `in_memory_token_bucket`. Allowed values are `in_memory_token_bucket`, `redis_token_bucket`, `sliding_window`
- `--port` - port on which the API will be available. Default is `8000`

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
