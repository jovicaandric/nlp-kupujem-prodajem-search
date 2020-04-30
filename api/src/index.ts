import Express from 'express';
import { Ad } from './model/Ad';
import { Client } from '@elastic/elasticsearch';

const es = new Client({ node: process.env.ELASTICSEARCH_HOST })
const app = Express();
const port = 8080 || process.env.PORT;

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.options('*', (req, res) => {
    res.send(200);
});

app.get("/search/:query", (req, res) => {
    es.search({
        index: 'kp-nlp-ad-search',
        size: 10000,
        body: {
            _source: {
                excludes: ['html']
            },
            query: {
                match: { name: req.params.query },

            }
        }
    }).then((esHit: any) => {
        const ads: Ad[] = esHit.body.hits.hits.map((hit: any) => hit._source as Ad);
        res.send(ads);
    }).catch(error =>
        console.error(error));
});

app.listen(port, () => {
    console.log(`server started at http://localhost:${port}`);
});