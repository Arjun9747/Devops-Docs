![image](https://github.com/user-attachments/assets/991ccebf-870a-46ab-b671-94cf4b93c790)

**Data Plane**
1. Microservices Pods --> for accessing the applications
2. Ingress GW Pod --> for entry point for external traffic
3. Egress GW Pod --> for exit point for traffic, service mesh, policy enforced

**Control Plane**
1. Istiod --> Brain
2. Pilot --> Configure Envoy Proxy
3. Citadel -->Cert and TLS
4. Galley --> Handling Config Validation
5. Istio CA --> Issues public and Private TLS cert to ensure communication between services.

**Use Case**
1. Used for App to App Communications. 
2. All Istio based resources are deployed on isito-system namespace.
3. Traffic Mgmt --> Virtual Service to configure routing within the mesh.
   * When a request is made into a service , Istio intercepts the traffic and uses the rules defined in the Virtual Service to decide .
   * Which destination the traffic should go
   * Traffic should split across multiple versions
   * Whether any additonal rules should apply (timeout, retries)

**Yaml Config**
1. GW-API for gw and virtual service
2. Configure egress settings for external service
3. For creating service entries


1. Rate Limiting
   * Filter by ip/headers/path prefix (200 req per sec)
   * Gateway Configuration
   * Points to Docker image for service
   * Redis for storing rate limiting data
  
**Script**
	1. A client sends a request to the application, which is routed through the Istio Gateway.
	Rate Limiter Filter: The Rate Limiter Filter checks the incoming request against the configured rate limiting rules (200 req/sec) based on IP, headers, or path prefix.
 
	2. Rate Limiting Server: If the request matches a rate limiting rule, the Rate Limiter Filter sends a request to the Rate Limiting Server to check if the request should be allowed or blocked.
 
	3. Rate Limiting Server: If the request matches a rate limiting rule, the Rate Limiter Filter sends a request to the Rate Limiting Server to check if the request should be allowed or blocked
 
	4. Redis: The Rate Limiting Server checks the Redis database to see if the request limit has been exceeded for the given IP, headers, or path prefix.
 
	5. Rate limiting decision: If the request limit has not been exceeded, the Rate Limiting Server returns an "allow" decision to the Rate Limiter Filter. If the limit has been exceeded, it returns a "block" decision
 
	6. Metrics collection: The Rate Limiter Filter sends metrics to StatsD, which collects and exports rate limiting metrics for monitoring.
 
	7. Rate limiting: The configuration ensures that the application is protected from excessive traffic, preventing overload and potential downtime.
 
	8.Flexibility: The rate limiting rules can be customized based on IP, headers, or path prefix, allowing for flexible and targeted rate limiting.
 
	9.Monitoring and alerting: The integration with StatsD enables monitoring and alerting on rate limiting metrics, helping to detect issues and optimize performance.
