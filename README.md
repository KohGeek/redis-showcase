# Redis Showcase with Python

Showcase of Redis with Python client, as requested by UECS3203 Advanced Database Systems. The showcase targets a simple comment box system with username and timestamp.

## Requirements

- Python 3.5+
- Redis Server
  - RedisSearch module
  - RedisJSON module

For Redis server, the program is built to run with the `redis/redis-stack-server` docker image on a local machine, running on the default port.

Install all packages listed in the `requirements.txt`.

The python file defaults to `localhost:6379` for your redis server. If you intend to use it with other addresses, the code will have to be modified.
