package com.kupujem.prodajem.nlp.api.elasticsearch;

import java.io.IOException;
import java.util.Arrays;
import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@Component
public class ElasticsearchClient {

    private final RestHighLevelClient restClient;

    @Autowired
    public ElasticsearchClient(final ElasticsearchConfiguration configuration) throws IOException {
        final HttpHost[] hosts = Arrays.stream(configuration.getHostname().split(","))
            .map(host -> new HttpHost(host, configuration.getPort())).toArray(HttpHost[]::new);
        this.restClient = new RestHighLevelClient(RestClient.builder(hosts));
    }

    @Bean
    public RestHighLevelClient restHighLevelClient() {
        return restClient;
    }

}
