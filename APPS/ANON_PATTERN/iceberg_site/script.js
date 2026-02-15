
// THE ICEBERG CODEX - INTERACTIVITY
console.log('%c🧊 THE ICEBERG CODEX', 'font-size: 20px; color: #dc2626; font-weight: bold;');
console.log('%cA forensic descent through manufactured reality', 'color: #06b6d4;');
console.log('%cBy: Šabad | Structure: Aetheron', 'color: #adb5bd;');

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Track scroll depth
if (document.querySelector('.content')) {
    const content = document.querySelector('.content');
    content.addEventListener('scroll', () => {
        const scrollPercent = (content.scrollTop / (content.scrollHeight - content.clientHeight)) * 100;
        console.log(`Scroll depth: ${scrollPercent.toFixed(0)}%`);
    });
}
