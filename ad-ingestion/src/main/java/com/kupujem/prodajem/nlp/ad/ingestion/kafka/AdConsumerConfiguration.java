package com.kupujem.prodajem.nlp.ad.ingestion.kafka;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties
@ConfigurationProperties("kafka.consumer.ad")
public class AdConsumerConfiguration {

    private String servers;
    private String topic;
    private String keyDeserializer;
    private String valueDeserializer;
    private String consumerGroup;
    private int pollTimeout;
    private int maxPollRecords;
    private String offsetReset;

    public String getServers() {
        return servers;
    }

    public void setServers(final String servers) {
        this.servers = servers;
    }

    public String getTopic() {
        return topic;
    }

    public void setTopic(final String topic) {
        this.topic = topic;
    }

    public String getKeyDeserializer() {
        return keyDeserializer;
    }

    public void setKeyDeserializer(final String keyDeserializer) {
        this.keyDeserializer = keyDeserializer;
    }

    public String getValueDeserializer() {
        return valueDeserializer;
    }

    public void setValueDeserializer(final String valueDeserializer) {
        this.valueDeserializer = valueDeserializer;
    }

    public String getConsumerGroup() {
        return consumerGroup;
    }

    public void setConsumerGroup(final String consumerGroup) {
        this.consumerGroup = consumerGroup;
    }

    public int getPollTimeout() {
        return pollTimeout;
    }

    public void setPollTimeout(final int pollTimeout) {
        this.pollTimeout = pollTimeout;
    }

    public int getMaxPollRecords() {
        return maxPollRecords;
    }

    public void setMaxPollRecords(int maxPollRecords) {
        this.maxPollRecords = maxPollRecords;
    }

    public String getOffsetReset() {
        return offsetReset;
    }

    public void setOffsetReset(final String offsetReset) {
        this.offsetReset = offsetReset;
    }
}
