package com.kupujem.prodajem.nlp.ad.ingestion.elasticsearch;

import java.io.IOException;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import static org.elasticsearch.client.RequestOptions.DEFAULT;
import static org.elasticsearch.common.xcontent.XContentType.JSON;

@Component
public class ElasticsearchPublisher {

    private final RestHighLevelClient client;
    private final ElasticsearchConfiguration configuration;

    @Autowired
    public ElasticsearchPublisher(final RestHighLevelClient client, final ElasticsearchConfiguration configuration) {
        this.client = client;
        this.configuration = configuration;
    }

    public void publish(final String document) {
        final IndexRequest request = new IndexRequest(configuration.getIndex());
        request.source(document, JSON);
        System.out.println(document);
        try {
            client.index(request, DEFAULT);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
