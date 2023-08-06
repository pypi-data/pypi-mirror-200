import os
import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import json


###############################
# Profile handling
###############################
def get_profile(clsobj, spec_category):
    profile_source = clsobj.args['profile_source']
    if profile_source == "api":
        profile, is_valid, l_msg = get_profile_from_api(clsobj, spec_category)
    elif profile_source == "file":
        profile, is_valid, l_msg = get_profile_from_file(clsobj)
    else:
        raise Exception("profile_source={api/file} must be specified")

    msg = f"Profile source: {profile_source}" + "\n"
    msg += l_msg
    msg += f"Profile: {json.dumps(profile, indent=4)}" + "\n"

    return is_valid, profile, msg

###############################
# API based profile
###############################
def call_api(apicred, urlsuffix):
    msg = ""
    apikey = apicred.get('api_key', apicred.get('apikey'))
    htuser = apicred.get('basicauth', {}).get('user', "")
    htpass = apicred.get('basicauth', {}).get('pass', "")

    # Construct the url
    server = apicred['server']
    if not server.startswith("http"):
        server = "https://" + server
    if server.endswith("/"):
        server = server[:-1]
    if urlsuffix.startswith("/"):
        urlsuffix = urlsuffix[1:]
    url = server + "/" + urlsuffix

    headers = {
        'accept': 'application/json',
        'X-API-Key': apikey,
    }

    msg += f"Calling URL: {url}" + "\n"
    if (htuser == '') and (htpass == ''):
        response = requests.get(url,
                                headers=headers,
                                verify=False,
                                timeout=10)
    else:
        response = requests.get(url,
                                headers=headers,
                                auth=HTTPBasicAuth(htuser, htpass),
                                verify=False,
                                timeout=10)
    is_valid = True if response.status_code == 200 else False
    msg += f"Response: {response.reason}" + "\n"

    return is_valid, response, msg


def load_profile_api(args, spec_category):
    msg = ""

    # API endpoint for anomalies service
    apicred = args['apicred']
    urlsuffix = f"/api/v2/dashboard/specs/"
    is_valid, response, l_msg = call_api(apicred, urlsuffix=urlsuffix)
    msg += l_msg
    if not is_valid:
        return None, is_valid, msg

    # now, loop through to get the app name
    app_name = None
    specs = []
    jdata = response.json()['data']
    for app_id, app_spec in jdata.items():
        if app_id == spec_category:
            for app in app_spec:
                app_name = app['name'] # for now, use the last app, generalize later

                # now, get the specs from the app
                app_name_url = spec_category.split('.')[-1]
                urlsuffix = f"/api/v2/app/{app_name_url}/{urllib.parse.quote(app_name)}/policies"
                is_valid, response, l_msg = call_api(apicred, urlsuffix)
                msg += l_msg
                if not is_valid:
                    continue
                    # return None, is_valid, msg

                specs += response.json()['data']

    spec = {
        "specs": specs
    }

    return spec, is_valid, msg

def get_profile_from_api(clsobj, spec_category):
    """
    Read the profile json from API
    """

    msg = ""

    if (not hasattr(clsobj, "args")):
        raise Exception(
            "'args' transform attribute should be defined"
        )
    for p in ['apicred']:
        if clsobj.args.get(p) == None:
            raise Exception(
                f"'{p}' attribute in args should be defined"
                )

    # call the API to get the anomaly specs
    msg += f"Loading profile from API" + "\n"
    specs, is_valid, l_msg = load_profile_api(clsobj.args, spec_category)
    msg += l_msg

    if specs != None:
        specs = specs["specs"]
        msg += f"Found {len(specs)} policies for spec: {spec_category}" + "\n"

    return specs, is_valid, msg


###############################
# File based profile
###############################
def get_profile_from_file(clsobj):
    """
    Read the profile json from profilespec
    """

    is_valid = False
    msg = ""

    if (not hasattr(clsobj, "profiledir")) and (not hasattr(clsobj, "profilefile")):
        raise Exception(
            "'profiledir' transform attribute should be defined to use default get_profile method"
        )

    paths = []
    if hasattr(clsobj, "profilefile"):
        paths.append(self.profilefile)

    if hasattr(clsobj, "profiledir"):
        paths.extend(
            [
                clsobj.profiledir + "/profile.json",
                clsobj.profiledir + "/profile.yaml",
                clsobj.profiledir + "/profilespec.json",
                clsobj.profiledir + "/profilespec.yaml",
            ]
        )

    profile = None
    for p in paths:
        if not os.path.exists(p):
            continue
        if p.endswith(".json"):
            profile = json.load(open(p))
        elif p.endswith(".yaml"):
            profile = yaml.load(open(p))

    if profile is None:
        raise Exception("Profile could not be found")

    specs = profile.get("specs")
    if specs != None:
        is_valid = True
        msg += f"Found {len(specs)} specs to work on" + "\n"
    else:
        msg += f"No specs to work on" + "\n"

    return specs, is_valid, msg


###############################
# DB handlers
###############################


###############################
# Dataset handlers
###############################
def construct_dataset_list(clsobj, specs):
    if not hasattr(clsobj, 'get_dataset_registry'):
        raise Exception(
            "get_datasets expects get_dataset_registry method"
        )

    # call the overloaded method to get the dataset registry
    registry = clsobj.get_dataset_registry()

    # what are all the datasets in the spec
    spec_datasets = []
    for spec in specs:
        type = spec.get('config', {}).get('source', {}).get('type')
        dataset = spec.get('config', {}).get('source', {}).get('dataset')
        if type != 'registry':
            continue
        if dataset == None:
            continue
        spec_datasets.append(dataset)

    # iterate to keep only the datasets in the spec
    datasets = {}
    for dataset in registry.datasets:
        name = dataset.name
        for subset in dataset.subsets:
            d = f"{name}-{subset['name']}"
            if d in spec_datasets:
                # make a lookup table
                datasets[d] = dataset

    return datasets
