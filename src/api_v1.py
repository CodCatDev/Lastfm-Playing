import flask as fl
from lastfm import getRecentTrack, getBase64Image, getPlaceholder
import flask_cors as cors

bp = fl.Blueprint('apiV1', __name__)
cors.CORS(app=bp)

@bp.get('/')
async def card():
    user = fl.request.args.get('user', default='NONE')
    if user == "NONE":
        return {
        "code": 400,
        "error": True,
        "msg":"Arg 'user' not found or Null-type",
        "data":{}
    }, 400
    track, err = await getRecentTrack(user)
    if not err:
        return {
        "code": 500,
        "error": True,
        "msg":track, 
        "data":{}
    }, 500
    with open('cardTemplate.svg', 'r') as f:
        cardSvg = f.read()
    if track['img'] == "" or track['img'] == None:
        b64 = await getPlaceholder()
    else:
        status = await getBase64Image(track['img'])
        if status[1] == False:
            b64 = await getPlaceholder()
        else:
            b64 = status[0]
    if track['isNowPlaying']:
        statusText = "Listen now"
    else:
        statusText = f"Listened on {track['date']} (UTC+0)"
    cardSvg = cardSvg.format(
        title=track["title"],
        artist=track["artist"],
        album=track["album"],
        status=statusText,
        b64Image=b64,
    )
    return fl.Response(cardSvg, mimetype="image/svg+xml")