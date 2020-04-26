import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

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

    this.http.get("http://35.207.72.77:8080/search/" + this.query).subscribe((results: any) => { this.results = results; this.loader = false; });
  }
}
