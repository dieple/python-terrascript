from iterfzf import iterfzf

def fetch_regions():
    """
    Fetch all region from AWS
    :return: List of region codes
    """
    region_data = []
    for region in Regions.get_regions():
        # skip these gov regions
        if "us-gov" in str(region['code']):
            continue
        region_data.append(region['code'])
    return region_data


def prompt_user(iterable_data, **prompt_options):
    """
    Display the selection option (iterable_data)
    :param iterable_data:
    :param prompt_options:
    :return: The user selected data
    """
    return iterfzf(iterable_data, **prompt_options)


def prompt_region():
    """
    Fetch and display list of all possible region codes for user to select
    :return: User selected region
    """
    region_options = {"multi": False,
                      "mouse": False,
                      "prompt": "Select region to build > "}
    return  prompt_user(fetch_regions(), **region_options)


def prompt_account(iterable_data):
    """
    Display and prompt user to select which workspace/account to build
    :param iterable_data:
    :return: the select account
    """
    account_options = {"multi": False,
                       "mouse": False,
                       "prompt": "Select account/env to build > "}

    return prompt_user(iterable_data, **account_options)


def prompt_tfaction(iterable_data):
    """
    Fetch and display list of all possible region codes for user to select
    :return: User selected region
    """
    tfaction_options = {"multi": False,
                        "mouse": False,
                        "prompt": "Select action to perform > "}

    return  prompt_user(iterable_data, **tfaction_options)


def user_confirmation(question):
    check = str(input("{0} ? (Y/N): ".format(question))).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return user_confirmation(question)
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return user_confirmation(question)


