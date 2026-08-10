package com.fitvision.authservice.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SignupRequest {

    private String userName;
    private String name;
    private int age;
    private String gender;
    private String phoneNo;
    private String email;
    private String password;
}
