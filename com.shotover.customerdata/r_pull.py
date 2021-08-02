import os
import asyncio
import json
import aiohttp
import time


# URL vars
url_vars = {
    "JIRA_BASICAUTH": os.environ.get('JIRA_BASICAUTH'),
    "JIRA_WORKSPACEID": os.environ.get('JIRA_WORKSPACEID'),
    "version": "1"
}

# Check variables are set
for var in url_vars:
    if not url_vars[var]:
        print(f"Environment variable: {var} is required. Please set and rerun script.")
        exit()

# Set final url
url = f"https://api.atlassian.com/jsm/insight/workspace/{url_vars['JIRA_WORKSPACEID']}/v{url_vars['version']}/object/navlist/iql"

headers = {
    "Accept": "application/json",
    "Authorization": f"Basic {url_vars['JIRA_BASICAUTH']}",
    "Content-Type": "application/json"
}

# Products & IDs
ProductIDs = {
    "ATOM": (22, 308, 312),
    "ION": (12, 86, 90),
    "ARS-600": (35, 423, 427),
    "ARS-500": (8, 37, 51),
    "ARS-400": (14, 108, 112),
    "ARS-Redbox": (34, 404, 408),
    "ARS-KB-R": (16, 130, 134),
    "ARS-KB-H": (17, 141, 145),
    "GETAC-F110": (28, 359, 480),
    "PAN-GCS": (29, 363, 479),
    "NUC-GCS": (30, 367, 478),
    "RP-1": (31, 375, 379),
    "MC1-CPU-25": (32, 387, 391),
    "EARTH-QUARK": (33, 399, 477)
}

# Root loop
async def get_product_info():
    '''
    Pull customer equipment information from Jira/Insight API using ProductIDs above.

    Parses, formats, and writes data to text file in tuple() 
    '''
    async with aiohttp.ClientSession() as session:
        # create queue
        post_tasks = []
        # prepare coroutines
        for key in ProductIDs.keys():
            post_tasks.append(post(session, key, *ProductIDs[key]))
        # execute them all simultaneously
        resp = await asyncio.gather(*post_tasks)

        with open('r_product_info.txt.python', 'w') as f:
            f.write(json.dumps(resp))


# Setup posts
async def post(session, product_name, product_id, name_id, org_id):
    '''  Generates a coroutine post request given supplied params, which can be gathered and 
    sent simultaneously using asyncio.gather()  '''

    # Using a passed session and given info, generate request payload
    payload = json.dumps({
        "iql": f"objectType = {product_name}",
        "objectTypeId": product_id,
        "page": 1,
        "resultsPerPage": 600,
        "includeAttributes": "true",
        "attributesToDisplay": {
            "attributesToDisplayIds": [
                name_id,
                org_id
            ]
        },
        "objectSchemaId": "4"
    })

    # Form the post request
    async with session.post(
        url,
        headers=headers,
        data=payload
    ) as response:
        # Parse json from response
        r_json = await response.json()
        # Temp storage for object entry processing
        inventory_store = []

        # Loop through each entry in the response
        for i in range(len(r_json["objectEntries"])):
            name = r_json["objectEntries"][i]["attributes"][0]["objectAttributeValues"][0]["displayValue"]
            org = r_json["objectEntries"][i]["attributes"][1]["objectAttributeValues"][0]["displayValue"]
            prod = name.split()[0]
            serial = name.split()[2]
            # Pull relevant info, store in tuple, and stash in inventory_store
            inventory_store.append((prod, serial, org))


        return inventory_store


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_product_info())
    loop.close()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(f'Completed execution in {time.perf_counter() - start} seconds')