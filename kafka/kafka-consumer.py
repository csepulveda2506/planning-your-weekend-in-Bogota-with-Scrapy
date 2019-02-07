import argparse
import datetime
import json
from contextlib import closing
from threading import Thread

import psycopg2 as postgres
from kafka import KafkaConsumer


def consume_topic(args):
    global consumer, db
    try:
        consumer = KafkaConsumer(args.topic[0],
                                 group_id='consumer-util',
                                 bootstrap_servers=args.server,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit='false')
        db = postgres.connect(user='pycon',
                              password='pycon2019',
                              host='localhost',
                              database='pycon2019',
                              port='5432')
        while True:
            for message in consumer:
                print(f"New message - Key: {message.key} Value: "
                      f"{message.value}")
                with closing(db.cursor()) as cur:
                    msg_value = json.loads(message.value.decode('ascii'))
                    day, month, year = msg_value['start-date'] \
                        .split('-')
                    start_date = datetime.date(int(year), int(month), int(day))
                    cur.execute("""
                        INSERT INTO sites (location, title, 
                        startDate, 
                        description, price, link) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (link)
                        DO UPDATE SET (location, title, 
                        startDate, 
                        description, price) = 
                        (EXCLUDED.location, EXCLUDED.title, 
                        EXCLUDED.startDate, EXCLUDED.description,
                        EXCLUDED.price); 
                        """, (msg_value['location'],
                              msg_value['title'],
                              start_date,
                              msg_value['description'],
                              msg_value['price'],
                              msg_value['link']))
                db.commit()
                consumer.commit()
    except KeyboardInterrupt:
        consumer.close()
        return
    finally:
        db.close()
        consumer.close()


parser = argparse.ArgumentParser(description="Start a sink connector for "
                                             "Kafka broker")
parser.add_argument('server', metavar='K', type=str, nargs='+',
                    help='Broker url(s)')

parser.add_argument('topic', metavar='T', type=str, nargs='+',
                    help='Topic name(s)')

args = parser.parse_args()

t = Thread(target=consume_topic, args=(args,))
t.start()
