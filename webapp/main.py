import os
import requests
from flask import Flask
from flask import render_template
from config import Config

ACCOUNT_ID = os.environ.get("ACCOUNT_ID", Config.ACCOUNT_ID)
BCOV_POLICY = os.environ.get("BCOV_POLICY", Config.BCOV_POLICY)

bc_url = f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"

bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

app = Flask(__name__)


@app.route("/<int(fixed_digits=13):video_id>")
def index(video_id):
    video_response = requests.get(f"{bc_url}/{video_id}", headers=bc_hdr)

    if video_response.status_code != 200:
        return "<font color=red size=20>Wrong Video ID</font>"

    video = video_response.json()

    video_name = video["name"]

    video_source = video["sources"][3]
    video_url = video_source["src"]
    widevine_url = ""
    microsoft_url = ""
    if "key_systems" in video_source:
        widevine_url = video_source["key_systems"]["com.widevine.alpha"]["license_url"]
        microsoft_url = video_source["key_systems"]["com.microsoft.playready"]["license_url"]
    track_url = video["text_tracks"][1]["src"]
    return render_template(
        "template.html",
        video_name=video_name,
        video_url=video_url,
        track_url=track_url,
        widevine_url=widevine_url,
        microsoft_url=microsoft_url,
    )
