package com.kupujem.prodajem.nlp.api.model;

import java.util.Map;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public final class Ad {

    private final String id;
    private final String name;
    private final String url;
    private final String thumbnail;
    private final Double price;
    private final String currency;
    private final String description;
    private final String location;
    private final Double lat;
    private final Double lon;
    private final String category;
    private final String subCategory;
    private final String posted;

    @JsonCreator
    public Ad(
        @JsonProperty("id") final String id,
        @JsonProperty("name") final String name,
        @JsonProperty("url") final String url,
        @JsonProperty("thumbnail") final String thumbnail,
        @JsonProperty("price") final Double price,
        @JsonProperty("currency") final String currency,
        @JsonProperty("description") final String description,
        @JsonProperty("location") final String location,
        @JsonProperty("lat") final Double lat,
        @JsonProperty("lon") final Double lon,
        @JsonProperty("category") final String category,
        @JsonProperty("subCategory") final String subCategory,
        @JsonProperty("posted") final String posted
    ) {
        this.id = id;
        this.name = name;
        this.url = url;
        this.thumbnail = thumbnail;
        this.price = price;
        this.currency = currency;
        this.description = description;
        this.location = location;
        this.lat = lat;
        this.lon = lon;
        this.category = category;
        this.subCategory = subCategory;
        this.posted = posted;
    }

    public Ad(final Map<String, Object> elasticsearchHit) {
        this.id = String.valueOf(elasticsearchHit.get("id"));
        this.name = String.valueOf(elasticsearchHit.get("name"));
        this.url = String.valueOf(elasticsearchHit.get("url"));
        this.thumbnail = String.valueOf(elasticsearchHit.get("thumbnail"));
        this.price = Double.valueOf(elasticsearchHit.get("price").toString());
        this.currency = String.valueOf(elasticsearchHit.get("currency"));
        this.description = String.valueOf(elasticsearchHit.get("description"));
        this.location = String.valueOf(elasticsearchHit.get("location"));
        this.lat = Double.valueOf(elasticsearchHit.get("lat").toString());
        this.lon = Double.valueOf(elasticsearchHit.get("lon").toString());
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

    public Double getPrice() {
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

    public Double getLat() {
        return lat;
    }

    public Double getLon() {
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

