package com.kupujem.prodajem.nlp.websocket.collector.websocket;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties
@ConfigurationProperties("websocket")
public class WebsocketConfiguration {
    private String url;

    public String url() {
        return url;
    }

    public void setUrl(final String url) {
        this.url = url;
    }
}
