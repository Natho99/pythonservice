import africastalking
from django.conf import settings
from rest_framework import viewsets
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication


# Initialize Africa's Talking SDK
africastalking.initialize(username="sandbox", api_key="atsk_a781dc1dbea1892def902c9a28692a3dd200b0869673d2fd22a06c9fd3eb090b10678606")  # Replace with your actual username and API key
sms = africastalking.SMS


# Function to send SMS
def send_sms(to, message):
    try:
        # Sending the SMS
        response = sms.send(message, [to])
        print(response)
    except Exception as e:
        print(f"Failed to send SMS: {e}")


# ViewSet for Customer
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [OAuth2Authentication]  # OAuth2 authentication
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]  # Protect with OAuth2


# ViewSet for Order
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [OAuth2Authentication]  # OAuth2 authentication
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]  # Protect with OAuth2

    # Override the create method to send an SMS when a new order is placed
    def perform_create(self, serializer):
        order = serializer.save()  # Save the order

        # Get customer phone number (assuming you have a 'phone_number' field in the Customer model)
        customer = order.customer
        phone_number = customer.phone_number  # Ensure that your Customer model has a phone_number field

        # Send SMS notification
        send_sms(
            to=phone_number,
            message=f"Hi {customer.name}, your order for {order.item} (amount: {order.amount}) has been successfully placed!"
        )


    