from CaesarAIAptemOTJ.CaesarAIGemini import CaesarAIGemini

from bs4 import BeautifulSoup
import markdown

class CaesarAIAptemOTJ:
    def __init__(self) -> None:
        self.caesaraigemini = CaesarAIGemini()

        self.general_otj_report = """
        FYI: {} hours, {} hours lecture. {} hours self study.

        {}

        """
        self.specific_otj_report = """
        FYI: {} hours

        {}

        """
    def convert_markdown_to_text(self,report):
        html = markdown.markdown(report)
        text = '\n'.join(BeautifulSoup(html,"lxml").findAll(string=True))
        return text
    def generate_normal_otj(self,message,lecture_hours=3,self_study_hours=5,prompt="generate a summary as well as an essay on a lecture:",verbose=0,convert_md=True):

        prompt = f"{prompt} {message}"

        overall_hours = lecture_hours + self_study_hours

        final_result = ""
        for result in self.caesaraigemini.send_message(prompt):
            if verbose == 1:
                print("CaesarAI:",result)
            final_result += result
        final_result = final_result.replace("**Essay**","").replace("**Summary**","").replace("**Essay:**","").replace("**Summary:**","")
        final_report = self.general_otj_report.format(overall_hours,lecture_hours,self_study_hours,final_result)
        if convert_md == True:
            return self.convert_markdown_to_text(final_report)
        else:
            return final_report
    def generate_specific_otj(self,message,overall_hours,prompt="generate a summary as well as an essay on a lecture:",verbose=0,convert_md=True):

        prompt = f"{prompt} {message}"


        final_result = ""
        for result in self.caesaraigemini.send_message(prompt):
            if verbose == 1:
                print("CaesarAI:",result)
            final_result += result
        final_result = final_result.replace("**Essay**","").replace("**Summary**","").replace("**Essay:**","").replace("**Summary:**","")
        final_report = self.specific_otj_report.format(overall_hours,final_result)
        if convert_md == True:
            return self.convert_markdown_to_text(final_report)
        else:
            return final_report





