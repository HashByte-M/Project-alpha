from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import all your helper functions here (from app.py)
from .models import (
    classify_files, get_ai_column_mapping, manual_column_mapper, load_and_normalize_data,
    get_processed_data, generate_data_quality_report, get_regional_status_summary,
    calculate_trend_stations, analyze_monsoon_performance, detect_drought_events, 
    find_nearest_station, get_gemini_analysis
)

@app.post("/api/upload")
async def upload_files(
    gw_station: UploadFile,
    rf_station: UploadFile,
    timeseries: UploadFile,
    ai_disabled: bool = Form(...),
    gemini_key: str = Form(None)
):
    gw_bytes = await gw_station.read()
    rf_bytes = await rf_station.read()
    ts_bytes = await timeseries.read()
    
    # Classify files, map columns (AI/manual), normalize data, etc.
    # Use the same logic as your Streamlit app
    
    file_contents = {
        gw_station.filename: gw_bytes,
        rf_station.filename: rf_bytes,
        timeseries.filename: ts_bytes,
    }
    probable_roles, _ = classify_files([gw_bytes, rf_bytes, ts_bytes])
    # ... follow same steps as app.py ...
    return {"status": "ok"}  # return all needed objects

@app.post("/api/map-columns")
def map_columns(raw_columns: list, target_schema: list, ai_disabled: bool, gemini_key: str = None):
    if ai_disabled:
        # Return manual mapping UI structure, frontend will render as dropdowns
        return {"manual": True, "options": raw_columns}
    else:
        mapping = get_ai_column_mapping(raw_columns, target_schema, gemini_key)
        return {"manual": False, "mapping": mapping}

@app.post("/api/gemini-analysis")
def gemini_analysis(prompt: str, gemini_key: str):
    result = get_gemini_analysis(prompt, gemini_key)
    return {"result": result}

# More endpoints for all dashboard logic, forecasting, reporting, etc.

# Example: Data Quality Report
@app.post("/api/data-quality")
def data_quality_report(csv: UploadFile, name: str):
    df = pd.read_csv(io.BytesIO(csv.file.read()))
    report = generate_data_quality_report(df, name)
    return {"report": report}