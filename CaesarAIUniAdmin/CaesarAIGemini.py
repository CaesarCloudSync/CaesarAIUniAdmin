import os
import io
import base64
import json
import markdown
from bs4 import BeautifulSoup
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv("CaesarAIUniAdmin/.env")
class CaesarAIGemini:
  def __init__(self) -> None:
    genai.configure(api_key = ("AIzaSyD0nX8qRA10j_zw0zj_-mrIkj6DdpF00nc"))

    self.model = genai.GenerativeModel('gemini-1.5-flash')
    print(self.model)
    self.chat = self.model.start_chat(history=[])
    self.vision_model = genai.GenerativeModel('gemini-pro-vision')
  def send_message(self,message):
    try:
      response = self.chat.send_message(message, stream=True)
      for chunk in response:
        try:
          print(chunk.text)
          yield chunk.text
        except ValueError as vex:
          yield ""
    except genai.types.generation_types.IncompleteIterationError:
      response.resolve()

  def get_history(self):
   for message in self.chat.history:
     yield json.dumps({message.role:message.parts[0].text})
  def describe_image(self,image_content):
    image_stream = io.BytesIO(image_content)
    image_stream.seek(0)
    img = Image.open(image_stream)
    response = self.vision_model.generate_content(img)
    return response.text
  def send_message_csv(self,df,message):
    for statement in df.get("statements"):
        prompt = f"""
        Using this as context enact this instruction
        Context:{statement}
        Instruction:{message}
        No extra information is needed.
        At the end of a generated result add this *.
        """
        result = self.send_message(prompt)
        #print(result)
        for statement in result:
          yield statement
  def convert_markdown_to_text(self,report):
      html = markdown.markdown(report)
      text = '\n'.join(BeautifulSoup(html,"lxml").findAll(string=True))
      return text  
if __name__ == "__main__":
  caesar = CaesarAIGemini()
  for i in caesar.send_message("hi"):
    print(i)
    

     
