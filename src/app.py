import flask as fl
import flask_cors as cors
import config

if config.API_KEY == "YOUR_API_KEY":
    print("Place your LASTFM Api key in config.py!")
    exit(1)

app = fl.Flask(
    __name__
)
cors.CORS(app=app)
app.json.sort_keys = False # type: ignore
app.json.ensure_ascii = False # type: ignore

@app.errorhandler(404)
async def pageNotFound(error):
    return {
        "code": 404,
        "error": True,
        "msg":"Not Found",
        "data":{},
    }, 404

@app.errorhandler(403)
async def forbidden(error):
    return {
        "code": 403,
        "error": True,
        "msg":"Forbidden",
        "data":{},
    }, 403

@app.errorhandler(405)
async def methodNotAllowed(error):
    return {
        "code": 405,
        "error": True,
        "msg":"Method not allowed",
        "data":{},
    }, 405

@app.route('/')
async def index():
    return {
        "code": 200,
        "error": False,
        "msg":"This is not a api, its a.. index page! Go to docs or api",
        "data":{},
    }, 200

@app.route('/api')
async def indexApi():
    return {
        "code": 200,
        "error": False,
        "msg":None,
        "data":{
            "apiVersions":['v1'],
            "docs":"https://github.com/CodCatDev/Lastfm-Playing/blob/main/DOCS.md"
        },
    }, 200

@app.route('/docs')
async def docs():
    return fl.redirect('https://github.com/CodCatDev/Lastfm-Playing/blob/main/DOCS.md', code=301)

# Api versions (blueprints)

import api_v1

app.register_blueprint(api_v1.bp, url_prefix="/api/v1")