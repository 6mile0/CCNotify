from starlette.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI, status, Response
import json
import os
from dotenv import load_dotenv
load_dotenv()
DATA_DIR = os.getenv('DATADIR')

app = FastAPI()

# cors回避
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ローカルのため全許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/api/v1/caldata")
def get_caldata():
    with open(f"{DATA_DIR}/latest.json", "r") as f:
        data = f.read()
        print(type(data))
        return json.loads(data)


@app.get("/api/v1/caldata/{cal_id}", status_code=status.HTTP_200_OK)
def get_caldata_by_id(cal_id: str, response: Response):
    if os.path.exists(f"{DATA_DIR}/processed/{cal_id}.json"):
        with open(f"{DATA_DIR}/latest.json", "r") as f:
            data = f.read()
            print(type(data))
            return json.loads(data)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"The requested data does not exist."}


@app.get("/api/v1/update", status_code=status.HTTP_200_OK)
def update_caldata(response: Response):
    try:
        os.system("python getter.py")
        response.status_code = status.HTTP_200_OK
        return {"message": "Update completed."}
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Update failed."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, log_level="info")
