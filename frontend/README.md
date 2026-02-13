# OCR + Translation Frontend

A modern Next.js web application for extracting text from images and translating them with live canvas overlay visualizations.

## Features

- **Image OCR**: Upload images and extract text using Surya OCR models
- **Real-time Translation**: Translate extracted text using IndicTrans2 (Indic languages to English)
- **Live Canvas Overlay**: Visualize translations overlaid on the original image with bounding boxes
- **Language Support**: Supports Kannada, Hindi, Bengali, Tamil, Telugu, and more
- **Toggle View**: Switch between original and translated text in real-time

## Tech Stack

- **Framework**: Next.js 16+ with TypeScript
- **Styling**: Tailwind CSS
- **API Communication**: Fetch API with JSON

## Installation

### Prerequisites
- Node.js 18+
- npm or yarn

### Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` with your backend API URL:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Development

Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Build

Build for production:
```bash
npm run build
npm start
```

## Deployment on Vercel

### Prerequisites
- Backend API deployed (e.g., on Render, Fly.io, or AWS)
- GitHub repository with this code

### Steps

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and sign in
3. Click "New Project" → Select your repository
4. In "Environment Variables", add:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://your-backend-api.com
   ```
5. Click "Deploy"

## Backend Integration

The frontend expects the backend API to expose a `/infer` endpoint:

### Request Format
```json
{
  "image_b64": "base64_encoded_image",
  "language": "kan_Knda",
  "target_language": "eng_Latn"
}
```

### Response Format
```json
{
  "success": true,
  "text": "original extracted text",
  "translated_text": "translated text",
  "pages": [
    {
      "width": 2000,
      "height": 3000,
      "lines": [
        {
          "text": "original line",
          "translation": "translated line",
          "bbox": [x1, y1, x2, y2],
          "polygon": [[x,y], [x,y], [x,y], [x,y]]
        }
      ]
    }
  ],
  "processing_time": 2.5
}
```

## Language Codes (FLORES-200)

Supported source languages (for Indic→English translation):
- `kan_Knda` - Kannada
- `hin_Deva` - Hindi
- `ben_Beng` - Bengali
- `tam_Tamil` - Tamil
- `tel_Telu` - Telugu

Target language:
- `eng_Latn` - English

## Troubleshooting

### CORS Issues
If you get CORS errors, make sure your backend is configured with:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "your-vercel-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Image Upload Not Working
- Check that `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Verify the backend is running and accessible
- Check browser console for detailed error messages

## Project Structure

```
app/
  page.tsx        # Main application page
  layout.tsx      # Root layout
  globals.css     # Global styles

components/
  CanvasOverlay.tsx  # Canvas rendering component

lib/
  types.ts        # TypeScript interfaces
```

## License

MIT

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
