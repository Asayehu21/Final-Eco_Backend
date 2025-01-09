import uuid
import logging
from decimal import Decimal
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Cart, Transaction, ShippingAddress
from rest_framework import generics

# Set up logger
logger = logging.getLogger(__name__)
from django.shortcuts import render
# from rest_framework.decorators import api_view, permission_classes
from .models import Product, Cart, CartItem, Transaction
from .serializers import ProductSerializer, DetailedProductSerializer, CartSerializer, CartItemSerializer, SimpleCartSerializer, UserSerializer, ShippingAddressSerializer
from rest_framework import status
from django.conf import settings


# Create your views here.

BASE_URL = settings.REACT_BASE_URL

# BASE_URL = "http://localhost:5173"


@api_view(["GET"])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)

@api_view(["POST"])
def add_item(request):
    try:
        cart_code = request.data.get("cart_code")
        product_id = request.data.get("product_id")

        cart, created_at =Cart.objects.get_or_create(cart_code = cart_code)
        product = Product.objects.get(id=product_id)

        cartitem, created = CartItem.objects.get_or_create(cart=cart, product = product)
        cartitem.quantity = 1
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response({"data": serializer.data, "message": "CartItem created successfully"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status= 400)


@api_view(["GET"])
def product_in_cart(request):
    cart_code = request.query_params.get("cart_code")
    product_id = request.query_params.get("product_id")

    cart = Cart.objects.get(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    product_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

    return Response({'product_in_cart': product_exists_in_cart})


@api_view(["GET"])
def get_cart_stat(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer =SimpleCartSerializer(cart)
    return Response(serializer.data)


@api_view(["GET"])
def get_cart(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["PATCH"])
def update_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = request.data.get("quantity")
        quantity = int(quantity)
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data":serializer.data, "message":"Cartitem updated successfully!"})

    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['POST'])
def delete_cartitem(request):
    cartitem_id = request.data.get("item_id")
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response({"message": "Item Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    return Response({"username": user.username})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)



# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def initiate_payment(request):
#     if request.user:
#         try:
#             #generate a unique transaction reference
#             tx_ref = str(uuid.uuid4())
#             cart_code = request.data.get("cart_code")
#             cart = Cart.objects.get(cart_code=cart_code)
#             user = request.user

#             amount = sum([item.quantity  * item.product.price for item in cart.items.all()])
#             tax = Decimal("0.15")
#             total_amount = amount * tax

#             currency = "ETB"
#             redirect_url = f"{BASE_URL}/payment_status/"

#             transaction = Transaction.objects.create(
#                 ref = tx_ref,
#                 cart = cart,
#                 amount = total_amount,
#                 currency = user,
#                 user = user,
#                 status = 'pending'
#             )

#             flutterwave_payload ={
#                 "tx_ref":tx_ref,
#                 "amount":str(total_amount),
#                 "currency":currency,
#                 "redirect_url":redirect_url,
#                 "customer": {
#                     "email":user.email,
#                     "name":user.username,
#                     "phonenumber":user.phone
#                 },
#                 "customizations":{
#                     "title":"Shoppit Payment"
#                 }
#             }

#             #Set up the header for the payment
#             headers = {
#                 "Authorization":f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
#                 "Content-Type": "application/json"
#             }

#             #make the api request to fluterwave

#             response = requests.post(
#                 'https://api.flutterwave.com/v3/payments',
#                 json = flutterwave_payload,
#                 headers=headers
#             )

#             #check if request was successfull
#             if response.status_code == 200:
#                 return Response(response.json(), status=status.HTTP_200_OK)
#             else:
#                 return Response(response.json(), status=response.status_code)
            
#         except requests.exceptions.RequestException as e:
#             #log the error and return an error response
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    if request.user:
        try:
            # Generate a unique transaction reference
            tx_ref = str(uuid.uuid4())
            cart_code = request.data.get("cart_code")
            cart = Cart.objects.get(cart_code=cart_code)
            user = request.user

            # Calculate total amount of items in the cart (quantity * price)
            amount = sum([item.quantity * item.product.price for item in cart.items.all()])

            # Tax percentage
            tax_percentage = Decimal("0.15")
            
            # Calculate tax
            tax = amount * tax_percentage

            # Calculate total amount (items cost + tax)
            total_amount = amount + tax

            currency = "ETB"
            redirect_url = f"{BASE_URL}/payment_status/"

            # Create the transaction record
            transaction = Transaction.objects.create(
                ref=tx_ref,
                cart=cart,
                amount=total_amount,
                currency=currency,
                user=user,
                status='pending'
            )

            flutterwave_payload = {
                "tx_ref": tx_ref,
                "amount": str(total_amount),
                "currency": currency,
                "redirect_url": redirect_url,
                "customer": {
                    "email": user.email,
                    "name": user.username,
                    "phonenumber": user.phone
                },
                "customizations": {
                    "title": "Shoppit Payment"
                }
            }

            # Set up the header for the payment
            headers = {
                "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                "Content-Type": "application/json"
            }

            # Make the API request to Flutterwave
            response = requests.post(
                'https://api.flutterwave.com/v3/payments',
                json=flutterwave_payload,
                headers=headers
            )

            # Check if the request was successful
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response(response.json(), status=response.status_code)

        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            # Log the error and return an error response
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['POST'])
def payment_callback(request):
    status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')

    user = request.user

    if status == 'successful':
        #verify the transaction using flutter's API
        headers = {
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"
        }

        response = requests.get(f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify", headers=headers)
        response_data = response.json()

        if response_data['status'] == 'success':
            transaction = Transaction.objects.get(ref=tx_ref)

            #Confirm the transaction details
            if (response_data['data']['status'] == "successful"
                 and float(response_data['data']['amount']) == float(transaction.amount)
                 and response_data['data']['currency'] == transaction.currency):
                
                #update transaction and cart status to paid
                transaction.status = 'completed'
                transaction.save()

                cart = transaction.cart
                cart.paid = True
                cart.user = user
                cart.save()

                return Response({'message': "Payment Successful!", "subMessage": "You have successfully made payment"}, status=200)
            else:
                #Payment verification failed
                return Response({"message":"Payment Verification failed", "subMessage": "You have Error by Verification"}, status=400)
        else:
            return Response({"message":"Failed to verify transaction with flutterwave",  "subMessage": "We could Error with flutterwave"}, status=403)
    else:
        #Payment was not successful
        return Response({"message":"Payment was not successfull! "}, status=400)
    

class ShippingAddressView(generics.ListCreateAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer