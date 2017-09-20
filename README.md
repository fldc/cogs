# HASS-Cog:
Home Assistant Cog for [Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot). Red-DiscordBot is a multipurpose bot for Discord developed by Twentysix26.

## Installation:
1) Clone this repo to a folder accessable by your Red bot

2) Edit hass.py lines 8 and 9.

Line 8: Ensure that in the first set of `''` that you put your Home Assistant IP address (port not needed)<sup>1</sup>. In the second set of `''`, put the password you use for Home Assistant. If you don't have a password, remove the `,''`

For Example: `remote.API('192.168.11.5', 'password', '8765')`

Line 9: Enter a URL that you want to be taken to when clicking on the title of an embeded message. These are the sections where Light status and Climate status will be reported.

3) You need to have Home Assistant installed (but not configured), on the system running your discord bot in order to get homeassistant.remote imported for use with the cog.

### Troubleshooting:
<sup>1</sup> If you are not running Home Assistant on the default port (`8123`), add another set of `''` after the API Password, and enter the port number you are using. For example: `remote.API('', '', '8765')` 

## Questions/Issues:
If you have any questions or issues, please open an issue here. Feel free to make a pull request if you want to add or fix something
