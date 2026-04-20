# Hardware Telemetry UI - Testing Guide

## Test Overview

| Category | Count | Location |
|----------|-------|----------|
| Unit Tests | 2 | `lib/stores/telemetry.test.ts` |
| Framework | Vitest | - |

## Running Tests

### Run All Tests

```bash
cd /Users/luisvalencia/Documents/hardware-telemetry-ui
npx vitest run
```

### Watch Mode

```bash
npx vitest
```

### Coverage

```bash
npx vitest run --coverage
```

## Test Structure

```
hardware-telemetry-ui/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ChatWindow.svelte
│   │   │   ├── Gauge.svelte
│   │   │   ├── MetricsChart.svelte
│   │   │   └── ConnectionStatus.svelte
│   │   └── stores/
│   │       ├── telemetry.ts
│   │       └── telemetry.test.ts    # Tests
│   └── routes/
├── tests/
└── vitest.config.ts
```

## Test Descriptions

### telemetry.test.ts

| Test | Description |
|------|-------------|
| `should export telemetry store` | Verify store export |
| `should have connect and disconnect methods` | Verify methods exist |

## Writing Tests

### Basic Test

```typescript
import { describe, it, expect } from 'vitest';

describe('Example', () => {
    it('should work', () => {
        expect(1 + 1).toBe(2);
    });
});
```

### Testing Store Export

```typescript
import { describe, it, expect } from 'vitest';

describe('TelemetryStore', () => {
    it('should export telemetry store', async () => {
        const { telemetry } = await import('$lib/stores/telemetry');
        
        expect(telemetry).toBeDefined();
    });
});
```

### Mocking Store

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('$lib/stores/telemetry', () => {
    return {
        telemetry: {
            messages: [],
            telemetry: [],
            connected: false,
            latency: 0,
            latest: null,
            connect: vi.fn(),
            disconnect: vi.fn(),
            sendMessage: vi.fn().mockResolvedValue(undefined)
        }
    };
});
```

## Component Testing

### Testing Svelte Components

```typescript
import { render, screen } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import Gauge from '$lib/components/Gauge.svelte';

describe('Gauge', () => {
    it('renders label', () => {
        render(Gauge, { value: 50, max: 100, label: 'CPU Usage' });
        
        expect(screen.getByText('CPU Usage')).toBeDefined();
    });
});
```

### Props Testing

```typescript
import { testComponent } from 'vitest-svelte';

testComponent(Gauge, {
    props: {
        value: 75,
        max: 100,
        label: 'GPU Usage'
    },
    expect: {
        text: '75%'
    }
});
```

## Best Practices

### 1. Use Mocking for External Dependencies

```typescript
vi.mock('$lib/stores/telemetry', () => ({
    telemetry: { /* mock */ }
}));
```

### 2. Clean Up Between Tests

```typescript
beforeEach(() => {
    vi.clearAllMocks();
});
```

### 3. Test Component Behavior, Not Implementation

```typescript
// ❌ Test implementation
const instance = new TelemetryStore();
expect(instance.telemetry.length).toBe(0);

// ✅ Test behavior
await store.sendMessage('hello');
expect(store.messages.length).toBe(1);
```

## Vitest Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
    plugins: [sveltekit()],
    test: {
        include: ['src/**/*.{test,spec}.{js,ts}'],
        environment: 'jsdom',
        globals: true
    }
});
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install
        run: npm ci
      
      - name: Test
        run: npx vitest run
```
