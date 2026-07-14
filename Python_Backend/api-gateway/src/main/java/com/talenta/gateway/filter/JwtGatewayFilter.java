package com.talenta.gateway.filter;

import com.talenta.gateway.constants.GatewayConstants;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletRequestWrapper;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.crypto.SecretKey;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.Pattern;

@Slf4j
@Component
public class JwtGatewayFilter extends OncePerRequestFilter {

    private static final Pattern JOB_DETAIL_PATH = Pattern.compile("^/api/jobs/[0-9]+$");
    private final SecretKey key;
    private final ObjectMapper objectMapper;

    public JwtGatewayFilter(@Value("${jwt.secret}") String secret, ObjectMapper objectMapper) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.objectMapper = objectMapper;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {

        String path = request.getRequestURI();
        String method = request.getMethod();

        if (isPublicEndpoint(method, path) || HttpMethod.OPTIONS.name().equals(method)) {
            filterChain.doFilter(request, response);
            return;
        }

        String token = extractToken(request);
        if (token == null) {
            writeUnauthorized(response);
            return;
        }

        try {
            Claims claims = parseClaims(token);
            String userId = claims.getSubject();
            String role = claims.get(GatewayConstants.CLAIM_ROLE, String.class);

            if (isBlank(userId) || isBlank(role)) {
                writeUnauthorized(response);
                return;
            }

            MutableHttpServletRequest mutableRequest = new MutableHttpServletRequest(request);
            mutableRequest.removeHeader(GatewayConstants.HEADER_USER_ID);
            mutableRequest.removeHeader(GatewayConstants.HEADER_ROLE);
            mutableRequest.putHeader(GatewayConstants.HEADER_USER_ID, userId);
            mutableRequest.putHeader(GatewayConstants.HEADER_ROLE, role);

            filterChain.doFilter(mutableRequest, response);

        } catch (JwtException | IllegalArgumentException e) {
            log.warn("JWT validation failed: {}", e.getMessage());
            writeUnauthorized(response);
        }
    }

    private String extractToken(HttpServletRequest request) {
        String header = request.getHeader(GatewayConstants.HEADER_AUTHORIZATION);
        if (header == null || !header.startsWith(GatewayConstants.BEARER_PREFIX)) {
            return null;
        }

        String token = header.substring(GatewayConstants.BEARER_PREFIX.length()).trim();
        return token.isEmpty() ? null : token;
    }

    private Claims parseClaims(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    private boolean isBlank(String value) {
        return value == null || value.isBlank();
    }

    private boolean isPublicEndpoint(String method, String path) {
        if (HttpMethod.GET.matches(method)) {
            return Set.of(
                    "/api/jobs",
                    "/api/jobs/open")
                    .contains(path)
                    || JOB_DETAIL_PATH.matcher(path).matches();
        }
        if (HttpMethod.POST.matches(method)) {
            return Set.of(
                        "/api/auth/login",
                        "/api/auth/get-otp")
                .contains(path);
        }
        return false;
    }

    private void writeUnauthorized(HttpServletResponse response) throws IOException {
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        ObjectNode error = objectMapper.createObjectNode();
        error.put("message", GatewayConstants.UNAUTHORIZED);
        error.put("statusCode", HttpServletResponse.SC_UNAUTHORIZED);

        ObjectNode body = objectMapper.createObjectNode();
        body.putNull("data");
        body.putArray("errors").add(error);
        response.getWriter().write(objectMapper.writeValueAsString(body));
    }

    private static class MutableHttpServletRequest extends HttpServletRequestWrapper {

        private final Map<String, String> customHeaders = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);
        private final Set<String> removedHeaders = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);

        public MutableHttpServletRequest(HttpServletRequest request) {
            super(request);
        }

        public void putHeader(String name, String value) {
            removedHeaders.remove(name);
            customHeaders.put(name, value);
        }

        public void removeHeader(String name) {
            customHeaders.remove(name);
            removedHeaders.add(name);
        }

        @Override
        public String getHeader(String name) {
            String value = customHeaders.get(name);
            if (value != null) {
                return value;
            }
            return removedHeaders.contains(name) ? null : super.getHeader(name);
        }

        @Override
        public Enumeration<String> getHeaderNames() {
            List<String> names = Collections.list(super.getHeaderNames()).stream()
                    .filter(name -> !removedHeaders.contains(name) && !customHeaders.containsKey(name))
                    .collect(java.util.stream.Collectors.toCollection(ArrayList::new));
            names.addAll(customHeaders.keySet());
            return Collections.enumeration(names);
        }

        @Override
        public Enumeration<String> getHeaders(String name) {
            String value = customHeaders.get(name);
            if (value != null) {
                return Collections.enumeration(List.of(value));
            }
            return removedHeaders.contains(name)
                    ? Collections.emptyEnumeration()
                    : super.getHeaders(name);
        }
    }
}
