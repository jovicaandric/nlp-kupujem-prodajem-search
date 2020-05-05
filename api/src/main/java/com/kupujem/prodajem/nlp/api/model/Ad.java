package com.kupujem.prodajem.nlp.api.model;

import java.util.Date;
import java.util.Map;


public final class Ad {

    private final String id;
    private final String name;
    private final String url;
    private final String thumbnail;
    private final String price;
    private final String currency;
    private final String description;
    private final String location;
    private final String lat;
    private final String lon;
    private final String category;
    private final String subCategory;
    private final String posted;

    public Ad(final Map<String, Object> elasticsearchHit) {
        this.id = String.valueOf(elasticsearchHit.get("id"));
        this.name = String.valueOf(elasticsearchHit.get("name"));
        this.url = String.valueOf(elasticsearchHit.get("url"));
        this.thumbnail = String.valueOf(elasticsearchHit.get("thumbnail"));
        this.price = String.valueOf(elasticsearchHit.get("price"));
        this.currency = String.valueOf(elasticsearchHit.get("currency"));
        this.description = String.valueOf(elasticsearchHit.get("description"));
        this.location = String.valueOf(elasticsearchHit.get("location"));
        this.lat = String.valueOf(elasticsearchHit.get("lat"));
        this.lon = String.valueOf(elasticsearchHit.get("lon"));
        this.category = String.valueOf(elasticsearchHit.get("category"));
        this.subCategory = String.valueOf(elasticsearchHit.get("subCategory"));
        this.posted = String.valueOf(elasticsearchHit.get("posted"));
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getUrl() {
        return url;
    }

    public String getThumbnail() {
        return thumbnail;
    }

    public String getPrice() {
        return price;
    }

    public String getCurrency() {
        return currency;
    }

    public String getDescription() {
        return description;
    }

    public String getLocation() {
        return location;
    }

    public String getLat() {
        return lat;
    }

    public String getLon() {
        return lon;
    }

    public String getCategory() {
        return category;
    }

    public String getSubCategory() {
        return subCategory;
    }

    public String getPosted() {
        return posted;
    }
}

