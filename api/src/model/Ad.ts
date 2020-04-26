export class Ad {
    id: number;
    url: string;
    currency: string;
    lat: string;
    lon: string;
    name: string;
    posted: Date;
    price: string;
    category: string;
    subCategory: string;
    location: string;
    description: string;
    thumbnail: string;

    constructor(data: any) {
        this.id = data.ad_id;
        this.url = data.ad_url;
        this.currency = data.currency;
        this.lat = data.lat;
        this.lon = data.lon;
        this.name = data.name;
        this.posted = new Date(data.posted);
        this.price = new String(data.price).split('&')[0];
        const parsedUrl = new String(data.ad_url).split('/');
        this.category = parsedUrl[1];
        this.subCategory = parsedUrl[2];
        this.thumbnail = data.thumbnail;
    }
}