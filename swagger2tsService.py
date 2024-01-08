import requests

response = requests.get("http://localhost:5062/swagger/v1/swagger.json")

def export(operationId, Path, Method, Tag):
    output = operationId + '(): Promise<AxiosResponse<'+operationId+'[], any>> {\nreturn axios.' + Method + '("http://localhost:5062' + Path + '");\n}'
    return output

def exportFile(data, tag):
    fileText = 'import axios, { AxiosResponse } from "axios"; \n class '+tag+'Service {\n'+data+'\n} \nexport default new '+tag+'Service();'
    return fileText

data = response.json()
tag_dict = {}

for path, methods in data['paths'].items():
    for method, details in methods.items():
        operation_id = details.get('operationId')
        tags = details.get('tags', [])
        if tags:
            tag = tags[0]
            if operation_id:
                tag_dict.setdefault(tag, []).append(export(operationId=operation_id, Path=path, Method=method, Tag=tag))
                print(export(operationId=operation_id, Path=path, Method=method, Tag=tag))

for tag, exports in tag_dict.items():
    filename = f"{tag.capitalize()}Service.ts"
    fText = ""
    with open(filename, "w") as file:
        for export_output in exports:
            fText += export_output + "\n"
        file.write(exportFile(fText, tag) + "\n")                          
    print(f"{filename} dosyasına yazıldı.")
