<script lang="ts">
	import ChatWindow from '$lib/components/ChatWindow.svelte';
	import Gauge from '$lib/components/Gauge.svelte';
	import MetricsChart from '$lib/components/MetricsChart.svelte';
	import ConnectionStatus from '$lib/components/ConnectionStatus.svelte';
	import { telemetry } from '$lib/stores/telemetry';

	const data = $derived(telemetry.latest);
	const memPercent = $derived(data ? (data.memoryUsed / data.memoryTotal) * 100 : 0);
</script>

<div class="min-h-screen bg-gray-950 text-gray-100 p-6">
	<header class="flex justify-between items-center mb-6">
		<div>
			<h1 class="text-2xl font-bold">Hardware Telemetry Dashboard</h1>
			<p class="text-gray-400 text-sm">Real-time ML hardware monitoring</p>
		</div>
		<ConnectionStatus connected={telemetry.connected} latency={telemetry.latency} />
	</header>

	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
		<div class="lg:col-span-2 space-y-6">
			<div class="h-96">
				<ChatWindow 
					messages={telemetry.messages} 
					onSend={(msg) => telemetry.sendMessage(msg)} 
				/>
			</div>
			<div class="grid grid-cols-2 gap-4">
				{#if data}
					<Gauge value={data.gpuUtilization} max={100} label="GPU Utilization" />
					<Gauge value={memPercent} max={100} label="Memory Usage" />
					<Gauge value={data.cpuUtilization} max={100} label="CPU Usage" />
					<Gauge value={data.temperature} max={100} label="GPU Temperature" unit="°C" />
				{:else}
					<div class="col-span-2 bg-gray-800 rounded-lg p-8 border border-gray-700 text-center text-gray-500">
						Waiting for telemetry data...
					</div>
				{/if}
			</div>
		</div>

		<div class="space-y-4">
			<MetricsChart 
				data={telemetry.telemetry.map(t => ({ timestamp: t.timestamp, value: t.gpuUtilization }))}
				label="GPU Utilization"
				color="#3b82f6"
			/>
			<MetricsChart 
				data={telemetry.telemetry.map(t => ({ timestamp: t.timestamp, value: t.tokensPerSecond }))}
				label="Tokens/Second"
				color="#10b981"
			/>
			<MetricsChart 
				data={telemetry.telemetry.map(t => ({ timestamp: t.timestamp, value: t.temperature }))}
				label="Temperature (°C)"
				color="#ef4444"
			/>
			<div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
				<h3 class="text-gray-400 text-sm mb-3">Quick Stats</h3>
				{#if data}
					<div class="space-y-2 text-sm">
						<div class="flex justify-between">
							<span class="text-gray-500">Power Draw</span>
							<span class="font-mono">{data.powerDraw.toFixed(1)}W</span>
						</div>
						<div class="flex justify-between">
							<span class="text-gray-500">Fan Speed</span>
							<span class="font-mono">{data.fanSpeed}%</span>
						</div>
						<div class="flex justify-between">
							<span class="text-gray-500">Latency</span>
							<span class="font-mono">{data.latency}ms</span>
						</div>
					</div>
				{:else}
					<p class="text-gray-500 text-sm">No data available</p>
				{/if}
			</div>
		</div>
	</div>
</div>
