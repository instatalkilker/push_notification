from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import messaging, credentials

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("instatalk-301bd-adminsdk.json")
firebase_admin.initialize_app(cred)

app = FastAPI()

# Define the request model
class MessagePayload(BaseModel):
    registration_token: str
    message: str
    # time: str

@app.post("/send_message/")
async def send_message(payload: MessagePayload):
    # Create a message with the provided payload
    message = messaging.Message(
        data={
            'message': payload.message
            # 'time': payload.time,
        },
        token=payload.registration_token,
    )

    try:
        # Send a message to the device corresponding to the provided registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        return {"message": "Successfully sent message", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
