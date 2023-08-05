## About

This SDK instruments Python web frameworks to capture http requests and auto-generates Postman Live Collections.

The minimum supported version for Python is: 3.7+.


## Installation Process

```
pip install postman-sdk
```


## Initializing the SDK

At the top of your app.py file, before app is initialized, add this.

```python
import postman_sdk as pm

pm.initialize(
    {
        "api_key": "<add-postman-api-key-here>",
        "collection_id": "<add-collection-id-here>"
    }
)
```


## Configuration

**For initialization the SDK, the following values can be configured -**


- **collection_id**: Postman collectionId where requests will be added. This is the id for your live collection.
  - Type: ```string```

- **api_key**: Postman api key needed for authentication. 
  - Type: ```string```

- **debug**: Enable/Disable debug logs.
  - Type: ```boolean```
  - Default: ```False```

- **enable**: Enable/Disable the SDK. Disabled SDK does not capture any new traces, nor does it use up system resources.
  - Type: ```boolean```
  - Default: ```True```

- **truncate_data**: Truncate the request and response body so that no PII data is sent to Postman. This is **enabled** by default. Disabling it sends actual request and response payloads.
  - Example: 
    > Sample payload or non-truncated payload:

    ```JSON
    {
        "first_name": "John",
        "age": 30
    }
    ```

    > Truncated payload:

    ```JSON
    {
        "first_name": {
            "type": "str"
        },
        "age": {
            "type": "int"
        }
    }
    ```
  - Type: ```boolean```
  - Default: ```True```

- **redact_sensitive_data**: Redact sensitive data such as api_keys and auth tokens, before they leave the sdk. This is **enabled** by default, and these are the redaction rules set:
  ```python
    {
        "pm_postman_api_key": r"PMAK-[a-f0-9]{24}-[a-f0-9]{34}",
        "pm_postman_access_key": r"PMAT-[0-9a-z]{26}",
    }
    ```
  - Example:
    ```python
    {
    "redact_sensitive_data": {
        "enable": True(default), 
        "rules": { # This is optional, if the `rules` key is not passed, the default set of rules will be used.
            "<rule name>": "<regex to match the rule>", # such as -
            "basic_auth": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
            },
        }
    }
    ```
  - Type: ```object```

- **ignore_incoming_requests**: List of regexes to be ignored from instrumentation. This rule only applies to endpoints that are **served** by the application/server.
  - Example:
      ```python
      {
          "ignore_incoming_requests": ["knockknock", "^get.*"]
      }
      ```
      The above example, will ignore any endpoint that contains the word "knockknock" in it, and all endpoints that start with get, and contain any characters after that.
  - Type: ```dict```

- **ignore_outgoing_requests**: List of regexes to be ignored from instrumentation. This rule only applies to endpoints that are **called** by the application/server.
  - Example:
      ```python
      {
          "ignore_outgoing_requests": ["knockknock", "^get.*"]
      }
      ```
      The above example, will ignore any endpoint that contains the word "knockknock" in it, and all endpoints that start with get, and contain any characters after that.
  - Type: ```dict```

- **buffer_interval_in_milliseconds**: The interval in milliseconds that the SDK waits before sending data to Postman. The default interval is 5000 milliseconds. This interval can be tweaked for lower or higher throughput systems.
  - Type: ```int```
  - Default: ```5000```

