from . import rest_api_bp


@rest_api_bp.route("/rest_api_test", methods=("GET",))
def rest_api_test():
    return "test", 200
