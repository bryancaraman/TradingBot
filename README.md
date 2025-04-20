# TradingBot

## Setup Kafka

1. Start off by downloading the repository to your chosen folder

2. Create a virtual Python environment (ideally using Python 3.11): source venv/bin/activate

3. Then, run this command in that folder to install the necessary packages: pip install kafka-python finnhub-python pyspark spacy

4. Now download the spacy model with: python -m spacy download en_core_web_md

5. Start your local Kafka server in a terminal session (can follow Kafka quickstart)

6. In another terminal session, run this command within the Kafka folder to create the two topics: 
    bin/kafka-topics.sh --create --topic topic1 --bootstrap-server localhost:9092
    bin/kafka-topics.sh --create --topic topic2 --bootstrap-server localhost:9092

7. Now navigate to the assignment_3 folder and run the market_news.py file: python market_news.py

8. In a third terminal session, navigate to the assignment_3 folder and run the named_entities_count.py file: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 named_entities_count.py localhost:9092 subscribe topic1

## Setup Elasticsearch, Kibana, and Logstash

1. Navigate to 'elasticsearch.yml' in 'elasticsearch/config' and set 'xpack.security.enabled' to 'false'

2. Run Elasticsearch: bin/elasticsearch

3. Navigate to 'kibana.yml' in 'kibana/config' and uncomment the line 'elasticsearch.hosts: ["http://localhost:9200/"]'

4. Run Kibana: bin/kibana

5. Add the 'logstash.conf' file from the assignment_3 repo to the logstash-9.0.0 folder

6. Run Logstash: bin/logstash -f logstash.conf

7. Open Kibana and open Stack Management under Management in the sidebar

8. Create a new data view under Kibana -> Data Views with the name 'named_entities' as the index pattern

9. Go to Analytics -> Visualize Library in the sidebar and create a new visualization using Legacy -> Aggregation Based -> Vertical Bar

10. Use named_entities as the data source 

11. Go to Metrics -> Y-Axis and change the aggregation to sum

12. Add a bucket for the X-Axis, select the Terms aggregation, name.keyword field, change the size to 10, and click update

Everything will be running and data will appear in 60 second intervals!