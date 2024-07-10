import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private loggedIn: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  get isLoggedIn() {
    return this.loggedIn.asObservable();
  }

  setLoggedIn(value: any){
    this.loggedIn.next(value);
  }

  constructor(private httpclient: HttpClient, private router:Router) { }

  login(data: any){
    return this.httpclient.post("http://127.0.0.1:5000/login", data)
  }

  register(data: any){
    return this.httpclient.post("http://127.0.0.1:5000/register", data)
  }

  logout() {
    this.loggedIn.next(false);
    this.router.navigate(['/home']);
  }

  search(data: any){
    return this.httpclient.post("http://127.0.0.1:5000/search", data)
  }

  book_flight(data: any){
    return this.httpclient.put("http://127.0.0.1:5000/book_flight", data)
  }

  fetch_bookings(userId:any){
    return this.httpclient.get("http://127.0.0.1:5000/bookings?userId=" + userId.toString())
  }

  cancel_booking(bid:any){
    return this.httpclient.delete("http://127.0.0.1:5000/cancelFlights?bid=" + bid.toString())
  }
}
