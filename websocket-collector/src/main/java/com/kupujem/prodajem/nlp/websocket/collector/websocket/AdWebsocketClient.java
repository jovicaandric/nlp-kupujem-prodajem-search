package com.kupujem.prodajem.nlp.websocket.collector.websocket;

import java.io.IOException;
import com.neovisionaries.ws.client.WebSocketException;
import com.neovisionaries.ws.client.WebSocketFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class AdWebsocketClient {

    private final WebsocketConfiguration configuration;
    private final AdHandler handler;

    @Autowired
    public AdWebsocketClient(final WebsocketConfiguration configuration, final AdHandler handler) {
        this.configuration = configuration;
        this.handler = handler;
    }

    public void connect() throws IOException, WebSocketException {
        new WebSocketFactory()
            .createSocket(configuration.url())
            .addListener(handler)
            .connect();
    }
}
