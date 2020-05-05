package com.kupujem.prodajem.nlp.api.controller;

import java.io.IOException;
import java.util.List;
import com.kupujem.prodajem.nlp.api.elasticsearch.ElasticserachRepository;
import com.kupujem.prodajem.nlp.api.model.Ad;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping(path = "/api/")
public class AdController {

    private ElasticserachRepository repository;

    @Autowired
    public AdController(final ElasticserachRepository repository) {
        this.repository = repository;
    }

    @GetMapping(path = "search/{query}", produces = "application/json")
    public ResponseEntity<List<Ad>> query(@PathVariable final String query) throws IOException {
        return ResponseEntity.ok(repository.findAllBy(query));
    }
}
