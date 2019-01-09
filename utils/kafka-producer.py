from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda m: json.dumps(m).encode(
                             'ascii'))

with open('test-data.json') as f:
    data = json.load(f)

for item in data:
    try:
        future = producer.send('pycon-test-topic',
                               key=bytes(item['link'], "ascii"),
                               value=item)
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        print(log.exception())
        pass
    except KeyboardInterrupt:
        producer.close()
