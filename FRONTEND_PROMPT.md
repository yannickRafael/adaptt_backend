# ADAPTT Frontend Development Prompt

## Project Overview
Create a modern, responsive web interface for ADAPTT (Transparency in Infrastructure Projects). The system allows citizens to monitor infrastructure projects, view transparency scores, and subscribe to project updates via SMS/WhatsApp.

## Tech Stack Requirements
- **Framework**: React with TypeScript (or Next.js for SSR)
- **Styling**: Tailwind CSS
- **State Management**: React Query for API calls
- **UI Components**: shadcn/ui or Material-UI
- **Maps**: Leaflet or Google Maps for project locations
- **Charts**: Recharts or Chart.js for transparency scores visualization

## Design Requirements
- Mobile-first responsive design
- Portuguese language (Mozambique)
- Clean, accessible interface
- Dark mode support (optional)
- Fast loading times

---

## API Endpoints Reference

### Base URL
```
Production: https://your-ec2-ip-or-domain.com
Development: http://localhost:5001
```

### 1. Projects API

#### GET /api/projects
Get list of all projects with basic info and transparency scores.

**Response:**
```json
[
  {
    "project_id": "9oFiIdSZv4Ruc2SdaVWQ",
    "project_name": "Manutenção Periódica de Estradas",
    "status": "Active",
    "transparency_score": 5,
    "alert_color": "YELLOW"
  }
]
```

#### GET /api/projects/{project_id}
Get detailed information about a specific project.

**Response:**
```json
{
  "project_id": "9oFiIdSZv4Ruc2SdaVWQ",
  "project_name": "Manutenção Periódica de Estradas",
  "status": "Active",
  "transparency_score": 5,
  "alert_color": "YELLOW",
  "simple_message": "Faltam documentos críticos...",
  "data_raw": {
    "title": "Project Title",
    "description": "...",
    "budget": {...},
    "locations": [...],
    "parties": [...],
    "implementationPeriod": {...}
  }
}
```

#### GET /api/projects/{project_id}/documents
Get all documents for a specific project.

**Response:**
```json
[
  {
    "document_id": "doc123",
    "project_id": "9oFiIdSZv4Ruc2SdaVWQ",
    "document_type": "feasibilityStudy",
    "title": "Estudo de Viabilidade",
    "status": "available",
    "url": "https://...",
    "date_published": "2024-01-15"
  }
]
```

---

### 2. Locations API

#### GET /api/locations
Get all available regions/provinces.

**Response:**
```json
[
  {
    "id": "maputo",
    "name": "Maputo",
    "region": "Sul",
    "country": "Mozambique"
  },
  {
    "id": "gaza",
    "name": "Gaza",
    "region": "Sul",
    "country": "Mozambique"
  }
]
```

---

### 3. User Registration API

#### POST /api/users/register
Register a new user.

**Request:**
```json
{
  "name": "João Silva",
  "phone_number": "+258841234567",
  "region_id": "maputo"
}
```

**Response (Success):**
```json
{
  "message": "Utilizador registado com sucesso.",
  "user_id": 1,
  "name": "João Silva",
  "phone_number": "+258841234567",
  "region_id": "maputo"
}
```

**Response (Error):**
```json
{
  "error": "Este número de telefone já está registado."
}
```

---

### 4. Subscriptions API

#### POST /api/subscriptions
Subscribe to a project.

**Request:**
```json
{
  "user_id": 1,
  "project_id": "9oFiIdSZv4Ruc2SdaVWQ",
  "notification_channel": "wpp"
}
```

**Response:**
```json
{
  "message": "Subscrição realizada com sucesso.",
  "subscription_id": 1,
  "user_id": 1,
  "project_id": "9oFiIdSZv4Ruc2SdaVWQ",
  "notification_channel": "wpp"
}
```

#### DELETE /api/subscriptions
Unsubscribe from a project.

**Request:**
```json
{
  "user_id": 1,
  "project_id": "9oFiIdSZv4Ruc2SdaVWQ"
}
```

**Response:**
```json
{
  "message": "Subscrição cancelada com sucesso."
}
```

#### GET /api/subscriptions/user/{user_id}
Get all subscriptions for a user.

**Response:**
```json
[
  {
    "subscription_id": 1,
    "user_id": 1,
    "project_id": "9oFiIdSZv4Ruc2SdaVWQ",
    "subscribed_at": "2024-11-26 12:30:06",
    "notification_enabled": 1,
    "notification_channel": "wpp",
    "project_name": "Manutenção Periódica de Estradas",
    "status": "Active",
    "transparency_score": 5,
    "alert_color": "YELLOW"
  }
]
```

---

### 5. Messaging API (Admin Only)

#### POST /api/messages/send-bulk
Send bulk SMS/WhatsApp messages.

**Request:**
```json
{
  "message": "Alerta: Mudança no projeto X",
  "phone_numbers": ["+258841234567", "+258849876543"]
}
```

**Response:**
```json
{
  "total": 2,
  "successful": 2,
  "failed": 0,
  "results": [
    {
      "phone": "+258841234567",
      "success": true,
      "message_sid": "SM123...",
      "error": null
    }
  ]
}
```

---

## Key Features to Implement

### 1. Home Page
- Hero section with project statistics
- Featured projects with transparency scores
- Search and filter functionality
- Map view of projects by region

### 2. Projects List Page
- Filterable table/grid of all projects
- Sort by: transparency score, date, region
- Filter by: region, status, alert color
- Pagination
- Color-coded transparency indicators:
  - RED: Score 0-3 (Critical issues)
  - YELLOW: Score 4-7 (Some concerns)
  - GREEN: Score 8-10 (Good transparency)

### 3. Project Detail Page
- Full project information
- Transparency score breakdown
- Document availability checklist
- Budget information
- Timeline/milestones
- Location map
- Subscribe button
- Share functionality

### 4. User Registration/Login
- Phone number-based registration
- Region selection dropdown
- Form validation (Mozambican phone format)
- Success/error messaging

### 5. User Dashboard
- List of subscribed projects
- Notification preferences (SMS/WhatsApp)
- Manage subscriptions
- View project updates

### 6. About/Help Page
- How transparency scoring works
- How to use SMS/WhatsApp commands
- FAQ
- Contact information

---

## UI Components Needed

### Cards
- ProjectCard (list view)
- ProjectDetailCard
- SubscriptionCard
- StatCard (for dashboard metrics)

### Forms
- RegistrationForm
- SubscriptionForm
- SearchForm

### Data Display
- ProjectsTable
- DocumentsChecklist
- TransparencyScoreGauge
- AlertBadge (RED/YELLOW/GREEN)

### Maps
- ProjectsMap (showing all projects)
- ProjectLocationMap (single project)

### Charts
- TransparencyScoreChart
- ProjectStatusPieChart
- RegionalDistributionChart

---

## Color Scheme Suggestions

```css
/* Alert Colors */
--alert-red: #EF4444;      /* Critical */
--alert-yellow: #F59E0B;   /* Warning */
--alert-green: #10B981;    /* Good */

/* Primary Colors */
--primary: #2563EB;        /* Blue */
--secondary: #64748B;      /* Slate */

/* Background */
--bg-primary: #FFFFFF;
--bg-secondary: #F8FAFC;
```

---

## Sample User Flows

### Flow 1: Browse and Subscribe
1. User visits homepage
2. Browses projects or searches by region
3. Clicks on project to view details
4. Sees transparency score and missing documents
5. Registers with phone number
6. Subscribes to project (chooses SMS or WhatsApp)
7. Receives confirmation

### Flow 2: Manage Subscriptions
1. User logs in with phone number
2. Views dashboard with subscribed projects
3. Sees project updates/alerts
4. Can unsubscribe from projects
5. Can change notification preferences

---

## Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 640px)

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px)

/* Desktop */
@media (min-width: 1025px)
```

---

## Accessibility Requirements
- WCAG 2.1 Level AA compliance
- Keyboard navigation
- Screen reader support
- High contrast mode
- Portuguese language labels
- Clear error messages

---

## Performance Targets
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- Lighthouse Score: > 90

---

## Additional Features (Nice to Have)
- PWA support for offline access
- Push notifications (web)
- Export project data to PDF
- Share project on social media
- Multi-language support (Portuguese/English)
- Admin dashboard for analytics

---

## Development Notes

### API Error Handling
All endpoints return standard error format:
```json
{
  "error": "Error message in Portuguese"
}
```

### Phone Number Format
- Mozambican format: +258 XX XXX XXXX
- Also accepts: 8X/9X XXXXXXX (auto-prefixed with +258)

### Transparency Score
- Scale: 0-10
- Based on critical document availability
- RED (0-3): Missing critical documents
- YELLOW (4-7): Some documents missing
- GREEN (8-10): All/most documents available

---

## Getting Started

1. Set up React/Next.js project with TypeScript
2. Install dependencies (Tailwind, React Query, etc.)
3. Create API client with base URL configuration
4. Build reusable components (cards, forms, etc.)
5. Implement pages in order: Home → Projects List → Project Detail → User Dashboard
6. Add responsive design and accessibility
7. Test with real API endpoints
8. Deploy to production

---

## Environment Variables

```env
REACT_APP_API_BASE_URL=https://your-api-domain.com
REACT_APP_GOOGLE_MAPS_API_KEY=your-key-here
```

---

This should provide everything needed to build a complete, production-ready frontend for the ADAPTT system!
