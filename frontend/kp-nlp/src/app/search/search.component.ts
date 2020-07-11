import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent {
  public results = [];
  public loader = false;
  public query = "";

  constructor(private http: HttpClient) { }

  search() {
    this.results = [];
    this.loader = true;

    const url = `${environment.apiUrl}/api/search/${this.query}`;
    this.http.get(url).subscribe((results: any) => { this.results = results; this.loader = false; });
  }

  negativePriceToLabel(price) {
    switch (price) {
      case -1: return "Kontakt";
      case -2: return "Dogovor";
      case -3: return "Poziv";
      case -4: return "Besplatno";
      case -5: return "Kupujem";
      case -6: return "Tražim";
      default: return price;
    }
  }
}
