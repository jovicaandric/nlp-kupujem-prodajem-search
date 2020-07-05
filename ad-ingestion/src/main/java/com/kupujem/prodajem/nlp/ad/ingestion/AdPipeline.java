package com.kupujem.prodajem.nlp.ad.ingestion;

import com.kupujem.prodajem.nlp.ad.ingestion.elasticsearch.ElasticsearchPublisher;
import com.kupujem.prodajem.nlp.ad.ingestion.kafka.AdConsumer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class AdPipeline {

    private final AdConsumer consumer;
    private final ElasticsearchPublisher publisher;

    @Autowired
    public AdPipeline(final AdConsumer consumer, final ElasticsearchPublisher publisher) {
        this.consumer = consumer;
        this.publisher = publisher;
    }

    public void processAds() {
        List<String> ads = consumer.consume();
        publisher.publish(ads);
    }
}
