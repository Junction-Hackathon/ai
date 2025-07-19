import asyncio
import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

async def test_kafka():
    print("Testing Kafka connection...")
    
    try:
        producer = AIOKafkaProducer(
            bootstrap_servers="192.168.1.104:19092",
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        await producer.start()
        print("Producer connected successfully!")
        
        await producer.send_and_wait("video.process.start", {"test": "message"})
        print("Test message sent!")
        
        await producer.stop()
    except Exception as e:
        print(f"Producer failed: {e}")
        return
    
    try:
        consumer = AIOKafkaConsumer(
            "video.process.start",
            bootstrap_servers="192.168.1.104:19092",
            group_id="test-consumer",
            auto_offset_reset="earliest",
            value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else None
        )
        
        await consumer.start()
        print("Consumer connected successfully!")
        
        try:
            async for msg in consumer:
                print(f"Received message: {msg.value}")
                break
        except Exception as e:
            print(f"No messages or consume error: {e}")
        
        await consumer.stop()
        
    except Exception as e:
        print(f"Consumer failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_kafka())