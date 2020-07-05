package com.kupujem.prodajem.nlp.ad.ingestion.kafka;

import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.Properties;

import static org.apache.kafka.clients.consumer.ConsumerConfig.AUTO_OFFSET_RESET_CONFIG;
import static org.apache.kafka.clients.consumer.ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG;
import static org.apache.kafka.clients.consumer.ConsumerConfig.FETCH_MIN_BYTES_CONFIG;
import static org.apache.kafka.clients.consumer.ConsumerConfig.GROUP_ID_CONFIG;
import static org.apache.kafka.clients.consumer.ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG;
import static org.apache.kafka.clients.consumer.ConsumerConfig.MAX_POLL_RECORDS_CONFIG;
import static org.apache.kafka.clients.consumer.ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG;

@Component
public class AdConsumer {

    private static final Logger LOGGER = LogManager.getLogger(AdConsumer.class);

    private final KafkaConsumer<String, String> consumer;
    private final AdConsumerConfiguration configuration;

    public AdConsumer(final AdConsumerConfiguration configuration) {
        this.configuration = configuration;
        final Properties properties = new Properties();
        properties.put(BOOTSTRAP_SERVERS_CONFIG, configuration.getServers());
        properties.put(KEY_DESERIALIZER_CLASS_CONFIG, configuration.getKeyDeserializer());
        properties.put(VALUE_DESERIALIZER_CLASS_CONFIG, configuration.getValueDeserializer());
        properties.put(GROUP_ID_CONFIG, configuration.getConsumerGroup());
        properties.put(AUTO_OFFSET_RESET_CONFIG, configuration.getOffsetReset());
        properties.put(MAX_POLL_RECORDS_CONFIG, configuration.getMaxPollRecords());
        properties.put(FETCH_MIN_BYTES_CONFIG, configuration.getFetchMinBytes());
        this.consumer = new KafkaConsumer<String, String>(properties);
        consumer.subscribe(Collections.singletonList(configuration.getTopic()));
    }

    public List<String> consume() {
        try {
            final ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(configuration.getPollTimeout()));
            final List<String> result = new LinkedList<>();
            records.forEach(record -> result.add(record.value()));
            consumer.commitSync();
            return result;
        } catch (final Exception e) {
            LOGGER.error("An error occurred while polling messages", e);
            return Collections.emptyList();
        }
    }
}
