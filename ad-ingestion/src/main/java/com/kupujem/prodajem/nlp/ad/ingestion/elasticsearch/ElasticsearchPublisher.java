package com.kupujem.prodajem.nlp.ad.ingestion.elasticsearch;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.elasticsearch.action.bulk.BulkRequest;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.List;

import static org.elasticsearch.client.RequestOptions.DEFAULT;
import static org.elasticsearch.common.xcontent.XContentType.JSON;

@Component
public class ElasticsearchPublisher {

    private static final Logger LOGGER = LogManager.getLogger(ElasticsearchPublisher.class);

    private final RestHighLevelClient client;
    private final ElasticsearchConfiguration configuration;
    private final ObjectMapper mapper;

    @Autowired
    public ElasticsearchPublisher(final RestHighLevelClient client, final ElasticsearchConfiguration configuration) {
        this.client = client;
        this.configuration = configuration;
        this.mapper = new ObjectMapper();
    }

    public void publish(final List<String> documents) {
        final BulkRequest bulkRequest = new BulkRequest();

        for (String document : documents) {
            final IndexRequest request = new IndexRequest(configuration.getIndex());
            final String docId = extractDocId(document);
            request.id(docId);
            request.source(document, JSON);
            bulkRequest.add(request);
        }

        try {
            if (bulkRequest.numberOfActions() > 0) {
                client.bulk(bulkRequest, DEFAULT);
                LOGGER.info("Published {} documents to '{}' index", documents.size(), configuration.getIndex());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String extractDocId(String doc) {
        try {
            JsonNode on = mapper.readValue(doc, JsonNode.class);
            return on.get("id").asText();
        } catch (IOException e) {
            return "null";
        }
    }
}
