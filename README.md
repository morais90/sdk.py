<p align="center">
  <img width="300" src="./assets/logo.png" alt="sdk.py logo">
</p>

**sdk.py** is a high-level library to help you create SDK interfaces for your API.

```python
from sdk import API, Collection, Endpoint, HTTPMethod

class UserCollection(Collection):
    all = Endpoint(name="")
    add = Endpoint(name="", http_method=HTTPMethod.POST)
    get = Endpoint(name=":id")
    update = Endpoint(name=":id", http_method=HTTPMethod.PUT)
    remove = Endpoint(name=":id", http_method=HTTPMethod.DELETE)


class ReqResAPI(API):
    users = UserCollection()

    class Meta:
        base_url = "https://reqres.in/api"

>>> reqres = ReqResAPI()
>>> request = reqres.users.add()
>>> request.json().data
{'id': '606', 'createdAt': '2021-11-17T13:50:01.397Z'}
```

[![Test](https://github.com/morais90/sdk.py/actions/workflows/test.yml/badge.svg)](https://github.com/morais90/sdk.py/actions/workflows/test.yml)

## :heavy_check_mark: What you're going to find in this library

- [x] A high level interface to create your SDK client.
- [ ] A layer of validation of inputs and outputs in client-side.
- [ ] A Python typing definition of your API.
