import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from '../login.service';
import { AnyCatcher } from 'rxjs/internal/AnyCatcher';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  public searchForm!:FormGroup;
  allFlights: any;
  searchClicked = false;

  constructor(private fb:FormBuilder,private router:Router, private loginservice : LoginService) { }

  ngOnInit(): void {
    this.searchForm = this.fb.group({
      source:['',Validators.required],
      destination:['',Validators.required],
      date:['', Validators.required]
    })
  }

  search(){
    this.searchClicked = true;
    this.loginservice.search(this.searchForm.value).subscribe(
      (res: any) => {
        this.allFlights = res;
      },
      (err: any) => {
        alert("Something went wrong!");
      }
    )}

    BookFlight(flight:any){
      var data = {
        "fno": flight.fno,
        "userId": window.localStorage.getItem("userId")
      }
      if(confirm("Confirm Booking???")){
        this.loginservice.book_flight(data).subscribe(
          (res: any)=>{
            if(res.status){
              alert(res.message);
              this.router.navigate(['/bookings']);
            }
            else {
              alert(res.message);
              this.router.navigate(['/dashboard']);
            }
          },
          (err) => {
            console.log(err);
          }
        )
      }

    }
}
