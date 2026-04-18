<script>
    import '../app.css';
    import Navbar from '$lib/components/Navbar.svelte';
    import Footer from '$lib/components/Footer.svelte';
    
    let { children } = $props();
</script>

<svelte:head>
    <title>CARDIE - Clínica Quiropráctica</title>
    <meta name="description" content="Salud y bienestar quiropráctico. Agenda tu cita en Clínica CARDIE." />
</svelte:head>

<div class="min-h-screen bg-cardie-dark text-base-content flex flex-col font-sans selection:bg-primary selection:text-primary-content antialiased">
    <Navbar />
    <main class="flex-grow">
        {@render children()}
    </main>
    <Footer />
</div>
