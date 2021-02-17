# Roam Twitter Bot

[![GitHub](https://img.shields.io/github/license/adithyabsk/keep2roam?logo=6cc644&style=plastic)](https://github.com/adithyabsk/roam_bot/blob/master/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Twitter Follow](https://img.shields.io/twitter/follow/adithya_balaji?style=social)](https://twitter.com/intent/follow?screen_name=adithya_balaji)

## Roadmap

The future roadmap for different features.

- [ ] Draft README on setting up bot for other people

  - [ ] Acquiring Twitter API credentials
  - [ ] Deploying bot to Heroku

- [ ] Roam

  - [x] Pull blocks from roam database using a single backling/tag
  - [ ] Implement arbitrary tag inclusion and exclusion
  - [ ] Rules for tag parents and children
  - [ ] Allow users to provide custom datomic expressions
  - [ ] Look into integration with official Roam (beta) API
  
- [ ] Bot

  - [x] Split long tweets into threads (max size = 9)
  - [ ] Handle tweeting in the preferred timezone
  - [ ] NLTK for better tweet processing and splitting
  - [ ] Directly link to Roam block (for public roam graphs)
  - [ ] Remove cap on tweet thread size
  - [ ] Add draft tweet feature

- [ ] Advertise the project

  - [ ] Slack
  - [ ] Reddit
  - [ ] Twitter
