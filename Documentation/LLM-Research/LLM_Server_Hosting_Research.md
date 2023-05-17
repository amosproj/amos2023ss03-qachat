# Research on LLM Server Hosting
**Author:** Hafidz Arifin  
**Date:** May 2023

## Method 1: On-Premises Hosting
* Confidentiality
    * higher level of confidentiality since the server and data are physically located within the organization's premises.
    * Access to server and data can be more tightly controlled, reducing the risk of unauthorized access.
* Integrity
    * organization has full control over the server environment, which allows for better monitoring and ensuring data integrity.
    * Regular backups and disaster recovery plans can be implemented to mitigate the risk of data loss or corruption.
* Availability
    * provides greater control over server availability.
    * implementing redundant systems, backup power supplies, and network infrastructure to ensure high availability.
* Usability
    * may require dedicated IT resources for server maintenance, updates, and troubleshooting.
    * Technical expertise is necessary to manage and operate the server effectively.
* Possible Storage Space
    * allows for flexible storage options based on the organization's requirements.
* Access Speed
    * depends on the organization's internal network infrastructure.
* Comments
    * On-premises hosting offers a higher level of control and security but requires significant initial investment and ongoing maintenance.

## Method 2: Cloud Hosting
* Confidentiality
    * Public cloud hosting providers implement robust security measures to ensure confidentiality.
    * Data encryption, access controls, and network isolation help protect sensitive information.
* Integrity
    * Cloud hosting providers offer various tools and technologies to ensure data integrity.
    * Regular data backups, redundancy, and fault-tolerant infrastructure contribute to maintaining data integrity.
* Availability
    * Public cloud hosting typically provides high availability through distributed data centers and redundant infrastructure.
    * Service Level Agreements (SLAs) guarantee a certain level of uptime and availability.
* Usability
    * Cloud hosting simplifies server management and maintenance tasks.
    * The cloud provider handles infrastructure management, allowing the organization to focus on the LLM server's functionality.
* Possible Storage Space
    * Public cloud hosting offers scalable storage options.
    * The organization can easily increase or decrease the storage capacity based on current needs.
* Access Speed
    * The access speed for cloud hosting depends on the organization's internet connection.
    * Public cloud providers usually have robust networks and content delivery systems to ensure fast and reliable access.
* Comments
    * Public cloud hosting provides scalability, cost-effectiveness, and easy management but requires reliance on a third-party provider.

## Conclusion
* Since we don't have the same capacity as a full time developer I suggest we go with Method 2 (cloud hosting). 
* There are several options for this method from several hosting provider such as AWS, Google Cloud and Azure are widely used. 
* There are also others such as IBM Cloud, NVIDIA GPU, Hugging Face Space or even Supabase.
  

## A bit more research on cloud hosting
* GPU (Graphics Processing Unit) is important for hosting large language models (LLMs) due to the computational demands of deep learning tasks involved in natural language processing.
* From the three (AWS, Google Cloud and Azure) performance, storage options are similar.  
* [Pricing comparison](https://intellipaat.com/blog/aws-vs-azure-vs-google-cloud/?US):
  * For small instance Google Cloud is the best option
  * For large instance AWS is best option
* Speed
  * Google Cloud provides a high-speed global network with dedicated interconnects to connect to Google's network backbone. This results in faster data transfer and lower latency when compared to other cloud providers.
* Comments:
  * While AWS and Azure have larger market shares, Google Cloud has unique strengths in data analytics, machine learning, Kubernetes, and a global network infrastructure. Additionally, if your organization already uses Google Workspace or prioritizes sustainability, GCP may offer seamless integration and alignment with your values. 