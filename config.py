# config.py

from authomatic.providers import oauth2

CONFIG = {

'tw': { # Your internal provider name

# Provider class
'class_': oauth2.Google,

# Twitter is an AuthorizationProvider so we need to set several other properties too:
'consumer_key': '692021064973-s1m38r36dunrhusuhcvnmfbj5uj3eavf.apps.googleusercontent.com',
'consumer_secret': '2cC1Y9SYjvLSDDJRFJFfu9dp',
}}

}
