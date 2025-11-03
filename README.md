# LogiSync-Gen AI for Automated Logistics Documentation

A comprehensive logistics documentation system powered by AI for creating, updating, and optimizing logistics documentation.

## Features

1. **Route Documentation and Optimization**
   - Optimized route planning with turn-by-turn instructions
   - Intelligent fuel stop recommendations
   - Compliance checkpoint integration
   - Real-time route optimization

2. **Customer Communication Automation**
   - Personalized delivery notifications
   - Automated delay explanations
   - Proof of delivery confirmations
   - Service quality follow-ups

3. **Compliance Document Generation**
   - FMCSA compliance reports
   - Safety inspection documentation
   - Environmental impact assessments
   - Driver qualification files

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI/ML**: OpenAI GPT-4, OR-Tools
- **Containerization**: Docker
- **Documentation**: Word, PDF generation

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/logisync-v2.git
cd logisync-v2
```

2. Create a `.env` file with the following variables:
```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=logisync
POSTGRES_DB=logisync
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

3. Start the application using Docker:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Route Optimization
- `POST /api/v1/routes/optimize`
  - Optimizes route and generates documentation
  - Input: Locations, cargo details, time constraints

### Customer Communications
- `POST /api/v1/customer-communications/{notification_type}`
  - Generates personalized customer notifications
  - Types: delivery_confirmation, delay_notification, proof_of_delivery

### Compliance Documents
- `POST /api/v1/compliance-documents/{document_type}`
  - Generates regulatory compliance documents
  - Types: FMCSA, safety_inspection, environmental, driver_qualification

## Directory Structure

```
logisync-v2/
├── src/
│   ├── api/
│   │   └── endpoints.py
│   ├── models/
│   │   └── database.py
│   ├── services/
│   │   ├── route_optimizer.py
│   │   └── document_generator.py
│   ├── config.py
│   └── main.py
├── documents/
│   ├── routes/
│   └── compliance/
│       └── drivers/
├── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
