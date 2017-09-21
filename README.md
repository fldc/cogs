# HASS-Cog:
Home Assistant Cog for [Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot). Red-DiscordBot is a multipurpose bot for Discord developed by Twentysix26.

## Installation:
1) Clone this repo to a folder accessable by your Red bot

2) Add IP and API key information from HASS using Discord<sup>1</sup> (DM or private channel recommended) using the following commands:

[p]ip_hass
[p]apikey_hass

3) You need to have Home Assistant installed (but not configured), on the system running your discord bot in order to get homeassistant.remote imported for use with the cog.

### Troubleshooting:
<sup>1</sup> If you are not running Home Assistant on the default port (`8123`), edit hass.py on your local server and edit line 18 as follows, then comment out line 33. Optionally change the URL in line 34 to match your desired URL. Note: See [Issue #3](/../../issues/3)

For example: `remote.API('192.168.11.5', 'password', '8765')` 

## Questions/Issues:
If you have any questions or issues, please open an issue on GitHub. Feel free to make a pull request if you want to add or fix something.
