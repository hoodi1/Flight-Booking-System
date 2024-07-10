import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from '../login.service';

@Component({
  selector: 'app-bookings',
  templateUrl: './bookings.component.html',
  styleUrl: './bookings.component.css'
})
export class BookingsComponent {
    
  constructor(private service: LoginService, private router: Router){}

  userId = window.localStorage.getItem("userId");
  noBookings = false;
  bookings: any = [];
  userDetails: any;
  noBookMsg = ""

  ngOnInit(){
    console.log(this.userId)
    this.service.fetch_bookings(this.userId).subscribe(
      (res: any) => {
          if(!res.status){
            alert(res.message);
            this.router.navigate(["/dashboard"]);
          } else {
            if(!res.data.length){
              this.noBookings = true; 
              this.noBookMsg = res.message;
            } else {
              this.bookings = res.data[1];
              this.userDetails = res.data[0];
            }
          }
      },
      (err) => {
        alert("Something went wrong.")
      }
    )
  }

  cancelBooking(booking: any){
    this.service.cancel_booking(booking.bid).subscribe(
      (res:any) => {
        if(res.status){
          if(res.deleteStatus){
            alert(res.message);
            window.location.reload();
          } else {
            alert(res.message);
            window.location.reload();
          }
        } else {
          alert(res.message);
          window.location.reload();
        }
      }
    )
  }
}
