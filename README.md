# TradingBot

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