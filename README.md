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

To test the API interactively:

```
$ python main.py interactive
Command: interactive / Arguments: ['interactive']
Loaded 1568 bookmarks as bookmarks
--Return--
> pinprick/main.py(52)interactive()->None
-> pdb.set_trace()
(Pdb) bookmark = bookmarks[0]
(Pdb) bookmark
<Bookmark description="Ask HN: I just got my first team lead. What should I do? | Hacker News" url="news.ycombinator.com">
(Pdb) bookmark.url
'https://news.ycombinator.com/item?id=3407643'
(Pdb) bookmark.__dict__
{'description': 'Ask HN: I just got my first team lead. What should I do? | Hacker News', 'extended': '', 'url': 'https://news.ycombinator.com/item?id=3407643', ... }
```
