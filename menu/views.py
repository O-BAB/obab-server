from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openai import OpenAI
from rest_framework.response import Response
from rest_framework.views import APIView


class OpenAIView(APIView):
    def ask_openai(self, message):
        client = OpenAI(api_key=getattr(settings, "OPENAI_API_KEY"))

        message = "나의 기분과 날씨는" + str(message) + "인데 한국어로 추천하는 메뉴 3개와 그 이유를 답변해줘"
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]
        )
        print(completion.choices[0].message)
        return completion.choices[0].message

    @swagger_auto_schema(
        tags=["메뉴 추천"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"prompt": openapi.Schema(type=openapi.TYPE_STRING, description="오늘의 날씨, 기분, 싫어하는 음식 등등")},
        ),
    )
    def post(self, request):
        prompt = request.data.get("prompt")
        if prompt is None:
            return Response({"error": "No prompt provided"}, status=400)
        # response = self.ask_openai(message=prompt)
        return Response(data={"response": prompt})
