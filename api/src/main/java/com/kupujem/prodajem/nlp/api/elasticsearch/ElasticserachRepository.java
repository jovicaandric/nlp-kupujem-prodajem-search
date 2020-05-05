package com.kupujem.prodajem.nlp.api.elasticsearch;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import com.kupujem.prodajem.nlp.api.model.Ad;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.index.query.QueryStringQueryBuilder;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import static org.elasticsearch.client.RequestOptions.DEFAULT;

@Repository
public class ElasticserachRepository {

    private final RestHighLevelClient client;
    private final ElasticsearchConfiguration configuration;

    @Autowired
    public ElasticserachRepository(final RestHighLevelClient client, final ElasticsearchConfiguration configuration) {
        this.client = client;
        this.configuration = configuration;
    }

    public List<Ad> findAllBy(final String query) throws IOException {
        final QueryStringQueryBuilder queryBuilder = new QueryStringQueryBuilder("*" + query + "*");
        queryBuilder.defaultField("name");

        final SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();
        sourceBuilder.query(queryBuilder);
        sourceBuilder.size(1000);
        final SearchRequest request = new SearchRequest(configuration.getIndex());
        request.source(sourceBuilder);
        final List<Ad> ads = new LinkedList<>();

        client
            .search(request, DEFAULT)
            .getHits().forEach(hit -> ads.add(new Ad(hit.getSourceAsMap())));

        return ads;
    }
}
