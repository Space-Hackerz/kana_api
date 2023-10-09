from flask import request
from flask import Blueprint
from kana_api.api import firms as firms
from dotenv import load_dotenv
from os import environ

from kana_api.api.db import insert_fire_report

report_bp = Blueprint("report", __name__, url_prefix="/rest_api/report")


@report_bp.route("/report_wildfire", methods=("POST",))
def report_wildfire():

    json_data = request.get_json()
    latitude = json_data["latitude"]
    longitude = json_data["longitude"]
    load_dotenv()
    map_key = environ.get("MAP_KEY")
    satellite_confirmed = firms.is_on_fire(map_key, latitude, longitude)
    insert_fire_report(latitude, longitude, satellite_confirmed)

    return {"message": "success"}, 200
