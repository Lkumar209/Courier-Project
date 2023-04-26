# Install Courier SDK: pip install trycourier
from trycourier import Courier

client = Courier(auth_token="pk_prod_E7E2HD1Q3V4ZYJM9D4BHK5RZQFYW")

resp = client.send_message(
        message={
        "to": {
        "email": "pranav.belligundu@gmail.com"
        },
        "content": {
        "title": "Welcome to Courier!",
        "body": "Want to hear a joke? {{joke}}"
        },
        "data":{
        "joke": "Why does Python live on land? Because it is above C level"
        }
    }
)