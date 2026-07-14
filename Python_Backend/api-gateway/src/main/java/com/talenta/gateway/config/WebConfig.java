package com.talenta.gateway.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        String[] origins = {
                "https://trusted-domain.com",
                "https://another-trusted.com",
                "http://localhost",
                "http://127.0.0.1:3000",
                "http://localhost:5173",
                "https://coming-revivable-scandal.ngrok-free.dev"
        };

        registry.addMapping("/api/**")
                .allowedOrigins(origins)
                .allowedMethods("*")
                .allowedHeaders("Content-Type", "Authorization")
                .allowCredentials(true);
    }
}

