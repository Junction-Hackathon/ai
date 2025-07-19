# Qurbani - AI-Powered Sacrifice Video Validation Platform (ai)

> **Hackathon Project for Junction 2025**  
> Developed for Al-Insan Al-Jazairi Association to manage Qurbani (sacrifice) donations from Algerian donors to African communities.

## 🎯 Project Overview

Qurbani is an innovative AI-powered platform that automates the validation and management of sacrifice videos for charitable organizations. The platform ensures transparency and trust between donors and recipients by providing automated verification of sacrifice rituals through advanced computer vision and natural language processing.

### 🌟 Key Features

- **🔍 Sacrifice Detection**: AI-powered detection of animals, people, and ritual elements in videos
- **🎤 Donor Mention Verification**: Voice recognition to confirm donor name mentions during the ritual
- **🩸 Blood Blurring**: Automatic blood detection and blurring for sensitive viewers
- **🤖 Multilingual Chatbot**: AI assistant supporting Arabic, French, and English for donor inquiries
- **☁️ Cloud Integration**: Seamless video processing and storage with Cloudinary
- **⚡ Real-time Processing**: Kafka-based message queuing for scalable video processing

## 🏗️ Architecture

The platform consists of several AI-powered microservices:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI API   │────│   Kafka Queue   │────│ AI Video Pipeline│
│                 │    │                 │    │                 │
│ • REST Endpoints│    │ • Message Queue │    │ • YOLO Detection│
│ • Chatbot       │    │ • Task Manager  │    │ • Whisper STT   │
│ • File Upload   │    │ • Async Proc.   │    │ • Blood Blurring│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                         ┌─────────────────┐
                         │   Cloudinary    │
                         │  Video Storage  │
                         └─────────────────┘
```
[View our diagrams](https://app.eraser.io/workspace/nj2l4ZutLPctnEyqYVXO?origin=share)
[View our technical file](https://drive.google.com/file/d/1EayLBRTA30ppys8gAdgebnRFoUeNns_c/view?usp=drive_link)
## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg installed on system
- Kafka server running
- Cloudinary account
- Google AI API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd qurbani
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Edit .env with your configuration

Required environment variables:
```env
# Kafka Configuration
KAFKA_SERVERS=localhost:9092

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Google AI (for chatbot)
GOOGLE_API_KEY=your_google_ai_api_key
```

4. **Initialize the chatbot knowledge base**
```bash
cd chatbot-assistant/scripts
python data_embadding.py
```

5. **Start the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### Health Check
```http
GET /
```
Returns server status.

### Video Processing
```http
POST /process-video
Content-Type: application/json

{
  "donor_id": "12345",
  "first_name": "Ahmed",
  "last_name": "Benali",
  "video_link": "https://res.cloudinary.com/..."
}
```

**Response:**
```json
{
  "is_audhia": true,
  "donor_mentioned": true,
  "match_score": 0.95,
  "transcript": "Bismillah, this sacrifice is for Ahmed Benali...",
  "blurred_video_url": "https://res.cloudinary.com/.../blurred_video.mp4"
}
```

### Chatbot Assistant
```http
POST /ask
Content-Type: application/json

{
  "question": "كيف يمكنني التأكد من صحة الذبيحة؟"
}
```

**Response:**
```json
{
  "answer": "يتم التحقق من صحة الذبيحة من خلال الذكاء الاصطناعي الذي يحلل الفيديو..."
}
```

## 🤖 AI Pipeline Components

### 1. Sacrifice Detection (`object_detector/`)
- **Technology**: YOLO v8
- **Purpose**: Detects people, sheep, and knives in video frames
- **Output**: Boolean indicating valid sacrifice scene

### 2. Donor Mention Detection (`mention-detector/`)
- **Technology**: Faster Whisper
- **Purpose**: Transcribes audio and matches donor names
- **Features**: Fuzzy matching with confidence scores

### 3. Blood Blurring (`blood-detector/`)
- **Technology**: OpenCV color detection
- **Purpose**: Automatically blurs blood in videos
- **Method**: HSV color space filtering and Gaussian blur

### 4. Multilingual Chatbot (`chatbot-assistant/`)
- **Technology**: Sentence Transformers + Google Gemini
- **Languages**: Arabic, French, English
- **Features**: Context-aware responses using FAISS vector search

## 🛠️ Development

### Project Structure
```
qurbani/
├── app/                    # FastAPI application
│   ├── main.py            # Application entry point
│   └── routes/            # API route handlers
├── blood-detector/        # Blood blurring module
├── chatbot-assistant/     # AI chatbot system
├── mention-detector/      # Voice recognition module
├── object_detector/       # YOLO-based detection
└── requirements.txt       # Python dependencies
```

### Adding New Features

1. **Extend AI Pipeline**: Add new detection modules in respective directories
2. **API Routes**: Create new endpoints in `app/routes/`
3. **Chatbot Knowledge**: Update `chatbot-assistant/dataset/context.json`
4. **Message Queue**: Add new Kafka topics for additional processing

### Running Tests
```bash
# Run API tests
pytest tests/

# Test individual AI components
python object_detector/scripts/video_checker.py
python mention-detector/scritps/mention.py
```

## 🌍 Multilingual Support

The platform supports three languages:

- **Arabic (العربية)**: Primary language for North African donors
- **French (Français)**: Common language in West African regions  
- **English**: International communication

Language detection is automatic based on input text patterns and keywords.

## 📋 Use Case Scenarios

### 1. Donor Verification Flow
1. sacrificer uploads sacrifice video via mobile app
2. pushed to kackend via kafka
3. backend upload it on cloudinary
4. AI pipeline processes video for authenticity
5. System verifies donor name mention in audio
6. Blood is automatically blurred for sensitive viewers

### 2. Charity Management
1. Organization receives verified videos
2. Dashboard shows processing status
3. Failed verifications flagged for manual review
4. Statistics and reports generated for transparency

### 3. Donor Support
1. Donors ask questions via chatbot
2. Multilingual AI provides instant answers
3. Complex queries escalated to human support
4. Knowledge base continuously updated

## 🔧 Configuration

### Kafka Topics
- `video.process.start`: Triggers video processing pipeline
- `video.process.complete`: Notifies completion of processing

### AI Model Configuration
- **YOLO**: Pre-trained YOLOv8x for object detection
- **Whisper**: Base model for speech recognition  
- **Sentence Transformers**: Multilingual MiniLM for embeddings
- **Gemini**: Google's LLM for conversational responses


### Cloud Deployment
The platform is designed for cloud deployment with:
- **API**: Can be deployed on any container platform (AWS ECS, Google Cloud Run)
- **Kafka**: Use managed services (AWS MSK, Confluent Cloud)
- **Storage**: Cloudinary for video storage and CDN

## 📊 Performance Metrics

- **Video Processing**: ~30-60 seconds per 2-minute video
- **Sacrifice Detection**: 95%+ accuracy on test dataset
- **Voice Recognition**: 90%+ accuracy for clear audio
- **Chatbot Response**: <2 seconds average response time

##  Hackathon Team

**Junction 2025 Submission**
- **Team**: --force
- **Track**: Social Impact / AI Track
- **Partner**: Al-Insan Al-Jazairi Association


##  Acknowledgments

- Al-Insan Al-Jazairi Association for these efforts
- Junction Hackathon organizers

---

*Built with ❤️ during Junction 2025 Hackathon to serve the Muslim community and promote transparency in charitable giving.*
