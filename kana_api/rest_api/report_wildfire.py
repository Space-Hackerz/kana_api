from . import report_bp
from flask import request


@report_bp.route("/report_wildfire", methods=("POST",))
def report_wildfire():

    if request.method == "POST":
        json_data = request.get_json()
        print("parsing data")
        return {"message": "success"}, 200
    return {"error": "Invalid request method."}, 409
