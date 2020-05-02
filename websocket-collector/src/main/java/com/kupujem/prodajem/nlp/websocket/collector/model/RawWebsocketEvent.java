package com.kupujem.prodajem.nlp.websocket.collector.model;

public class RawWebsocketEvent {

    private String type;
    private String service;
    private RawWebsocketPayload[] payload;

    public String getType() {
        return type;
    }

    public void setType(final String type) {
        this.type = type;
    }

    public String getService() {
        return service;
    }

    public void setService(final String service) {
        this.service = service;
    }

    public RawWebsocketPayload[] getPayload() {
        return payload;
    }

    public void setPayload(final RawWebsocketPayload[] payload) {
        this.payload = payload;
    }
}
