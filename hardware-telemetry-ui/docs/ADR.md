# Architecture Decision Records - Hardware Telemetry UI

## ADR-001: Use Svelte 5 with Runes

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need modern reactivity system:
- Better performance than Svelte 4
- Simpler state management
- Fine-grained reactivity

### Decision

Use Svelte 5 runes ($state, $derived, $effect, $props):

```typescript
let count = $state(0);
const double = $derived(count * 2);
```

### Consequences

**Positive**:
- Fine-grained reactivity
- Better performance
- Cleaner code

**Negative**:
- Learning curve
- New patterns to learn

---

## ADR-002: Use Tailwind CSS v4

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need styling solution:
- Rapid UI development
- Consistent design
- Easy theming

### Decision

Use Tailwind CSS v4 with @tailwindcss/vite:

```css
@import "tailwindcss";
```

### Consequences

**Positive**:
- Fast development
- Consistent styling
- Small bundle size

---

## ADR-003: Use Vitest for Testing

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need testing framework:
- Good Svelte support
- Fast
- Simple

### Decision

Use Vitest:

```bash
npm install -D vitest @testing-library/svelte jsdom
```

### Consequences

**Positive**:
- Fast tests
- Good Svelte integration
- Simple API

---

## ADR-004: Class-Based Store

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need centralized state management:
- Multiple components need telemetry data
- Real-time updates
- Connection state

### Decision

Use class-based store with Svelte 5 runes:

```typescript
class TelemetryStore {
    messages = $state([]);
    telemetry = $state([]);
    connected = $state(false);
    
    connect() { /* ... */ }
}

export const telemetry = new TelemetryStore();
```

### Consequences

**Positive**:
- Centralized state
- Easy to test
- Reactive

---

## ADR-005: SSE for Real-Time Data

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need real-time telemetry:
- WebSocket complexity not needed
- Server-initiated updates
- Simple reconnection

### Decision

Use Server-Sent Events:

```typescript
const eventSource = new EventSource('/api/v1/telemetry');
eventSource.onmessage = (e) => {
    const data = JSON.parse(e.data);
    store.update(data);
};
```

### Consequences

**Positive**:
- Simple
- Automatic reconnection
- Lightweight

**Negative**:
- One-way communication
- Not supported in IE

---

## ADR-006: SVG Charts

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need lightweight charts:
- No heavy chart libraries
- Custom styling
- Small bundle

### Decision

Use custom SVG charts:

```svelte
<svg>
    <path d={pathD()} stroke={color} />
</svg>
```

### Consequences

**Positive**:
- Small bundle
- Full control
- Fast

**Negative**:
- More code
- Need SVG knowledge

---

## ADR-007: Environment Variable Configuration

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need API URL configuration:
- Different dev/prod URLs
- Easy to change

### Decision

Hardcode for now, env vars later:

```typescript
const API_URL = 'http://localhost:8080';
```

### Consequences

**Positive**:
- Simple
- Works for dev

**Negative**:
- Not flexible
