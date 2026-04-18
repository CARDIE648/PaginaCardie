<script>
    import Hero from '$lib/components/Hero.svelte';
    import AboutChiropractic from '$lib/components/AboutChiropractic.svelte';
    import Packages from '$lib/components/Packages.svelte';
    import Contact from '$lib/components/Contact.svelte';
</script>

<svelte:head>
    <!-- Precarga de imágenes críticas -->

</svelte:head>

<div class="flex flex-col gap-0 w-full overflow-hidden">
    <Hero />
    <AboutChiropractic />
    <Packages />
    <Contact />
</div>
