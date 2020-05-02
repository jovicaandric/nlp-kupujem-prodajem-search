import WebSocket from 'ws';
import { Ad } from './model/Ad';
import { Client } from '@elastic/elasticsearch';
import cheerio from 'cheerio';

const ws = new WebSocket('wss://ws.kupujemprodajem.com/wsfeed?get=combined');
const es = new Client({ node: process.env.ELASTICSEARCH_HOST })

ws.on('message', function incoming(data: any) {
    const rawSocketData: any[] = JSON.parse(data).payload;
    rawSocketData.forEach(ad => {
        if (ad) {
            const parsedAd: Ad = new Ad(ad);
            const dom = cheerio.load(ad.html);
            const location = dom('#adDescription' + parsedAd.id + ' > div > section.locationSec').text();
            const description = dom('#adDescription' + parsedAd.id + ' > div > section.nameSec > div.fixedHeight > div.adDescription.descriptionHeight').text();
            parsedAd.location = location ? location.trim() : '';
            parsedAd.description = description ? description.trim() : '';
            es.index({
                index: 'kp-nlp-ad-search',
                body: parsedAd
            }).catch(esError => console.error("An error occurred while writing to es.", esError));
        }
    });
});

ws.on('close', (code, reason) => {
    console.error("Closing websocket connection ", code, reason);
})

ws.on('error', (error) => {
    console.error("An error occurred on websocket ", error);
})