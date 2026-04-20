export interface TelemetryData {
	timestamp: number;
	gpuUtilization: number;
	gpuMemory: number;
	cpuUtilization: number;
	memoryUsed: number;
	memoryTotal: number;
	temperature: number;
	fanSpeed: number;
	powerDraw: number;
	tokensPerSecond: number;
	latency: number;
}

class TelemetryStore {
	messages = $state<Array<{ role: string; content: string }>>([]);
	telemetry = $state<TelemetryData[]>([]);
	connected = $state(false);
	latency = $state(0);
	
	private eventSource: EventSource | null = null;
	private maxHistory = 60;

	connect() {
		if (this.eventSource) return;
		
		try {
			this.eventSource = new EventSource('http://localhost:8080/api/v1/telemetry');
			
			this.eventSource.onopen = () => {
				this.connected = true;
			};
			
			this.eventSource.onmessage = (e) => {
				try {
					const data = JSON.parse(e.data) as TelemetryData;
					this.telemetry = [...this.telemetry.slice(-this.maxHistory), data];
					this.latency = data.latency;
				} catch {}
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

	async sendMessage(content: string) {
		this.messages = [...this.messages, { role: 'user', content }];
		
		try {
			const resp = await fetch('http://localhost:8080/api/v1/chat', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ messages: this.messages, stream: true })
			});
			
			if (!resp.ok) throw new Error('Request failed');
			
			const reader = resp.body?.getReader();
			const decoder = new TextDecoder();
			let assistantMessage = '';
			
			this.messages = [...this.messages, { role: 'assistant', content: '' }];
			
			while (reader) {
				const { done, value } = await reader.read();
				if (done) break;
				
				const chunk = decoder.decode(value);
				assistantMessage += chunk;
				this.messages[this.messages.length - 1] = { 
					role: 'assistant', 
					content: assistantMessage 
				};
			}
		} catch (err) {
			this.messages = [...this.messages, { 
				role: 'assistant', 
				content: `Error: ${err instanceof Error ? err.message : 'Failed to connect'}` 
			}];
		}
	}

	get latest(): TelemetryData | null {
		return this.telemetry.length > 0 ? this.telemetry[this.telemetry.length - 1] : null;
	}
}

export const telemetry = new TelemetryStore();
