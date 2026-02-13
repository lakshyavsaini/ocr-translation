export interface TextLine {
  text: string;
  translation: string;
  bbox: [number, number, number, number];
  polygon: number[][];
}

export interface Page {
  width: number;
  height: number;
  lines: TextLine[];
}

export interface InferResponse {
  success: boolean;
  text: string;
  translated_text: string;
  pages: Page[];
  processing_time: number;
  error?: string;
}
