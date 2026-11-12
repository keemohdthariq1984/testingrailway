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
    # Updated Frankfurter v2 endpoint
    url = "https://frankfurter.dev"
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        
    if response.status_code != 200:
        raise HTTPException(
            status_code=502, 
            detail=f"Frankfurter API returned status {response.status_code}: {response.text}"
        )
        
    data = response.json()
    
    # Map the list of quote objects into a dictionary (e.g., {"USD": 0.225, ...})
    rates = {item["quote"]: item["rate"] for item in data}
    date = data[0]["date"] if data else "unknown"
    
    return {
        "date": date,
        "base": "MYR",
        "pairs": {
            "USD/MYR": round(1 / rates["USD"], 4),
            "GBP/MYR": round(1 / rates["GBP"], 4),
            "JPY/MYR": round(1 / rates["JPY"], 6),
            "100_JPY/MYR": round((1 / rates["JPY"]) * 100, 4)
        }
    }
