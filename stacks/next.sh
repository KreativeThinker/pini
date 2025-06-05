#!/bin/bash

# Next.js Stack Setup Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }

log_info "Setting up Next.js project..."

# Check for pnpm
if ! command -v pnpm &> /dev/null; then
    log_info "Installing pnpm..."
    npm install -g pnpm
fi

# Create Next.js app
log_info "Creating Next.js application..."
pnpm create next-app . --typescript --eslint --tailwind --app --src-dir --import-alias "@/*" --use-pnpm

# Install additional dev dependencies
if [ "$ENABLE_FORMATTERS" = true ]; then
    log_info "Installing formatters..."
    pnpm add -D prettier eslint-config-prettier
fi

if [ "$INIT_COMMITIZEN" = true ]; then
    log_info "Installing commitizen..."
    pnpm add -D commitizen @commitlint/cli @commitlint/config-conventional
fi

# Add useful dev dependencies
log_info "Installing additional development tools..."
pnpm add -D @types/node

# Update package.json scripts
log_info "Updating package.json scripts..."
# Use node to update package.json
node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));

pkg.scripts = {
  ...pkg.scripts,
  'format': 'prettier --write .',
  'format:check': 'prettier --check .',
  'lint:fix': 'next lint --fix',
  'type-check': 'tsc --noEmit'
};

fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
"

# Create additional useful directories
mkdir -p src/components/ui
mkdir -p src/lib
mkdir -p src/hooks

# Create a basic layout component
cat > src/components/ui/layout.tsx << 'EOF'
import { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              ${PROJECT_NAME}
            </h1>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  )
}
EOF

# Create a basic utility file
cat > src/lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF

# Update the main page to use the layout
cat > src/app/page.tsx << 'EOF'
import Layout from '@/components/ui/layout'

export default function Home() {
  return (
    <Layout>
      <div className="px-4 py-6 sm:px-0">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to ${PROJECT_NAME}
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            ${PROJECT_DESCRIPTION}
          </p>
          <div className="space-x-4">
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Get Started
            </button>
            <button className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </Layout>
  )
}
EOF

# Install additional Tailwind utilities
pnpm add clsx tailwind-merge

log_success "Next.js project structure created!"
log_info "Run 'pnpm dev' to start the development server"
