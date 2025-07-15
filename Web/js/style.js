const explicationBox = document.getElementById('explication');

function changeTextWithFade(newText) {
    explicationBox.classList.add('fade-out');

    setTimeout(() => {
        explicationBox.textContent = newText;
        void explicationBox.offsetWidth;
        explicationBox.classList.remove('fade-out');
    }, 0);
}

document.querySelectorAll('.mot-cle').forEach((mot) => {
    mot.addEventListener('mouseenter', () => {
        const texte = mot.getAttribute('data-explication');
        changeTextWithFade(texte);
    });

    mot.addEventListener('mouseleave', () => {
        changeTextWithFade("Survolez un mot-clé pour voir l'explication ici.");
    });
});


const encadre = document.querySelector('.encadre-haut');

window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    const targetTop = scrollY + 300; // 100px de marge depuis le haut
    encadre.style.top = `${targetTop}px`;
});
