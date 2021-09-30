# Exercises - Chapter 03 Selecting a Service Platform

1. Compare IaaS, PaaS, and SaaS on the basis of cost, configurability, and control (hint make a chart)

* IaaS:
    * Cost: We are charged for computation, storing data and networking, this is all dependent on the architecture, if the architecture is optimised we wouldn't incur any additional charge.
    * Configurability: We can configure almost everything and we have a control over patching softwares, etc.
    * Control: We have a high level of all over the system.

* PaaS:
    * Cost: Costs are higher than IaaS as the provider manages the rest of framework.
    * Configurability: We don't have much control over the framework. We can just make changes to our applications, since we are using the entire platform as a service, for example we can choose our OS but patching is done by the provider.
    * Control: We just bring our data and and application to get going and start using the services.

* SaaS:
    * Cost: This is the costliest service platform, as we are using a completely developed applications and tailoring/using it according to our requirements.
    * Configurability: We cannot configure it, we just consume the service that is being provided.
    * Control: We do not have any control over it.

2. What are the caveats to consider in adopting Software as a Service?
* We should adopt a SaaS which has transparency in their agreement and does not lock us in(vendor lock-in).
* The provider's hosting policies should not conflict with our company's policies.


3. List the key advantages of virtual machines.
    * Easy for provisioning and taking them down/terminating
    * It is has many advantages as compared to physical machines w.r.t creating, starting, modifying, shutting down and terminating, all of this can be done via an API and can be implemented on a large scale without putting in too much efforts.
    * VMs have good application isolation.
    * We can provision a VM for a specific task and terminate it whenever required.



4. Why might you choose physical over virtual machines?
* Choosing a physical over virtual machine can have many reasons, it could be for compliance, better security, or to have better I/O for disk and network.



5. Which factors might make you choose private over public cloud services?
* One of the main reason to choose private cloud services is security.
* Another reason would be country specific data policies.
* Also considering technical issues for secure application.