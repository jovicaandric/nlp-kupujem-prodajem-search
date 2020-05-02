package com.kupujem.prodajem.nlp.websocket.collector.kafka;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties
@ConfigurationProperties("kafka.producer.ad")
public class AdProducerConfiguration {
    private String topic;
    private String servers;
    private String keySerializer;
    private String valueSerializer;

    public String topic() {
        return topic;
    }

    public void setTopic(final String topic) {
        this.topic = topic;
    }

    public String servers() {
        return servers;
    }

    public void setServers(final String servers) {
        this.servers = servers;
    }

    public String keyDeserializer() {
        return keySerializer;
    }

    public void setKeySerializer(final String keySerializer) {
        this.keySerializer = keySerializer;
    }

    public String valueDeserializer() {
        return valueSerializer;
    }

    public void setValueSerializer(final String valueSerializer) {
        this.valueSerializer = valueSerializer;
    }
}
