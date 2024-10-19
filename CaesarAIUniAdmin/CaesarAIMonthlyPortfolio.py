import re
import docx
from CaesarAIUniAdmin.CaesarAIGemini import CaesarAIGemini
class CaesarAIMonthlyPortfolio:
    def __init__(self) -> None:
        self.caesaraigemini = CaesarAIGemini()
        self.ksb_regex = r'([A-Z]\d{1,2}:)'
        self.evidence_placeholder = "Insert evidence here"
    def getText(self,filename):
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    def extract_ksb_list(self,ksb_list):
        merged_list = []

        # Loop through the list in steps of 2
        for i in range(0, len(ksb_list), 2):
            if i + 1 < len(ksb_list):
                # If there's a pair, merge the two strings
                merged_list.append(ksb_list[i] + ksb_list[i + 1])
            else:
                # If there's only one element left, append it as is
                merged_list.append(ksb_list[i])
        return merged_list
    def get_ksbs(self,filename):
        text = self.getText(filename)
        ksb_list = re.split(self.ksb_regex,text)[1:]
        ksbs = self.extract_ksb_list(ksb_list)
        return ksbs
    def get_populated_ksbs(self,ksbs):
        return list(filter(lambda x:self.evidence_placeholder not in x,ksbs))
    def get_unpopulated_ksbs(self,ksbs):
        return list(filter(lambda x:self.evidence_placeholder in x,ksbs))
    def generate_report(self,evidence,prompt="generate a summary as well as an essay on a lecture:",feedback="",verbose=0,convert_md=True):

        prompt = f"{prompt} Evidence: {evidence} Feedback: {feedback}"


        final_report = ""
        for result in self.caesaraigemini.send_message(prompt):
            if verbose == 1:
                print("CaesarAI:",result)
            final_report += result

        if convert_md == True:
            return self.caesaraigemini.convert_markdown_to_text(final_report)
        else:
            return final_report
    def generate_monthly_report(self,evidence,prompt="in star method using Situation,Task,Action and Result as headers. rework and expand upon evidence with more detail so that it matches the feedback given. To denote a screenshot use (screenshot). Any extra info required from me put it in the area needed in brackets",feedback="",verbose=0,convert_md=True):

        prompt = f"{prompt} Evidence: {evidence} Feedback: {feedback}"


        final_report = ""
        for result in self.caesaraigemini.send_message(prompt):
            if verbose == 1:
                print("CaesarAI:",result)
            final_report += result

        if convert_md == True:
            return self.caesaraigemini.convert_markdown_to_text(final_report)
        else:
            return final_report

