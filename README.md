# Locust based TFE load-testing stack

### The tests exercise the TFE API's for the purposes of load testing the system.

### The tests should mirror typical user workloads, which can then be run at scale.

# Start tests with a WebUI, you can start/stop/configure the runs through a UI
```
docker run --rm -p 8089:8089 \
    -e ORGANIZATION_NAME=MY_ORG_NAME \
    -e USER_TOKEN=MY_USER_TOKEN \
    --workdir /test \
    -v $(pwd):/test locustio/locust -f /test/terraform-run.py --host https://MY_TFE_HOST/api/v2
```

# Sample Invocation without a WebUI, 
## user and rate are passed in as CLI arguments
```
docker run --rm /
    -e ORGANIZATION_NAME=MY_ORG_NAME \
    -e USER_TOKEN=MY_USER_TOKEN \
    --workdir /test \
    -v $PWD:/mnt/locust locustio/locust -f /mnt/locust/terraform-run.py --host https://MY_TFE_HOST/api/v2 --headless -u 1 -r 1
```

# TODO
- add a profile for different type of test workloads
- add delete all workspaces job