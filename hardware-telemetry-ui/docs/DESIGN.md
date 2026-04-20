# Hardware Telemetry UI - Design Patterns & Svelte 5

## Svelte 5 Runes

### $state - Reactive State

```typescript
// Basic state
let count = $state(0);

// Object state
let data = $state<TelemetryData>({
    gpuUtilization: 0,
    temperature: 0,
});

// Array state
let messages = $state<Array<{ role: string; content: string }>>([]);
```

### $derived - Derived Values

```typescript
// Computed value
const percentage = $derived((value / max) * 100);

// Conditional derived
const color = $derived(
    percentage > 80 ? 'text-red-500' :
    percentage > 60 ? 'text-yellow-500' :
    'text-green-500'
);
```

### $effect - Side Effects

```typescript
$effect(() => {
    // Runs when dependencies change
    console.log(`GPU: ${data.gpuUtilization}%`);
});
```

### $props - Component Props

```typescript
interface Props {
    value: number;
    max: number;
    label: string;
    unit?: string;
}

let { value, max, label, unit = '%' }: Props = $props();
```

### $props with Snippets

```svelte
<!-- Parent -->
<Child>
    {#snippet extra()}
        <span>Additional info</span>
    {/snippet}
</Child>

<!-- Child -->
let { children } = $props();
{@render children()}
```

## Component Patterns

### Props with Defaults

```typescript
interface Props {
    value: number;
    max: number;
    label: string;
    unit?: string;
}

let { 
    value, 
    max, 
    label, 
    unit = '%' 
}: Props = $props();
```

### Event Handlers

```typescript
function handleSend() {
    if (input.trim() && onSend) {
        onSend(input);
        input = '';
    }
}

function handleKey(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
}
```

### Reactive Statements

```typescript
// Run when data changes
$: if (data) {
    console.log('Data updated');
}

// Computed with $
const double = $ => count * 2;
```

## Store Patterns

### Class-Based Store

```typescript
class TelemetryStore {
    messages = $state<Array<{ role: string; content: string }>>([]);
    telemetry = $state<TelemetryData[]>([]);
    connected = $state(false);
    
    private eventSource: EventSource | null = null;
    private maxHistory = 60;
    
    connect() {
        this.eventSource = new EventSource(url);
    }
}

export const telemetry = new TelemetryStore();
```

### Using Store in Components

```svelte
<script lang="ts">
    import { telemetry } from '$lib/stores/telemetry';
</script>

{#each telemetry.messages as msg}
    <div>{msg.content}</div>
{/each}
```

## Pattern: EventSource Management

```typescript
class Store {
    private eventSource: EventSource | null = null;
    
    connect() {
        if (this.eventSource) return;
        
        try {
            this.eventSource = new EventSource(url);
            
            this.eventSource.onopen = () => {
                this.connected = true;
            };
            
            this.eventSource.onmessage = (e) => {
                const data = JSON.parse(e.data);
                this.update(data);
            };
            
            this.eventSource.onerror = () => {
                this.connected = false;
                this.disconnect();
            };
        } catch {
            this.connected = false;
        }
    }
    
    disconnect() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
        this.connected = false;
    }
}
```

## Pattern: History Truncation

```typescript
private maxHistory = 60;

addItem(item: TelemetryData) {
    this.telemetry = [
        ...this.telemetry.slice(-this.maxHistory),
        item
    ];
}
```

## Pattern: Async Fetch with Error Handling

```typescript
async sendMessage(content: string) {
    this.messages = [...this.messages, { role: 'user', content }];
    
    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: this.messages })
        });
        
        if (!resp.ok) throw new Error('Request failed');
        
        // Handle streaming response
    } catch (err) {
        this.messages = [...this.messages, { 
            role: 'assistant', 
            content: `Error: ${err}` 
        }];
    }
}
```

## Pattern: SVG Chart

```svelte
<script lang="ts">
    interface DataPoint {
        timestamp: number;
        value: number;
    }
    
    let { data, label, color = '#3b82f6' }: Props = $props();
    
    const width = 300;
    const height = 120;
    const padding = 10;
    
    const maxValue = $derived(Math.max(...data.map(d => d.value), 1));
    const minValue = $derived(Math.min(...data.map(d => d.value), 0));
    const range = $derived(maxValue - minValue || 1);
    
    const pathD = $derived(() => {
        if (data.length < 2) return '';
        return data.map((d, i) => 
            `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(d.value)}`
        ).join(' ');
    });
</script>

<svg viewBox="0 0 {width} {height}">
    <path d={pathD()} stroke={color} fill="none" />
</svg>
```

## SOLID Principles

### Single Responsibility

Each component has one job:

| Component | Responsibility |
|-----------|---------------|
| `Gauge` | Display single metric |
| `MetricsChart` | Display time-series |
| `ChatWindow` | Chat UI |
| `ConnectionStatus` | Connection indicator |
| `telemetry.ts` | State + API |

### Interface Segregation

Small, focused props:

```typescript
// ❌ Large interface
interface Props {
    data: TelemetryData;
    onUpdate: () => void;
    onError: () => void;
    theme: Theme;
}

// ✅ Focused interfaces
interface GaugeProps {
    value: number;
    max: number;
    label: string;
}
```
