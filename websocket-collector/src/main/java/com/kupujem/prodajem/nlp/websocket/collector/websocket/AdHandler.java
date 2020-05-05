package com.kupujem.prodajem.nlp.websocket.collector.websocket;

import java.io.IOException;
import java.text.ParseException;
import java.util.Arrays;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.kupujem.prodajem.nlp.websocket.collector.kafka.AdProducer;
import com.kupujem.prodajem.nlp.websocket.collector.model.Ad;
import com.kupujem.prodajem.nlp.websocket.collector.model.RawWebsocketEvent;
import com.neovisionaries.ws.client.WebSocket;
import com.neovisionaries.ws.client.WebSocketAdapter;
import com.neovisionaries.ws.client.WebSocketException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import static com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS;

@Component
public class AdHandler extends WebSocketAdapter {

    private final static Logger LOGGER = LogManager.getLogger(AdHandler.class);

    private final AdProducer producer;

    @Autowired
    public AdHandler(final AdProducer producer) {
        this.producer = producer;
    }

    @Override
    public void onTextMessage(WebSocket ws, String message) throws IOException {
        final ObjectMapper mapper = new ObjectMapper();
        mapper.disable(WRITE_DATES_AS_TIMESTAMPS);
        final RawWebsocketEvent rawWebsocketEvent = mapper.readValue(message, RawWebsocketEvent.class);
        Arrays.stream(rawWebsocketEvent.getPayload()).forEach(payload -> {
            if (payload != null) {
                try {
                    final Ad ad = new Ad(payload);
                    if (!ad.getPrice().equals("Kupujem")) {
                        final String adJson = mapper.writeValueAsString(ad);
                        producer.publish(adJson);
                    }
                } catch (final JsonProcessingException | ParseException exception) {
                    LOGGER.error("An error occurred during serialization. ", exception);
                }
            }
        });
    }

    @Override
    public void onError(WebSocket websocket, WebSocketException cause) throws Exception {
        LOGGER.error("An error occurred. ", cause);
    }
}
