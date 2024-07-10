import { Component } from '@angular/core';
import { LoginService } from './login.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  isLoggedIn$!: Observable<boolean>;

  constructor(private service: LoginService) {

   }
  
  ngOnInit() {
    this.isLoggedIn$ = this.service.isLoggedIn;
  }

}
