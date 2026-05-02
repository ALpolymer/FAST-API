import asyncio
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import(
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    FileResponse,
    StreamingResponse
)

app = FastAPI(title= "Custom Respone Types")

@app.get("/hello", response_class = PlainTextResponse)
def hello():
    #return "Hello, plain text!"
    return PlainTextResponse("Hello, plain text!")

@app.get("/home", response_class=HTMLResponse)
def home():
    html = """
    <html>
        <head><title>Home</title></head>
        <body>
            <h1>Welcome to FastAPI</h1>
            <p>This is an HTML response.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/greet/{name}", response_class=HTMLResponse)
def greet(name: str, title: str | None = None):
    display = f"{title} {name}" if title else name
    html = f"""
    <html>
        <head><title>Home</title></head>
        <body>
            <h1>Welcome {display} to FastAPI</h1>
            <p>This is an HTML response.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/go")
def go():
    return RedirectResponse("/docs", status_code= status.HTTP_307_TEMPORARY_REDIRECT)

@app.get("/download/{filename}", response_class= FileResponse)
def download(filename: str):
    safe_name = Path(filename).name
    file_path = Path(__file__).parent / safe_name
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"File {safe_name} not found")
    return FileResponse(path=file_path, filename=safe_name)

@app.get("/stream")
def stream():
    def generate():
        for i in range(10):
            yield f"Line - {i}\n"
    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/countdown")
async def countdown():
    async def tick():
        for i in range(10, 0, -1):
            yield f"{i}...\n"
            await asyncio.sleep(1)
        yield "Boooooooooommmmmm!!!!\n"
    return StreamingResponse(tick(), media_type="text/plain")