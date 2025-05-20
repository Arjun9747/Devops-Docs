
![image](https://github.com/user-attachments/assets/18c49e6f-869d-4c22-aa79-fc3087318618)

**NodePort**
1. does not have static DNS name, port number(port mgmt issues), ip exposure risk, no ssl termination

**Load Balancer Cons**
1. Dependant on cloud provider
2. Costly --> for 10 services --> 10 ALB

Ingress is yaml file where we define the rules. 
Ingress controller pod is a k8s service which will reads the ingress file 
Nginx pod will take care of routing policy

**Cloud ALB-->Ingress contoroller pod --> myapp-ingress --> myapp-service --> myapp-pod**

Rules are called ingress resource which are k8s native.
Proxy pods are called nginx controllers
Ingress controller uses **host headers**(like app.com) and path (/images) to determine where the traffic should go

**Two Types of Routing**
• Path-Based Routing → Routes traffic based on the URL path (e.g., /api, /dashboard).
. Host-Based Routing → Routes traffic based on the domain name (app1.company.com, app2.company.com)

**Host Based Routing**
• When you want to route based on the domain name or subdomain.
• Perfect for multi-tenant applications where each tenant gets its own subdomain.
• Useful for production and staging separation:
	• dev.example.com → development
	• prod.example.com → production

**Path Based Routing**
	• Single domain → multiple services (/api, /app, /login).
	• Applications are logically grouped (e.g., frontend, backend, admin panel).
  . Simpler SSL configuration—one certificate for one domain.

 **IngressClass** is a Kubernetes resource that defines which Ingress Controller should handle Ingress resources. It acts as a way to classify and separate traffic routing based on specific controllers within the cluster.


 **Workflow**

 1. You install ingress controller
 2. K8S controller watches for changes to Ingress resources
 3. You define Ingress routing rules in yaml
 4. DNS --> Ingress Controller --> Service
 5. Routing Mechanism based on Host and Path based routing
 6. TLS/HTTPS routing
 7. Dynamically updates its internal routing configuration (Eg: NGINX reloads configs)

 






