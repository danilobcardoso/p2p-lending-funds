import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  serverData: JSON;
  employeeData: JSON;

  portifolio: any[];
  returns: any[];
  view: any[] = [1800, 400];

  // options
  yAxisLabel: string = 'Valor';
  timeline: boolean = true;

  colorScheme = {
    domain: ['#5AA454', '#E44D25',  '#7aa3e5', '#a8385d', '#aae3f5']
  };



  constructor(private httpClient: HttpClient) {

    this.getAllEmployees()

  }

  getAllEmployees() {
    this.httpClient.get('http://127.0.0.1:5002/portfolio').subscribe(data => {
      this.portifolio = data as any[];
    })

    this.httpClient.get('http://127.0.0.1:5002/returns').subscribe(data => {
      console.log(data);
      this.returns = data as any[];
    })
  }



  onSelect(data): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  }

  onActivate(data): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  onDeactivate(data): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

}
