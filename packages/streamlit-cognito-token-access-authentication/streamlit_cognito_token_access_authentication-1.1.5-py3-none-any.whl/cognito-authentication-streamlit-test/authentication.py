import streamlit as st
from .decode_verify_jwt import verify_jwt

import requests
import base64
from jose import jwk, jwt

# ------------------------------------
# Read constants from secrets file
# ------------------------------------
COGNITO_DOMAIN = st.secrets["COGNITO_DOMAIN"]
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
APP_URI = st.secrets["APP_URI"]
CATALYST_CLIENT_ID = st.secrets["CATALYST_CLIENT_ID"]
USERPOOL_ID = st.secrets["USERPOOL_ID"]
REGION = st.secrets["REGION"]

class Authentication:
    """
    Instantiate a cognito authentication object.
    
    Authentication can be either user login (user logins in directly in streamlit app 
    or verifying a user token (user already logged in via a hosting app such as Catalyst).

    :param type: The type of authentication: user or token.
    :type type: str
    """

    def __init__(self, type):
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = None
        if "response_code" not in st.session_state:
            st.session_state.response_code = None
        if "logout" not in st.session_state:
            st.session_state.logout = False
        if "username" not in st.session_state:
            st.session_state.username = None
        if "auth_type" not in st.session_state:
            st.session_state.auth_type = None
        self.access_token = ""
        st.session_state.auth_type = type

    def initialise_st_state_vars():
        """
        Initialise Streamlit state variables.
        Returns:
            Nothing.
        """
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = None
        if "response_code" not in st.session_state:
            st.session_state.response_code = None
        if "logout" not in st.session_state:
            st.session_state.logout = False
        if "username" not in st.session_state:
            st.session_state.username = None
        if "auth_type" not in st.session_state:
            st.session_state.auth_type = None

    def get_env_variables(self, access_token):
        """
        Gets env variables necessary for cognito api.

        :param access_token: The access token to verify with cognito.
        :type muiltiplier: str

        Returns:
            { 
            "USERPOOL_ID": USERPOOL_ID,
            "CATALYST_CLIENT_ID": CATALYST_CLIENT_ID,
            "REGION": REGION,
            "token": access_token
            }
        """
        # provide CATALYST_CLIENT_ID since catalyst is the host app for the dashboard app
        env_vars = { 
            "USERPOOL_ID": USERPOOL_ID,
            "CATALYST_CLIENT_ID": CATALYST_CLIENT_ID,
            "REGION": REGION,
            "token": access_token
        }
        self.access_token = access_token
        return env_vars


    def cognito_authenticate(self, auth_code=None, access_token=None):
        """
        Gets user tokens by making a post request call.

        Args:
            auth_code: Authorization code from cognito server.

        Returns:
            {
            'access_token': access token from cognito server if user is successfully authenticated.
            'id_token': access token from cognito server if user is successfully authenticated.
            }

        """
        # Variables to make a post request
        proxies = {
        "http":"http://evapzen.fpl.com:10262",
        "https":"http://evapzen.fpl.com:10262"
        }
        url = ""
        headers = None
        body = None
        response = None
        print(f'params: {auth_code} :::::  {access_token}')
        if st.session_state.auth_type == "user" and auth_code is not None:
            url = f"{COGNITO_DOMAIN}/oauth2/token"
            client_secret_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
            client_secret_encoded = str(
                base64.b64encode(client_secret_string.encode("utf-8")), "utf-8")
            headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {client_secret_encoded}",
            }
            body = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "code": auth_code,
            "redirect_uri": APP_URI
            }
            print(f'USERS: headers {headers}')
            print(f'USERS: body {body}')
            response =  requests.post(url, headers=headers, data=body, proxies=proxies)
            print(f'RESPONSE {response}')
            print(f'RESPONSE {response.json()}')
            self.update_response(response)
        else:
            if access_token is not None:
                url = f"{COGNITO_DOMAIN}/oauth2/userInfo"
                headers = {
                "Authorization": f"Bearer {access_token}",
                }
                print(f'TOKEN: headers {headers}')
                response = requests.post(url, headers=headers, proxies=proxies)
                print(f'RESPONSE {response}')
                print(f'RESPONSE {response.json()}')
                self.update_response(response)


        
        

        

    def user_token_decode(self, token_response):
        if st.session_state.auth_type == "user":
            id_token = ""
            catalyst_status=""
            try:
                id_token = token_response.json()["id_token"] 
            except (KeyError, TypeError):
                decoded_token = ""
                catalyst_status = ""

            
            if id_token !="":
                print(f'check IF {id_token}')
                decoded_token = jwt.decode(id_token, '', algorithms=['RS256'], audience=CLIENT_ID, options={
                    "verify_signature": False,
                    "verify_iss": False,
                    "verify_sub": False,
                    "verify_at_hash": False
                    })  
                print(f'DECODED {decoded_token}')
                catalyst_status = decoded_token["catalyst:status"]
                #catalyst_status = decoded_token["catalyst_status"]

        return token_response, catalyst_status

    def authenticate(self):
        """
        access_token only used for authenticate_token
        Sets the streamlit state variables after user authentication.
        Returns:
            Nothing.
        """


        auth_code = ""
        print(f'authenticate: {st.session_state.auth_type} ::: {st.session_state["authenticated"]}')
        if st.session_state.auth_type == "user":
            auth_code = authenticate_user.get_auth_code()
        try:
            token_response = ""
            if not st.session_state["authenticated"]:
                if st.session_state.auth_type == "user":
                    token_response = self.cognito_authenticate(auth_code)
                    result_response, catalyst_status = self.user_token_decode(token_response)

                    if catalyst_status != 'ACTIVE':
                        raise Exception("User account is not active")
                    elif result_response.status_code !=200:
                        raise Exception("Unsuccessful login")
                    st.session_state["authenticated"] = True
                else:
                    token_response = self.cognito_authenticate(auth_code)
                    # if token_response != "" and token_response.status_code == 200:
                    #     print(f'Inside 200 CHECK {token_response.status_code}')
                    #     st.session_state.response_code = 200
                    #     st.session_state.visibility = "hidden"
                    #     st.session_state.authenticated = True
                    #     st.session_state["authenticated"] = True
                st.experimental_rerun()
        except Exception as e:
            print(e)

    def update_response(self, token_response):
        print(f'Inside 200 CHECK {token_response}')
        if st.session_state.auth_type == "user":
            result_response, catalyst_status = self.user_token_decode(token_response)
            if catalyst_status != 'ACTIVE':
                raise Exception("User account is not active")
            elif result_response.status_code !=200:
                raise Exception("Unsuccessful login")
            st.session_state.authenticated = True
            st.session_state.logout = False
            #st.experimental_rerun()
            #self.auth_side_nav()
        else:
            st.session_state.response_code = token_response.status_code
            if token_response.status_code == 200:
                st.session_state.response_code = token_response.status_code
                #st.session_state.visibility = "hidden"
                st.session_state.authenticated = True
                st.session_state.logout = False
                st.session_state.username = token_response.json()["email"]
                print(f'Inside 200 after RUN {st.session_state.authenticated} ')
                print(f'Inside 200 afterAFTERRUN {st.session_state.authenticated}')
            else:
                st.session_state.authenticated = False

    def login_widget(self, form_name: str='Login', location: str='main') -> tuple:
        """
        Creates a login widget.
        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        Returns
        -------
        str
            Name of the authenticated user.
        bool
            The status of authentication, None: no credentials entered, 
            False: incorrect credentials, True: correct credentials.
        str
            Username of the authenticated user.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        print(f'FROM LOGIN WIDGET {st.session_state}' )

        if not st.session_state.authenticated:
            if location == 'main':
                login_form = st.form('Login', clear_on_submit=True)
            elif location == 'sidebar':
                login_form = st.sidebar.form('Login', clear_on_submit=True)
            login_form.subheader(form_name)
            access_token = login_form.text_input("Access Token", value="", help="copy and paste" ,key="my_input")
            submitted = login_form.form_submit_button("Login")

            if access_token !="" and submitted:
                print(f'access_token from side {access_token}')
                self.cognito_authenticate(access_token=access_token) 
            print (f'login widget: {st.session_state.authenticated} {st.session_state.username}')
        return st.session_state.authenticated, st.session_state.username

    def logout(self, button_name ='Logout', location ='main'):
        """
        Creates a logout button.
        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name):
                st.session_state.authenticated = False
                st.session_state.logout = True
                st.session_state.username = None
        elif location == 'sidebar':
            if st.sidebar.button(button_name):
                st.session_state.authenticated = False
                st.session_state.logout = True
                st.session_state.username = None