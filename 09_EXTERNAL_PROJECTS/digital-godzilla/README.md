# Digital Godzilla: The Interactive Mythology

Welcome to the Digital Godzilla Kino Portal - an interactive mythology exploring systemic corruption through absurdist satire.

## Overview

Digital Godzilla is an interactive streaming platform featuring 10 episodes of absurdist satire that reveal hidden structures in our world. The platform combines entertainment with education, using surreal narratives to illuminate real-world power structures and manipulation techniques.

## Features

- **Enhanced Cyberpunk Aesthetic**: Dynamic dark backgrounds with neon gradients, glitch effects, animated scan lines, and digital rain
- **Immersive Visual Effects**: Animated backgrounds, floating particles, cyberpunk borders, and VHS-style text effects
- **Interactive Episodes**: Navigate through scenes with progress tracking
- **Kino Mode**: Auto-scrolling playback for immersive experience
- **Character Database**: Detailed profiles of all mythology characters with hover cards
- **Codex**: Educational companion explaining real-world connections
- **Progress Saving**: Automatically saves your reading position
- **Responsive Design**: Works on all device sizes

## Tech Stack

- React with Vite
- Tailwind CSS for styling
- Framer Motion for animations
- React Router for navigation
- JSON-based content management

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd digital-godzilla
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to `http://localhost:5173`

### Building for Production

To create a production build:

```bash
npm run build
```

The build will be created in the `dist` directory and can be deployed to any static hosting service.

## Visual Enhancements

The portal features advanced visual effects including:

- **Animated backgrounds** with grid patterns and digital rain
- **Glitch text effects** with randomized clipping animations
- **Cyberpunk borders** with animated gradient outlines
- **Floating particles** with random movement patterns
- **Scan line animations** for authentic CRT monitor feel
- **Gradient progress bars** with smooth animations
- **Interactive hover effects** with scaling and color transitions
- **Corner accents** on cards for cyberpunk styling
- **Text glow effects** and neon color schemes

## Project Structure

```
digital-godzilla/
├── public/
│   ├── episodes/          # Episode content in JSON format
│   ├── characters/        # Character data
│   └── images/            # Static images
├── src/
│   ├── components/        # Reusable UI components
│   ├── pages/             # Page components
│   ├── styles/            # Global styles
│   └── utils/             # Utility functions
├── package.json
└── vite.config.js
```

## Deployment

The application is built to be deployed as a static site. It can be hosted on platforms like Vercel, Netlify, or any web server capable of serving static files.

For Vercel deployment:
1. Push your code to a Git repository
2. Connect your repository to Vercel
3. Vercel will automatically detect the Vite project and build/deploy it

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for bugs and feature requests.

## License

This work is licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).