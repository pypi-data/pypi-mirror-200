import requests
import shutil

from via_hub_logistc.model.zephry import TestFolder, TestCycle

class ReportManager():

    def __init__(self):
        self.url = None
        self.token = None

        self.lst_scenarios = []
        self.release_id = None
        self.cycle_date = None
        self.host_id = None
        self.poject_id = None
        self.folder_name = None
        self.router_env = None
        self.cycle_description = None
        self.cycle_interation = None
        self.cycle_status = None
        self.plan_id = None
        self.project_key = None
        self.file_path = None
        self.env_runner = None

    @property
    def lst_scenarios(self):
        return self._lst_scenarios

    @lst_scenarios.setter
    def lst_scenarios(self, value):
        self._lst_scenarios = value

    @property
    def release_id(self):
        return self._release_id

    @release_id.setter
    def release_id(self, value):
        self._release_id = value
    
    @property
    def cycle_date(self):
        return self._cycle_date

    @cycle_date.setter
    def cycle_date(self, value):
        self._cycle_date = value

    @property
    def host_id(self):
        return self._host_id

    @host_id.setter
    def host_id(self, value):
        self._host_id = value

    @property
    def poject_id(self):
        return self._poject_id

    @poject_id.setter
    def poject_id(self, value):
        self._poject_id= value

    @property
    def folder_name(self):
        return self._folder_name

    @folder_name.setter
    def folder_name(self, value):
        self._folder_name= value

    @property
    def router_env(self):
        return self._router_env

    @router_env.setter
    def router_env(self, value):
        self._router_env= value
    
    @property
    def cycle_description(self):
        return self._cycle_description

    @cycle_description.setter
    def cycle_description(self, value):
        self._cycle_description= value

    @property
    def cycle_interation(self):
        return self._cycle_interation

    @cycle_interation.setter
    def cycle_description(self, value):
        self._cycle_interation= value

    @property
    def cycle_status(self):
        return self._cycle_status

    @cycle_status.setter
    def cycle_status(self, value):
        self._cycle_status= value

    @property
    def plan_id(self):
        return self._plan_id

    @plan_id.setter
    def plan_id(self, value):
        self._plan_id= value
    
    @property
    def project_key(self):
        return self._project_key

    @project_key.setter
    def project_key(self, value):
        self._project_key= value
    
    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path= value

    @property
    def env_runner(self):
        return self._env_runner

    @env_runner.setter
    def env_runner(self, value):
        self._env_runner= value

    ### Search key the of project in jira ###
    def get_project_key(self):
        url = self.url + '/rest/api/2/user/search'

        querystring = {"username": self.user}

        headers = {
            "Authorization": f'Basic {self.token}'
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        return response.json()[0]["key"]

    ### Search id the of cycle in jira ###
    def get_cycle_id(self, cycle):

        uri = self.url + f'/testrun/{cycle}?fields=id'

        headers = {
            "Authorization": f'Basic {self.token}'
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()["id"]

    ### Add name the of cycle test in jira ###
    def create_cycle_name(self, project_id: int, release: str):
        uri = self.url + \
            f'/rest/tests/1.0/testrun/search?fields=id,key,name&query=testRun.projectId%20IN%20({project_id})'

        headers = {
            "Authorization": f"Basic {self.key}"
        }

        response = requests.request("GET", uri, headers=headers)

        cycles = response.json()['results']

        count_release = 0

        for cycle in cycles:
            if str(cycle['name']).find(release) > 0:
                count_release = count_release + 1

        return f'{release} | C{count_release + 1}'

    ###Create new folder for test regression ###
    def create_folder(self, folder_name: str, projectKey: str):
        uri = self.url + "/rest/atm/1.0/folder"

        headers = {
            "Authorization": f"Basic {self.key}"
        }

        payload = TestFolder(projectKey, folder_name, "TEST_RUN").__dict__

        requests.request("POST", uri, json=payload, headers=headers)

        return folder_name

    ###Create new cycle for test regression ###
    def create_cycle_test(self, folder_name: str, test_plan: str,  key: str, name_cycle: str, descripption: str, iteration: str, owner: str, cycle_date: str, status: str):

        payload = TestCycle(
            name_cycle,
            descripption,
            key,
            folder_name,
            iteration,
            owner,
            test_plan,
            cycle_date,
            status,
            []
        ).__dict__

        uri = self.url + "/rest/atm/1.0/testrun"

        headers = {
            "Authorization": f"Basic {self.key}"
        }

        response = requests.request("POST", uri, json=payload, headers=headers)

        return response.json()["key"]

    ### Add scenarios to an existing cycle ###
    def save_result_runner_tests(self, cycle: str, list_scenarios: dict):

        for scenario in list_scenarios:
            uri = self.url + \
                f'/rest/atm/1.0/testrun/{cycle}/testcase/{scenario["id"]}/testresult'

            headers = {
                "Authorization": f"Basic {self.key}"
            }

            requests.request('POST', uri, json=scenario["tc"], headers=headers)

    ### Add report the runner for existing cycle  ###
    def save_report_rennur(self, cycle, file_path):

        shutil.make_archive(file_path + '/report', 'zip', file_path)

        uri = self.url + f"/rest/atm/1.0/testrun/{cycle}/attachments"

        headers = {
           "Authorization": f"Basic {self.key}"
        }

        requests.request("POST", uri, files={"report_file": f'{file_path}/report.zip'}, headers=headers)

    ### Get info the of created test case ###
    def get_owner_test_case(self, test_key):

        uri = self.url + f'/rest/atm/1.0/testcase/{test_key}'

        headers = {
           "Authorization": f"Basic {self.token}"
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()["owner"]
    
    ### Get info the of created test case ###
    def get_user(self):

        uri = self.url + f'/rest/atm/2/user/search'

        headers = {
           "Authorization": f"Basic {self.token}"
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()[0]["key"]