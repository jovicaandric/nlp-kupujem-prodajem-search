package com.kupujem.prodajem.nlp.websocket.collector.model;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

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
    private final Date posted;

    public Ad(final RawWebsocketPayload payload) throws ParseException {
        this.id = payload.getAd_id();
        this.name = payload.getName();
        this.url = payload.getAd_url();
        this.thumbnail = payload.getThumbnail();
        this.price = payload.getPrice().split("&")[0];
        this.currency = payload.getCurrency();
        final String[] parsedUrl = payload.getAd_url().split("/");
        this.category = parsedUrl[1];
        this.subCategory = parsedUrl[2];
        this.posted = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss").parse(payload.getPosted());
        this.lat = payload.getLat();
        this.lon = payload.getLon();
        final Document html = Jsoup.parse(payload.getHtml());
        this.location = html.select("#adDescription" + id + " > div > section.locationSec").text();
        this.description = html.select("#adDescription" + id + "> div > section.nameSec > div.fixedHeight > div.adDescription.descriptionHeight")
            .text();
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

    public Date getPosted() {
        return posted;
    }
}
