from fastapi import FastAPI

app = FastAPI()


@app.get("/{number}")
async def root(number: int = 1):
    return {"message": number}