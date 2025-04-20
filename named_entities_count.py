import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.streaming import DataStreamReader
from collections import Counter
from kafka import KafkaProducer
import spacy
import json

spark = SparkSession.builder \
    .appName("NamedEntityStreaming") \
    .getOrCreate()

nlp = spacy.load("en_core_web_md")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sends message to topic2
def send_to_kafka(entities_count):
    producer.send('topic2', value=entities_count)
    producer.flush()  

excluded_labels = {
    "CARDINAL", 
    "ORDINAL",   
    "DATE",      
    "TIME",     
    "QUANTITY",  
    "PERCENT",   
    "MONEY",     
}

# Extract named entities and update global entity counter
def extract_and_update_entities(text, global_entity_count):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ not in excluded_labels]
    for entity in entities:
        global_entity_count[entity] += 1

# Hold running counts of named entities
global_entity_count = Counter()

# Create stream reading from topic1
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic1") \
    .option("startingOffsets", "latest") \
    .load()

# Convert the value column to string
text_df = df.selectExpr("CAST(value AS STRING) as text")

# Extract entities and update the global count
def process_batch(batch_df, batch_id):
    global global_entity_count

    for row in batch_df.collect():
        extract_and_update_entities(row['text'], global_entity_count)

    ranked_entities = [{"name": entity, "count": count} for entity, count in global_entity_count.items()]
    ranked_entities.sort(key=lambda x: x["count"], reverse=True)

    send_to_kafka(ranked_entities)

# Write to topic2 every minute
query = text_df.writeStream \
    .foreachBatch(process_batch) \
    .trigger(processingTime="1 minute") \
    .start()

query.awaitTermination()
