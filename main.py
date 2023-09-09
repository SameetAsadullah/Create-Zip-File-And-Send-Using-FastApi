import zipfile
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import os

## FastApi configuration
app = FastAPI()

## Route
@app.post("/zip/download")
@app.post("/zip/download/")
async def zip_download():
    zip_bytes_io = io.BytesIO()
    with zipfile.ZipFile(zip_bytes_io, 'w', zipfile.ZIP_DEFLATED) as zipped:
        for dirname, subdirs, files in os.walk('output'):
            zipped.write(dirname)
            for filename in files:
                zipped.write(os.path.join(dirname, filename))

    response = StreamingResponse(
                iter([zip_bytes_io.getvalue()]),
                media_type="application/x-zip-compressed",
                headers = {"Content-Disposition":f"attachment;filename=output.zip",
                            "Content-Length": str(zip_bytes_io.getbuffer().nbytes)}
            )
    zip_bytes_io.close()
    return response
