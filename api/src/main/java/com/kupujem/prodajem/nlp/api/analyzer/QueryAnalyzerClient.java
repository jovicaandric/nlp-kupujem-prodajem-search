package com.kupujem.prodajem.nlp.api.analyzer;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Component
public class QueryAnalyzerClient {

    private static final Logger LOGGER = LogManager.getLogger(QueryAnalyzerClient.class);

    private final String url;
    private final RestTemplate restTemplate;

    @Autowired
    public QueryAnalyzerClient(final QueryAnalyzerConfiguration configuration) {
        this.url = configuration.getUrl();
        this.restTemplate = new RestTemplateBuilder().build();
    }

    public String buildElasticsearchQuery(final String userQuery) {
        final HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));

        final Map<String, String> body = new HashMap<>();
        body.put("query", userQuery);

        final HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);

        try {
            final ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);
            if (response.getStatusCode() == HttpStatus.OK) {
                return response.getBody();
            } else {
                LOGGER.warn("Unsuccessful query analyzer request: status code {}", response.getStatusCode());
            }
        } catch (final RestClientException e) {
            LOGGER.error("Failed to analyze query", e);
        }

        return buildDefaultElasticsearchQuery(userQuery);
    }

    private String buildDefaultElasticsearchQuery(final String userQuery) {
        return "{\"query\": {"
            + "\"multi_match\": {"
            + "\"query\": \"" + userQuery + "\","
            + "\"fields\": [\"name\", \"description\"],"
            + "\"fuzziness\": \"AUTO\"}}}";
    }
}
