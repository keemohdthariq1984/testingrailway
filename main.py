import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Forex API is live! Visit /rates to see MYR pairs."
    }

@app.get("/rates")
async def get_forex_rates():
    url = "https://frankfurter.app"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch forex data")
        
    data = response.json()
    rates = data["rates"]
    
    # Invert the rates (since API returns 1 MYR -> X Foreign Currency)
    return {
        "date": data["date"],
        "base": "MYR",
        "pairs": {
            "USD/MYR": round(1 / rates["USD"], 4),
            "GBP/MYR": round(1 / rates["GBP"], 4),
            "JPY/MYR": round(1 / rates["JPY"], 6),
            "100_JPY/MYR": round((1 / rates["JPY"]) * 100, 4)
        }
    }
