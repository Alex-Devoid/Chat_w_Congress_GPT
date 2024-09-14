import requests
from fastapi import HTTPException


BASE_URL = "https://api.congress.gov/v3"

def get_member_details(member_id, api_key=None):
    """
    Fetch detailed information about a specific member of Congress by ID.
    :param member_id: The ID of the member.
    :param api_key: The API key for authentication.
    :return: A dictionary containing the member's details.
    """
    url = f"{BASE_URL}/member/{member_id}"
    response = requests.get(url, params={"api_key": api_key})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching member details")
    return response.json()

def search_members(api_key=None, **kwargs):
    """
    Search for members of Congress using optional query parameters.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit', etc.
    :return: A dictionary containing the list of members.
    """
    url = f"{BASE_URL}/member"
    
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    # print(response.message)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching members")
    return response.json()


def get_bill_details(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch detailed information about a specific bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format'.
    :return: A dictionary containing the bill's details.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill details")
    return response.json()

def get_bill_actions(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of actions on a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of actions.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/actions"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill actions")
    
    # Ensure response has the expected structure
    return response.json()

def get_bill_amendments(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of amendments to a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of amendments.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/amendments"
    params = {"api_key": api_key}
    params.update(kwargs)
    print('hi')
    response = requests.get(url, params=params)
    print(" get_bill_amendments response: ")
    print(response)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill amendments")
    return response.json()

def get_bill_committees(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of committees associated with a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of committees.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/committees"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill committees")
    return response.json()

def get_bill_cosponsors(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of cosponsors on a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of cosponsors.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/cosponsors"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill cosponsors")
    return response.json()

def get_bill_related_bills(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of related bills to a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of related bills.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/relatedbills"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching related bills")
    return response.json()

def get_bill_subjects(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of legislative subjects on a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of subjects.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/subjects"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill subjects")
    return response.json()

def get_bill_summaries(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of summaries for a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of summaries.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/summaries"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill summaries")
    return response.json()

def get_bill_text_versions(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of text versions for a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of text versions.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/text"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill text versions")
    return response.json()

def get_bill_titles(congress, bill_type, bill_number, api_key, **kwargs):
    """
    Fetch the list of titles for a specified bill.

    :param congress: The congress number.
    :param bill_type: The type of bill (e.g., hr, s, hjres, etc.).
    :param bill_number: The bill's assigned number.
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of titles.
    """
    url = f"{BASE_URL}/bill/{congress}/{bill_type}/{bill_number}/titles"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching bill titles")
    return response.json()

def get_committee_prints(congress, chamber, api_key, **kwargs):
    """
    Fetch a list of committee prints filtered by the specified congress and chamber.

    :param congress: The congress number.
    :param chamber: The chamber name (house, senate, or nochamber).
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of committee prints.
    """
    url = f"{BASE_URL}/committee-print/{congress}/{chamber}"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching committee prints")
    return response.json()

def get_committee_meetings(congress, chamber, api_key, **kwargs):
    """
    Fetch a list of committee meetings filtered by the specified congress and chamber.

    :param congress: The congress number.
    :param chamber: The chamber name (house, senate, or nochamber).
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of committee meetings.
    """
    url = f"{BASE_URL}/committee-meeting/{congress}/{chamber}"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching committee meetings")
    return response.json()

def get_house_communications(congress, communication_type, api_key, **kwargs):
    """
    Fetch a list of House communications filtered by the specified congress and communication type.

    :param congress: The congress number.
    :param communication_type: The type of communication (ec, ml, pm, pt).
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of House communications.
    """
    url = f"{BASE_URL}/house-communication/{congress}/{communication_type}"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching House communications")
    return response.json()

def get_senate_communications(congress, communication_type, api_key, **kwargs):
    """
    Fetch a list of Senate communications filtered by the specified congress and communication type.

    :param congress: The congress number.
    :param communication_type: The type of communication (ec, pm, pom).
    :param api_key: The API key for authentication.
    :param kwargs: Optional parameters like 'format', 'offset', 'limit'.
    :return: A dictionary containing the list of Senate communications.
    """
    url = f"{BASE_URL}/senate-communication/{congress}/{communication_type}"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching Senate communications")
    return response.json()



def get_committee_details( chamber, committee_code, api_key, **kwargs):
    """
    Fetch detailed information about a specific committee.
    """
    url = f"{BASE_URL}/committee/{chamber}/{committee_code}"
    params = {"api_key": api_key}
    params.update(kwargs)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching committee details")
    return response.json()