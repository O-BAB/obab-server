# from openai import OpenAI
# from django.conf import settings
#
#
# def ask_openai(message):
#     client = OpenAI(
#         api_key=getattr(settings, "OPENAI_API_KEY")
#     )
#
#     message = str(message) + "한국어로 답변해줘"
#     completion = client.chat.completions.create(
#       model="gpt-3.5-turbo",
#       messages=[
#         {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#         {"role": "user", "content": message}
#       ]
#     )
#     return completion.choices[0].message