import argparse
import requests
from subprocess import Popen, PIPE
import logging
import json

class DailyIndex:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.age = 14
        self.logger = logging.getLogger("DailyIndex")

    def get_search_template_url(self):
        return "http://{}:{}/_template/{}_template".format(self.host, self.port, self.name)
    
    def get_search_alias_name(self):
        return self.name + "_search"
    
    def get_search_template_pattern(self):
        return self.name + "*"
    
    def get_write_alias_name(self):
        return self.name + "_write"
    
    def get_write_index_url(self):
        return "http://{}:{}/<{}-{{now%2Fd}}-1>".format(self.host, self.port, self.name)
    
    def get_write_index_rollover_url(self):
        return "http://{}:{}/{}/_rollover".format(self.host, self.port, self.get_write_alias_name())
    
    def custom_header(self):
        return {"Content-Type": "application/json"}

    def create_search_template(self):
        alias = {}
        alias[self.get_search_alias_name()] = {}
        data = {
            "index_patterns": [self.get_search_template_pattern()],
            "aliases": alias,
        }
        headers = {"Content-Type": "application/json"}
        url = self.get_search_template_url()
        response = requests.put(url, json=data, headers=self.custom_header())
        print(response.content)

    def delete_search_template(self):
        url = self.get_search_template_url()
        response = requests.delete(url)
        print(response.content)

    def get_search_template(self):
        url = self.get_search_template_url()
        response = requests.get(url)
        print(response.content)
 
    def create_write_index_with_alias(self):
        url = self.get_write_index_url()
        aliases = {}
        aliases[self.get_write_alias_name()] = {}
        data = {"aliases": aliases}
        response = requests.put(url, json=data, headers=self.custom_header())
        print(response.content)
    
    def create(self):
        self.create_search_template()
        self.create_write_index_with_alias()

    def rollover(self):
        url = self.get_write_index_rollover_url()
        data = {
            "conditions":
            {
                "max_age":"1d",
                "max_docs":1000000,
                "max_size":"5gb"
            }
        }
        response = requests.post(url, json=data, headers=self.custom_header())
        print(response.content)

    def delete_old_index(self):
        age_filter_list = {
            "filtertype": "age",
            "source": "name",
            "timestring": "%Y.%m.%d",
            "unit": "days",
            "unit_count": self.age,
            "direction": "older"
        }
        pattern_filter_list = {
            "filtertype": "pattern",
            "kind": "prefix",
            "value": "{}-".format(self.name),
        }
        filter_list = [age_filter_list, pattern_filter_list]
         
        args = ["curator_cli", "--host", self.host, "--port", str(self.port), "delete_indices",  "--filter_list", json.dumps(filter_list) ]
        self.run_subprocess(args)

    
    def run_subprocess(self, args):
        p = Popen(args, stderr=PIPE, stdout=PIPE)
        stdout, stderr = p.communicate()
        print('STDOUT={0}'.format(stdout.decode('utf-8')))
        print('STDERR={0}'.format(stderr.decode('utf-8')))

 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="the name of index", default="index")
    parser.add_argument("--host", help="the host of elasticsearch", default="localhost")
    parser.add_argument("--port", help="the port of elasticsearch", default=9200)
    parser.add_argument("--action", help="the action that will be done (create, view, delete, rollover, delete_old)", default="rollover")
    args = parser.parse_args()
    name = args.name 
    host = args.host 
    port = args.port 
    dailyIndex = DailyIndex(args.host, args.port, args.name)
    action =args.action
    if action == "create":
        dailyIndex.create()
    elif action == "delete":
        dailyIndex.delete_search_template()
    elif action == "rollover":
        dailyIndex.rollover()
    elif action == "delete_old":
        dailyIndex.delete_old_index()
    else: 
        dailyIndex.get_search_template()

if __name__ == '__main__':
    main()