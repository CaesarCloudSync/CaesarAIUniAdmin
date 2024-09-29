import os
import json
import time
import requests
host = "https://caesaraiaptemotj-662756251108.us-central1.run.app"
route ="v1/generalreport" #  "v1/specificreport" # 
uri = f"{host}/{route}"
class CaesarAIAptemReport:
    @staticmethod
    def generate_report(general=True):
        with open("messages.json","r") as f:
            if general:
                report_type = "general_report"
            else:
                report_type = "specific_report"
            messages = json.load(f)[report_type]["unfinished"]
        for ind,otj in enumerate(messages):
            response = requests.get(uri,params=otj)
            if not os.path.isdir("Reports"):
                os.mkdir("Reports")
            if not os.path.isdir(f"Reports/{otj['month']}_{otj['module']}"):
                os.mkdir(f"Reports/{otj['month']}_{otj['module']}")
            with open(f"Reports/{otj['month']}_{otj['module']}/{otj['title']}.txt", 'wb') as f:
                f.write(response.content)
            print(f"Progress: {ind+ 1}/{len(messages)} - {((ind + 1)/len(messages)) * 100}%")
            time.sleep(2)


        
if __name__ == "__main__":

    CaesarAIAptemReport.generate_report(general=True)