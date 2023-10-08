from dotenv import load_dotenv
from os import environ
from flask import jsonify, request, Blueprint
from kana_api.api import firms as firms

info_bp = Blueprint("info", __name__, url_prefix="/rest_api/info")


@info_bp.route("/get_fire_info", methods=("POST",))
def get_fire_info():
    json_data = request.get_json()
    latitude = json_data["location"]["latitude"]
    longitude = json_data["location"]["longitude"]
    load_dotenv()
    map_key = environ.get("MAP_KEY")
    fire_data = firms.convert_area_dataframe(
        firms.get_fire_data(map_key, longitude, latitude)
    )
    return jsonify({"fire_data": fire_data}), 200
