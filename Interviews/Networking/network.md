**Google.com**

```makrdown

✅ 1. URL Input & Browser Parsing

When I type www.google.com and press Enter, the browser:
Parses the URL
Checks if it’s a valid format (scheme: https, host: www.google.com)
Looks into the browser cache or HSTS list to decide whether to upgrade from HTTP to HTTPS

✅ 2. DNS Resolution

The browser then resolves www.google.com into an IP address through DNS. Here's how:

Checks local DNS cache
Then OS-level cache
Then queries the configured DNS server (e.g., from your ISP or 8.8.8.8)

The DNS resolver goes through:

Root DNS server → .
TLD server → .com
Authoritative server → google.com
It finally returns multiple A or AAAA records (for load balancing/CDN)

✅ 3. TCP & TLS Handshake

Once the IP is resolved, the browser establishes a connection:

🔹 TCP Handshake:
3-way handshake: SYN → SYN-ACK → ACK

Uses port 443 (for HTTPS)

🔹 TLS Handshake:
ClientHello, ServerHello

Exchange of certificates

Cipher negotiation

Establish shared secret (session key)

🔐 Ensures encrypted communication

✅ 4. HTTP Request
After handshake, the browser sends an HTTP GET request:

http
Copy
Edit
GET / HTTP/1.1
Host: www.google.com
User-Agent: Chrome/...
Accept: text/html
Includes cookies, auth headers (if any)

Might use HTTP/2 or HTTP/3 (QUIC)

✅ 5. Server Processing
The request hits Google’s load balancer or CDN (e.g., Cloud CDN or edge nodes):

Load balancer routes request to nearest/data-available backend

Server processes request

Generates dynamic/static content (HTML, CSS, JS)

Response might be cached (e.g., Fastly, Akamai)

✅ 6. HTTP Response
The server sends back:

http
Copy
Edit
HTTP/1.1 200 OK
Content-Type: text/html
Content-Encoding: gzip
Body contains raw HTML content

May use chunked transfer or gzip compression

Includes headers: cache-control, cookies, CORS, etc.

✅ 7. Rendering in Browser
Browser parses and renders content:

Parses HTML → builds DOM

Loads CSS → builds CSSOM

Executes JS → modifies DOM

Handles layout → Render Tree

Renders pixels on screen (via GPU if needed)

⏱️ Uses parallel downloads for resources (CSS, JS, images)

✅ 8. Final Steps
JS might make AJAX/fetch requests

Browser updates tab title, history

User sees Google homepage
```

**Certificate**

```markdown

🔸 1. Client (Browser) Requests Secure Connection
User types https://example.com

Browser starts a TLS handshake over port 443

🔸 2. Server Sends Certificate (Public Key)
The server sends:

Its public certificate (X.509 format)

Any intermediate certificates

Certificate contains:

Server’s public key

Digital signature of the certificate, created using the CA’s private key

🔸 3. Client Verifies Certificate
Browser checks if the certificate:

Is not expired

Is issued to the correct domain (CN or SAN)

Was signed by a trusted CA (whose public key is in browser's root store)

✅ If verified, the server’s identity is trusted

🔸 4. Key Exchange (Encrypted Session)
Depends on algorithm (RSA or ECDHE):
Let’s take ECDHE as a modern example:

Client generates a random session key (used for symmetric encryption)

Encrypts this key using the server’s public key

Sends it to server

🔐 Only the server can decrypt it using its private key

🔸 5. Encrypted Communication Begins
Both client and server now use the shared session key to:

Encrypt and decrypt HTTP data (e.g., GET, POST)

Use symmetric encryption (e.g., AES)
```
