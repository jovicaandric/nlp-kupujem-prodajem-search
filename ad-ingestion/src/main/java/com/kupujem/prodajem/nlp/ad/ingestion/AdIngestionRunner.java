package com.kupujem.prodajem.nlp.ad.ingestion;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class AdIngestionRunner implements CommandLineRunner {

    private static final Logger LOGGER = LogManager.getLogger(AdIngestionRunner.class);

    private final AdPipeline pipeline;

    public AdIngestionRunner(final AdPipeline pipeline) {
        this.pipeline = pipeline;
    }

    @Override
    public void run(final String... args) {
        try {
            while (true) {
                pipeline.processAds();
            }
        } catch (final Exception exception) {
            LOGGER.error("An error occurred while processing ad pipeline.", exception);
        }
    }
}
