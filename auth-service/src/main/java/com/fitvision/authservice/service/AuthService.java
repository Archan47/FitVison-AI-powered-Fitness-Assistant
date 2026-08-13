package com.fitvision.authservice.service;

import com.fitvision.authservice.dto.AuthResponse;
import com.fitvision.authservice.dto.LoginRequest;
import com.fitvision.authservice.dto.SignupRequest;
import com.fitvision.authservice.dto.UserDto;
import com.fitvision.authservice.model.User;
import com.fitvision.authservice.model.VerificationStatus;
import com.fitvision.authservice.repo.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.ui.ModelMap;

import java.util.List;
import java.util.Optional;

@Service
@Slf4j
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public UserDto signUp(SignupRequest signupRequest) {

        Optional<User> existingUser = userRepository.findByEmail(signupRequest.getEmail());
        if (existingUser.isPresent()){
            throw  new RuntimeException("User already exists with email " + signupRequest.getEmail());
        }

        User newUser = new User();
        newUser.setUserName(signupRequest.getUserName());
        newUser.setName(signupRequest.getName());
        newUser.setAge(signupRequest.getAge());
        newUser.setGender(signupRequest.getGender());
        newUser.setPhoneNo(signupRequest.getPhoneNo());
        newUser.setEmail(signupRequest.getEmail());

        newUser.setPassword(passwordEncoder.encode(signupRequest.getPassword()));

        newUser.setVerificationStatus(VerificationStatus.UNVERIFIED);

        User savedUser = userRepository.save(newUser);
        log.info("New user registered : {}", savedUser.getUserName());

        return new UserDto(
                savedUser.getUserName(),
                savedUser.getName(),
                savedUser.getAge(),
                savedUser.getGender(),
                savedUser.getPhoneNo(),
                savedUser.getEmail()
        );
    }


    public AuthResponse login(LoginRequest loginRequest) {
        log.info("Login attempt for email: {}", loginRequest.getEmail());

        User user = userRepository.findByEmail(loginRequest.getEmail())
                .orElseThrow(() ->
                        new RuntimeException("Invalid email or password")
                );

        if (!passwordEncoder.matches(
                loginRequest.getPassword(),
                user.getPassword())) {

            throw new RuntimeException("Invalid email or password");
        }

        if (user.getVerificationStatus() != VerificationStatus.VERIFIED) {
            throw new RuntimeException("Please verify your email before login");
        }

        String token = jwtService.generateToken(user.getUserName());
        log.info("Login successful for userName: {}", user.getUserName());

        return new AuthResponse(token, "Login successful");
    }

    // This service is for just testing
    public List<UserDto> allUsers() {
        List<User> users = userRepository.findAll();
        return users.stream()
                .map(user -> new UserDto(
                        user.getUserName(),
                        user.getName(),
                        user.getAge(),
                        user.getGender(),
                        user.getPhoneNo(),
                        user.getEmail()
                ))
                .toList();
    }

}
