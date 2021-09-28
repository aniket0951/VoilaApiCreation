from rest_framework.response import Response
from django.http import JsonResponse


# -------- responses success response --------
def success_result(result, message):
    return JsonResponse({"result": result, "message": message, 'isAuthenticatedUser': True})


# --------- failure response ----------
def failure_result(result, message):
    return JsonResponse({"result": result, "message": message})


# ------------- success response with data------------------------
def success_result_with_data(result, message, data_name, data):
    return JsonResponse({"result": result, "message": message, data_name: data})


# ---------------- success response with array data------------------------
def success_result_with_array(result, message, data_name, data):
    return JsonResponse({"result": result, "message": message, data_name: [data]})


# ---------------  request send success but missing data------------------------
def success_missing_data(result, message):
    return JsonResponse({"result": result, "message": f"Please provide a {message} this is required"})


# ------------------ un-Authorized request -------------------------------------
def unauthorized_request():
    return JsonResponse({"result": False, 'message': "unauthorized request"})


# -------------- un-authorized driver or user --------------------------------
def unauthorized_user():
    return JsonResponse({"result": False, 'message': "you are not authorized partner", 'isAuthenticatedUser': False})
