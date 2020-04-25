import WebSocket from 'ws';
import { Ad } from './model/Ad';
import { Client } from '@elastic/elasticsearch';

const ws = new WebSocket('wss://ws.kupujemprodajem.com/wsfeed?get=combined');
const es = new Client({ node: 'http://35.207.72.77:9200' })

ws.on('message', function incoming(data: any) {
    const rawSocketData: any[] = JSON.parse(data).payload;
    rawSocketData.forEach(ad => {
        if (ad) {
            const parsedAd: Ad = new Ad(ad);
            es.index({
                index: 'kp_ad',
                body: parsedAd
            }).catch(esError => console.error("An error occurred while writing to es.", esError));
        }
    });
});