# rfq-intelligence-engine

to run rule engine 
uv run python -m src.main


to train model 
uv run python -m src.ml.trainer



Chat Message 
|
Pub/Sub (Ingestion)
|
Dataflow (Apache Beam Streaming)
|
Cloud Run  (Rule + ML + LLM Service)
|
BigQuery/Pubsub (Trade Output)



pub/sub topic

gcloud pubsub topics create rfq-messages
gcloud pubsub subscriptions create rfq-sub --topic=rfq-messages

BigQuery

bq mk rfq_dataset
bq mk rfq_dataset.trades


Inference API
POST /predict
    {
        "message":"quote 10m eurusd spot"
    }

Response 
    Trade Object

    Rule Layer
        ↓
    Flair ML
        ↓
    Confidence Routing
        ↓
    Vertex AI (if needed)    


Upload model 
docker run -e USE_GCS=true -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json -v D:\gcp-key\gcp-key.json:/app/key.json  rfq-trainer:optimized    

flair prediction service

https://<cloud run url >/predict

{
        "text":"quote 10m eurusd spot"
    }




Training Service -> Flair Prediction Service  -> Pipline Service 

