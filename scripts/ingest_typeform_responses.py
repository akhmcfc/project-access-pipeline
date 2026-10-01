"""
6_ingest_typeform_responses.py - Ingest Typeform Responses into Database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import requests
import json
from datetime import datetime
from config.config import DATABASE_FILE, TYPEFORM_API_TOKEN
from config.config import SURVEY_2_FORM_ID, SURVEY_3_FORM_ID

TYPEFORM_API_BASE = "https://api.typeform.com/forms"

def get_typeform_responses(form_id):
    """Fetch all responses from a Typeform"""
    url = f"{TYPEFORM_API_BASE}/{form_id}/responses"
    
    headers = {
        "Authorization": f"Bearer {TYPEFORM_API_TOKEN}"
    }
    
    params = {
        "page_size": 1000
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching responses from Typeform: {e}")
        return None

def extract_survey_2_data(response):
    """Extract Survey 2 response data"""
    data = {
        "candidate_id": None,
        "submitted_at": response.get("submitted_at"),
        "answers": {}
    }
    
    for answer in response.get("answers", []):
        field_type = answer.get("field", {}).get("type")
        field_ref = answer.get("field", {}).get("ref")
        
        # Extract candidate_id from hidden field
        if field_type == "hidden":
            data["candidate_id"] = answer.get("value")
        
        # Parse different answer types
        elif field_type == "choice":
            data["answers"][field_ref] = answer.get("choice", {}).get("label")
        elif field_type == "choices":
            data["answers"][field_ref] = [c.get("label") for c in answer.get("choices", [])]
        elif field_type == "text":
            data["answers"][field_ref] = answer.get("text")
    
    return data

def extract_survey_3_data(response):
    """Extract Survey 3 response data"""
    data = {
        "candidate_id": None,
        "submitted_at": response.get("submitted_at"),
        "answers": {}
    }
    
    for answer in response.get("answers", []):
        field_type = answer.get("field", {}).get("type")
        field_ref = answer.get("field", {}).get("ref")
        
        # Extract candidate_id
        if field_type == "hidden":
            data["candidate_id"] = answer.get("value")
        
        elif field_type == "choice":
            data["answers"][field_ref] = answer.get("choice", {}).get("label")
        elif field_type == "choices":
            data["answers"][field_ref] = [c.get("label") for c in answer.get("choices", [])]
        elif field_type == "text":
            data["answers"][field_ref] = answer.get("text")
        elif field_type == "rating":
            data["answers"][field_ref] = answer.get("number")
    
    return data

def ingest_survey_2_responses():
    """Fetch and store Survey 2 responses"""
    print("\n" + "="*70)
    print("📥 INGESTING SURVEY 2 RESPONSES")
    print("="*70 + "\n")
    
    responses = get_typeform_responses(SURVEY_2_FORM_ID)
    if not responses:
        print("❌ Failed to fetch Survey 2 responses")
        return 0
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    count = 0
    for response in responses.get("items", []):
        data = extract_survey_2_data(response)
        
        if not data["candidate_id"]:
            print(f"⚠️  Skipping response - no candidate_id")
            continue
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO mid_bootcamp_2026 
                (candidate_id, changed_universities, changed_destination, 
                 changed_major, biggest_challenge, bootcamp_resources_used,
                 support_needed, what_working_well, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data["candidate_id"],
                json.dumps(data["answers"].get("changed_universities", [])),
                data["answers"].get("changed_destination"),
                data["answers"].get("changed_major"),
                data["answers"].get("biggest_challenge"),
                json.dumps(data["answers"].get("bootcamp_resources", [])),
                data["answers"].get("support_needed"),
                data["answers"].get("what_working_well"),
                data["submitted_at"]
            ))
            
            count += 1
            print(f"✅ {data['candidate_id']}")
        
        except Exception as e:
            print(f"❌ Error storing {data['candidate_id']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*70}")
    print(f"✅ SURVEY 2: Ingested {count} responses")
    print(f"{'='*70}\n")
    
    return count

def ingest_survey_3_responses():
    """Fetch and store Survey 3 responses"""
    print("\n" + "="*70)
    print("📥 INGESTING SURVEY 3 RESPONSES")
    print("="*70 + "\n")
    
    responses = get_typeform_responses(SURVEY_3_FORM_ID)
    if not responses:
        print("❌ Failed to fetch Survey 3 responses")
        return 0
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    count = 0
    for response in responses.get("items", []):
        data = extract_survey_3_data(response)
        
        if not data["candidate_id"]:
            print(f"⚠️  Skipping response - no candidate_id")
            continue
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO post_bootcamp_2026
                (candidate_id, heard_back_status, universities_applied_to,
                 acceptances_received, final_choice, bootcamp_impact_final,
                 most_valuable_element, resources_missing, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data["candidate_id"],
                data["answers"].get("heard_back"),
                data["answers"].get("universities_applied"),
                json.dumps(data["answers"].get("acceptances_received", [])),
                data["answers"].get("final_choice"),
                data["answers"].get("bootcamp_impact"),
                data["answers"].get("most_valuable"),
                data["answers"].get("resources_missing"),
                data["submitted_at"]
            ))
            
            count += 1
            print(f"✅ {data['candidate_id']}")
        
        except Exception as e:
            print(f"❌ Error storing {data['candidate_id']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*70}")
    print(f"✅ SURVEY 3: Ingested {count} responses")
    print(f"{'='*70}\n")
    
    return count

def ingest_all_responses():
    """Ingest all survey responses"""
    print("\n" + "="*70)
    print("🔄 TYPEFORM RESPONSE INGESTION PIPELINE")
    print("="*70)
    
    survey_2_count = ingest_survey_2_responses()
    survey_3_count = ingest_survey_3_responses()
    
    print(f"\n{'='*70}")
    print("📊 INGESTION SUMMARY")
    print(f"{'='*70}")
    print(f"Survey 2 responses: {survey_2_count}")
    print(f"Survey 3 responses: {survey_3_count}")
    print(f"Total: {survey_2_count + survey_3_count}")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    ingest_all_responses()
