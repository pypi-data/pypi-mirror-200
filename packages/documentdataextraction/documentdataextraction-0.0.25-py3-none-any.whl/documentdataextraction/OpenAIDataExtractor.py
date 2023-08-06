import requests, json, traceback, openai
import os
from invoice2data import extract_data
from flask import request
import loggerutility as logger
from PIL import Image
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path
import cv2
import pytesseract
import yaml
from .GenerateExtractTemplate import GenerateExtractTemplate
import pdfplumber
import pdftotext
import datetime

class OpenAIDataExtractor:

    def pytesseract_ocr(self,PDF_file):
        image_file_list = []
        with TemporaryDirectory() as tempdir:
            pdf_pages = convert_from_path(PDF_file, 500)
            for page_enumeration, page in enumerate(pdf_pages, start=1):
                filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
                page.save(filename, "JPEG")
                image_file_list.append(filename)

            for image_file in image_file_list:
                text = str(((pytesseract.image_to_string(Image.open(image_file)))))

            return text
        
    def pdfplumber_ocr(self,PDF_file):
        OCR_Text=''
        pdffile = pdfplumber.open(PDF_file)
        for i in range(len(pdffile.pages)):
            OCRTEXT = pdffile.pages[i].extract_text()
            OCR_Text = OCR_Text +'\n'+ OCRTEXT
        
        return OCR_Text
    
    def pdftotext_ocr(self,PDF_file):
        with open(PDF_file, "rb") as f:
            pdf = pdftotext.PDF(f)

        OCR_Text = "\n\n".join(pdf)
        return OCR_Text

    def OpenAIDataExtract(self,file_path : str, jsonData : str, templates : str, input_module : str):
        try:

            logger.log(f"json data   ::::: 51 {jsonData}","0")
            ent_name = ""
            ent_code = ""
            if 'proc_instr' in jsonData.keys():
                proc_instr = jsonData['proc_instr']
            
            if 'proc_api_key' in jsonData.keys():
                proc_api_key = jsonData['proc_api_key']

            if 'userId' in jsonData.keys():
                userId = jsonData['userId']
                
            if 'objName' in jsonData.keys():
                objName = jsonData['objName']

            if 'ent_code' in jsonData.keys():
                ent_code = jsonData['ent_code']

            if 'ent_name' in jsonData.keys():
                ent_name = jsonData['ent_name']
 
            if 'IS_OCR_EXIST' in jsonData.keys():
                IS_OCR_EXIST = jsonData['IS_OCR_EXIST']

            
            if 'proc_mtd' in jsonData.keys():
                proc_mtd = jsonData['proc_mtd']
                proc_mtd_value = proc_mtd.split("-")
            
            OCR_Text = ""
            finalResult = ""
            result = {}

            if IS_OCR_EXIST == 'false':
                logger.log(f"OCR Start !!!!!!!!!!!!!!!!!77","0")            
                if '.PDF' in file_path or '.pdf' in file_path:

                    if proc_mtd_value[0] == 'PP':
                        OCR_Text=self.pdfplumber_ocr(file_path)

                    elif proc_mtd_value[0] == 'PT':
                        OCR_Text=self.pdftotext_ocr(file_path)

                    elif proc_mtd_value[0] == 'PO':
                        OCR_Text=self.pytesseract_ocr(file_path)

                    logger.log(f"OpenAI pdf ocr ::::: {OCR_Text}","0")
                

                else:
                    path = file_path
                    image = cv2.imread(path, 0)
                    OCR = pytesseract.image_to_string(image)
                    logger.log(f"{OCR}","0")
                    OCR_Text = OCR
                
                logger.log(f"OCR End !!!!!!!!!!!!!!!!!100","0")

                # if os.path.exists('ocrdatalog/') == False:
                #     os.mkdir('ocrdatalog')

                # ocrdatafile= open("ocrdatalog/"+userId+"_"+objName+"_ocrdata.txt","w+")
                # ocrdatafile.write(OCR_Text)
                # ocrdatafile.close()

                # if ent_code is None and ent_name is None:
                if not ent_code and not ent_name:
                    try:
                        logger.log(f"Template Extraction call Start !!!!!!!!!!!!!!!!!109","0")
                        resultdata = extract_data(invoicefile=file_path,templates=templates,input_module=input_module)
                        logger.log(f"Template Extraction call End !!!!!!!!!!!!!!!!!111","0")
                        logger.log(f"Template extracted data  ::::: 113 {resultdata}","0")
                        resultdata['isTemplateExtracted']='true'
                        # resultdata['OCR_DATA']=OCR_Text
                        if 'ent_code' in resultdata.keys():
                            result["EXTRACT_TEMPLATE_DATA"] = resultdata
                            result['OCR_DATA']=OCR_Text
                            return result
                        
                    except Exception as e:
                        logger.log(f'\n Exception : {e}', "1")

            else:
                # with open("ocrdatalog/"+userId+"_"+objName+"_ocrdata.txt",'r') as f:
                #     OCR_Text = f.read()
                if 'OCR_DATA' in jsonData.keys():
                    OCR_Text = jsonData['OCR_DATA']

            if proc_instr:
                logger.log(f'\n[ Open ai starting time 131 :        {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                openai.api_key = proc_api_key
                if '<DOCUMENT_DATA>' in proc_instr:
                    proc_instr = proc_instr.replace('<DOCUMENT_DATA>',OCR_Text)
                    logger.log(f'\n[ Open ai " model " Value              :      "text-davinci-003" ]', "0")
                    logger.log(f'\n[ Open ai " prompt " Value             :      "{proc_instr}" ]', "0")
                    logger.log(f'\n[ Open ai " temperature " Value        :      "0" ]', "0")
                    logger.log(f'\n[ Open ai " max_tokens " Value         :      "1800" ]', "0")
                    logger.log(f'\n[ Open ai " top_p " Value              :      "1" ]', "0")
                    logger.log(f'\n[ Open ai " frequency_penalty " Value  :      "0" ]', "0")
                    logger.log(f'\n[ Open ai " presence_penalty " Value   :      "0" ]', "0")
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt= proc_instr,
                    temperature=0,
                    max_tokens=1800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )

                else:
                    logger.log(f'\n[ Open ai " model " Value              :      "text-davinci-003" ]', "0")
                    logger.log(f'\n[ Open ai " prompt " Value             :      "{OCR_Text+proc_instr}" ]', "0")
                    logger.log(f'\n[ Open ai " temperature " Value        :      "0" ]', "0")
                    logger.log(f'\n[ Open ai " max_tokens " Value         :      "1800" ]', "0")
                    logger.log(f'\n[ Open ai " top_p " Value              :      "1" ]', "0")
                    logger.log(f'\n[ Open ai " frequency_penalty " Value  :      "0" ]', "0")
                    logger.log(f'\n[ Open ai " presence_penalty " Value   :      "0" ]', "0")
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt= OCR_Text+'\n'+proc_instr,
                    temperature=0,
                    max_tokens=1800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
                logger.log(f"Response openAI completion endpoint::::: {response}","0")
                finalResult=str(response["choices"][0]["text"])
                logger.log(f'\n [ Open ai completion time 171 :      {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                # print('line no. 102 !!!!!!!!!!!!!!!!!!!!',type(finalResult))
                logger.log(f"OpenAI completion endpoint finalResult ::::: {finalResult}","0")
                result["EXTRACT_LAYOUT_DATA"] = finalResult
                result['OCR_DATA']=OCR_Text

                # if os.path.exists('openailog/') == False:
                #     os.mkdir('openailog')

                # openaifile= open("openailog/"+userId+"_"+objName+"_openaidata.txt","w+")
                # openaifile.write(finalResult)
                # openaifile.close()
            
            logger.log(f"Response Return !!!!!!!!!!!! 142","0")
            return result
            
        
        except Exception as e:
            logger.log(f'\n In getCompletionEndpoint exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str(e)
            returnErr = self.getErrorXml(descr, trace)
            logger.log(f'\n Print exception returnSring inside getCompletionEndpoint : {returnErr}', "0")
            return str(returnErr)
        
    def getErrorXml(self, descr, trace):
        errorXml = '''<Root>
                            <Header>
                                <editFlag>null</editFlag>
                            </Header>
                            <Errors>
                                <error type="E">
                                    <message><![CDATA['''+descr+''']]></message>
                                    <trace><![CDATA['''+trace+''']]></trace>
                                    <type>E</type>
                                </error>
                            </Errors>
                        </Root>'''

        return errorXml


    def getlayouttextaidata(self):
        try:
            result = {}
            final_result = {}
            finalResult = ""
            proc_api_key = ""
            proc_instr = ""
            ent_name = ""
            ent_code = ""
            ent_type = ""
            ocr_return_data = ""
            
            jsonData = request.get_data('jsonData', None)
            jsonData = json.loads(jsonData[9:])
            logger.log(f"jsonData API openAI class::: !!!!!227 {jsonData}","0")

            if 'extract_templ' in jsonData.keys():
                given_temp_path = jsonData['extract_templ']
            
            if 'ent_code' in jsonData.keys():
                ent_code = jsonData['ent_code']
            
            if 'ent_type' in jsonData.keys():
                ent_type = jsonData['ent_type']

            if 'ent_name' in jsonData.keys():
                ent_name = jsonData['ent_name']

            if 'proc_instr' in jsonData.keys():
                proc_instr = jsonData['proc_instr']

            if 'proc_api_key' in jsonData.keys():
                proc_api_key   = jsonData['proc_api_key']

            if 'userId' in jsonData.keys():
                userId = jsonData['userId']

            if 'objName' in jsonData.keys():
                objName = jsonData['objName']
            
            if 'OCR_DATA' in jsonData.keys():
                ocr_return_data = jsonData['OCR_DATA']

            # with open("ocrdatalog/"+userId+"_"+objName+"_ocrdata.txt",'r') as f:
            #     ocr_return_data = f.read()
            #     logger.log(f"ocr_return_data !!!!!!!!!!!!!!!!!230 {ocr_return_data}","0")
            #     print(ocr_return_data)

            if proc_instr:
                logger.log(f'\n [ Open ai starting time 262 :            {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                openai.api_key = proc_api_key
                if '<DOCUMENT_DATA>' in proc_instr:
                    proc_instr = proc_instr.replace('<DOCUMENT_DATA>',ocr_return_data)
                    logger.log(f'\n[ Open ai " model " Value              :      "text-davinci-003" ]', "0")
                    logger.log(f'\n[ Open ai " prompt " Value             :      "{proc_instr}" ]', "0")
                    logger.log(f'\n[ Open ai " temperature " Value        :      "0" ]', "0")
                    logger.log(f'\n[ Open ai " max_tokens " Value         :      "1800" ]', "0")
                    logger.log(f'\n[ Open ai " top_p " Value              :      "1" ]', "0")
                    logger.log(f'\n[ Open ai " frequency_penalty " Value  :      "0" ]', "0")
                    logger.log(f'\n[ Open ai " presence_penalty " Value   :      "0" ]', "0")
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt= proc_instr,
                    temperature=0,
                    max_tokens=1800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )

                else:
                    logger.log(f'\n[ Open ai " model " Value              :      "text-davinci-003" ]', "0")
                    logger.log(f'\n[ Open ai " prompt " Value             :      "{ocr_return_data+proc_instr}" ]', "0")
                    logger.log(f'\n[ Open ai " temperature " Value        :      "0" ]', "0")
                    logger.log(f'\n[ Open ai " max_tokens " Value         :      "1800" ]', "0")
                    logger.log(f'\n[ Open ai " top_p " Value              :      "1" ]', "0")
                    logger.log(f'\n[ Open ai " frequency_penalty " Value  :      "0" ]', "0")
                    logger.log(f'\n[ Open ai " presence_penalty " Value   :      "0" ]', "0")
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt= ocr_return_data+'\n'+proc_instr,
                    temperature=0,
                    max_tokens=1800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
                logger.log(f"Response openAI completion endpoint::::: {response}","0")
                finalResult=str(response["choices"][0]["text"])
                logger.log(f'\n[ Open ai completion time  301  :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                ymlfilepath = "/"+(given_temp_path)+"/"+str(ent_name).strip().replace(" ","_").replace(".","")+".yml"
                if os.path.exists(ymlfilepath) == False and ent_name and ent_code:
                    logger.log(f'\n[ Template creation Start time  305  :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                    templatecreation = GenerateExtractTemplate()
                    templatecreation.generateHeaderTemplate(ymlfilepath,ent_name,ent_code,ent_type)
                    logger.log(f'\n[ Template creation End time  308  :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")

                print('line no. 237 !!!!!!!!!!!!!!!!!!!!',type(finalResult))
                logger.log(f"OpenAI completion endpoint finalResult ::::: {finalResult}","0")
                # openaifile= open("openailog/"+userId+"_"+objName+"_openaidata.txt","w+")
                # openaifile.write(finalResult)
                # openaifile.close()
                result["EXTRACT_LAYOUT_DATA"] = finalResult
                final_result['status'] = 1
                final_result['result'] = result
        except Exception as ex:
            final_result['status'] = 0
            final_result['error'] = str(ex)
        logger.log(f"Return result value !!!!!!!!! 203 {final_result}","0")
        return final_result
