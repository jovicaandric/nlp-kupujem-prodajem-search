package com.kupujem.prodajem.nlp.websocket.collector.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

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
    private final Date posted;

    public Ad(final RawWebsocketPayload payload) throws ParseException {
        this.id = payload.getAd_id();
        this.name = payload.getName();
        this.url = payload.getAd_url();
        this.thumbnail = payload.getThumbnail();
        this.price = parsePrice(payload);
        this.currency = payload.getCurrency().toUpperCase();
        final String[] parsedUrl = payload.getAd_url().split("/");
        this.category = parsedUrl[1];
        this.subCategory = parsedUrl[2];
        this.posted = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss").parse(payload.getPosted());
        this.lat = parseDouble(payload.getLat());
        this.lon = parseDouble(payload.getLon());
        final Document html = Jsoup.parse(payload.getHtml());
        this.location = html.select("#adDescription" + id + " > div > section.locationSec").text();
        this.description = html.select("#adDescription" + id + "> div > section.nameSec > div.fixedHeight > div.adDescription" +
                ".descriptionHeight").text();
    }

    @JsonIgnore
    public boolean isValid() {
        return price != null && !price.equals(PriceDescription.LOOKING.getValue()) && !price.equals(PriceDescription.BUYING.getValue());
    }

    private Double parsePrice(final RawWebsocketPayload payload) {
        final String rawPrice = payload.getPrice().split("&")[0].replace(".", "").replace(",", ".");

        try {
            Double price = Double.valueOf(rawPrice);
            return price;
        } catch (NumberFormatException e) {
            PriceDescription priceDescription = PriceDescription.getByLabel(rawPrice);

            if (priceDescription != null) {
                return priceDescription.getValue();
            }

            return null;
        }
    }

    private Double parseDouble(final String value) {
        try {
            Double doubleValue = Double.valueOf(value);
            return doubleValue;
        } catch (NumberFormatException e) {
            return null;
        }
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

    public Date getPosted() {
        return posted;
    }

    enum PriceDescription {
        CONTACT("Kontakt", -1d),
        AGREEMENT("Dogovor", -2d),
        CALL("Pozvati", -3d),
        FREE("Besplatno", -4d),
        BUYING("Kupujem", -5d),
        LOOKING("Tražim", -6d);

        private final String label;
        private final Double value;

        PriceDescription(final String label, final Double value) {
            this.label = label;
            this.value = value;
        }

        public String getLabel() {
            return label;
        }

        public Double getValue() {
            return value;
        }

        public static PriceDescription getByLabel(final String label) {
            switch (label) {
                case "Kontakt":
                    return CONTACT;
                case "Dogovor":
                    return AGREEMENT;
                case "Pozvati":
                    return CALL;
                case "Besplatno":
                    return FREE;
                case "Kupujem":
                    return BUYING;
                case "Tražim":
                    return LOOKING;
                default:
                    return null;
            }
        }
    }

}
