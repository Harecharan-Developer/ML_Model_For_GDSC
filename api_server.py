from fastapi import FastAPI, Form, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
import pickle
import json  # Ensure json is imported correctly
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("pyfirebasesdk.json")
firebase_admin.initialize_app(cred)
    
db=firestore.client()

app = FastAPI()

# Load the pkl file
with open('ml_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.post("/predict")
async def predict_fish(
    Temperature: float = Form(...),
    Turbidity: float = Form(...),
    Dissolved_Oxygen: float = Form(...),
    PH: float = Form(...),
    Ammonia: float = Form(...),
    Nitrate: float = Form(...),
    entry_id:int =Form(...),
    population:int = 50
):
    try:
        
        # Perform prediction using the loaded model
        prediction = model.predict([[entry_id, Temperature, Turbidity, Dissolved_Oxygen, PH, Ammonia, Nitrate, population]])
        # Prepare the response as a JSON object directly

        weight= prediction[0][0]  # Assuming model output format
        length= prediction[0][1]
        
        if length >= 20 and length <= 26 and weight >= 150 and weight <= 250:
            fish_type = "Rui"
        elif length >= 15 and length <= 25 and weight >= 180 and weight <= 300:
            fish_type = "Koi"
        elif length >= 18 and length <= 30 and weight >= 200 and weight <= 625:
            fish_type = "Silvercarp"
        elif length >= 10 and  weight >= 120:
            fish_type = "Karpio"
        else:
            fish_type = "Salmon"

        try:
            # Query documents
            fish_data_collection = db.collection('buoys').where("id", "==", entry_id).stream()

            # Update documents
            for doc in fish_data_collection:
                data = doc.to_dict()
                print("Updating document:", doc.id)
                doc.reference.update({"fish": fish_type})
                print("Document updated successfully.")

            # Commit batched writes
            batch.commit()
            print("Batch committed successfully.")

        except Exception as e:
            print("An error occurred in db updation part:", str(e))



        return fish_type  # No need to use json.dumps() here

    except Exception as e:
        return JSONResponse(content={"error in prediction ": str(e)})


