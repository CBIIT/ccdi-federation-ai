# CCDI Data Federation Resource

Data federation enables users to pull data from across various resources as if they were accessing a single virtual database, rather than consolidating all data into a single centralized repository. The data remain at the original source but become searchable and findable to the research community through a standard application programming interface (API). 

This allows the creation of a virtual cohort and facilitates large-scale analytic research by making deidentified participant-level data (non-PHI/PII) findable across the sources.

## Participating Organizations
The [Childhood Cancer Data Initiative (CCDI)](https://ccdi.cancer.gov/data-federation-resource) is piloting data federation with:
* Kids First Data Resource Center
* The Pediatric Cancer Data Commons
* St. Jude Cloud
* The Treehouse Childhood Cancer Initiative
* CCDI ecDNA
* Pediatric Solid Tumor Program-IUSCCC

---

## Data Access
Researchers can search for deidentified individual-level data through the API, which provides metadata to aid in the creation of virtual cohorts across multiple data types.

* **[Access the CCDI Data Federation Resource API](https://ccdi.cancer.gov/data-federation-resource#)**
* **[Access Participating Nodes API](https://ccdi.cancer.gov/data-federation-resource#)**

> **Important Note:** The API does not deliver raw files. It provides an open-access subset of metadata (e.g., demographics) and indicates the location of the complete data set. Data access is governed by the specific policies of each contributing resource.

---

## Permissible Values
The API enforces controlled vocabularies for key metadata fields. Permissible Value (PV) documentation describes the exact allowed values, their caDSR definitions, and concept codes for each data domain:

* **[Subject Permissible Values](pv/subject-pv-metadata.md)** — `sex`, `race`, `ethnicity`, and other subject-level fields
* **[Sample Permissible Values](pv/sample-pv-metadata.md)** — `age_at_diagnosis`, `anatomical_sites`, `library_strategy`, and other sample-level fields
* **[File Permissible Values](pv/file-pv-metadata.md)** — File type and format metadata fields

---

## Additional Resources
To support node development and integration, the following resources are available:

| Resource | Description |
| :--- | :--- |
| **[OpenAPI Specification](https://federation.ccdi.cancer.gov/api-docs/)** | Technical documentation for the API. |
| **[Data Model Navigator](https://explore.ccdi.cancer.gov/data-model)** | Tool to explore CCDI data structures. |
| **[Resource Wiki](https://github.com/CBIIT/ccdi-federation-api/wiki)** | Detailed documentation and guides. |
| **[GitHub Repository](https://github.com/CBIIT/ccdi-federation-api)** | Source code and development tracking. |
| **[CCDI Blog](https://ccdi.cancer.gov/news/blog)** | Updates and news regarding the federation. |
| **[Subject Permissible Values](pv/subject-pv-metadata.md)** | Allowed values for subject-level metadata fields (sex, race, ethnicity) with caDSR definitions. |
| **[Sample Permissible Values](pv/sample-pv-metadata.md)** | Allowed values for sample-level metadata fields (age_at_diagnosis, anatomical_sites, library_strategy) with caDSR definitions. |
| **[File Permissible Values](pv/file-pv-metadata.md)** | Allowed values for file-level metadata fields with caDSR definitions. |

---

## Contribute & Contact
Organizations are invited to join the federation by implementing the CCDI API and harmonizing data to CCDI standards.

* **Inquiries:** To become a member or ask questions, email the team at [ncichildhoodcancerdatainitiative@mail.nih.gov](mailto:ncichildhoodcancerdatainitiative@mail.nih.gov).