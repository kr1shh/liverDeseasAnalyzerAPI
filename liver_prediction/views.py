# liver_prediction/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LiverSerializer,ChatbotResponseSerializer
from .utils import load_model
import google.generativeai as genai




class PredictLiver(APIView):
    def post(self, request):
        serializer = LiverSerializer(data=request.data)
        if serializer.is_valid():
            model = load_model()
            data = [[
                serializer.validated_data['age'],
                serializer.validated_data['gender'],
                serializer.validated_data['total_bilirubin'],
                serializer.validated_data['direct_bilirubin'],
                serializer.validated_data['alkaline_phosphotase'],
                serializer.validated_data['alamine_aminotransferase'],
                serializer.validated_data['total_proteins'],
                serializer.validated_data['albumin'],
                serializer.validated_data['albumin_and_globulin_ratio']
            ]]
            prediction = model.predict(data)[0]
            
            # Customizing the response based on prediction
            if prediction == 1:
                message = "You do not have liver disease."
            else:
                message = "You have liver disease."
                
            return Response({"status": "ok", "prediction": prediction, "message": message}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

genai.configure(api_key="AIzaSyCPS2FFkq6iK1wlPzqn_614B1xLanC3pCc")
model = genai.GenerativeModel('gemini-pro')

greeting_responses = {
    "hello": "Hello!",
    "hi": "Hi there!",
    "hey": "Hey!",
    "good morning": "Good morning!",
    "good afternoon": "Good afternoon!",
    "good evening": "Good evening!",
    "how are you": "Hi, how are you?",
    "what's up": "What's up?",
    "howdy": "Howdy!",
    "greetings": "Greetings!",
    "salutations": "Salutations!",
    "yo": "Yo!",
    "nice to meet you": "Hi, it's nice to meet you!",
    "your day": "Hello, how's your day going?",
    "what's new": "Hey, what's new?",
    "long time": "Hey, long time no see!",
    "what's happening": "Hey, what's happening?",
    "how have you been": "Hi, how have you been?",
    "what's cooking": "Hey, what's cooking?",
    "how's everything": "Hey, how's everything?",
    "your day been": "Hi, how's your day been?",
    "what's crackin'": "Hey, what's crackin'?",
    "good to see you": "Hi, good to see you!"
}

class LiverDiseaseChatbot(APIView):
    def post(self, request):
        serializer = ChatbotResponseSerializer(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data['user_message'].lower()
            
            if user_message == 'bye':
                bot_response = "Bye!"
                request.session['active'] = False  # End the conversation
            elif user_message in greeting_responses:
                bot_response = greeting_responses[user_message]
            else:
                bot_response = self.get_bot_response(user_message)
                request.session['active'] = True  # Continue the conversation
                
            return Response({'user_message': user_message, 'bot_response': bot_response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_bot_response(self, message):
        # Generate response using Gemini model
        response = ""
        for chunk in model.generate_content(message, stream=True):
            response += chunk.text

        # Clean up the response
        clean_response = response.replace('*', '').replace('\n', ' ').strip()
        return clean_response