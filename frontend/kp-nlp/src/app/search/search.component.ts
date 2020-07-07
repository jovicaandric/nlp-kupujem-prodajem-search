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
}
