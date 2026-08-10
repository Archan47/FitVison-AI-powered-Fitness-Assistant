package com.fitvision.authservice.controller;


import com.fitvision.authservice.dto.SignupRequest;
import com.fitvision.authservice.dto.UserDto;
import com.fitvision.authservice.service.AuthService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("api/v1/auth")
@Slf4j
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;


    @PostMapping("/signup")
    public ResponseEntity<UserDto> signUp(@RequestBody SignupRequest signupRequest){

        UserDto userDto = authService.signUp(signupRequest);
        log.info("Signup request from : {} ", signupRequest.getUserName());
        return new ResponseEntity<>(userDto, HttpStatus.CREATED);

    }

    @GetMapping("/users")
    public ResponseEntity<List<UserDto>> allUsers() {

        List<UserDto> users = authService.allUsers();

        return ResponseEntity.ok(users);
    }

}
