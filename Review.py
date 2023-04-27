import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3

app = FastAPI()

# Allow cross-origin resource sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle POST requests to /approve
@app.post('/approve')
async def approve(booking_id: str, status: int):
    # Publish the approval event to an SNS topic
    topic_arn = os.getenv('topicArn') or 'arn:aws:sns:ap-southeast-2:867964100065:booking-approval-topic'
    sns = boto3.client('sns')
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps({'bookingId': booking_id, 'status': status})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'message': 'Approval event published'}

# Health Check 
@app.get('/')
async def health_check():
    return {'message': 'OK'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
