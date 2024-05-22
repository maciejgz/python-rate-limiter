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

#### Leaky bucket algorithm
The leaky bucket algorithm is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The leaky bucket algorithm works by maintaining a bucket of tokens. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the bucket. If the bucket is empty, the request is queued and throttled to one per second. The leaky bucket algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.

#### Sliding window algorithm
The sliding window algorithm is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The sliding window algorithm works by maintaining a window of tokens. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the window. If the window is empty, the packet is dropped or delayed until a token becomes available. The sliding window algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.

## Configuration

The rate limiter can be configured by setting the following environment variables:
- `RATE_LIMITER_ALGORITHM` - the rate limiting algorithm to use. Available options are:
    - in_memory_token_bucket
    - redis_token_bucket - TODO
    - leaky_bucket - TODO
    - sliding_window - TODO

## Installation

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

To run rate-limiter localy, run the following command:

```bash
$env:RATE_LIMITER_ALGORITHM="redis_token_bucket"; $env:MASTER_NODE="True"; fastapi run main.py --port 8000
```

Params:
- `MASTER_NODE` - if set to `True` the instance will be responsible for refilling the tokens. Default is `False`
- `RATE_LIMITER_ALGORITHM` - the rate limiting algorithm to use. Default is `in_memory_token_bucket`
- `--port` - port on which the API will be available. Default is `8000`

### Docker

#### Run Redis

```bash
docker-compose -f docker/redis.yml up -d 
```

Then you can connect to Redis using the following command:
```bash
 docker exec -it python-rate-limiter-redis redis-cli
```

#### Build the image

```bash
docker build -t rate-limiter:latest .
```

#### Run the container

```bash
docker run --network python-rate-limiter-network -p 8000:8000 -e "REDIS_HOST=python-rate-limiter-redis" -e "MASTER_NODE=True" -e "RATE_LIMITER_ALGORITHM=redis_token_bucket" python-rate-limiter:latest
```