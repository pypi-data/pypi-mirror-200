# manuscriptify

Compile Google docs into a manuscript


## Installation and Setup

#### 1. Install manuscriptify

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip install manuscriptify

#### 2. Setup your project

    $ cat << EOF >> ~/.zshrc

    # manuscriptify project config
    export MSFY_PROJECT_FOLDER='my awesome novel'
    export MSFY_PSEUDONYM='John Smith'
    export MSFY_CATEGORY='YA' # Adult/Middle School/etc
    export MSFY_GENRE='Adventure Fantasy'
    export MSFY_TITLE='My Awesome Novel'
    EOF

    $ source ~/.zshrc

Notes:

1. If using ubuntu you should use ~/.profile instead of ~/.zshrc
1. If using windows you must use WSL/ubuntu at present

#### 3. Organise your writing folder

Manuscriptify inspects the 'writing' folder inside your
project folder. That's where you need to put your writing.
You can have as many levels of structure as you want, but
you need to place an integer value (to be used as the sort
key) in the description field of each object in the folder
tree.

&nbsp;  

![view details](tests/media3.png "View details")

&nbsp;  

![edit description](tests/media4.png "Edit description")

## Usage

    $ manuscriptify
    My Awesome Novel compiled successfully

    # The contents of the writing folder inside
    # your project folder was assembled and
    # placed in a new doc in the manuscripts
    # folder.
