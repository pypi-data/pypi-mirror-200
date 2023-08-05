from kafka import KafkaProducer
from bdaserviceutils import get_kafka_binder_brokers
from alidaargparser import get_asset_property
import json

class Notifier:
    def __init__(self) -> None:
        self.isActive = False

        if get_asset_property(asset_name="go_manager", property="brokers") is not None:
            self.producer = KafkaProducer(bootstrap_servers=get_asset_property(asset_name="go_manager", property="brokers").split(","))
            self.topic = get_asset_property(asset_name="go_manager", property="topic")
            self.isActive = True

    def something_has_changed(self, metadata):
        if self.isActive:
            message = {"message": "Generic output updated", "metatada": metadata}
            self.producer.send(self.topic, json.dumps(message).encode('utf-8'))

