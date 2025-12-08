Software Requirements Specification (SRS)
for
Calculator Microservice
Version 1.0
Prepared by: Mohit
Organization: Personal Project
Date: December 7, 2025
 
Revision History
Name	Date	Reason for Changes	Version
1. Introduction
1.1 Purpose
This Software Requirements Specification (SRS) document describes the functional and non-functional requirements for the Calculator Microservice, Version 1.0. This document covers the complete specification of the calculator microservice, including its API endpoints, data handling, and system architecture. The microservice provides basic arithmetic operations (addition, subtraction, multiplication, division) as a RESTful API service.
1.2 Document Conventions
This document follows the following conventions:
- Requirements are numbered using the format REQ-XXX for functional requirements 
  and REQ-NF-XXX for non-functional requirements
- Technical terms are defined in Section 1.3 (Definitions)
- Priority levels: Must Have (M), Should Have (S), Could Have (C)
- Code snippets and API endpoints are shown in monospace font- References to external documents are indicated by [REF-XX]
1.3 Intended Audience and Reading Suggestions
This document is intended for:
- Developers: Focus on Sections 2 (Overall Description), 3 (Specific Requirements), 
  and 4 (System Architecture) for implementation details
- Project Managers: Review Section 1 (Introduction) and Section 2.4 (Project Scope) 
  for project overview and objectives
- Testers: Refer to Section 3 (Specific Requirements) for acceptance criteria 
  and test cases
- Stakeholders: Read Section 1 (Introduction) and Section 2 (Overall Description) 
  for high-level understanding
1.4 Project Scope
The Calculator Microservice is a backend service designed to perform basic 
arithmetic operations via HTTP REST API endpoints. The project aims to:
- Provide a simple, reliable calculator service accessible via API
- Demonstrate microservice architecture principles
- Serve as a foundation for evolving into a production-ready system
- Support integration with other applications or services

The system will handle basic arithmetic operations (add, subtract, multiply, divide) 
for integer and floating-point numbers. Future enhancements may include calculation 
history, user authentication, and advanced mathematical operations.
1.5 References
- FastAPI Documentation: https://fastapi.tiangolo.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Docker Documentation: https://docs.docker.com/
- IEEE 830-1998: Recommended Practice for Software Requirements Specifications
- REST API Design Best Practices
- Python PEP 8 Style Guide: https://pep8.org/
2. Overall Description
2.1 Product Perspective
The Calculator Microservice is a standalone backend service that can operate 
independently or be integrated into larger systems. It follows a microservice 
architecture pattern, allowing it to be:
- Deployed independently using Docker containers
- Scaled horizontally as needed
- Integrated with other services via REST API
- Maintained and updated without affecting other system components

The microservice communicates with:
- API Consumers: External applications or services that make HTTP requests
- PostgreSQL Database: For storing calculation history (future enhancement)
- Docker Environment: Container orchestration platform
2.2 Product Features
The Calculator Microservice provides the following main features:

1. Arithmetic Operations Module
   - Addition operation endpoint
   - Subtraction operation endpoint
   - Multiplication operation endpoint
   - Division operation endpoint

2. Input Validation Module
   - Data type validation (integers, floats)
   - Error handling for invalid inputs
   - Division by zero protection

3. API Documentation Module
   - Auto-generated Swagger UI documentation
   - ReDoc alternative documentation
   - Interactive API testing interface

4. Database Integration Module (Future)
   - Calculation history storage
   - Data retrieval capabilities
2.3 User Classes and Characteristics
The system serves the following user classes:

1. API Consumers
   - Characteristics: External applications, services, or developers
   - Experience Level: Technical users familiar with REST APIs
   - Access: Public API endpoints
   - Usage: Programmatic access via HTTP requests

2. Developers
   - Characteristics: Software developers maintaining the service
   - Experience Level: Intermediate to advanced Python/FastAPI knowledge
   - Access: Source code, development environment
   - Usage: Development, debugging, maintenance

3. System Administrators
   - Characteristics: DevOps or infrastructure personnel
   - Experience Level: Docker, container orchestration experience
   - Access: Deployment environment, monitoring tools
   - Usage: Deployment, monitoring, scaling
2.4 Operating Environment
Hardware Requirements:
- Minimum: 1 CPU core, 512MB RAM
- Recommended: 2 CPU cores, 1GB RAM

Operating System:
- Linux (Ubuntu 20.04+, Debian, or similar)
- Windows/macOS (for development)
- Containerized: Any OS supporting Docker

Software Dependencies:
- Python 3.8 or higher
- FastAPI framework
- Uvicorn ASGI server
- PostgreSQL 12+ (for database operations)
- Docker and Docker Compose

Network Environment:
- HTTP/HTTPS protocol support
- Port 8000 (default, configurable)
2.5 Design and Implementation Constraints
Technical Constraints:
- Must use Python 3.8+ as the programming language
- Must use FastAPI framework for API development
- Must use PostgreSQL for data persistence
- Must be containerized using Docker for deployment
- Must follow RESTful API design principles
- Must support asynchronous operations for scalability
- Must use Pydantic for data validation

Architectural Constraints:
- Microservice architecture pattern must be maintained
- Service must be stateless (no session storage)
- API must be stateless and idempotent where possible

Standards and Compliance:
- Must follow Python PEP 8 style guidelines
- Must use type hints for code clarity
- API responses must follow JSON format
- HTTP status codes must follow REST conventions
2.6 User Documentation
•	API documentation (Swagger UI, ReDoc)
•	Developer documentation
•	Deployment guides
•	Quick reference materials

2.7 Assumptions and Dependencies
•	Assumptions (database availability, network, etc.)
•	External software dependencies
•	Python package dependencies
•	Infrastructure requirements

3. System Features
Detailed breakdown of three features:
3.1 Arithmetic Operations Feature
3.1.1 Description and Priority
The Arithmetic Operations feature provides four basic mathematical operations (addition, subtraction, multiplication, division) through REST API endpoints. This is the core functionality of the calculator microservice and enables external applications to perform calculations programmatically.Priority: High - This is a must-have feature and the primary purpose of the system.
3.1.2 Stimulus/Response Sequences
Scenario 1: Successful Addition Operation
•	Stimulus: Client sends POST request to /post/add with JSON body {"a": 10, "b": 5}
•	System Action: Validates input, performs calculation (10 + 5)
•	Response: Returns {"result": 15} with HTTP 200 status code
Scenario 2: Successful Subtraction Operation
•	Stimulus: Client sends POST request to /post/subtract with JSON body {"a": 10, "b": 5}
•	System Action: Validates input, performs calculation (10 - 5)
•	Response: Returns {"result": 5} with HTTP 200 status code
Scenario 3: Successful Multiplication Operation
•	Stimulus: Client sends POST request to /post/multiply with JSON body {"a": 10, "b": 5}
•	System Action: Validates input, performs calculation (10 * 5)
•	Response: Returns {"result": 50} with HTTP 200 status code
Scenario 4: Successful Division Operation
•	Stimulus: Client sends POST request to /post/divide with JSON body {"a": 10, "b": 5}
•	System Action: Validates input, checks for division by zero, performs calculation (10 / 5)
•	Response: Returns {"result": 2.0} with HTTP 200 status code
Scenario 5: Division by Zero Error
•	Stimulus: Client sends POST request to /post/divide with JSON body {"a": 10, "b": 0}
•	System Action: Validates input, detects division by zero
•	Response: Returns error message "Division by zero is not allowed" with HTTP 400 status code
Scenario 6: Floating Point Operations
•	Stimulus: Client sends POST request with floating point numbers {"a": 3.14, "b": 2.5}
•	System Action: Validates input, performs calculation
•	Response: Returns {"result": <calculated float>} with HTTP 200 status code
3.1.3 Functional Requirements
REQ-001: The system shall provide a POST endpoint at /post/add that accepts two numeric values (a, b) and returns their sum.REQ-002: The system shall provide a POST endpoint at /post/subtract that accepts two numeric values (a, b) and returns their difference (a - b).REQ-003: The system shall provide a POST endpoint at /post/multiply that accepts two numeric values (a, b) and returns their product.REQ-004: The system shall provide a POST endpoint at /post/divide that accepts two numeric values (a, b) and returns their quotient (a / b).REQ-005: The system shall support both integer and floating-point number operations for all arithmetic endpoints.REQ-006: The system shall return calculation results as JSON with a "result" field containing the numeric value.REQ-007: The system shall return HTTP 200 status code for successful calculations.REQ-008: The system shall handle negative numbers correctly in all operations.
3.2 Input Validation Feature
3.2.1 Description and Priority
The Input Validation feature ensures all incoming data is properly validated before processing, preventing errors, security issues, and ensuring data integrity. This feature validates data types, required fields, and business rules.Priority: High - Critical for system reliability, security, and user experience.
3.2.2 Stimulus/Response Sequences
Scenario 1: Valid Input
•	Stimulus: Client sends request with valid numeric values {"a": 10, "b": 5}
•	System Action: Validates input types and values
•	Response: Processes request normally and returns result
Scenario 2: Invalid Data Type - String Instead of Number
•	Stimulus: Client sends request {"a": "abc", "b": 5}
•	System Action: Validates input, detects invalid data type
•	Response: Returns HTTP 422 with validation error: "Input should be a valid number"
Scenario 3: Missing Required Field
•	Stimulus: Client sends request {"a": 10} (missing "b")
•	System Action: Validates required fields
•	Response: Returns HTTP 422 with error: "Field required: b"
Scenario 4: Null or Empty Values
•	Stimulus: Client sends request {"a": null, "b": 5}
•	System Action: Validates for null values
•	Response: Returns HTTP 422 with validation error
Scenario 5: Invalid JSON Format
•	Stimulus: Client sends malformed JSON
•	System Action: Detects JSON parsing error
•	Response: Returns HTTP 422 with error: "Invalid JSON format"
3.2.3 Functional Requirements
REQ-009: The system shall validate that request payloads contain required fields ("a" and "b") for all calculation endpoints.REQ-010: The system shall validate that input values are numeric (integer or float) and reject non-numeric values.REQ-011: The system shall return HTTP 422 (Unprocessable Entity) status code for validation errors.REQ-012: The system shall provide clear, descriptive error messages indicating which fields failed validation and why.REQ-013: The system shall validate JSON format and return appropriate error for malformed JSON requests.REQ-014: The system shall reject null or undefined values for required numeric fields.
3.3 Error Handling Feature
3.3.1 Description and Priority
The Error Handling feature provides robust error management for various failure scenarios, ensuring the system remains stable and provides meaningful feedback to API consumers.Priority: High - Essential for system reliability and user experience.
3.3.2 Stimulus/Response Sequences
Scenario 1: Division by Zero
•	Stimulus: Client attempts division with zero as divisor
•	System Action: Detects division by zero before calculation
•	Response: Returns HTTP 400 with error: "Division by zero is not allowed"
Scenario 2: Internal Server Error
•	Stimulus: Unexpected system error occurs during processing
•	System Action: Catches exception, logs error
•	Response: Returns HTTP 500 with generic error message (no sensitive info exposed)
Scenario 3: Invalid Endpoint
•	Stimulus: Client requests non-existent endpoint
•	System Action: Route not found
•	Response: Returns HTTP 404 with error: "Endpoint not found"
Scenario 4: Unsupported HTTP Method
•	Stimulus: Client uses GET instead of POST for calculation endpoint
•	System Action: Method not allowed
•	Response: Returns HTTP 405 with error: "Method not allowed"
3.3.3 Functional Requirements
REQ-015: The system shall detect and prevent division by zero operations, returning HTTP 400 with appropriate error message.REQ-016: The system shall catch and handle all unexpected errors gracefully without crashing.REQ-017: The system shall return appropriate HTTP status codes for different error types (400, 404, 405, 422, 500).REQ-018: The system shall return error responses in consistent JSON format with "detail" field containing error message.REQ-019: The system shall not expose sensitive system information (stack traces, internal paths) in error responses to end users.REQ-020: The system shall log all errors for debugging and monitoring purposes.

3.4 API Documentation Feature
3.4.1 Description and Priority
The API Documentation feature provides automatically generated, interactive documentation for all API endpoints, enabling developers to understand and test the API without external documentation.Priority: Medium - Important for developer experience but not critical for core functionality.
3.4.2 Stimulus/Response Sequences
Scenario 1: Access Swagger UI Documentation
•	Stimulus: User navigates to /docs endpoint in web browser
•	System Action: Serves Swagger UI interface
•	Response: Displays interactive API documentation with all endpoints, schemas, and testing interface
Scenario 2: Access ReDoc Documentation
•	Stimulus: User navigates to /redoc endpoint in web browser
•	System Action: Serves ReDoc interface
•	Response: Displays alternative formatted API documentation
Scenario 3: Interactive API Testing
•	Stimulus: User clicks "Try it out" in Swagger UI and submits test request
•	System Action: Processes request through actual API endpoint
•	Response: Returns actual API response displayed in documentation interface
3.4.3 Functional Requirements
REQ-021: The system shall provide Swagger UI documentation at /docs endpoint.REQ-022: The system shall provide ReDoc documentation at /redoc endpoint.REQ-023: The system shall include complete request/response schemas in the documentation.REQ-024: The system shall include example requests and responses for each endpoint.REQ-025: The system shall allow interactive API testing through the documentation interface.REQ-026: The system shall automatically update documentation when API endpoints are modified.

3.5 Response Format Feature
3.5.1 Description and Priority
The Response Format feature ensures all API responses follow a consistent structure and format, making it easy for API consumers to parse and handle responses.Priority: Medium - Important for API usability and consistency.
3.5.2 Stimulus/Response Sequences
Scenario 1: Successful Calculation Response
•	Stimulus: Valid calculation request
•	System Action: Formats response in standard JSON structure
•	Response: Returns {"result": <number>} with appropriate HTTP status
Scenario 2: Error Response
•	Stimulus: Invalid request or error condition
•	System Action: Formats error response in standard structure
•	Response: Returns {"detail": "<error message>"} with appropriate HTTP status
3.5.3 Functional Requirements
REQ-027: The system shall return all successful responses in JSON format with Content-Type: application/json.REQ-028: The system shall return calculation results in consistent format: {"result": <numeric_value>}.REQ-029: The system shall return error responses in consistent format: {"detail": "<error_message>"}.REQ-030: The system shall include appropriate HTTP status codes in all responses.
________________________________________
Copy this into your SRS doc
4. External Interface Requirements
4.1 User Interfaces
Documentation interfaces
4.2 Hardware Interfaces
Container and network requirements
4.3 Software Interfaces
PostgreSQL, Docker, Python runtime
4.4 Communication Interfaces
HTTP/HTTPS, JSON format, request/response structures
5. Other Nonfunctional Requirements
5.1 Performance Requirements
Response times, throughput, scalability
5.2 Safety Requirements
Data validation, error handling, system stability
5.3 Security Requirements
Input validation, error information, data protection
5.4 Software Quality Attributes
Reliability, maintainability, usability, scalability, portability, testability
6. Other Requirements
•	Legal/regulatory
•	Localization
•	Compatibility
•	Deployment
•	Monitoring and logging

Appendix A: Glossary
•	Definitions of technical terms (API, ASGI, Docker, FastAPI, etc.)
Appendix B: Analysis Models
•	System architecture diagram
•	Request flow diagram
•	Data flow diagram

Appendix C: Issues List
•	Open issues (database integration, authentication, rate limiting, etc.)
•	Pending decisions

