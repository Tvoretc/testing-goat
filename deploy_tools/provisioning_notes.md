Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

eg, on Ubuntu:

  sudo add-apt-repository ppa:fkrull/deadsnakes
  sudo apt-get install nginx git python36 python3.6-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv

## SSH keys reset
https://stackoverflow.com/questions/10101127/fabric-asks-for-password-even-though-i-can-ssh-using-credential

For me, I had to reset SSH agent identities with:
ssh-add -D
Then add my key back with:
ssh-add -K keyname
Careful, this will delete all identities from SSH agent.
