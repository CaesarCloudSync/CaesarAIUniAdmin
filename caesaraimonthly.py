import re
import os
import time
import json
from CaesarAIUniAdmin.CaesarAIMonthlyPortfolio import CaesarAIMonthlyPortfolio

class CaesarAIMonthly:
    @staticmethod
    def run(ksb_dir="KSBS_MD",convert_md=False):
        feedback_filename = "/home/amari/Desktop/CaesarAIUniAdmin/MonthlyPortfolio/feedback.json"
        with open(feedback_filename,"r") as f:
            feedback_json = json.load(f)
        filename = "/home/amari/Desktop/CaesarAIUniAdmin/MonthlyPortfolio/DTS 1.2 -Amari-EPA-Portfolio.docx"
        caesaraimp = CaesarAIMonthlyPortfolio()
        ksbs = caesaraimp.get_ksbs(filename)
        # TODO Add Feedback from Aptem to json then run, it should generate all that is needed.
        # Missing:  ,
        #redundant = ['K16', 'K8','K22']
        populated_ksbs = caesaraimp.get_populated_ksbs(ksbs)

        prompt = "rework and expand upon evidence with more detail so that it matches the feedback given. To denote a screenshot use (screenshot). Any extra info required from me put it in the area needed in brackets"
        for ind,ksb in enumerate(populated_ksbs[16:]):
            try:
                ksb_prefix = re.search(caesaraimp.ksb_regex,ksb).group().replace(":","")
                print(ind)
                report = caesaraimp.generate_report(ksb,prompt=prompt,feedback=feedback_json[ksb_prefix],convert_md=convert_md)
                if not os.path.isdir(f"MonthlyPortfolio/{ksb_dir}"):
                    os.mkdir(f"MonthlyPortfolio/{ksb_dir}")
                with open(f"MonthlyPortfolio/{ksb_dir}/{ksb_prefix}.txt", 'w+') as f:
                    f.write(report)
                print(f"Progress: {ind+ 1}/{len(populated_ksbs)} - {((ind + 1)/len(populated_ksbs)) * 100}%")
                time.sleep(6)
            except KeyError as kex:
                print(f"KSB No Feedback:\n{ksb}")
                continue

if __name__ == "__main__":
    pass



    #print(report)
