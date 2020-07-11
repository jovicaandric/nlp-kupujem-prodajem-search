package com.kupujem.prodajem.nlp.api.elasticsearch;

import java.io.IOException;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.kupujem.prodajem.nlp.api.model.Ad;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Repository;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Repository
public class ElasticsearchRepository {

    private static final Logger LOGGER = LogManager.getLogger(ElasticsearchRepository.class);

    private final String url;

    @Autowired
    public ElasticsearchRepository(final ElasticsearchConfiguration configuration) {
        this.url = String.format(
            "http://%s:%s/%s/_search?size=25",
            configuration.getHostname(),
            configuration.getPort(),
            configuration.getIndex()
        );
    }

    public List<Ad> findAllBy(final String query) {
        final HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));

        final HttpEntity<String> entity = new HttpEntity<>(query, headers);
        final RestTemplate restTemplate = new RestTemplateBuilder().build();

        try {
            final ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);
            if (response.getStatusCode() == HttpStatus.OK) {
                return deserializeAdDocuments(response.getBody());
            } else {
                LOGGER.error(
                    "Elasticsearch search query request: {} {}",
                    response.getStatusCode(),
                    response.getStatusCode().getReasonPhrase()
                );
            }
        } catch (final RestClientException | IOException e) {
            LOGGER.error("Elasticsearch search query failed", e);
        }

        return new LinkedList<>();
    }

    private List<Ad> deserializeAdDocuments(final String responseBody) throws IOException {
        final List<Ad> ads = new LinkedList<>();

        final ObjectMapper mapper = new ObjectMapper();
        final JsonNode responseNode = mapper.readValue(responseBody, JsonNode.class);
        final JsonNode hits = responseNode.get("hits").get("hits");

        hits.elements().forEachRemaining(jsonNode -> {
            final String source = jsonNode.get("_source").toString();
            try {
                final Ad ad = mapper.readValue(source, Ad.class);
                ads.add(ad);
            } catch (final IOException e) {
                LOGGER.error("Failed to deserialize ad document", e);
            }
        });

        return ads;
    }
}
