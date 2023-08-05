from ..morphclass import RequestsApi
import morphqs.logging.loghandler as loghandler
import json
import urllib

def add_integration(default_branch, repo_url, integration_name):
    """
    The add_integration function is used to create a new integration in Morpheus.
        It takes three arguments: 
            1) default_branch - the branch that will be checked out by default when cloning the repo (defaults to master)
            2) repo_url - The URL of the repository you want to integrate with Morpheus. This can be either an SSH or HTTPS URL, but it must have read access for Morpheus. 
            3) integration_name - The name of your new integration as it will appear in your list of integrations.
    
    :param default_branch: Set the default branch for the integration
    :param repo_url: Specify the url of the repo to be integrated
    :param integration_name: Find the integration id
    :return: A dictionary, with a key of &quot;success&quot;
    :doc-author: Trelent
    """
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    integrationname = urllib.parse.quote(integration_name)
    intid = cl.get(f"/api/integrations?name={integrationname}").json()
    try: 
        intid = intid["integrations"][0]["id"]
    except IndexError as e:
        intid = None
    if intid is not None: 
        logger.info(f"Integration {integration_name} already exists. Skipping.")
        logger.info(f"Integration ID: {intid}")
        logger.debug(intid)
        return intid
    else:
        logger.info(f"Integration {integration_name} does not exist. Creating.")
        root_int_payload = {"integration": {
                                "refresh": True,
                                "credential": {"type": "local"},
                                "type": "git",
                                "config": {
                                    "defaultBranch": default_branch, #"highered",
                                    "cacheEnabled": False
                                },
                                "name": integration_name, #"Morpheus Quickshots Base Repo",
                                "serviceUrl": repo_url #"https://gitlab.com/jaredlutgen/morpheus_quickshots.git"
                            }}
        logger.debug(f"Creating integration {integration_name} with payload {root_int_payload}")
        resp = cl.post("/api/integrations", data = json.dumps(root_int_payload)).json()
        logger.debug(resp)
        intid = resp["integration"]["id"]
        if resp["success"] == True:
            logger.info(f"Successfully created integration {integration_name}")
        if resp["success"] == False:
            logger.error(f"Failed to create integration {integration_name}")
            logger.error(resp["errors"])
        logger.debug(intid)
        logger.debug(resp)
        return intid