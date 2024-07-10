import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginService } from '../login.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

  public registerForm!:FormGroup
  constructor(private fb:FormBuilder,private router:Router, private loginservice : LoginService) { }

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      username:['',Validators.required],
      password:['',Validators.required],
      email:['', Validators.required]
    })
  }

  register(){
    this.loginservice.register(this.registerForm.value).subscribe(
      (res: any) => {
        if(res.userExist){
          this.loginservice.setLoggedIn(true);
          window.localStorage.setItem("userId", res.userId);
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
