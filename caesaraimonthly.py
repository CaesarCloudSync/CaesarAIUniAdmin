import re
import os
import time
from CaesarAIUniAdmin.CaesarAIMonthlyPortfolio import CaesarAIMonthlyPortfolio


if __name__ == "__main__":
    filename = "/home/amari/Desktop/CaesarAIAptemOTJ/MonthlyPortfolio/DTS 1.2 -Amari-EPA-Portfolio.docx"
    caesaraimp = CaesarAIMonthlyPortfolio()
    ksbs = caesaraimp.get_ksbs(filename)
    feedback ="""
        This criteria focuses on the Roles, functions and activities within Digital Technology solutions within
        an organisation. I like that you had the opportunity to speak to service owners regarding an
        opportunity and complete a security assessment. To develop your submission further, you should
        make sure to include some screenshots or snippets so showcase the work carried out. I would also
        like to see a discussion of why this task was completed and its benefit to the business. You should
        also outline what you were looking for when you reviewed software and also note some of the
        security improvements suggested and how these would enable to software to perform better."""
    populated_ksbs = caesaraimp.get_populated_ksbs(ksbs)
    for ind,ksb in enumerate(populated_ksbs):
        ksb_prefix = re.search(caesaraimp.ksb_regex,ksb).group().replace(":","")
        print(ind)
        report = caesaraimp.generate_report(ksb,prompt="rework and expand upon evidence with more detail so that it matches the feedback given. To denote a screenshot use (screenshot)",feedback=feedback,convert_md=True)
        if not os.path.isdir(f"MonthlyPortfolio/KSBS"):
            os.mkdir(f"MonthlyPortfolio/KSBS")
        with open(f"MonthlyPortfolio/KSBS/{ksb_prefix}.txt", 'w+') as f:
            f.write(report)
        print(f"Progress: {ind+ 1}/{len(populated_ksbs)} - {((ind + 1)/len(populated_ksbs)) * 100}%")
        time.sleep(3)


    #print(report)
