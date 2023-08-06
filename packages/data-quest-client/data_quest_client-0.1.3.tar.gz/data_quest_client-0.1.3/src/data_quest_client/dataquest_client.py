import datetime
import requests

from msal.application import ConfidentialClientApplication


class DataQuestClient:
    __app = None
    __scopes = None
    __token = None
    __authenticated_client = False

    def __init__(self, dq_url):
        self.__dq_url = dq_url

    def with_application_authentication(self, client_id, scopes, authority, client_secret):
        """
        Authenticates the data_quest_client with the credentials of the application utilizing the instance.
        :param client_id: The Application (client) ID that the Azure portal – App registrations experience assigned to your app.
        :param scopes: scopes requested to access a protected API. For this flow (client credentials), the scopes should be of the form "{ResourceIdUri/.default}"
        :param authority: URL client will call to acquire token.
        :param client_secret: The client secret that you generated for your app in the app registration portal.
        :return: data_quest_client class.
        """
        self.__scopes = scopes
        self.__app = ConfidentialClientApplication(client_id, client_secret, authority)
        self.__authenticated_client = True

        return self

    def query(self, query, variables=None, client_token=None):
        """
        Maks a request to DataQuest with a JSON response.
        :param query: query to be sent to DQ.
        :param variables: variables used in query.
        :param client_token: An optional Ouath2.0 token response object. Should contain key 'access_token'. Can be used
        to authenticate queries on behalf of a user or application.
        :return: a JSON string representing the data returned form DQ.
        """
        token = None
        if client_token is not None:
            token = client_token
        else:
            token = self.__get_token()

        if token is not None:
            header = {'Authorization': 'Bearer ' + token['access_token']}
        else:
            header = {}
        query_result = requests.post(self.__dq_url, json={'query': query, 'variables': variables}, verify=False,
                                     headers=header)

        return query_result

    def __get_token(self):
        """
        set token attribute as a token object retrieved from current authority.
        :return: a token response object.
        """
        if not self.__authenticated_client:
            return None

        if self.__token is not None and datetime.UTC < self.__token.ExpiresOn:
            return self.__token

        token_response = self.__app.acquire_token_for_client(self.__scopes)
        if "access_token" in token_response:
            self.__token = token_response
            return self.__token
        else:
            raise Exception("Token acquisition failed. Validate credentials.")
