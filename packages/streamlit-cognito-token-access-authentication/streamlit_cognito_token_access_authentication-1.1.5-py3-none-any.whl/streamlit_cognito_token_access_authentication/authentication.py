import streamlit as st
from .decode_verify_jwt import verify_jwt
import requests
import base64
from jose import jwk, jwt
import os
import json


class Authentication:
    # ------------------------------------
    # Read constants from secrets file
    # ------------------------------------

    """
    Instantiate a cognito authentication object.
    
    Authentication can be either user login (user logins in directly in streamlit app 
    or verifying a user token (user already logged in via a hosting app such as Catalyst).

    :param type: The type of authentication: user or token.
    :type type: str
    """

    def __init__(self, config):
        print(f'__init__ {config}')
        print(f'__init__ {config["APP_ID"]}')
        self.COGNITO_DOMAIN = config["COGNITO_DOMAIN"]
        self.CLIENT_ID = config["CLIENT_ID"]
        self.USERPOOL_ID = config["USERPOOL_ID"]
        self.REGION = config["REGION"]
        self.HTTP_PROXY = config["HTTP_PROXY"]
        self.APP_ID = config["APP_ID"] # used to authenticate a user in a cognito group.
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
        st.session_state.auth_type = type
        if "access_token" not in st.session_state:
            st.session_state.access_token = None 
    
    def get_env_variables(self, access_token):
        """
        Gets env variables necessary for cognito api.

        :param access_token: The access token to verify with cognito.
        :type muiltiplier: str

        Returns:
            { 
            "USERPOOL_ID": USERPOOL_ID,
            "CLIENT_ID": CLIENT_ID,
            "REGION": REGION,
            "HTTP_PROXY": HTTP_PROXY,
            "token": access_token
            }
        """
        # provide CLIENT_ID of the host app
        env_vars = { 
            "USERPOOL_ID": self.USERPOOL_ID,
            "CLIENT_ID": self.CLIENT_ID,
            "REGION": self.REGION,
            "HTTP_PROXY": self.HTTP_PROXY,
            "token": access_token
        }
        st.session_state.access_token = access_token
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
        "http": self.HTTP_PROXY,
        "https": self.HTTP_PROXY
        }
        url = ""
        headers = None
        body = None
        response = None
        #print(f'params: {auth_code} :::::  {access_token}')
        if access_token is None:
            st.session_state.authenticated = None
            st.session_state.username = 'noToken'
            return
        with st.spinner(text="Signing in..."):
            # first verify token signature
            env_vars = self.get_env_variables(access_token)
            verify_results = verify_jwt(env_vars, proxies)
            if (verify_results is False):
                print("Error in token signature verification")
                st.session_state.authenticated = False
                return 

            # check if optional APP_ID exists for specific cognito group check
            # verify token cognito client_id matches app client_id
            is_client_id = False
            is_in_group = False
            print(f'self.APP_ID {self.APP_ID}')
            if self.APP_ID:
                is_client_id, is_in_group = self.user_token_decode(access_token, self.CLIENT_ID, self.APP_ID)
                if is_in_group is False:
                    print("User not in cognito group")
                    st.session_state.authenticated = None
                    st.session_state.username = 'notInUserGroup'
                    return 
            else:
                is_client_id, is_in_group = self.user_token_decode(access_token, self.CLIENT_ID)
            
            if is_client_id is False:
                print("Client Id does not match app id")
                st.session_state.authenticated = False
                return             

            # now call cognito api with token
            url = f"{self.COGNITO_DOMAIN}/oauth2/userInfo"
            headers = {
            "Authorization": f"Bearer {access_token}",
            }
            response = requests.post(url, headers=headers, proxies=proxies)
            #print(f'RESPONSE TOKEN {response.json()}')
            self.update_response(response)  

    def user_token_decode(self, token_response, client_id, group=None):
        is_clientId = False
        is_in_group = False
        
        if token_response !="":
            decoded_token = jwt.decode(token_response, '', algorithms=['RS256'], audience=self.CLIENT_ID, options={
                "verify_signature": False,
                "verify_iss": False,
                "verify_sub": False,
                "verify_at_hash": False
                })  
            print(f'client_id {client_id} -  decoded_token {decoded_token}')
            if client_id == decoded_token["client_id"]:
                is_clientId = True

            if group:
                is_in_group = self.check_user_groups(decoded_token)

        return is_clientId, is_in_group
    
    def check_user_groups(self, decoded_token):
        cognito_pool_groups = decoded_token["cognito:groups"]
        print(cognito_pool_groups)
        is_in_group =  any(self.APP_ID in gp for gp in cognito_pool_groups)
        print(f'is_in_group {is_in_group}') 
        return is_in_group

    def update_response(self, token_response):
        print(f'Inside 200 CHECK {token_response}')
        
        st.session_state.response_code = token_response.status_code
        if token_response.status_code == 200:
            st.session_state.response_code = token_response.status_code
            #st.session_state.visibility = "hidden"
            st.session_state.authenticated = True
            st.session_state.logout = False
            st.session_state.username = token_response.json()["email"]

        else:
            st.session_state.authenticated = False
            st.session_state.logout = True

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
        
        else:
            try:
                token = None
                user = ""
                params = st.experimental_get_query_params()
                user = params['user'][0]
                token = params['token'][0]
                #print(f'token from params: {token}')
            except Exception as e:
                print(f'{e}')
                
            if user:
                user = "for " + user  
            if location == 'main':
                login_form = st.form(f'Login', clear_on_submit=True)
            elif location == 'sidebar':
                login_form = st.sidebar.form('Login', clear_on_submit=True)
            login_form.subheader(f'User Authentication {user}')
            #access_token = login_form.text_input("Access Token", value="", help="copy and paste" ,key="my_input")
            submitted = login_form.form_submit_button("Login", type="primary")

            if submitted:
                self.cognito_authenticate(access_token=token) 
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
                st.session_state.authenticated = None
                st.session_state.logout = True
                st.session_state.username = None
        elif location == 'sidebar':
            if st.sidebar.button(button_name):
                st.session_state.authenticated = None
                st.session_state.logout = True
                st.session_state.username = None


    # def initiate_user_buttons(self):
    #     self.login_link = f"{COGNITO_DOMAIN}/login?client_id={CLIENT_ID}&response_type=code&scope=email+openid&redirect_uri={APP_URI}"
    #     self.logout_link = f"{COGNITO_DOMAIN}/logout?client_id={CLIENT_ID}&logout_uri={APP_URI}"

    #     self.html_css_login = """
    #     <style>
    #     .button-login {
    #     background-color: skyblue;
    #     color: white !important;
    #     padding: 1em 1.5em;
    #     text-decoration: none;
    #     text-transform: uppercase;
    #     }

    #     .button-login:hover {
    #     background-color: #555;
    #     text-decoration: none;
    #     }

    #     .button-login:active {
    #     background-color: black;
    #     }

    #     </style>
    #     """
    #     self.html_button_login = (
    #         self.html_css_login
    #         + f"<a href='{self.login_link}' class='button-login' target='_self'>Log In</a>"
    #     )
    #     self.html_button_logout = (
    #         self.html_css_login
    #         + f"<a href='{self.logout_link}' class='button-login' target='_self'>Log Out</a>"
    #     )

    def button_login(self):
        """

        Returns:
            Html of the login button.
        """
        
        return st.markdown(f"{self.html_button_login}", unsafe_allow_html=True)


    def button_logout(self):
        """

        Returns:
            Html of the logout button.
        """
        return st.sidebar.markdown(f"{self.html_button_logout}", unsafe_allow_html=True)

    # ----------------------------------
    # Get authorization code after login
    # ----------------------------------
    def get_auth_code(self):
        """
        Gets auth_code state variable.

        Returns:
            Nothing.
        """
        auth_query_params = st.experimental_get_query_params()
        try:
            auth_code = dict(auth_query_params)["code"][0]
        except (KeyError, TypeError):
            print(f'{Exception}')
            auth_code = ""

        return auth_code