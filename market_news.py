import finnhub
import time
import json
from kafka import KafkaProducer

finnhub_client = finnhub.Client(api_key="d01ht79r01qile5vp7u0d01ht79r01qile5vp7ug")

# Create a Kafka producer and topic
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'topic1'

while True:
    try:
        # Call the finnhub API to receive all general news
        news_response = finnhub_client.general_news('crypto', min_id=0)
        
        for article in news_response:
            # Get the headline of each news article
            headline = article.get('headline')
            if headline:
                producer.send(topic, {'headline': headline})
                print(f"Sent to Kafka: {headline}")

    except Exception as e:
        print(f"Error: {e}")
    
    # Wait 60 sec before looping to call for more news
    time.sleep(60)
