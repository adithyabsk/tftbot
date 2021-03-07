# Roam Twitter Bot

[![GitHub License](https://img.shields.io/github/license/adithyabsk/roam_bot?logo=6cc644&style=plastic)](https://github.com/adithyabsk/roambot/blob/master/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Twitter Follow](https://img.shields.io/twitter/follow/adithya_balaji?style=social)](https://twitter.com/intent/follow?screen_name=adithya_balaji)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adithyabsk?style=social)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

<!-- Since the Repo was renamed, we need to use roam_bot for now, this might
break soon though. -->

## Setting up

### Twitter Credentials

[Apply for a twitter developer account](https://developer.twitter.com/en/apply/user.html)
which will let you the credentials you need to create a bot. Should get
automatically approved since you are an individual developer. Once approved,
getting credentials should be intuitive.

### Roam credentials

If you signed up using Google OAuth, make sure to reset your password so that
you can set a manual password.

## Deploying

### Heroku

* TODO

### Locally

Developed on Python 3.8+

```shell
$ python -m venv roam_bot
$ ./roam_bot/bin/activate
(roam_bot) $ pip install -r requirements.txt
(roam_bot) $ pip install -e .
(roam_bot) $ cp .env.sample .env  # now update these values manually
```

You should just be able to run the cron script in a background process.

```shell
(roam_bot) $ nohup ./cron.py &
```

## Running Tests

Running the simple tests.

```shell
(roam_bot) $ pip install -r requirements-dev.txt
(roam_bot) $ pytest
```

Running the integration tests. WARNING: these actually tweet out using the
provided credentials and require configuring your local environment according to
the instructions above.

```shell
(roam_bot) $ INTEGRATION=1 pytest -s -k integration
```

## Roadmap

The future roadmap for different features.

- [ ] Draft README on setting up bot for other people

  - [ ] Acquiring Twitter API credentials
  - [ ] Deploying bot to Heroku

- [ ] Roam

  - [x] Pull blocks from roam database using a single backlink/tag
  - [ ] Implement arbitrary tag inclusion and exclusion
  - [ ] Rules for tag parents and children
  - [ ] Allow users to provide custom datomic expressions
  - [ ] Look into integration with official Roam (beta) API
  
- [ ] Bot

  - [x] Split long tweets into threads (max size = 9)
  - [x] For some reason Heroku does not seem to like "cron" mode of APScheduler
    only interval seems to work.
  - [x] Refactor bot into python package
  - [ ] Handle tweeting in the preferred timezone
  - [ ] NLTK for better tweet processing and splitting
  - [ ] Directly link to Roam block (for public roam graphs)
  - [ ] Remove cap on tweet thread size
  - [ ] Add draft tweet feature

- [ ] Advertise the project

  - [ ] Slack
  - [ ] Reddit
  - [ ] Twitter
