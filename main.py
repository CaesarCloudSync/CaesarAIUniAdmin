import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from CaesarAIUniAdmin.CaesarAIAptemOTJ import CaesarAIAptemOTJ
from CaesarAIUniAdmin.CaesarAIMonthlyPortfolio import CaesarAIMonthlyPortfolio
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MonthlyReport(BaseModel):
    title:str
    message:str
    feedback:str

JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
caesaraiotj = CaesarAIAptemOTJ()   
caesaraimp = CaesarAIMonthlyPortfolio()
# TODO Next Reusable API by uploading docx,then ask any questions on it.
@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAI Template. Hello"

@app.get("/v1/generalreport")
async def caesaraiaptemotjgeneralreport(title:str,message:str,lecture_hours:int,self_study_hours:int):
    final_report = caesaraiotj.generate_normal_otj(message,lecture_hours,self_study_hours)
    headers = {'Content-Disposition': f'attachment; filename="{title}.txt"'}
    return Response(final_report,headers=headers,media_type="text/plain")
@app.get("/v1/specificreport")
async def caesaraiaptemotjspecificreport(title:str,message:str,overall_hours:int):
    final_report = caesaraiotj.generate_specific_otj(message,overall_hours,)
    headers = {'Content-Disposition': f'attachment; filename="{title}.txt"'}
    return Response(final_report,headers=headers,media_type="text/plain")

@app.post("/v1/monthlyreport")
async def caesaraimonthlyreport(monthlyreport : MonthlyReport):
    final_report = caesaraimp.generate_monthly_report(monthlyreport.message,feedback=monthlyreport.feedback)
    headers = {'Content-Disposition': f'attachment; filename="{monthlyreport.title}.txt"'}
    return Response(final_report,headers=headers,media_type="text/plain")



if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
