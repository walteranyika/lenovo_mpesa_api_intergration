# Create your views here.
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main import mpesa
from main.serializers import PaymentSerializer


@api_view(["POST"])
def initiate_payment(request):
    serializer = PaymentSerializer(data=request.data)  # {"phone":"254733444555", "amount": 10}
    if serializer.is_valid(raise_exception=True):
        phone = serializer.validated_data["phone"]
        amount = serializer.validated_data["amount"]
        headers = mpesa.generate_request_headers()
        data = {
            "BusinessShortCode": mpesa.get_business_shortcode(),
            "Password": mpesa.generate_password(),
            "Timestamp": mpesa.get_current_timestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": mpesa.get_business_shortcode(),
            "PhoneNumber": phone,
            "CallBackURL": mpesa.get_callback_url(),
            "AccountReference": "Something unique",
            "TransactionDesc": "Payment for services"
        }
        resp = requests.post(mpesa.get_payment_url(), json=data, headers=headers)
        print("RESPONSE FROM SAF", resp.json())
        return Response({"message": "Initiated STK push"})


@api_view(["POST"])
def handle_callback(request):
    data = request.data
    print("CALLBACK FROM SAF", data)
    return Response({"message": "Received Callback"})
