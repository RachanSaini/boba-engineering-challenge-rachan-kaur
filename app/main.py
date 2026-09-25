from fastapi import FastAPI
from app.api.trades import router as trades_router

app = FastAPI(
    title="Trade API",
    version="1"
)
app.include_router(trades_router)

@app.get("/")
def root():
    return {"message": "API is working"}


if __name__ == "__main__":
    main()