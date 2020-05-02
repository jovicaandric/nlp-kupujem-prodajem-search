package com.kupujem.prodajem.nlp.websocket.collector.model;

public class RawWebsocketPayload {

    private String ad_id;
    private String ad_url;
    private String name;
    private String thumbnail;
    private String price;
    private String html;
    private String posted;
    private String currency;
    private String lat;
    private String lon;
    private String url;
    private String location_id;

    public String getAd_id() {
        return ad_id;
    }

    public void setAd_id(final String ad_id) {
        this.ad_id = ad_id;
    }

    public String getAd_url() {
        return ad_url;
    }

    public void setAd_url(final String ad_url) {
        this.ad_url = ad_url;
    }

    public String getName() {
        return name;
    }

    public void setName(final String name) {
        this.name = name;
    }

    public String getThumbnail() {
        return thumbnail;
    }

    public void setThumbnail(final String thumbnail) {
        this.thumbnail = thumbnail;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(final String price) {
        this.price = price;
    }

    public String getHtml() {
        return html;
    }

    public void setHtml(final String html) {
        this.html = html;
    }

    public String getPosted() {
        return posted;
    }

    public void setPosted(final String posted) {
        this.posted = posted;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(final String currency) {
        this.currency = currency;
    }

    public String getLat() {
        return lat;
    }

    public void setLat(final String lat) {
        this.lat = lat;
    }

    public String getLon() {
        return lon;
    }

    public void setLon(final String lon) {
        this.lon = lon;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(final String url) {
        this.url = url;
    }

    public String getLocation_id() {
        return location_id;
    }

    public void setLocation_id(final String location_id) {
        this.location_id = location_id;
    }
}
