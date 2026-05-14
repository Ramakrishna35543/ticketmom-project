TicketMom Support Intelligence Agent

An AI-powered customer support intelligence system built using Amazon Bedrock, Strands Agents, Bedrock AgentCore Runtime, and Retrieval-Augmented Generation (RAG) architecture.

This project processes TicketMom support records, applies PII-safe parsing and embedding workflows, and delivers grounded responses using Bedrock foundation models with MCP-based tool integrations.

Features
Retrieval-Augmented Generation (RAG) pipeline
Amazon Bedrock integration using Converse API
Titan Embeddings v2 vector generation
MCP Weather Tool integration
PII detection and redaction pipeline
Automated evaluation workflow
Streamlit-based UI
AgentCore Runtime deployment support
Production-ready architecture structure
Architecture
Archive.zip
   ↓
Parser & PII Redaction
   ↓
Chunking Pipeline
   ↓
Titan Embeddings v2
   ↓
Vector Store Indexing
   ↓
Strands Agent
   ↓
Bedrock AgentCore Runtime
   ↓
MCP Weather Tool Integration
AWS Services Used
Service	Purpose
Amazon Bedrock	Foundation model inference and embeddings
Bedrock AgentCore Runtime	Agent deployment and orchestration
Titan Embeddings v2	Vector embedding generation
Amazon CloudWatch	Logging and monitoring
OpenSearch (Production-ready)	Vector search and retrieval
Project Structure
ticketmom/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
│
├── src/
│   ├── agent.py
│   ├── app.py
│   ├── backend_test.py
│   ├── bedrock_client.py
│   ├── chunking.py
│   ├── config.py
│   ├── embeddings.py
│   ├── evaluate.py
│   ├── memory.py
│   ├── mcp_weather_server.py
│   ├── parse_ticketmom.py
│   ├── rag_tool.py
│   ├── streamlit_app.py
│   └── ui.py
│
├── screenshots/
├── requirements.txt
└── README.md
Security & Guardrails
PII Protection

Sensitive customer information is protected using:

Regex-based email masking
Phone number redaction
Customer identifier filtering
Output validation safeguards
Intent Restrictions

The agent explicitly refuses:

Customer identity disclosure
PII extraction requests
Unauthorized sensitive data access
MCP Weather Tool

The mcp_weather_server.py tool provides historical weather lookups for event-related support analysis.

Supported capabilities:

Historical temperature lookup
Weather condition verification
Event date validation
Context-aware retrieval
Evaluation Metrics

The system includes automated evaluation pipelines for:

Correctness
Groundedness
Completeness
PII Safety
Tool Usage Accuracy

Bedrock foundation models are used as evaluation judges for scoring agent quality.

Streamlit UI

The project includes a lightweight Streamlit-based UI for testing agent interactions locally.

Run UI
streamlit run src/streamlit_app.py

Open:

http://localhost:8501
Installation & Setup
1. Clone Repository
git clone https://github.com/your-username/ticketmom-project.git
cd ticketmom-project
2. Create Virtual Environment
python -m venv venv
3. Activate Environment
Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
Execution Workflow

Run the pipeline step-by-step:

python -m genai.ticketmom.src.unzip_archive
python -m genai.ticketmom.src.parse_ticketmom
python -m genai.ticketmom.src.chunking
python -m genai.ticketmom.src.vector_store --build
python -m genai.ticketmom.src.evaluate
Sample Query
python -m genai.ticketmom.src.app "What is the sentiment for Cosmic Ballet?"
Production Improvements

Planned production enhancements include:

IAM least-privilege hardening
OpenSearch encryption and VPC isolation
CI/CD integration pipelines
Automated regression evaluation
CloudWatch token/cost monitoring
Infrastructure-as-Code deployment support
Screenshots

Add screenshots inside the screenshots/ directory.

Example:

Streamlit UI
AWS Bedrock Agent Console
Backend evaluation output
MCP tool execution
Author

RamaKrishna

MCA Student | AI & Backend Development Enthusiast