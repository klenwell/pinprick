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
