from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from typing import Optional
import uvicorn, os

app = FastAPI()

@app.post("/upload-file/{}")
async def upload_file(path: Optional[str] = None, file: UploadFile = File(...)):
    contents = await file.read()
    # 在此處處理文件內容，例如保存到特定位置或進行其他操作
    save_path = "" if path is None else path
    file_path = os.path.join(save_path, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    return {"filename": file.filename}

@app.get("/download-file")
async def download_file(filename: str, path: Optional[str] = None):
    # 指定下載的檔案路徑
    file_path = "" if path is None else path
    file_path = file_path + filename
    # 使用 FileResponse 回傳檔案
    return FileResponse(file_path, filename=filename)

def generate_file_list(directory, prefix: Optional[str] = None):
    file_list = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_link = f"<a href='download-file?filename={file_path}'>{file}</a>"
            #file_link = f"{prefix}/download-file?filename={file_path}"
            file_list.append(file_link)
    
    return file_list

@app.get("/list-file")
def list_files_with_links(directory, prefix: Optional[str] = None):
    # file_list = []
    # # 遍歷目錄中的所有檔案和子目錄
    # for root, dirs, files in os.walk(directory):
    #     for file in files:
    #         file_path = os.path.join(root, file)
    #         file_link = f"http://127.0.0.1:5000/download-file?filename={file_path}"
    #         file_list.append(file_link)
    
    # return HTMLResponse(status_code=200, content=file_list, background=True)
    file_list = generate_file_list(directory, prefix)
    file_list_html = "<br>".join(file_list)
    html_content = f"""
    <html>
    <body>
    <h1>檔案清單：</h1>
    {file_list_html}
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
