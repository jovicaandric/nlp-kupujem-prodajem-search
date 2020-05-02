package com.kupujem.prodajem.nlp.websocket.collector.kafka;

import java.util.Properties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import static org.apache.kafka.clients.producer.ProducerConfig.BOOTSTRAP_SERVERS_CONFIG;
import static org.apache.kafka.clients.producer.ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG;
import static org.apache.kafka.clients.producer.ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG;

@Component
public class AdProducer {

    private AdProducerConfiguration configuration;
    private final Producer<String, String> producer;

    @Autowired
    public AdProducer(final AdProducerConfiguration configuration) {
        this.configuration = configuration;
        final Properties properties = new Properties();
        properties.put(BOOTSTRAP_SERVERS_CONFIG, configuration.servers());
        properties.put(KEY_SERIALIZER_CLASS_CONFIG, configuration.keyDeserializer());
        properties.put(VALUE_SERIALIZER_CLASS_CONFIG, configuration.valueDeserializer());
        producer = new KafkaProducer<String, String>(properties);
    }

    public void publish(final String message) {
        producer.send(new ProducerRecord<>(configuration.topic(), message));
    }
}
