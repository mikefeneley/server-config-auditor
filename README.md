# server-config-auditor

The inital idea was to have a tool which enforced best practices
for different server software. I started with Apache and used online 
resources such as:

http://www.tecmint.com/apache-security-tips/

https://geekflare.com/10-best-practices-to-secure-and-harden-your-apache-web-server/

https://geekflare.com/apache-web-server-hardening-security/

to determine which behavior should be enforced. 

I later found out about STIGS provided by the DOD. These have well defined behavior
which is better than the unfocused approach I used here. I am abandoning this project
and starting a new one which enforces STIG specifications for various software
tools.

The new Apache STIG tool will be hosted here:

https://github.com/mikefeneley/stig_apache_2.2_nix
