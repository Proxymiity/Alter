[![CodeQL](https://github.com/Proxymiity/Alter/workflows/CodeQL/badge.svg)](https://github.com/Proxymiity/Alter/actions?query=workflow%3ACodeQL)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Proxymiity_Alter&metric=alert_status)](https://sonarcloud.io/dashboard?id=Proxymiity_Alter)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f657d4ee17004f8f9517ab5aee129c7d)](https://www.codacy.com/gh/Proxymiity/Alter/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Proxymiity/Alter&amp;utm_campaign=Badge_Grade)

# Alter
A modular Discord bot.

A kinda-indev bot that supports translations, database, and more to come.  
Check the [development board](https://github.com/Proxymiity/Alter/projects/2) to see what's next.

Current internal features:
  - [x] Fully modular system with module reloading if needed
  - [x] Smooth error handling
  - [x] Fully automated help system
  - [x] Permission checks
  - [x] Database support

Current modules:
  - Core
    - get help for a command
    - properly shutdown instances
    - changes server locale
  - Moderation
    - basic ban, unban, idban, kick tools
    - [ ] mute/unmute is planned
    - *logs may be planned, but discord's mod logs are better*
  - Utility
    - Server info
    - User info
  - [ ] Pterodactyl module  
    *will be able to fully interact with [pterodactyl](https://pterodactyl.io/)'s api to remote turn on and off servers with an api key*
  - [ ] Some random manga stuff  
    *will be able to search by image (reverse search), and send random manga images or whatever*

# Running this yourself
Good luck. I currently won't offer any help running this project.  
You can clone the project, open the config files in `./data/`. The bot should start with its default values in the database.

No one is perfect, and I'm not that good at develoment; as such, you can, if you want, PR to this project.


This project uses [discord.py](https://github.com/Rapptz/discord.py) by [Rapptz](https://github.com/Rapptz) on its latest version.  
You can check out my [other projects](https://proxymiity.fr/code), or my [about:me](https://proxymiity.fr/about) page.
