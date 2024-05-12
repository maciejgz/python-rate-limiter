# python-rate-limiter

## Description

Playground for analyzing the ways to limit the rate of API calls in Python. The main goal is to create a simple and efficient rate limiter that can be used in any Python project and to test different approaches to rate limiting.
For test purposes simple API writtern in fastapi is used.

## Algorithms used

### Rate limiting
Rate limiting is a technique used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. Rate limiting can be used to prevent denial of service attacks, to prevent spam, and to ensure that the network is used in a fair way.

#### Token bucket algorithm
The token bucket algorithm is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The token bucket algorithm works by maintaining a bucket of tokens. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the bucket. If the bucket is empty, the packet is dropped or delayed until a token becomes available. The token bucket algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.

#### Leaky bucket algorithm
The leaky bucket algorithm is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The leaky bucket algorithm works by maintaining a bucket of tokens. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the bucket. If the bucket is empty, the packet is dropped or delayed until a token becomes available. The leaky bucket algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.

#### Sliding window algorithm
The sliding window algorithm is a rate limiting algorithm that is used to control the rate of traffic sent or received by a network. It is used to prevent abuse of the network and to ensure that the network is used in a fair way. The sliding window algorithm works by maintaining a window of tokens. Each token represents a unit of traffic that can be sent or received by the network. When a packet of traffic is sent or received by the network, a token is removed from the window. If the window is empty, the packet is dropped or delayed until a token becomes available. The sliding window algorithm is a simple and efficient way to control the rate of traffic sent or received by a network.

## Configuration

The rate limiter can be configured by setting the following environment variables:
- `RATE_LIMITER_ALGORITHM` - the rate limiting algorithm to use (token_bucket, leaky_bucket, sliding_window)