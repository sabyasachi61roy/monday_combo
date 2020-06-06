import re
import hashlib
import json
import requests
from django.conf import settings

MAILCHIMP_API_KEY = getattr(settings,"MAILCHIMP_API_KEY", None)
MAILCHIMP_DATA_CENTER = getattr(settings,"MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_LIST_ID = getattr(settings, "MAILCHIMP_LIST_ID", None)

def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError("String passed is not a valid email address")
    return email

def get_subscriber_hash(member_email):
    check_email(member_email)
    member_email = member_email.lower().encode()
    hash_email = hashlib.md5(member_email)
    return hash_email.hexdigest()


class Mailchimp(object):
    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(
            dc=MAILCHIMP_DATA_CENTER
        )
        self.list_id = MAILCHIMP_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(
                                    api_url = self.api_url,
                                    list_id=self.list_id
        )

    def get_members_endpoint(self):
        return self.list_endpoint + "/members"

    def check_valid_status(self, status):
        choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending', 'transactional']
        if status not in choices:
            raise ValueError("Not a valid choice for email status")
        return status

    def add_email(self, email):     #This method can be override by *return self.change_subscription_status(email, status='subscribed')*
        status = "subscribed"
        self.check_valid_status(status)
        data = {
            "email_address": email,
            "status": status,
        }
        endpoint = self.get_members_endpoint()
        r = requests.get(endpoint, auth=("", self.key), data=json.dumps(data))
        return  r.json()

    def check_subscription_status(self, email):
        hashed_email = get_subscriber_hash(email)
        print("HASHED EMAIL: ", hashed_email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        r = requests.get(endpoint, auth=("", self.key))
        return r.status_code, r.json()

    def change_subscription_status(self, email, status):  # check_status=False
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        data = {
            "status": self.check_valid_status(status)
        }
        # if check_status:
        #     return requests.get(endpoint, auth=("", self.key), data=json.dumps(data)).json()
        r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def subscribe(self, email):
        return self.change_subscription_status(email, status='subscribed')

    def unsubscribe(self, email):
        return self.change_subscription_status(email, status='unsubscribed')
    
    def delete_subscriber(self, email):
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email + "/actions/delete-permanent"
        return requests.post(endpoint, auth=("", self.key))

    def update_subscriber(self, email):
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        data = {
            "language": "English",
            "merge_fields": {"FNAME":"Debopriyo", "LNAME":"Das", "PHONE":"6001261818", "BIRTHDAY":"04/10"}
        }
        r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        return  r.json()