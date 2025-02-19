import sys

import uvicorn
from fastapi import FastAPI
class Application:
    @classmethod
    def setup(cls, app: FastAPI):

        return app


app = FastAPI(
    title="Shopping Bot",
    description="Voice UX for Shopping",
)

app = Application.setup(app)

# Running the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=8)
