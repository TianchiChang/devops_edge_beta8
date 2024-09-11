import snowflake.client

def generate_token():
    guid = snowflake.client.get_guid()
    return guid
