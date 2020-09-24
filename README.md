Locust based TFE load-testing stack


# Start tests with a WebUI, you can start/stop/configure the runs through a UI
docker run -p 8089:8089 \
    -v $PWD:/mnt/locust locustio/locust \
    -f /mnt/locust/terraform-run.py \
    --host https://MY_TFE_HOST/api/v2 \

# Sample Invocation against TFC
## This is a
docker run /
    -v $PWD:/mnt/locust locustio/locust /
    -f /mnt/locust/terraform-run.py /
    --host https://MY_TFE_HOST/api/v2 /
    --headless /
    -u 1 /
    -r 1 /



# TODO
- add env vars to point to startup
- add delete all workspaces job