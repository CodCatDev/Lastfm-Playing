<div align="center">
    <h1>LastFm-Playing Documentation</h1>
    <a href="README.md">Go back</a> | <a href='https://api.codcatdev.site/lastfmPlaying/'>API Url</a>
</div>

## Navigation

- [Navigation](#navigation)
- [Usage](#usage)
    - [Get card](#get-card)
- [Errors](#errors)
    - [Formatting](#format)
- [Self-Hosting](#self-hosting)
    - [Requirements](#requirements)
    - [Download and install libs](#download-and-install-libs)
    - [Run](#running)
    - [Usage for self-host](#endpoints-for-self-hosting)
        - [Get card (Self-Host)](#get-card-self-host)

# Usage

API Endpoint url is `api.codcatdev.site/lastfmPlaying`. Lets start

## Get card

For getting a card, you need a GET request to api

```bash
curl https://api.codcatdev.site/lastfmPlaying/?user={USER}
```
```markdown
<img alt="card" src="https://api.codcatdev.site/lastfmPlaying/?user={USER}">
or
![](https://api.codcatdev.site/lastfmPlaying/?user={USER})
```

Return a `svg card` with content-type `image/svg+xml; charset=utf-8`

Parameters
| Arg | Value | Description | 
| :--- | :--- | :--- |
| `user` | `String (e.g: ?user=codcatdev)` | `Last.fm username` |

# Errors

## Format

```json
{
    "code":404, // Code error [INT]
    "error":true, // Error or api response [BOOL]
    "msg":"Not found", // Message in error [STR]
    "data":{} // JSON. Maybe.. with error data [JSON]
}
```

# Self-Hosting

## Requirements

- Python 3.13
- 200 Mb+ RAM

## Download and install libs

Go to SSH on your server and run

```bash
git clone https://github.com/CodCatDev/Lastfm-Playing.git
cd Lastfm-Playing
cd src
```

Create a Venv

```bash
python3 -m venv venv
```

If you get an error, install Python-Venv module

For Ubuntu/Debian: `sudo apt update && sudo apt install python3-venv python3-pip -y`

For CentOS/RHEL/Rocky Linux/AlmaLinux: `sudo dnf install python3 python3-pip -y`

For Alpine Linux: `apk add python3 py3-pip`

For Arch Linux: `sudo pacman -Syu python python-pip --noconfirm`

---

open venv and install libs

```bash
source venv/bin/activate
```

P.s if it not working, use a SH command:
```sh
. venv/bin/activate
```

And install libs

```bash
pip install -r requirements.txt
```

## Running

```bash
gunicorn --bind 0.0.0.0:80 app:app
```

And done! Server running on `http://YOUR_SERVER_IP/`

## Endpoints for self-hosting

For self-host, endpoint is different!

### Get card (SELF-HOST)

```bash
curl http://YOUR_SEVRER_IP/api/v1/?user={USER}
```
```markdown
<img alt="card" src="http://YOUR_SEVRER_IP/api/v1/?user={USER}">
or
![](http://YOUR_SEVRER_IP/api/v1/?user={USER})
```

Return a `svg card` with content-type `image/svg+xml; charset=utf-8`

Parameters
| Arg | Value | Description | 
| :--- | :--- | :--- |
| `user` | `String (e.g: ?user=codcatdev)` | `Last.fm username` |
