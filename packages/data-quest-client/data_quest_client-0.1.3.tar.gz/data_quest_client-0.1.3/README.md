## This is a python module. It is used to make authenticated queries to Dataquest API.

**Installation**:
`pip install dataquest-client`

### Get Started

```Python
from data_quest_client import DataQuestClient

# define query
query = 'query sqlDataSources{\
                   sqlProvider {\
                     dataSources{\
                       definition {\
                         name\
                       }\
                     }\
                   }\
                }'

# instantiate client with authentication.
dq_client = DataQuestClient(self.dq_url).with_application_authentication("<client-id>", ["<scopes>"], "<authority>",
                                                                         "<client secret>")

# make a query.
response = dq_client.query(query)
```


### Authentication

Authentication of DQ calls made from this client is either added through the .WithApplicationAuthenticaion() method, or by passing a token to the Query methods.

- If you are making DQ calls on behalf of the application making the call, you can use .with_applicatin_authentication() to authenticate the application. This is the called the 'client credentials flow' in MSAL. https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow.
- If you are making DQ calls on behalf of an entity in Azure Active Directory, you must first retrieve a token on their behalf and then pass said token as a parameter to query().

If both of the above are utilized, preference is given to the identity of the token passed in the query method.

*Acquiring tokens on behalf of a user, not applications, is not a function currently supported by this client. But can be with user request.*