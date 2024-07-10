import { Component } from '@angular/core';
import { LoginService } from '../login.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  userId = window.localStorage.getItem("userId");

  constructor(private service: LoginService) { }
  
  ngOnInit() {
  }

  logout(){
    this.service.logout();
  }

}
