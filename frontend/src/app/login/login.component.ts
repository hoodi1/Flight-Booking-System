import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from '../login.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  public loginForm!:FormGroup
  constructor(private fb:FormBuilder,private router:Router, private loginservice : LoginService) { }

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      username:['',Validators.required],
      password:['',Validators.required]
    })
  }
  login(){
    this.loginservice.login(this.loginForm.value).subscribe(
      (res: any) => {
        if(res.userExist){
          this.loginservice.setLoggedIn(true);
          window.localStorage.setItem("userId", res.userId)
          this.router.navigate(['/dashboard']);
          alert(res.message);
        } else {
          this.router.navigate(['/home']);
          alert(res.message);
        }
      },
      (err: any) => {
        alert("Something went wrong!");
      }
    )
}

}
