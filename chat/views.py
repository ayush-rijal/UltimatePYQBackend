import os 
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
# from django.views.decorators.http import require_POST
# from django.utils.decorators import login_required
# from django.conf import settings
import json
from datetime import timedelta
from django.utils import timezone
from dotenv import load_dotenv
from .models import ChatInteraction
from .serializers import ChatInteractionSerializer, ChatInputSerializer


from rest_framework.decorators import api_view


#load env variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
API_KEY = os.getenv('CHATBOT_API_KEY')

# Define the API endpoint


@api_view(["POST"])
def chatbot(request):

    serializer = ChatInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_message = serializer.validated_data["message"]
    try:
        # parse request body
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '')


        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        

        #prese resquest to chatbot api  
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "googleai/gemini-2.0-flash",
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 150,
        }


        # Send the request to the Gemini API
        response = requests.post(API_KEY, headers=headers, json=payload)

        if response.status_code != 200:
            # Parse the response from the API
            return JsonResponse({'error': 'Error from API'}, status=500)


        # Extract the bot's response from the API response
        chatbot_response = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

        #save chatbot interaction to database
        if request.user.is_authenticated:
            ChatInteraction.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=chatbot_response
            )
        
        # Return the bot's response as JSON
        return JsonResponse({'response': chatbot_response})
    except Exception as e:
        # Handle any exceptions that occur during the request processing
        return JsonResponse({'error': str(e)}, status=500)
    

# @login_required

def get_interactions(request, period):
    

    try:
        #define time period for chat history
        now = timezone.now()
        periods = {
            'last_24_hours': now - timedelta(days=1),
            'last_7_days': now - timedelta(days=7),
            'last_30_days': now - timedelta(days=30),
            'last_90_days': now - timedelta(days=90),
        }

        if period not in periods:
            return JsonResponse({'error': 'Invalid period'}, status=400)
        
        # Get the chat history for the specified period
        interaction = ChatInteraction.objects.filter(
            user=request.user,
            timestamp__gte=periods[period]
        ).values('user_message', 'bot_response' '-timestamp')


        return JsonResponse(list(interaction), safe=False)
        
        serializer = ChatInteractionSerializer(interactions, many=True)
        return Response({"interactions": serializer.data})
    
    except Exception as e:
        # Handle any exceptions that occur during the request processing
        return JsonResponse({'error': str(e)}, status=500)















# import os
# import requests
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import status
# from datetime import timedelta
# from django.utils import timezone
# from dotenv import load_dotenv
# from .models import ChatInteraction
# from .serializers import ChatInteractionSerializer, ChatInputSerializer

# # Load environment variables
# load_dotenv()

# # Get API key from environment
# API_KEY = os.getenv("CHATBOT_API_KEY")


# @api_view(["POST"])
# # @permission_classes([AllowAny])  # Change to IsAuthenticated if auth is required
# def chatbot(request):
#     serializer = ChatInputSerializer(data=request.data)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     user_message = serializer.validated_data["message"]

#     try:
#         # Prepare request to chatbot API (OpenAI example)
#         headers = {
#             "Authorization": f"Bearer {API_KEY}",
#             "Content-Type": "application/json",
#         }
#         payload = {
#             "model": "gpt-3.5-turbo",
#             "messages": [{"role": "user", "content": user_message}],
#             "max_tokens": 150,
#         }

#         # Send request to chatbot API
#         response = requests.post(API_KEY, headers=headers, json=payload)
#         response_data = response.json()

#         if response.status_code != 200:
#             return Response(
#                 {"error": "Failed to get response from chatbot API"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         # Extract chatbot response
#         chatbot_response = response_data["choices"][0]["message"]["content"]

#         # Save interaction to database (if user is authenticated)
#         if request.user.is_authenticated:
#             ChatInteraction.objects.create(
#                 user=request.user,
#                 user_message=user_message,
#                 bot_response=chatbot_response,
#             )

#         return Response({"response": chatbot_response})

#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_interactions(request, period):
#     try:
#         # Define time periods
#         now = timezone.now()
#         periods = {
#             "90days": now - timedelta(days=90),
#             "30days": now - timedelta(days=30),
#             "7days": now - timedelta(days=7),
#             "yesterday": now - timedelta(days=1),
#         }

#         if period not in periods:
#             return Response(
#                 {"error": "Invalid period"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         # Query interactions for the user and time period
#         interactions = ChatInteraction.objects.filter(
#             user=request.user, timestamp__gte=periods[period]
#         )

#         # Serialize the data
#         serializer = ChatInteractionSerializer(interactions, many=True)
#         return Response({"interactions": serializer.data})

#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)