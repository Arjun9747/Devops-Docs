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


