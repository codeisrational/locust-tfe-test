from locust import HttpUser, TaskSet, task, between
import json, random, base64, os

import requests

ORGANIZATION_NAME = os.getenv('ORGANIZATION_NAME')

USER_TOKEN = os.getenv('USER_TOKEN')

HEADERS = {
    'Authorization': f"Bearer {USER_TOKEN}",
    'Content-Type': 'application/vnd.api+json'
}

FILE_UPLOAD_HEADERS = {
    'Authorization': f"Bearer {USER_TOKEN}",
    'Content-Type' : 'application/octet-stream'
}

# represents a basic terraform run
class TerraformRun(TaskSet):

    # executes the entire api driven flow
    @task
    def do_api_workflow(self):

        # reference an archive with our terraform files, hard-coded here as example
        archive_name = "initial.tar.gz"

        # create a workspace
        rand_value = random.randint(0,10000)
        post_path = f"/organizations/{ORGANIZATION_NAME}/workspaces"
        params = {
            "type": "workspaces",
            "attributes": {
                "name": f"workspace-{rand_value}",
                "execution-mode": "remote"
            }
        }

        payload = json.dumps({"data": params})

        workspace_response = self.client.post(post_path, payload, headers=HEADERS )

        # get workspace information
        workspace = json.loads(workspace_response.text)

        # get the workspace ID so we can use it to create a configuration-version
        workspace_id = workspace['data']['id']
        print(workspace)

        # create configuration version
        # returns configuration-version with '.data.attributes.upload-url'
        configuration_version_params = {
            "data": {
               "type": "configuration-versions"
            }
        }
        config_api_path = f"/workspaces/{workspace_id}/configuration-versions"
        response = self.client.post(config_api_path, json.dumps(configuration_version_params), headers=HEADERS)
        upload_url = json.loads(response.text)['data']['attributes']['upload-url']
        
        print(response.status_code)
        print(response.text)
        print(upload_url)

        # upload the archive to TFE
        file_data = open(f"{archive_name}", 'rb').read()
        encoded_file_data = base64.encodebytes(file_data)
        response = requests.put(upload_url, data=encoded_file_data, headers={'Content-Type':'application/octet-stream'})
        
        print(response.status_code)
        print(response.text)

# represents a terraform user
# assign tasks to a user
class TerraformUser(HttpUser):
    tasks = [TerraformRun]

    wait_time = between(10,20)