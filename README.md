# Pinprick
Python script to interact with Pinboard account using API and automate delivery of email
with random links.

For information on the Pinboard API, see:

- https://pinboard.in/howto/#api

To get a token for you Pinboard account, see:

- https://pinboard.in/settings/password

## Installation
- [Install Pyenv](https://wiki.klenwell.com/view/Python#Pyenv):

      pyenv install 3.8.x

- Clone repository:

      git clone git@github.com:klenwell/pinprick.git

- Set Python version:

      cd pinprick
      pyenv local 3.8.1

- Install dependencies:

      pip install -r requirements.txt

- Prepare `secrets.py` config file:

      cp -v config/secrets.py{-dist,}

- Update config settings in `secrets.py` and `services.py`.


## Mailer
Email is supported using the Gmail API. To set up API credentials and create a token, follow these steps:

- Log into your Gmail account.
- Create new cloud project: https://console.cloud.google.com/projectcreate
- Create credentials: https://console.cloud.google.com/apis/credentials
- Select OAuth Client: [console.cloud.google.com](https://console.cloud.google.com/apis/credentials/oauthclient)
- Create OAuth Consent Screen: https://console.cloud.google.com/apis/credentials/consent > External
  - Only external is available to non-workspace users.
- Create Client:
  - Type: Desktop App
- Download JSON file and save to `config` folder as `gmail-api-credential.json`.
- Enable Service: https://console.developers.google.com/apis/api/gmail.googleapis.com/overview

The first time you run the script, you'll get a link in console to authorize use of your account.

You may also still be able to use the Gmail SMTP mailer if you create an app password:

- https://support.google.com/accounts/answer/185833


## Usage

To test interactively:

```
$ python main.py interactive
Command: interactive / Arguments: ['interactive']
--Return--
-> breakpoint()
(Pdb) pinboard = BookmarkService()
(Pdb) len(pinboard.bookmarks)
1635
```

Send the daily mailer:

```
$ python main.py daily_mailer klenwell@gmail.com
Command: daily_mailer / Arguments: ['daily_mailer', 'klenwell@gmail.com']
Message delivered to klenwell@gmail.com
```
