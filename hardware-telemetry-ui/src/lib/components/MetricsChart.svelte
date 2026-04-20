<script lang="ts">
	interface DataPoint {
		timestamp: number;
		value: number;
	}

	interface Props {
		data: DataPoint[];
		label: string;
		color?: string;
	}

	let { data, label, color = '#3b82f6' }: Props = $props();
	
	const width = 300;
	const height = 120;
	const padding = 10;
	
	const maxValue = $derived(Math.max(...data.map(d => d.value), 1));
	const minValue = $derived(Math.min(...data.map(d => d.value), 0));
	const range = $derived(maxValue - minValue || 1);
	
	function getX(i: number): number {
		return padding + (i / Math.max(data.length - 1, 1)) * (width - 2 * padding);
	}
	
	function getY(v: number): number {
		return height - padding - ((v - minValue) / range) * (height - 2 * padding);
	}
	
	const pathD = $derived(() => {
		if (data.length < 2) return '';
		return data.map((d, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(d.value)}`).join(' ');
	});
	
	const areaD = $derived(() => {
		if (data.length < 2) return '';
		const line = pathD();
		const lastX = getX(data.length - 1);
		const firstX = getX(0);
		return `${line} L ${lastX} ${height - padding} L ${firstX} ${height - padding} Z`;
	});
</script>

<div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
	<h3 class="text-gray-400 text-sm mb-2">{label}</h3>
	<svg viewBox="0 0 {width} {height}" class="w-full h-32">
		<defs>
			<linearGradient id="gradient-{label}" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0%" stop-color={color} stop-opacity="0.3" />
				<stop offset="100%" stop-color={color} stop-opacity="0" />
			</linearGradient>
		</defs>
		{#if data.length >= 2}
			<path d={areaD()} fill="url(#gradient-{label})" />
			<path d={pathD()} stroke={color} stroke-width="2" fill="none" />
		{:else}
			<text x={width/2} y={height/2} text-anchor="middle" fill="#6b7280" font-size="12">
				No data
			</text>
		{/if}
	</svg>
</div>
