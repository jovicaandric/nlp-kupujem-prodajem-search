package com.kupujem.prodajem.nlp.websocket.collector;

import com.kupujem.prodajem.nlp.websocket.collector.websocket.AdWebsocketClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class AdWebsocketClientRunner implements CommandLineRunner {

    private final AdWebsocketClient client;

    @Autowired
    public AdWebsocketClientRunner(final AdWebsocketClient client) {
        this.client = client;
    }

    @Override
    public void run(final String... args) throws Exception {
        client.connect();
    }
}
