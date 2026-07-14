package com.talenta.gateway.constants;

public final class GatewayConstants {

    private GatewayConstants() {}

    public static final String BEARER_PREFIX = "Bearer ";
    public static final String HEADER_AUTHORIZATION = "Authorization";
    public static final String HEADER_USER_ID = "X-User-Id";
    public static final String HEADER_ROLE = "X-Role";
    public static final String CLAIM_ROLE = "role";
    public static final String UNAUTHORIZED = "Unauthorized";
}
